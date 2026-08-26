def split_text(
    text: str,
    chunk_size: int = 1000,
    chunk_overlap: int = 200
) -> list[dict]:

    if chunk_size <= 0:
        raise ValueError(
            "chunk_size must be greater than 0"
        )

    if chunk_overlap < 0:
        raise ValueError(
            "chunk_overlap cannot be negative"
        )

    if chunk_overlap >= chunk_size:
        raise ValueError(
            "chunk_overlap must be smaller than chunk_size"
        )

    chunks = []

    start = 0
    text_length = len(text)

    chunk_index = 0

    while start < text_length:

        end = start + chunk_size

        chunk = text[start:end].strip()

        if chunk:

            chunks.append({
                "text": chunk,

                "metadata": {
                    "chunk_index": chunk_index
                }
            })

            chunk_index += 1

        start = end - chunk_overlap

    return chunks