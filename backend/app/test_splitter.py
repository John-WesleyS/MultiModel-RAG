from app.ingestion.splitter import split_text


text = """
Machine learning is a branch of artificial intelligence.
It allows computers to learn patterns from data.

Supervised learning uses labeled training data.
The model learns a relationship between inputs and outputs.

Classification is a supervised learning task.
"""


chunks = split_text(
    text,
    chunk_size=80,
    chunk_overlap=20
)


for i, chunk in enumerate(chunks):

    print(f"\n--- CHUNK {i + 1} ---")

    print(chunk)