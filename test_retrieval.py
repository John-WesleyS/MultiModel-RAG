from app.embeddings.embedder import generate_query_embedding
from app.vectorstore.qdrant import search_similar_chunks


query = "explain about SOFTWARE MAINTENANCE PROCESS models"

query_vector = generate_query_embedding(query)

results = search_similar_chunks(
    query_vector,
    top_k=5,
    score_threshold=0.5
)

print("\nQuery:")
print(query)

print("\nRetrieved chunks:")

for i, result in enumerate(results, start=1):

    print("\n-----------------------------")

    print(f"Result {i}")

    print("Score:", result["score"])

    print("Metadata:", result["metadata"])

    print("Text:")
    print(result["text"])
    print("\n-----------------------------")