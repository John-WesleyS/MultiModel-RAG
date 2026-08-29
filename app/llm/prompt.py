from google.genai import types
from PIL import Image
import os


def build_rag_prompt(query, context):

    prompt = f"""
You are a helpful AI assistant.

You are answering questions using information retrieved
from the user's documents.

IMPORTANT RULES:

1. Answer the question using ONLY the provided context.
2. Do not use outside knowledge.
3. Do not make up information.
4. If the answer cannot be found in the context,
   clearly say that the information is not available
   in the provided documents.
5. Give a clear and concise answer.

====================
CONTEXT
====================

{context}

====================
USER QUESTION
====================

{query}

====================
ANSWER
====================
"""

    return prompt


def build_multimodal_prompt(query: str, context: dict) -> list:

    text_context = context.get("text_context", "")

    retrieved_media = context.get("media", [])

    instructions = f"""You are a helpful AI assistant.
You are answering questions using information retrieved from the user's documents.

IMPORTANT RULES:
1. Answer the question using ONLY the provided context (text descriptions and any attached images/media parts).
2. Do not use outside knowledge.
3. Do not make up information.
4. If the answer cannot be found in the context, clearly say that the information is not available in the provided documents.
5. Give a clear and concise answer.

====================
TEXT CONTEXT
====================
{text_context}
"""

    contents = [instructions]

    for item in retrieved_media:

        media_type = item["type"]

        media_path = item["path"]

        mime_type = item["mime_type"]

        if media_type == "image" and os.path.exists(
            media_path
        ):

            try:

                img = Image.open(media_path)

                contents.append(
                    f"\n[Attached image from source document: {item['filename']}]:\n"
                )

                contents.append(img)

            except Exception as e:

                print(
                    f"Error loading retrieved image {media_path}: {e}"
                )

        elif (
            media_type in ["audio", "video"]
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
                    f"\n[Attached {media_type} from source document: {item['filename']}]:\n"
                )

                contents.append(part)

            except Exception as e:

                print(
                    f"Error loading retrieved media {media_path}: {e}"
                )

    contents.append(
        f"\n====================\nUSER QUESTION\n====================\n{query}\n\n====================\nANSWER\n====================\n"
    )

    return contents