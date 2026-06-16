# ThousandEyes AI Support Agent MVP

Internal web app scaffold for a Cisco ThousandEyes API v7 and Transaction Script assistant.

## What it does

The app routes support-engineer questions into four workflows:

1. API v7 endpoint finder
2. API error troubleshooter
3. Python API script reviewer
4. ThousandEyes Transaction JavaScript/Selenium script reviewer

It is designed to ground answers in:

- Official ThousandEyes API v7 docs
- ThousandEyes OpenAPI specs
- Official ThousandEyes product docs
- Transaction Scripting Reference
- Python SDK docs/examples
- Internal TAC runbooks and sanitized resolved cases
- Optional ThousandEyes MCP server

## Architecture

```text
frontend/ React + Vite
backend/  FastAPI
          Agent router
          RAG retriever interface
          MCP client placeholder
          LLM provider placeholder
```

## Quick start

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open the frontend and point it at `http://localhost:8000`.

## Environment variables

Create `backend/.env` from `.env.example`.

```bash
OPENAI_API_KEY=replace_me
TE_MCP_URL=http://localhost:3333
VECTOR_DB_PATH=./data/index
```

## Next implementation steps

1. Replace `MockLLMProvider` with your approved Cisco/OpenAI provider.
2. Replace `StubRetriever` with a vector index over official docs and OpenAPI specs.
3. Connect `MCPClient` to the ThousandEyes MCP server running in Codex.
4. Add Cisco SSO/auth middleware.
5. Add logging with sensitive-value redaction.
6. Add unit tests with known API v7 endpoint examples and common support cases.

## Safety rules

- Do not store or log bearer tokens, passwords, client secrets, or cookies.
- Redact Authorization headers before saving conversations.
- Prefer curl reproduction for TAC escalation.
- Label generated examples as representative when not copied from official docs.
