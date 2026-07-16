import os
from dotenv import load_dotenv
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("key"),
    base_url="https://openrouter.ai/api/v1",
)


def ask_llm(prompt: str):
    response = client.chat.completions.create(
        model="google/gemini-2.5-flash",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        max_tokens=256,
        temperature=0.3,
    )

    return response.choices[0].message.content