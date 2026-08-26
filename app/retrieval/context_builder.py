def build_context(retrieved_chunks):

    if not retrieved_chunks:
        return ""

    context_parts = []

    for i, chunk in enumerate(retrieved_chunks, start=1):

        metadata = chunk.get("metadata", {})

        filename = metadata.get(
            "filename",
            "Unknown document"
        )

        chunk_index = metadata.get(
            "chunk_index",
            "Unknown"
        )

        text = chunk.get("text", "")

        context_part = f"""
[Source {i}]
Document: {filename}
Chunk: {chunk_index}

{text}
"""

        context_parts.append(context_part.strip())

    return "\n\n".join(context_parts)