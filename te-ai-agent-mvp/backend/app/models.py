from enum import Enum
from typing import Optional, Literal
from pydantic import BaseModel, Field


class Workflow(str, Enum):
    api_endpoint = "api_endpoint"
    api_error = "api_error"
    python_script = "python_script"
    transaction_script = "transaction_script"
    general = "general"


class AgentRequest(BaseModel):
    user_input: str = Field(..., min_length=3)
    workflow: Optional[Workflow] = None
    customer_context: Optional[str] = None
    include_curl: bool = True
    include_python_fix: bool = True


class Source(BaseModel):
    title: str
    url: str
    snippet: str
    authority: Literal["official", "internal", "sdk", "mcp", "unknown"] = "unknown"


class AgentResponse(BaseModel):
    workflow: Workflow
    answer_markdown: str
    sources: list[Source] = []
    redactions_applied: bool = False
