"""
AI chat proxy endpoint.

Proxies requests to the Anthropic API so the browser never makes a
cross-origin request directly to api.anthropic.com (avoiding CORS issues).

The user's API key arrives in the request body, is used for the Anthropic
call, and is then discarded — it is never stored in the database.
"""
import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

import httpx

router = APIRouter(prefix="/api/ai", tags=["ai"])
logger = logging.getLogger(__name__)

ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"
ANTHROPIC_VERSION = "2023-06-01"
# Use Haiku for fast, cheap responses in tutoring context
MODEL = "claude-haiku-4-5-20251001"
MAX_TOKENS = 300

SYSTEM_PROMPT_TEMPLATE = (
    "You are a math tutor helping a student with {topic}. "
    "The student is working on this problem: {problem_text}. "
    "Available hints for this problem: {hints}.\n\n"
    "Guide the student toward the answer without giving it away directly. "
    "Ask leading questions. Use LaTeX notation for math (wrap in \\( \\) "
    "for inline or \\[ \\] for display). Keep responses concise — 2-3 "
    "sentences max unless the student asks for more detail."
)


class AIChatMessage(BaseModel):
    role: str  # "user" | "assistant"
    content: str


class AIChatContext(BaseModel):
    topic: str = ""
    problem_text: str = ""
    hints: list[str] = []


class AIChatRequest(BaseModel):
    api_key: str
    messages: list[AIChatMessage]
    context: AIChatContext = AIChatContext()


@router.post("/chat")
async def ai_chat(req: AIChatRequest):
    """Proxy a chat request to Anthropic's API."""
    # Validate API key format
    if not req.api_key or not req.api_key.startswith("sk-ant-"):
        raise HTTPException(status_code=401, detail="Invalid API key")

    if not req.messages:
        raise HTTPException(status_code=400, detail="No messages provided")

    # Build system prompt from context
    hints_text = "; ".join(req.context.hints) if req.context.hints else "No hints available."
    system_prompt = SYSTEM_PROMPT_TEMPLATE.format(
        topic=req.context.topic or "math",
        problem_text=req.context.problem_text or "(not specified)",
        hints=hints_text,
    )

    # Build messages array for Anthropic
    messages = [{"role": m.role, "content": m.content} for m in req.messages]

    headers = {
        "x-api-key": req.api_key,
        "anthropic-version": ANTHROPIC_VERSION,
        "content-type": "application/json",
    }

    body = {
        "model": MODEL,
        "max_tokens": MAX_TOKENS,
        "system": system_prompt,
        "messages": messages,
    }

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(ANTHROPIC_API_URL, headers=headers, json=body)
    except httpx.ConnectError:
        raise HTTPException(status_code=502, detail="Could not reach AI service")
    except httpx.TimeoutException:
        raise HTTPException(status_code=502, detail="AI service timed out")
    except Exception as e:
        logger.error("AI proxy error: %s", e)
        raise HTTPException(status_code=502, detail="AI service unavailable")

    if response.status_code == 401:
        raise HTTPException(status_code=401, detail="Invalid API key")
    if response.status_code == 429:
        raise HTTPException(status_code=429, detail="Rate limited, try again")
    if response.status_code != 200:
        logger.error("Anthropic API error %s: %s", response.status_code, response.text[:200])
        raise HTTPException(status_code=502, detail="AI service unavailable")

    try:
        data = response.json()
        text = data["content"][0]["text"]
    except (KeyError, IndexError, ValueError) as e:
        logger.error("Unexpected Anthropic response format: %s", e)
        raise HTTPException(status_code=502, detail="AI service unavailable")

    return {"response": text}
