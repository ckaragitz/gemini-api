# Gemini API: A multi-modal app server

This repository contains the code for a multi-model / multi-modal demo, built using Google Cloud Vertex AI. The demo showcases the capabilities of different Vertex AI models and a RAG Search Engine:

## Chat models:
- **Chat-bison**: A large language model specifically trained for conversational AI.
- **Gemini-1.0-pro**: A general-purpose language model with strong performance on various tasks, including chat and SQL generation.
- **Gemini-1.5-pro**: A newer version of Gemini-pro with improved performance and capabilities, like a 1M token context window.

## RAG and Document Search:
- **Vertex Search**: Handles ingestion, chunking, embeddings, indexing, similarity search, and serving.
- **Gemini-1.0-pro**: Model used to generate summaries based on documents fetched from Vertex Search.

## Features
- **Multi-model support**: Choose between different models for chat and SQL generation.
- **Real-time chat**: Interact with the chatbot in real-time and receive responses instantly.
- **Contextual awareness**: The chatbot remembers previous conversations and uses them to provide more relevant responses.
- **SQL generation**: Generate SQL queries based on natural language prompts.
- **Search**: Search for documents and generate summaries based on a prompt.
