import os

from dotenv import load_dotenv
from xai_sdk import Client
from xai_sdk.chat import user


load_dotenv()


api_key = os.getenv("XAI_API_KEY")

if not api_key:
    raise ValueError("XAI_API_KEY is not set")


client = Client(api_key=api_key)

MODEL_NAME = "grok-4.6"


def generate_response(prompt: str) -> str:

    chat = client.chat.create(
        model=MODEL_NAME
    )

    chat.append(
        user(prompt)
    )

    response = chat.sample()

    return response.content