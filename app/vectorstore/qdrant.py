import uuid

from qdrant_client import QdrantClient

from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct
)


client = QdrantClient(
    path="./qdrant_data"
)


COLLECTION_NAME = "documents"


def create_collection():

    collections = client.get_collections()

    existing_collections = [
        collection.name
        for collection in collections.collections
    ]

    if COLLECTION_NAME not in existing_collections:

        client.create_collection(
            collection_name=COLLECTION_NAME,

            vectors_config=VectorParams(
                size=384,
                distance=Distance.COSINE
            )
        )


def store_chunks(chunks):

    points = []

    for chunk in chunks:

        point = PointStruct(
            id=str(uuid.uuid4()),
            vector=chunk["embedding"],
            payload={
                "text": chunk["text"],
                "metadata": chunk["metadata"]
            }
        )
        points.append(point)
    client.upsert(
        collection_name=COLLECTION_NAME,

        points=points
    )
    
def search_similar_chunks(query_vector, top_k=5):

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=top_k,
        with_payload=True
    )

    retrieved_chunks = []

    for result in results.points:

        retrieved_chunks.append({
            "text": result.payload["text"],
            "metadata": result.payload["metadata"],
            "score": result.score
        })

    return retrieved_chunks         