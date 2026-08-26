from app.embeddings.embedder import generate_embedding


text = "Machine learning is a branch of artificial intelligence."

embedding = generate_embedding(text)

print("Vector dimensions:", len(embedding))

print("First 10 values:")
print(embedding[:10])