from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import uuid
import os

from app.ingestion.file_detector import get_file_type
from app.ingestion.loader import load_document
from app.ingestion.processors.document_processor import process_document

from app.embeddings.embedder import (
    generate_embeddings,
    generate_query_embedding,
    generate_image_embedding,
)

from app.vectorstore.qdrant import (
    create_collection,
    store_chunks,
)

from app.retrieval.retriever import retrieve_multimodal
from app.retrieval.context_builder import build_context
from app.retrieval.source_builder import build_sources

from app.llm.prompt import build_multimodal_prompt
from app.llm.llm import generate_response


app = FastAPI()


# =========================================================
# STARTUP
# =========================================================

@app.on_event("startup")
def startup_event():

    create_collection()


# =========================================================
# CHAT REQUEST
# =========================================================

class ChatRequest(BaseModel):

    query: str


# =========================================================
# INGEST
# =========================================================

@app.post("/ingest")
async def ingest_document(
    file: UploadFile = File(...)
):

    document_id = str(uuid.uuid4())

    try:

        # 1. Detect file type
        file_type = get_file_type(
            file.filename
        )

        # 2. Read file bytes
        file_bytes = await file.read()

        # 3. Load document into raw unified form
        document = load_document(
            file_bytes=file_bytes,
            filename=file.filename,
            file_type=file_type,
            document_id=document_id
        )

        # 4. Process document (text chunking & local media extraction + description)
        chunks = process_document(document)

        if not chunks:

            return {
                "document_id": document_id,
                "filename": file.filename,
                "status": "No text or media content was extracted from the file."
            }

        # 5. Generate embeddings for each chunk
        embeddings = []

        for chunk in chunks:

            c_type = chunk["metadata"].get("chunk_type", "text")

            media_path = chunk["metadata"].get("media_path")

            # Generate true visual embedding for images
            if c_type == "image" and media_path and os.path.exists(media_path):

                try:

                    with open(media_path, "rb") as f:

                        img_bytes = f.read()

                    mime_type = chunk["metadata"].get(
                        "mime_type",
                        "image/jpeg"
                    )

                    emb = generate_image_embedding(
                        img_bytes,
                        mime_type
                    )

                    embeddings.append(emb)

                except Exception as e:

                    print(
                        f"Error generating visual embedding for {media_path}: {e}. Falling back to text."
                    )

                    emb = generate_query_embedding(
                        chunk["text"]
                    )

                    embeddings.append(emb)

            else:

                # For text, audio, and video summaries
                emb = generate_query_embedding(
                    chunk["text"]
                )

                embeddings.append(emb)

        # 6. Store in Qdrant
        store_chunks(chunks, embeddings)

        print("\n========== INGESTION COMPLETE ==========")
        print("Filename:", file.filename)
        print("File type:", file_type)
        print("Chunks stored:", len(chunks))
        print("========================================")

        return {
            "document_id": document_id,
            "filename": file.filename,
            "file_type": file_type,
            "file_size": len(file_bytes),
            "chunks_count": len(chunks),
            "status": "Document ingested and indexed successfully"
        }

    except ValueError as e:

        return {
            "error": str(e)
        }

    except Exception as e:

        return {
            "error": str(e)
        }


# =========================================================
# CHAT
# =========================================================

@app.post("/chat")
def chat(
    request: ChatRequest
):

    # 1. Retrieve similar chunks (Semantically query text & media vectors)
    retrieved_chunks = retrieve_multimodal(
        query=request.query,
        top_k=5,
        score_threshold=0.0
    )

    print("\n================ RETRIEVED CHUNKS ================")
    for c in retrieved_chunks:
        print(
            f"Score: {c['score']:.4f} | Type: {c['metadata'].get('chunk_type')} | Text: {c['text'][:100]}..."
        )
    print("===================================================")

    # 2. Build context
    context = build_context(
        retrieved_chunks
    )

    # 3. Build Multimodal RAG prompt parts
    prompt_parts = build_multimodal_prompt(
        query=request.query,
        context=context
    )

    # 4. Generate answer from Gemini LLM
    answer = generate_response(
        prompt_parts
    )

    # 5. Build sources
    sources = build_sources(
        retrieved_chunks
    )

    # 6. Return response
    return {
        "query": request.query,
        "answer": answer,
        "sources": sources
    }