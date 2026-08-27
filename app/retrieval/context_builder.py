def build_context(chunks):

    context_parts = []

    for i, chunk in enumerate(chunks, start=1):

        text = chunk["text"]
        metadata = chunk["metadata"]

        filename = metadata.get("filename", "Unknown")
        chunk_id = metadata.get("chunk_id", "Unknown")

        context_parts.append(
            f"""
[Source {i}]
Document: {filename}
Chunk: {chunk_id}

{text}
"""
        )

    return "\n".join(context_parts)