from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import uuid

from app.ingestion.loader import extract_pdf_text
from app.ingestion.cleaner import clean_text
from app.ingestion.splitter import split_text

from app.embeddings.embedder import generate_embeddings

from app.vectorstore.qdrant import (
    create_collection,
    store_chunks
)

from app.llm import generate_response


app = FastAPI()


@app.on_event("startup")
def startup_event():

    create_collection()


class ChatRequest(BaseModel):
    query: str


@app.post("/ingest")
async def ingest_document(
    file: UploadFile = File(...)
):

    # --------------------------------
    # 1. Create document ID
    # --------------------------------

    document_id = str(uuid.uuid4())


    # --------------------------------
    # 2. Read uploaded PDF
    # --------------------------------

    file_bytes = await file.read()


    # --------------------------------
    # 3. Extract text
    # --------------------------------

    text = extract_pdf_text(file_bytes)


    # --------------------------------
    # 4. Clean text
    # --------------------------------

    cleaned_text = clean_text(text)


    # --------------------------------
    # 5. Split into chunks
    # --------------------------------

    chunks = split_text(
        cleaned_text,
        chunk_size=1000,
        chunk_overlap=200
    )


    # --------------------------------
    # 6. Add metadata
    # --------------------------------

    for chunk in chunks:

        chunk_index = chunk["metadata"]["chunk_index"]

        chunk["metadata"]["document_id"] = document_id

        chunk["metadata"]["filename"] = file.filename

        chunk["metadata"]["chunk_id"] = (
            f"{document_id}_{chunk_index}"
        )


    # --------------------------------
    # 7. Generate embeddings
    # --------------------------------

    chunks = generate_embeddings(chunks)


    # --------------------------------
    # 8. Store chunks in Qdrant
    # --------------------------------

    store_chunks(chunks)


    # --------------------------------
    # 9. Return response
    # --------------------------------

    return {
        "message": "Document ingested successfully",

        "document_id": document_id,

        "filename": file.filename,

        "content_type": file.content_type,

        "total_chunks": len(chunks)
    }


@app.post("/chat")
def chat(request: ChatRequest):

    answer = generate_response(request.query)

    return {
        "query": request.query,
        "answer": answer
    }