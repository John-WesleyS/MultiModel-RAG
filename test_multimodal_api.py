import os
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_pipeline():

    with TestClient(app) as client:

        # 1. Create a dummy text file to ingest
        test_filename = "test_doc.txt"

        test_content = "Antigravity is a coding assistant built by the Google Deepmind team. It helps developers write code, test applications, and design plans."

        with open(test_filename, "w", encoding="utf-8") as f:

            f.write(test_content)

        print("Ingesting test file...")

        # Call ingest
        with open(test_filename, "rb") as f:

            response = client.post(
                "/ingest",
                files={
                    "file": (
                        test_filename,
                        f,
                        "text/plain"
                    )
                }
            )

        # Clean up local file
        if os.path.exists(test_filename):

            os.remove(test_filename)

        print(
            "Ingestion Response:",
            response.json()
        )

        assert response.status_code == 200

        assert "Document ingested and indexed successfully" in response.json().get(
            "status",
            ""
        )

        # 2. Call chat
        print("\nSending Chat query...")

        chat_response = client.post(
            "/chat",
            json={
                "query": "Who built Antigravity?"
            }
        )

        print(
            "Chat Response:",
            chat_response.json()
        )

        assert chat_response.status_code == 200

        answer = chat_response.json().get(
            "answer",
            ""
        )

        assert "Deepmind" in answer or "Google" in answer

        print(
            "\nSuccess! Multimodal RAG Pipeline fully verified."
        )



if __name__ == "__main__":

    test_pipeline()
