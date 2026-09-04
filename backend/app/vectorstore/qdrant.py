from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue,
)
import uuid


COLLECTION_NAME = "documents"
VECTOR_SIZE = 384

client = QdrantClient(
    path="./qdrant_data"
)


def create_collection():

    collections = client.get_collections()

    existing = [
        collection.name
        for collection in collections.collections
    ]

    recreate = False

    if COLLECTION_NAME in existing:

        try:

            info = client.get_collection(
                COLLECTION_NAME
            )

            # Check existing configuration size
            vectors_config = info.config.params.vectors

            if hasattr(
                vectors_config,
                "size"
            ):
                current_size = vectors_config.size
            else:
                current_size = 0

            if current_size != VECTOR_SIZE:

                print(
                    f"Collection size mismatch: expected {VECTOR_SIZE}, got {current_size}. Recreating."
                )

                recreate = True

        except Exception as e:

            print(
                f"Error checking collection config: {e}. Recreating."
            )

            recreate = True

    if recreate:

        client.delete_collection(
            COLLECTION_NAME
        )

        if COLLECTION_NAME in existing:
            existing.remove(COLLECTION_NAME)

    if COLLECTION_NAME not in existing:

        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=VECTOR_SIZE,
                distance=Distance.COSINE
            )
        )


def store_chunks(chunks, embeddings):

    points = []

    for chunk, embedding in zip(
        chunks,
        embeddings
    ):

        point = PointStruct(
            id=str(uuid.uuid4()),
            vector=embedding,
            payload={
                "text": chunk.get("text", ""),
                "metadata": chunk.get("metadata", {})
            }
        )

        points.append(point)

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )


def search_similar_chunks(
    query_vector,
    top_k=5,
    score_threshold=0.0
):

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=top_k,
        score_threshold=score_threshold,
        with_payload=True
    )

    formatted = []
    for point in results.points:
        payload = point.payload or {}
        formatted.append({
            "id": str(point.id),
            "score": float(point.score),
            "text": payload.get("text", ""),
            "metadata": payload.get("metadata", {})
        })

    return formatted


def delete_document_points(document_id: str) -> int:
    """
    Delete all points corresponding to a specific document_id.
    Returns the count of points deleted.
    """
    try:
        # Count points before deletion
        scroll_filter = Filter(
            must=[
                FieldCondition(
                    key="metadata.document_id",
                    match=MatchValue(value=document_id)
                )
            ]
        )
        
        points, _ = client.scroll(
            collection_name=COLLECTION_NAME,
            scroll_filter=scroll_filter,
            limit=10000,
            with_payload=False
        )
        count = len(points)

        client.delete(
            collection_name=COLLECTION_NAME,
            points_selector=scroll_filter
        )
        return count
    except Exception as e:
        print(f"Error deleting document points for {document_id}: {e}")
        return 0


def get_all_documents() -> list[dict]:
    """
    Scroll through Qdrant collection and group stored points by document_id.
    Returns list of document summaries.
    """
    try:
        points, _ = client.scroll(
            collection_name=COLLECTION_NAME,
            limit=10000,
            with_payload=True
        )

        docs_map = {}
        for point in points:
            payload = point.payload or {}
            metadata = payload.get("metadata", {})
            doc_id = metadata.get("document_id", "Unknown")

            if doc_id not in docs_map:
                docs_map[doc_id] = {
                    "document_id": doc_id,
                    "filename": metadata.get("filename", "Unknown"),
                    "file_type": metadata.get("file_type", "Unknown"),
                    "chunks_count": 0,
                    "media_count": 0
                }

            docs_map[doc_id]["chunks_count"] += 1
            if metadata.get("chunk_type") != "text":
                docs_map[doc_id]["media_count"] += 1

        return list(docs_map.values())
    except Exception as e:
        print(f"Error retrieving all documents: {e}")
        return []


def get_collection_stats() -> dict:
    """Return collection point count and status."""
    try:
        info = client.get_collection(COLLECTION_NAME)
        return {
            "collection_name": COLLECTION_NAME,
            "points_count": info.points_count,
            "vector_size": VECTOR_SIZE,
            "status": str(info.status)
        }
    except Exception as e:
        return {"error": str(e)}