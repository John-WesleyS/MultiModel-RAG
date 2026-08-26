from sentence_transformers import SentenceTransformer


model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


def generate_embeddings(chunks: list[dict]) -> list[dict]:

    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    embeddings = model.encode(texts)

    for chunk, embedding in zip(chunks, embeddings):

        chunk["embedding"] = embedding.tolist()

    return chunks