# ThousandEyes AI Support Agent — Architecture

## 1. Purpose

The ThousandEyes AI Support Agent is a personal support-assistance application intended for a small engineering team.

The application helps with:

* ThousandEyes API v7 endpoint selection
* API error troubleshooting
* Python API script review
* Transaction Test JavaScript and Selenium troubleshooting
* Chromium and Browser Synthetics investigation
* HAR and waterfall analysis
* Retrieval of relevant support documentation

This project is currently a local development tool and is not intended to be a production customer-facing service.

## 2. Design Principles

The project follows these principles:

* Use official ThousandEyes documentation first.
* Do not invent endpoint paths, parameters, schemas, or permissions.
* Keep secrets out of source code and generated answers.
* Separate retrieval, embedding, storage, and answer generation.
* Support replacing individual AI providers without rewriting the application.
* Prefer local models and local storage where practical.
* Keep deterministic fallback behavior while AI components are developed.

## 3. Current Technology Stack

### Frontend

* React
* Vite
* JavaScript
* CSS

The frontend provides the user interface and sends questions to the FastAPI backend.

### Backend

* Python 3.11
* FastAPI
* Uvicorn
* Pydantic
* HTTPX

The backend provides API endpoints, workflow routing, retrieval, and response generation.

### Knowledge Sources

* Endpoint catalog
* Sample OpenAPI specification
* Official ThousandEyes documentation summaries
* Browser Synthetics troubleshooting guides
* Transaction Test debugging guidance
* API authentication and error-code guidance
* Endpoint Agent and alert troubleshooting guidance

### Local AI Runtime

* Ollama

Ollama runs the embedding model and LLM as local services. FastAPI communicates with Ollama over its local HTTP API.

### Embedding Model

* EmbeddingGemma

EmbeddingGemma converts document chunks and user questions into numeric vectors.

The same embedding model must be used when:

* building the document index;
* embedding incoming user questions.

### Vector Database

* ChromaDB

ChromaDB stores:

* document chunk embeddings;
* source filename;
* document title;
* section heading;
* chunk identifier;
* chunk text;
* additional metadata.

The first implementation uses a local persistent Chroma database.

### Large Language Model

* Gemma 3 4B through Ollama

The LLM will receive:

* system instructions;
* user question;
* detected workflow;
* retrieved documentation chunks;
* endpoint catalog results;
* OpenAPI metadata.

It will generate the final support response.

Until LLM integration is complete, `MockLLMProvider` remains the deterministic fallback.

## 4. Application Architecture

```text
React Frontend
       |
       v
FastAPI Backend
       |
       v
Workflow Router
       |
       +--------------------+
       |                    |
       v                    v
Endpoint Catalog       OpenAPI Loader
       |                    |
       +---------+----------+
                 |
                 v
        Documentation Corpus
                 |
                 v
           Smart Chunker
                 |
                 v
     EmbeddingGemma via Ollama
                 |
                 v
              ChromaDB
                 |
                 v
      Top Relevant Document Chunks
                 |
                 + OpenAPI Metadata
                 + Endpoint Information
                 |
                 v
        Gemma 3 4B via Ollama
                 |
                 v
        Grounded Support Answer
```

## 5. Backend Components

### `main.py`

Defines FastAPI routes and connects application services.

### `router.py`

Classifies user input into workflows:

* `api_endpoint`
* `api_error`
* `python_script`
* `transaction_script`
* `general`

### `knowledge.py`

Loads endpoint knowledge and performs deterministic endpoint matching.

### `openapi_loader.py`

Loads OpenAPI metadata and extracts:

* methods;
* paths;
* summaries;
* parameters;
* response codes.

### `docs_loader.py`

Loads local Markdown documentation and currently provides keyword retrieval.

### `chunker.py`

Splits Markdown documents into searchable chunks.

Each chunk contains metadata such as:

* `chunk_id`
* `source`
* `document_title`
* `heading`
* `section_chunk_number`
* `content`
* `character_count`

### `embedding/base.py`

Defines the common interface used by embedding providers.

### `embedding/ollama_provider.py`

Calls Ollama to create embeddings with EmbeddingGemma.

### Future `vector_store.py`

Stores and queries embeddings in ChromaDB.

### `llm.py`

Currently contains deterministic support-response templates.

It will later be refactored to use Gemma 3 while retaining a deterministic fallback.

## 6. Retrieval-Augmented Generation Flow

### Indexing

```text
Markdown documents
       |
       v
Smart chunker
       |
       v
Document chunks
       |
       v
EmbeddingGemma
       |
       v
ChromaDB
```

Indexing is performed when:

* the knowledge base is created;
* documentation is added;
* documentation is modified;
* the embedding model changes.

### Querying

```text
User question
       |
       v
EmbeddingGemma
       |
       v
ChromaDB similarity search
       |
       v
Top relevant chunks
       |
       v
Gemma 3 answer generation
```

## 7. Data and Security

* Bearer tokens, passwords, cookies, and client secrets must not be committed.
* Secrets must not be included in documentation chunks.
* `.env` files must remain excluded from Git.
* Retrieved customer content should be sanitized before storage or logging.
* Ollama and ChromaDB run locally during development.
* The application should not expose Ollama directly to untrusted networks.
* Generated answers must clearly distinguish official facts from representative examples.

## 8. Local Model Selection

### Embedding model

`embeddinggemma`

Purpose:

* semantic search;
* document retrieval;
* similarity comparison.

### LLM

`gemma3:4b`

Purpose:

* answer synthesis;
* API troubleshooting;
* Python and JavaScript review;
* Transaction Test guidance.

If local performance is insufficient, model size may be changed without altering the retrieval architecture.

## 9. Development Roadmap

### Completed

* Phase 1: Frontend and backend scaffold
* Phase 2A: Endpoint coverage
* Phase 2B: External endpoint catalog
* Phase 3A: OpenAPI loader
* Phase 3B: Documentation loader
* Phase 3C.1: Smart document chunker

### In progress

* Phase 3C.2: Ollama embedding provider

### Planned

* Phase 3C.3: ChromaDB vector index
* Phase 3C.4: Semantic search integration
* Phase 4: Gemma 3 LLM integration
* Phase 5: Additional live knowledge and tool integrations
* Automated tests
* Simplified startup scripts
* Small-team deployment documentation

## 10. Agreed Local Stack

```text
Embedding runtime: Ollama
Embedding model:   embeddinggemma
Vector database:   ChromaDB
LLM runtime:       Ollama
LLM model:         gemma3:4b
```
