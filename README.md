# ClearLegal AI

An AI-powered assistant that answers general legal questions in plain English, backed by a FastAPI service and a lightweight web UI.

## Overview

ClearLegal AI is built for people who need quick, understandable answers to general legal questions without the jargon. The assistant is guardrailed with a system prompt that keeps it from giving legal advice, reminds users that answers vary by jurisdiction, and points them to a licensed attorney for anything beyond general information.

## Features

- **Landing page** introducing the product and its value proposition
- **Chat interface** for asking general legal questions and getting plain-English answers
- **Terms & Conditions page** with a redesigned, readable layout
- **Guardrailed responses** — the system prompt restricts the model to legal *information* (not advice), caps response length, and enforces plain-text (no markdown) replies
- **Health check endpoint** for monitoring/deployment

## Tech Stack

- **Backend:** FastAPI, Jinja2 templates, served via Uvicorn
- **LLM access:** OpenAI Python SDK configured against the OpenRouter API, calling `google/gemini-2.5-flash`
- **Frontend:** Vanilla HTML/CSS
- **Containerization:** Docker + docker-compose

## API

| Method | Route        | Description                                  |
|--------|--------------|-----------------------------------------------|
| GET    | `/`          | Landing page                                  |
| GET    | `/chat`      | Chat UI                                       |
| GET    | `/terms`     | Terms & Conditions page                       |
| GET    | `/health`    | Health check — returns service status         |
| POST   | `/api/chat`  | Send `{ "message": "..." }`, returns `{ "reply": "..." }` |

## Getting Started

### Prerequisites

- Python 3.10+
- An [OpenRouter](https://openrouter.ai/) API key

### Installation

```bash
git clone https://github.com/Mayankk1207/ClearLegalAI.git
cd ClearLegalAI
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```
key=your_openrouter_api_key_here
```

### Run locally

```bash
uvicorn main:app --reload
```

Visit `http://localhost:8000`.

### Run with Docker

```bash
docker-compose up --build
```

## Project Structure

```
ClearLegalAI/
├── main.py                # FastAPI app, routes, chat endpoint
├── service/
│   ├── api.py              # LLM client (OpenRouter) and ask_llm()
│   └── prompts.py           # System prompt / guardrails
├── templates/
│   ├── index.html           # Landing page
│   ├── chatbot.html          # Chat UI
│   └── terms.html            # Terms & Conditions page
├── static/
│   └── style.css
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## Roadmap

- Persist chat history (MongoDB integration is scaffolded via `pymongo` in dependencies but not yet wired up)
- Document upload + retrieval-augmented answers for user-specific contracts/agreements
- Configurable LLM provider (swap OpenRouter/Gemini for other models)
