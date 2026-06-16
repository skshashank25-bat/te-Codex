from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .models import AgentRequest, AgentResponse
from .router import route_workflow
from .redaction import redact_sensitive
from .knowledge import StubRetriever
from .llm import MockLLMProvider

app = FastAPI(title="ThousandEyes AI Support Agent MVP", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

retriever = StubRetriever()
llm = MockLLMProvider()


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/agent", response_model=AgentResponse)
async def agent(req: AgentRequest):
    clean_input, redacted = redact_sensitive(req.user_input)
    workflow = req.workflow or route_workflow(clean_input)
    sources = await retriever.search(clean_input, workflow.value)
    answer = await llm.generate(clean_input, workflow, sources)
    return AgentResponse(
        workflow=workflow,
        answer_markdown=answer,
        sources=sources,
        redactions_applied=redacted,
    )
