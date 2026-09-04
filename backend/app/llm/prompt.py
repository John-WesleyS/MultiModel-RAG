from google.genai import types
from PIL import Image
import os


def build_rag_prompt(query, context, conversation_history=""):

    # Handle context whether it's dict or string
    if isinstance(context, dict):
        text_context = context.get("text_context", "")
    else:
        text_context = str(context)

    history_section = ""
    if conversation_history:
        history_section = f"\n{conversation_history}\n"

    prompt = f"""You are a helpful AI assistant.
You are answering questions using information retrieved from the user's documents.

IMPORTANT RULES:
1. Answer the question using ONLY the provided context.
2. Do not use outside knowledge.
3. Do not make up information.
4. If the answer cannot be found in the context, clearly say that the information is not available in the provided documents.
5. Give a clear, accurate, and concise answer.
6. When relevant, cite the specific source(s) used (e.g. [Source 1], [Source 2]).

====================
CONTEXT
====================
{text_context}
{history_section}
====================
USER QUESTION
====================
{query}

====================
ANSWER
====================
"""
    return prompt


def build_multimodal_prompt(query: str, context: dict, conversation_history: str = "") -> list:

    # Handle context whether it's dict or string
    if isinstance(context, dict):
        text_context = context.get("text_context", "")
        retrieved_media = context.get("media", [])
    else:
        text_context = str(context)
        retrieved_media = []

    history_section = ""
    if conversation_history:
        history_section = f"\n{conversation_history}\n"

    instructions = f"""You are a helpful AI assistant.
You are answering questions using information retrieved from the user's documents.

IMPORTANT RULES:
1. Answer the question using ONLY the provided context (text descriptions and any attached images/media parts).
2. Do not use outside knowledge.
3. Do not make up information.
4. If the answer cannot be found in the context, clearly say that the information is not available in the provided documents.
5. Give a clear, accurate, and concise answer.
6. Cite the specific source(s) you use (e.g. [Source 1], [Source 2]).

====================
TEXT CONTEXT
====================
{text_context}
{history_section}"""

    contents = [instructions]

    for item in retrieved_media:

        media_type = item.get("type", "")
        media_path = item.get("path")
        mime_type = item.get("mime_type", "")
        filename = item.get("filename", "unknown")

        if media_type == "image" and media_path and os.path.exists(media_path):

            try:
                img = Image.open(media_path)
                contents.append(
                    f"\n[Attached image from source document: {filename}]:\n"
                )
                contents.append(img)
            except Exception as e:
                print(f"Error loading retrieved image {media_path}: {e}")

        elif (
            media_type in ["audio", "video"]
            and media_path
            and os.path.exists(media_path)
        ):

            try:
                with open(media_path, "rb") as f:
                    file_bytes = f.read()

                part = types.Part.from_bytes(
                    data=file_bytes,
                    mime_type=mime_type
                )
                contents.append(
                    f"\n[Attached {media_type} from source document: {filename}]:\n"
                )
                contents.append(part)
            except Exception as e:
                print(f"Error loading retrieved media {media_path}: {e}")

    contents.append(
        f"\n====================\nUSER QUESTION\n====================\n{query}\n\n====================\nANSWER\n====================\n"
    )

    return contents
