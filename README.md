# AMIT RAG Chatbot

A Retrieval-Augmented Generation (RAG) chatbot prototype for answering questions from user-provided documents. The project demonstrates the foundation of a document-question-answering system: documents are ingested, split into text chunks, converted into semantic embeddings, and prepared for vector-based retrieval through a FastAPI service.

> **Project status:** This repository is an actively structured prototype. Document ingestion and embedding generation are partially implemented, while the complete retrieval pipeline, production vector-store integration, chat endpoint, and conversation history still need to be completed.
>
> 
#DATA

> https://drive.google.com/drive/folders/1I5DNqdfrth52YsX9Jw01p2Zgj3u66pek?usp=sharing

## What Is RAG?

A traditional chatbot generates an answer from its language model knowledge. A RAG system first searches a trusted knowledge source, retrieves the most relevant passages, and then uses those passages as context for answer generation.

```text
User question
      |
      v
Create a query embedding
      |
      v
Retrieve similar document chunks
      |
      v
Build a context-aware prompt
      |
      v
Generate an answer with an LLM
      |
      v
Return the answer through an API
```

This architecture is useful when answers should be grounded in private documents such as course notes, policies, technical manuals, or internal knowledge bases.

## Current Architecture

The current repository contains the main building blocks of a future RAG application:

| Component | Current responsibility |
|---|---|
| Document ingestion | Reads PDF or TXT files, extracts text, and splits it into chunks. |
| Embedding service | Uses `BAAI/bge-small-en` through Sentence Transformers to encode text into vectors. |
| Vector storage layer | Provides a placeholder for storing and searching embeddings with PostgreSQL and pgvector. |
| RAG pipeline | Provides the intended location for retrieval, prompt construction, and LLM generation. |
| API layer | Starts a FastAPI application and exposes a health-style root endpoint. |
| Configuration layer | Reserved for environment variables, model names, and database settings. |

## Repository Structure

```text
.
├── app/
│   ├── api/
│   │   └── main.py
│   ├── chatbot/
│   │   └── rag_pipeline.py
│   ├── core/
│   │   └── config.py
│   ├── embeddings/
│   │   └── embedding_service.py
│   └── retrieval/
│       └── vector_store.py
├── docs/
│   └── data.pdf                 # Stored separately from GitHub in the project setup
├── ingest.py
├── requirements.txt
└── README.md
```

## Document Ingestion Flow

The `ingest.py` module currently supports PDF and TXT documents. It extracts text from a PDF using `PyPDF2`, divides the text into chunks of approximately 500 characters, generates an embedding for each chunk, and writes the generated vectors to a JSON file.

A simplified ingestion flow looks like this:

```python
text = extract_text("document.pdf")
chunks = split_text(text, chunk_size=500)
for chunk in chunks:
    vector = embed_text(chunk)
    save_embedding(chunk, vector)
```

The generated JSON and other derived retrieval artifacts are intentionally kept outside the GitHub repository when they become large. Add the Google Drive dataset link to this README after uploading the project data.

## Technology Stack

- **Python** for the application and data-processing code.
- **FastAPI** for the HTTP API layer.
- **Sentence Transformers** for semantic embeddings.
- **BAAI/bge-small-en** as the current embedding model.
- **PyPDF2** for extracting text from PDF files.
- **NumPy** for numerical operations.
- **PostgreSQL with pgvector** as the intended production vector-store option.
- **OpenAI-compatible or other LLM provider** as the intended answer-generation layer.

## Installation

Create and activate a virtual environment:

```bash
python -m venv .venv

# Windows PowerShell
.venv\Scripts\Activate.ps1

# macOS / Linux
source .venv/bin/activate
```

Install the dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install sentence-transformers PyPDF2
```

If you plan to use PostgreSQL with vector search, install PostgreSQL and enable the `pgvector` extension according to your operating system. Do not place database passwords or API keys directly in Python files.

## Environment Configuration

The configuration module is intended to load settings from environment variables. A future deployment should use a `.env` file locally and a secret manager in production.

Example configuration values:

```env
LLM_API_KEY=replace_with_your_local_secret
DATABASE_URL=postgresql://user:password@localhost:5432/amit_rag
EMBEDDING_MODEL=BAAI/bge-small-en
```

Never commit `.env`, API keys, database passwords, or certificates to GitHub.

## Running the Current API

From the project root, start the FastAPI application with:

```bash
uvicorn app.api.main:app --reload
```

Open the interactive API documentation at:

```text
http://127.0.0.1:8000/docs
```

The currently implemented root endpoint can be checked with:

```bash
curl http://127.0.0.1:8000/
```

The current response is a simple service-status message. A complete `/chat` endpoint is planned but is not implemented in the current prototype.

## Running Document Ingestion

Before running ingestion, update the document path in `ingest.py` to a local path. For example:

```python
ingest_file("docs/data.pdf")
```

Then execute:

```bash
python ingest.py
```

The script will extract the document text, create chunks, generate embeddings, and save the results to the configured JSON output path. The original version contains a machine-specific Windows path, so that path must be replaced before execution.

## Planned End-to-End RAG Pipeline

The intended production flow is:

1. Ingest one or more PDF or TXT files.
2. Normalize and split the extracted text into meaningful chunks.
3. Generate embeddings with the selected embedding model.
4. Store chunks and vectors in PostgreSQL with pgvector.
5. Embed each user query with the same embedding model.
6. Retrieve the nearest document chunks using cosine similarity or another vector metric.
7. Construct a prompt containing the retrieved context and the user question.
8. Send the prompt to the selected language model.
9. Return the answer and optional source references through FastAPI.
10. Store conversation history when the history endpoint and database schema are implemented.

## Security and Data Handling

This project is designed for document-based question answering, so the documents may contain private or sensitive information. Use private storage for confidential files, apply access control to the API, validate uploaded file types, limit file sizes, and avoid logging entire document contents in production.

The repository should contain source code and configuration examples only. Large documents, generated embeddings, database dumps, API keys, and user conversations should be stored separately and protected with appropriate permissions.

## Limitations

- The complete RAG retrieval and generation path is not implemented yet.
- `vector_store.py` currently describes the intended pgvector integration rather than providing a finished implementation.
- `rag_pipeline.py` contains a planned design rather than a complete answer-generation pipeline.
- The API currently exposes only a basic root endpoint.
- Some local file paths are machine-specific and must be changed.
- The JSON embedding store is suitable for experimentation but not ideal for large-scale retrieval.

## Future Improvements

The next development steps should include implementing the database schema, adding a complete pgvector repository, building `/chat` and `/chat/history` endpoints, adding request validation, returning source citations with every answer, adding automated tests, introducing authentication and rate limiting, and packaging the service with Docker.

## License and Usage Notice

This repository is intended for educational and experimental use. Verify the license of every document and model used by the application before deploying or redistributing the system.
