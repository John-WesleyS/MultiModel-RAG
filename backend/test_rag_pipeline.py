from app.embeddings.embedder import generate_query_embedding
from app.vectorstore.qdrant import search_similar_chunks
from app.retrieval.context_builder import build_context
from app.llm.prompt import build_rag_prompt


query = "What is Lehman's first law?"


# 1. Query → embedding

query_vector = generate_query_embedding(query)


# 2. Embedding → Qdrant retrieval

retrieved_chunks = search_similar_chunks(
    query_vector,
    top_k=5,
    score_threshold=0.0
)


# 3. Retrieved chunks → context

context = build_context(
    retrieved_chunks
)


# 4. Context + query → prompt

prompt = build_rag_prompt(
    query=query,
    context=context
)


print("\n==============================")
print("RETRIEVED CHUNKS")
print("==============================")

for chunk in retrieved_chunks:
    print(chunk)


print("\n==============================")
print("CONTEXT")
print("==============================")

print(context)


print("\n==============================")
print("FINAL PROMPT")
print("==============================")

print(prompt)