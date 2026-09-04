from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional
import uuid
import os
import shutil

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
    delete_document_points,
    get_all_documents,
    get_collection_stats,
)

from app.retrieval.retriever import retrieve_multimodal
from app.retrieval.context_builder import build_context
from app.retrieval.source_builder import build_sources

from app.llm.prompt import build_multimodal_prompt, build_rag_prompt
from app.llm.llm import generate_response
from app.llm.memory import conversation_manager


app = FastAPI(
    title="MultiModal-RAG API",
    description="MultiModal RAG system supporting documents, images, video, and audio with local embeddings and Gemini generation.",
    version="2.0.0"
)

# =========================================================
# CORS MIDDLEWARE
# =========================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure local media directory exists and mount static files
os.makedirs("media", exist_ok=True)
app.mount("/media", StaticFiles(directory="media"), name="media")


# =========================================================
# STARTUP EVENT
# =========================================================
@app.on_event("startup")
def startup_event():
    create_collection()


# =========================================================
# SCHEMAS
# =========================================================
class ChatRequest(BaseModel):
    query: str
    session_id: Optional[str] = None
    top_k: Optional[int] = 5
    score_threshold: Optional[float] = 0.0


# =========================================================
# ROOT & HEALTH
# =========================================================
@app.get("/")
def root():
    return {
        "name": "MultiModal-RAG API",
        "status": "online",
        "version": "2.0.0",
        "stats": get_collection_stats()
    }


# =========================================================
# INGEST PIPELINE (Gemini calls during ingestion: 0)
# =========================================================
@app.post("/ingest")
async def ingest_document(
    file: UploadFile = File(...)
):
    document_id = str(uuid.uuid4())

    try:
        # 1. Detect file type
        file_type = get_file_type(file.filename)

        # 2. Read file bytes
        file_bytes = await file.read()

        # 3. Load document into raw unified form
        document = load_document(
            file_bytes=file_bytes,
            filename=file.filename,
            file_type=file_type,
            document_id=document_id
        )

        # 4. Process document (text chunking & local media extraction)
        chunks = process_document(document)

        if not chunks:
            return {
                "document_id": document_id,
                "filename": file.filename,
                "status": "No text or media content was extracted from the file."
            }

        # 5. Generate local embeddings for each chunk (0 Gemini calls)
        texts_to_embed = []
        for chunk in chunks:
            c_type = chunk.get("metadata", {}).get("chunk_type", "text")
            chunk_text = chunk.get("text", "")
            if c_type == "text" or chunk_text.strip():
                texts_to_embed.append(chunk_text)
            else:
                # Media chunk placeholder description for local embedding
                filename = chunk.get("metadata", {}).get("filename", "")
                texts_to_embed.append(f"Media chunk {c_type} from {filename}")

        embeddings = generate_embeddings(texts_to_embed)

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
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {str(e)}")


# =========================================================
# QUERY / CHAT PIPELINE (Gemini called only here)
# =========================================================
@app.post("/chat")
async def chat(request: ChatRequest):
    query = request.query.strip()
    if not query:
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    session_id = request.session_id or str(uuid.uuid4())

    try:
        # 1. Retrieve relevant chunks (multimodal query embedding + Qdrant search)
        retrieved_chunks = retrieve_multimodal(
            query=query,
            top_k=request.top_k or 5,
            score_threshold=request.score_threshold or 0.0
        )

        # 2. Build context
        context = build_context(retrieved_chunks)

        # 3. Retrieve conversation history for memory
        conv_history = conversation_manager.format_history_for_prompt(session_id)

        # 4. Build multimodal prompt (attaches any retrieved images as PIL Images)
        prompt = build_multimodal_prompt(
            query=query,
            context=context,
            conversation_history=conv_history
        )

        # 5. Call Gemini ONLY here
        answer = generate_response(prompt)

        # 6. Record interaction in conversation memory
        conversation_manager.add_message(session_id=session_id, role="user", content=query)
        conversation_manager.add_message(session_id=session_id, role="assistant", content=answer)

        # 7. Build source citations
        sources = build_sources(retrieved_chunks)

        return {
            "answer": answer,
            "sources": sources,
            "session_id": session_id
        }

    except Exception as e:
        print(f"Error processing chat query: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# =========================================================
# DOCUMENT MANAGEMENT
# =========================================================
@app.get("/documents")
def list_documents():
    """List all indexed documents with chunk count and media references."""
    return {
        "documents": get_all_documents()
    }


@app.delete("/documents/{document_id}")
def delete_document(document_id: str):
    """Delete a document by ID: removes its vectors from Qdrant and cleans local media."""
    deleted_count = delete_document_points(document_id)

    # Delete local media folder if present
    media_dir = os.path.join("media", document_id)
    if os.path.exists(media_dir):
        try:
            shutil.rmtree(media_dir)
        except Exception as e:
            print(f"Error removing media directory {media_dir}: {e}")

    return {
        "status": "success",
        "message": f"Document {document_id} deleted successfully.",
        "document_id": document_id,
        "deleted_chunks": deleted_count
    }


# =========================================================
# CONVERSATION MEMORY ENDPOINTS
# =========================================================
@app.get("/chat/history/{session_id}")
def get_chat_history(session_id: str):
    """Get chat history for a given session."""
    return {
        "session_id": session_id,
        "history": conversation_manager.get_history(session_id)
    }


@app.delete("/chat/history/{session_id}")
def clear_chat_history(session_id: str):
    """Clear conversation history for a given session."""
    cleared = conversation_manager.clear_session(session_id)
    return {
        "session_id": session_id,
        "cleared": cleared
    }