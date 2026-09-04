from app.embeddings.embedder import generate_query_embedding
from app.vectorstore.qdrant import search_similar_chunks


def understand_query(query: str) -> str:
    # Basic query cleaning
    return query.strip() if query else ""


def retrieve_multimodal(
    query: str,
    top_k=5,
    score_threshold=0.0
) -> list[dict]:

    # 1. Understand query
    cleaned_query = understand_query(query)

    # 2. Query embedding (local Sentence Transformers)
    query_vector = generate_query_embedding(
        cleaned_query
    )

    # 3. Multimodal retrieval from Qdrant
    results = search_similar_chunks(
        query_vector,
        top_k=top_k,
        score_threshold=score_threshold
    )

    # 4. Format and ensure clean dict structures
    retrieved_chunks = []
    for item in results:
        if isinstance(item, dict):
            retrieved_chunks.append(item)
        else:
            payload = getattr(item, "payload", {}) or {}
            retrieved_chunks.append({
                "id": str(getattr(item, "id", "")),
                "score": float(getattr(item, "score", 0.0)),
                "text": payload.get("text", ""),
                "metadata": payload.get("metadata", {})
            })

    return retrieved_chunks

