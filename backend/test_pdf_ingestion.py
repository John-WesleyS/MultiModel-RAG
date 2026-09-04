import os
import fitz  # PyMuPDF
from PIL import Image
import io
from fastapi.testclient import TestClient
from main import app
from app.vectorstore.qdrant import client, COLLECTION_NAME, get_collection_stats, get_all_documents


def create_sample_pdf(filepath: str):
    """Generate a test PDF with text and an embedded image using PyMuPDF."""
    doc = fitz.open()

    # Page 1: Software Maintenance Process & Lehman's Laws
    page1 = doc.new_page()
    text_p1 = """SOFTWARE ENGINEERING AND MAINTENANCE
Lehman's Laws of Software Evolution:
1. Continuing Change: A system must be continually adapted or it becomes progressively less satisfactory.
2. Increasing Complexity: As a system evolves, its complexity increases unless work is done to maintain or reduce it.
3. Self Regulation: The evolution process is self-regulating with system attributes such as size, time between releases, and the number of reported faults being roughly invariant among releases.

Software Maintenance Process Models:
Maintenance involves corrective, adaptive, perfective, and preventive changes.
The maintenance process includes problem identification, analysis, design, implementation, and system testing.
"""
    page1.insert_text((50, 72), text_p1, fontsize=11)

    # Insert a small test diagram/image on page 1
    img = Image.new("RGB", (200, 100), color=(73, 109, 137))
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format="PNG")
    img_bytes = img_byte_arr.getvalue()
    rect = fitz.Rect(50, 350, 250, 450)
    page1.insert_image(rect, stream=img_bytes)

    # Page 2: Machine Learning & Supervised Learning
    page2 = doc.new_page()
    text_p2 = """MACHINE LEARNING CONCEPTS
Supervised learning is a paradigm in machine learning where algorithms are trained on labeled data.
Common supervised learning tasks include classification and regression.
In contrast, unsupervised learning discovers hidden patterns in unlabeled data.
"""
    page2.insert_text((50, 72), text_p2, fontsize=11)

    doc.save(filepath)
    doc.close()
    print(f"Created sample PDF: {filepath}")


def test_pdf_ingestion():
    test_pdf_path = "sample_test_doc.pdf"
    try:
        create_sample_pdf(test_pdf_path)

        with TestClient(app) as test_client:
            print("\n1. Ingesting PDF via POST /ingest...")
            with open(test_pdf_path, "rb") as f:
                response = test_client.post(
                    "/ingest",
                    files={"file": (test_pdf_path, f, "application/pdf")}
                )

            print("Ingestion HTTP Status:", response.status_code)
            data = response.json()
            print("Ingestion Response:", data)

            assert response.status_code == 200, f"Expected 200, got {response.status_code}"
            assert data["chunks_count"] > 0, "No chunks were stored!"
            assert "Document ingested and indexed successfully" in data["status"]

            doc_id = data["document_id"]
            print(f"\nDocument ID: {doc_id}")

            # 2. Confirm chunks stored in Qdrant
            stats = get_collection_stats()
            print("\n2. Qdrant Stats:", stats)
            assert stats["points_count"] >= data["chunks_count"], "Point count mismatch in Qdrant!"

            docs = get_all_documents()
            print("\n3. All Documents in Qdrant:", docs)
            matching = [d for d in docs if d["document_id"] == doc_id]
            assert len(matching) == 1, "Document not found in get_all_documents()!"
            print("Document verification in Qdrant: SUCCESS!")

            # 4. Check if media was extracted and saved locally
            media_folder = os.path.join("media", doc_id)
            if os.path.exists(media_folder):
                saved_media = os.listdir(media_folder)
                print(f"\n4. Extracted media in {media_folder}: {saved_media}")
            else:
                print(f"\n4. No media folder created at {media_folder}")

            print("\n=== PDF INGESTION & QDRANT STORAGE CONFIRMED SUCCESSFULLY ===")

    finally:
        if os.path.exists(test_pdf_path):
            os.remove(test_pdf_path)


if __name__ == "__main__":
    test_pdf_ingestion()
