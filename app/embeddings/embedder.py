import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set")

client = genai.Client(
    api_key=GEMINI_API_KEY
)

EMBEDDING_MODEL = "gemini-embedding-2"
EMBEDDING_DIM = 768


def generate_embeddings(texts: list[str]) -> list[list[float]]:

    if not texts:
        return []

    try:

        response = client.models.embed_content(
            model=EMBEDDING_MODEL,
            contents=texts,
            config=types.EmbedContentConfig(
                output_dimensionality=EMBEDDING_DIM
            )
        )

        return [
            emb.values
            for emb in response.embeddings
        ]

    except Exception as e:

        print(
            f"Error generating text embeddings: {e}"
        )

        raise e


def generate_query_embedding(query: str) -> list[float]:

    try:

        response = client.models.embed_content(
            model=EMBEDDING_MODEL,
            contents=query,
            config=types.EmbedContentConfig(
                output_dimensionality=EMBEDDING_DIM
            )
        )

        return response.embeddings[0].values

    except Exception as e:

        print(
            f"Error generating query embedding: {e}"
        )

        raise e


def generate_image_embedding(
    image_bytes: bytes,
    mime_type: str
) -> list[float]:

    try:

        part = types.Part.from_bytes(
            data=image_bytes,
            mime_type=mime_type
        )

        response = client.models.embed_content(
            model=EMBEDDING_MODEL,
            contents=[part],
            config=types.EmbedContentConfig(
                output_dimensionality=EMBEDDING_DIM
            )
        )

        return response.embeddings[0].values

    except Exception as e:

        print(
            f"Error generating image embedding: {e}"
        )

        raise e