import os
from fastapi.testclient import TestClient
from main import app


def test_pipeline():

    with TestClient(app) as client:

        # ----------------------------------------------------
        # 1. Ingest a test document (0 Gemini calls)
        # ----------------------------------------------------
        test_filename = "test_multimodal_doc.txt"
        test_content = (
            "DeepMind created Antigravity as an advanced agentic coding pair programmer. "
            "It runs local embeddings via Sentence Transformers, stores vectors in Qdrant, "
            "and only calls Gemini 2.5 Flash during the chat phase for reasoning."
        )

        with open(test_filename, "w", encoding="utf-8") as f:
            f.write(test_content)

        print("\n1. Ingesting test document...")
        with open(test_filename, "rb") as f:
            response = client.post(
                "/ingest",
                files={"file": (test_filename, f, "text/plain")}
            )

        if os.path.exists(test_filename):
            os.remove(test_filename)

        print("Ingestion Response:", response.json())
        assert response.status_code == 200
        ingest_data = response.json()
        assert "Document ingested and indexed successfully" in ingest_data.get("status", "")
        doc_id = ingest_data["document_id"]

        # ----------------------------------------------------
        # 2. List documents (GET /documents)
        # ----------------------------------------------------
        print("\n2. Checking GET /documents...")
        docs_response = client.get("/documents")
        assert docs_response.status_code == 200
        docs = docs_response.json().get("documents", [])
        print(f"Found {len(docs)} documents in vector store.")
        assert any(d["document_id"] == doc_id for d in docs), "Ingested document not found in /documents!"

        # ----------------------------------------------------
        # 3. Call /chat (First Turn)
        # ----------------------------------------------------
        print("\n3. Sending initial Chat query...")
        chat_response1 = client.post(
            "/chat",
            json={
                "query": "Who created Antigravity and what model does it use for local embeddings?"
            }
        )

        print("Chat Response 1 Status:", chat_response1.status_code)
        chat_data1 = chat_response1.json()
        print("Chat Response 1 Body:", chat_data1)
        assert chat_response1.status_code == 200
        answer1 = chat_data1.get("answer", "")
        sources1 = chat_data1.get("sources", [])
        session_id = chat_data1.get("session_id")

        assert "DeepMind" in answer1 or "Sentence Transformers" in answer1 or "Google" in answer1
        assert len(sources1) > 0, "Source citations missing from chat response!"
        assert session_id is not None, "session_id missing from chat response!"
        print(f"Turn 1 passed. Session ID: {session_id}")
        print("Sources citations verified:", sources1[0])

        # ----------------------------------------------------
        # 4. Multi-turn Conversation Memory (Turn 2)
        # ----------------------------------------------------
        print("\n4. Sending follow-up query with same session_id...")
        chat_response2 = client.post(
            "/chat",
            json={
                "query": "What vector database does it store vectors in?",
                "session_id": session_id
            }
        )
        assert chat_response2.status_code == 200
        chat_data2 = chat_response2.json()
        print("Chat Response 2 Body:", chat_data2)
        answer2 = chat_data2.get("answer", "")
        assert "Qdrant" in answer2 or "qdrant" in answer2.lower()

        # Check history endpoint
        hist_resp = client.get(f"/chat/history/{session_id}")
        assert hist_resp.status_code == 200
        history = hist_resp.json().get("history", [])
        print(f"Conversation history count: {len(history)} messages.")
        assert len(history) >= 4  # 2 turns = 4 messages

        # ----------------------------------------------------
        # 5. Document Deletion (DELETE /documents/{doc_id})
        # ----------------------------------------------------
        print(f"\n5. Deleting document {doc_id}...")
        del_resp = client.delete(f"/documents/{doc_id}")
        assert del_resp.status_code == 200
        print("Delete response:", del_resp.json())
        assert del_resp.json().get("status") == "success"

        # Verify it's gone from /documents
        docs_after = client.get("/documents").json().get("documents", [])
        assert not any(d["document_id"] == doc_id for d in docs_after), "Document was not deleted from /documents!"
        print("Document deletion verified!")

        print("\n=== FULL MULTIMODAL RAG PIPELINE FULLY VERIFIED AND PASSING ===")


if __name__ == "__main__":
    test_pipeline()

