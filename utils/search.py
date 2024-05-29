from google.cloud import discoveryengine
from google.api_core.client_options import ClientOptions

def search_engine(search_query: str, engine_id: str):
    """ search_query maps to the 'query' parameter, engine_id maps to the 'engine' parameter """

    project_id = "ck-vertex"
    location = "global"

    client_options = (
        ClientOptions(api_endpoint=f"{location}-discoveryengine.googleapis.com")
        if location != "global"
        else None
    )

    client = discoveryengine.SearchServiceClient(client_options=client_options)
    serving_config = f"projects/{project_id}/locations/{location}/collections/default_collection/engines/{engine_id}/servingConfigs/default_config"

    content_search_spec = discoveryengine.SearchRequest.ContentSearchSpec(
        snippet_spec=discoveryengine.SearchRequest.ContentSearchSpec.SnippetSpec(
            return_snippet=True
        ),
        summary_spec=discoveryengine.SearchRequest.ContentSearchSpec.SummarySpec(
            summary_result_count=5,
            include_citations=True,
            ignore_adversarial_query=True,
            ignore_non_summary_seeking_query=True,
            model_prompt_spec=discoveryengine.SearchRequest.ContentSearchSpec.SummarySpec.ModelPromptSpec(
                preamble="Return the summary in a markdown format."
            ),
            model_spec=discoveryengine.SearchRequest.ContentSearchSpec.SummarySpec.ModelSpec(
                version="stable",
            ),
        ),
    )

    try:
        search_request = discoveryengine.SearchRequest(
            serving_config=serving_config,
            query=search_query,
            page_size=10,
            content_search_spec=content_search_spec,
            query_expansion_spec=discoveryengine.SearchRequest.QueryExpansionSpec(
                condition=discoveryengine.SearchRequest.QueryExpansionSpec.Condition.AUTO,
            ),
            spell_correction_spec=discoveryengine.SearchRequest.SpellCorrectionSpec(
                mode=discoveryengine.SearchRequest.SpellCorrectionSpec.Mode.AUTO
            ),
        )

        search_response = client.search(search_request)
        return search_response

    except Exception as e:
        print(f"Error: {e}")
        return None

def process_search_response(search_response):
    serialized_results = []

    for result in search_response.results:
        result_dict = {
            "id": result.document.name.split('/')[-1],
            "title": "",
            "snippets": [],
            "link": "",
        }

        # Extracting title
        if "title" in result.document.derived_struct_data:
            result_dict["title"] = result.document.derived_struct_data["title"]

        # Extracting snippets
        if "snippets" in result.document.derived_struct_data:
            snippets = result.document.derived_struct_data["snippets"]
            for snippet in snippets:
                if "snippet" in snippet:
                    result_dict["snippets"].append(snippet["snippet"])

        # Extracting link
        if "link" in result.document.derived_struct_data:
            result_dict["link"] = result.document.derived_struct_data["link"]

        serialized_results.append(result_dict)

    summary_data = {
        "summary_text": search_response.summary.summary_text,
        "safety_attributes": {
            "categories": list(search_response.summary.safety_attributes.categories),
            "scores": list(search_response.summary.safety_attributes.scores),
        },
        "summary_with_metadata": {
            "summary": search_response.summary.summary_with_metadata.summary,
            "references": [
                {
                    "title": reference.title,
                    "document": reference.document,
                }
                for reference in search_response.summary.summary_with_metadata.references
            ],
        },
    }

    return {"results": serialized_results, "summary": summary_data}