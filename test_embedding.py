from app.embeddings.embedder import generate_query_embedding


query = "What is supervised learning?"

embedding = generate_query_embedding(query)

print("Embedding dimensions:", len(embedding))
print("First 10 values:", embedding[:10])