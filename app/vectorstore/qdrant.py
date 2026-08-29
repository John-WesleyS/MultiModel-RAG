from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct
)
import uuid


COLLECTION_NAME = "documents"

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

            # If it's a single vector config
            if hasattr(
                vectors_config,
                "size"
            ):
                current_size = vectors_config.size

            else:

                current_size = 0

            if current_size != 768:

                print(
                    f"Collection size mismatch: expected 768, got {current_size}. Recreating."
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

        existing.remove(COLLECTION_NAME)

    if COLLECTION_NAME not in existing:

        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=768,
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
                "text": chunk["text"],
                "metadata": chunk["metadata"]
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

    return results.points