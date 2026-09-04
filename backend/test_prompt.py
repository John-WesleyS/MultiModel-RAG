from app.embeddings.embedder import generate_query_embedding
from app.vectorstore.qdrant import search_similar_chunks
from app.retrieval.context_builder import build_context
from app.llm.prompt import build_rag_prompt


query = "What is Lehman's first law?"


# 1. Convert query into embedding

query_vector = generate_query_embedding(query)


# 2. Retrieve relevant chunks

retrieved_chunks = search_similar_chunks(
    query_vector,
    top_k=5,
    score_threshold=0.0
)


# 3. Build context

context = build_context(retrieved_chunks)


# 4. Build final prompt

prompt = build_rag_prompt(
    query=query,
    context=context
)


print("\n==============================")
print("FINAL RAG PROMPT")
print("==============================")

print(prompt)