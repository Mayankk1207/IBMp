from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from service.api import ask_llm
from service.prompts import LEGAL_SYSTEM_PROMPT

app = FastAPI(
    title="ClearLegal AI",
    description="AI-powered legal information assistant",
    version="1.0.0",
)

# -----------------------
# Static Files & Templates
# -----------------------

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


# -----------------------
# Models
# -----------------------

class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    reply: str


# -----------------------
# Pages
# -----------------------

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
    )


@app.get("/chat", response_class=HTMLResponse)
async def chatbot(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="chatbot.html",
    )


@app.get("/terms", response_class=HTMLResponse)
async def terms(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="terms.html",
    )


# -----------------------
# Health Check
# -----------------------

@app.get("/health")
async def health():
    return {
        "status": "ok",
        "service": "ClearLegal AI"
    }


# -----------------------
# Chat API
# -----------------------

@app.post("/api/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):

    # Prevent empty requests
    if not req.message.strip():
        return ChatResponse(
            reply="Please enter a legal question."
        )

    prompt = f"""
{LEGAL_SYSTEM_PROMPT}

User Question:
{req.message}
"""

    try:
        answer = ask_llm(prompt)

        if not answer:
            answer = "Sorry, I couldn't generate a response."

    except Exception as e:
        print(f"LLM Error: {e}")

        answer = (
            "Sorry, I'm unable to generate a response at the moment. "
            "Please try again in a few moments."
        )

    return ChatResponse(reply=answer)