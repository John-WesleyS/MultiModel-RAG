import os
from sentence_transformers import SentenceTransformer

# Local embedding model configuration (offline, zero Gemini calls)
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
EMBEDDING_DIM = 384

_model = None


def get_embedding_model() -> SentenceTransformer:
    """Lazy-load and cache the SentenceTransformer model singleton."""
    global _model
    if _model is None:
        _model = SentenceTransformer(EMBEDDING_MODEL_NAME)
    return _model


def get_embedding_dim() -> int:
    """Return the vector dimensionality of the embedding model."""
    return EMBEDDING_DIM


def generate_embeddings(texts: list[str]) -> list[list[float]]:
    """
    Generate vector embeddings for a list of text chunks locally.
    Uses local Sentence Transformers without calling Gemini.
    """
    if not texts:
        return []

    model = get_embedding_model()
    cleaned = [t if (isinstance(t, str) and t.strip()) else " " for t in texts]
    embeddings = model.encode(cleaned, convert_to_numpy=True)
    return [emb.tolist() for emb in embeddings]


def generate_query_embedding(query: str) -> list[float]:
    """
    Generate vector embedding for a single user query or text chunk.
    Uses local Sentence Transformers without calling Gemini.
    """
    model = get_embedding_model()
    text = query if (isinstance(query, str) and query.strip()) else " "
    embedding = model.encode(text, convert_to_numpy=True)
    return embedding.tolist()


def generate_image_embedding(image_bytes: bytes, mime_type: str = "image/jpeg") -> list[float]:
    """
    Fallback embedding for image chunks when multimodal visual embedder is not local.
    Returns a local query embedding without calling Gemini.
    """
    return generate_query_embedding(f"Image chunk ({mime_type})")
