from app.embeddings.embedder import generate_query_embedding
from app.vectorstore.qdrant import search_similar_chunks


def understand_query(query: str) -> str:

    # Basic query cleaning
    return query.strip()


def retrieve_multimodal(
    query: str,
    top_k=5,
    score_threshold=0.0
) -> list[dict]:

    # 1. Understand query
    cleaned_query = understand_query(query)

    # 2. Query embedding
    query_vector = generate_query_embedding(
        cleaned_query
    )

    # 3. Multimodal retrieval
    points = search_similar_chunks(
        query_vector,
        top_k=top_k,
        score_threshold=score_threshold
    )

    # 4. Format and rank/filter results
    retrieved_chunks = []

    for point in points:

        payload = point.payload

        retrieved_chunks.append({
            "id": point.id,
            "score": point.score,
            "text": payload.get("text", ""),
            "metadata": payload.get(
                "metadata",
                {}
            )
        })

    return retrieved_chunks
