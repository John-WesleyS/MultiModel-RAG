import os

from dotenv import load_dotenv
from google import genai


load_dotenv()


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set")


client = genai.Client(
    api_key=GEMINI_API_KEY
)


def generate_response(prompt):

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text


def describe_media(
    media_bytes: bytes,
    mime_type: str,
    media_type: str
) -> str:

    from google.genai import types

    part = types.Part.from_bytes(
        data=media_bytes,
        mime_type=mime_type
    )

    if media_type == "image":

        prompt = "Describe this image in detail for a search index. What is shown, what are the key concepts, text, visual details, and context?"

    elif media_type == "video":

        prompt = "Provide a detailed summary of the events, visual details, text, and any spoken dialogue in this video."

    elif media_type == "audio":

        prompt = "Transcribe and summarize this audio recording."

    else:

        prompt = "Describe this document media chunk in detail."

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[part, prompt]
        )

        return response.text

    except Exception as e:

        print(
            f"Error generating description for media: {e}"
        )

        return f"Media chunk ({media_type}) - Extraction failed."