import os
import shutil

from fastapi import (
    FastAPI,
    Request,
    UploadFile,
    File
)
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from rag.pipeline import chat
from rag.loader import process_pdf


app = FastAPI(
    title="ClearLegal AI",
    description="AI-powered legal information assistant",
    version="1.0.0",
)

# -----------------------
# Directories
# -----------------------

UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)

# -----------------------
# Static Files & Templates
# -----------------------

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static",
)

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
# Health
# -----------------------

@app.get("/health")
async def health():

    return {
        "status": "ok",
        "service": "ClearLegal AI",
    }

# -----------------------
# Upload PDF
# -----------------------

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    if not file.filename.endswith(".pdf"):

        return {
            "message": "Only PDF files are allowed."
        }

    filepath = os.path.join(
        UPLOAD_DIR,
        file.filename
    )

    with open(filepath, "wb") as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )

    # Build the vector database
    process_pdf(filepath)

    return {
        "message": "PDF uploaded successfully."
    }

# -----------------------
# Chat
# -----------------------

@app.post(
    "/api/chat",
    response_model=ChatResponse
)
async def chat_endpoint(req: ChatRequest):

    if not req.message.strip():

        return ChatResponse(
            reply="Please enter a legal question."
        )

    try:

        answer = chat(req.message)

        if not answer:

            answer = (
                "Sorry, I couldn't generate a response."
            )

    except Exception as e:

        print(e)

        answer = (
            "Sorry, I'm unable to generate a response "
            "at the moment."
        )

    return ChatResponse(
        reply=answer
    )