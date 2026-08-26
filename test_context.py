from app.embeddings.embedder import generate_query_embedding
from app.vectorstore.qdrant import search_similar_chunks
from app.retrieval.context_builder import build_context


query = "What is Lehman's first law?"

query_vector = generate_query_embedding(query)

retrieved_chunks = search_similar_chunks(
    query_vector,
    top_k=5,
    score_threshold=0.0
)

print("\n==============================")
print("QUERY")
print("==============================")

print(query)

print("\n==============================")
print("RETRIEVED CHUNKS")
print("==============================")

print("Number of chunks:", len(retrieved_chunks))

for i, chunk in enumerate(retrieved_chunks, start=1):

    print("\n-----------------------------")
    print(f"Result {i}")
    print("Score:", chunk["score"])
    print("Metadata:", chunk["metadata"])
    print("Text:", chunk["text"])


context = build_context(retrieved_chunks)

print("\n==============================")
print("CONTEXT")
print("==============================")

print(context)