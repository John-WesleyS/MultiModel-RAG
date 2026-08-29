import os


def build_context(chunks):

    context_parts = []

    retrieved_media = []

    for i, chunk in enumerate(chunks, start=1):

        text = chunk.get("text", "")

        metadata = chunk.get("metadata", {})

        filename = metadata.get("filename", "Unknown")

        chunk_index = metadata.get("chunk_index", "Unknown")

        chunk_type = metadata.get("chunk_type", "text")

        media_path = metadata.get("media_path")

        source_header = f"[Source {i}] (Type: {chunk_type.upper()})\nDocument: {filename}\nChunk Index: {chunk_index}"

        if chunk_type == "text":

            context_parts.append(
                f"{source_header}\n\n{text}"
            )

        else:

            context_parts.append(
                f"{source_header}\nDescription: {text}"
            )

            if media_path and os.path.exists(
                media_path
            ):

                retrieved_media.append({
                    "type": chunk_type,
                    "path": media_path,
                    "mime_type": metadata.get(
                        "mime_type"
                    ),
                    "filename": filename
                })

    return {
        "text_context": "\n\n====================\n\n".join(
            context_parts
        ),
        "media": retrieved_media
    }