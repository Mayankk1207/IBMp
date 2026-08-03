from rag.retrieval import retrieve
from service.prompts import build_prompt
from service.api import ask_llm


def chat(question: str):

    result = retrieve(question)

    docs = result["documents"][0]

    context = "\n\n".join(docs)

    prompt = build_prompt(question, context)

    return ask_llm(prompt)