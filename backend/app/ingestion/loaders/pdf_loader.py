from app.ingestion.extractors.pdf import extract_pdf
import fitz


def extract_pdf_text(file_bytes):

    document = fitz.open(
        stream=file_bytes,
        filetype="pdf"
    )

    text = "\n".join(
        page.get_text()
        for page in document
    )

    document.close()

    return text


def extract_pdf_data(file_bytes):

    document = fitz.open(
        stream=file_bytes,
        filetype="pdf"
    )

    text_parts = []

    media = []

    for page_number in range(len(document)):

        page = document[page_number]

        # Extract text
        page_text = page.get_text()

        text_parts.append(page_text)

        # Extract images
        image_list = page.get_images(full=True)

        for img_idx, img in enumerate(image_list):

            xref = img[0]

            base_image = document.extract_image(xref)

            image_bytes = base_image["image"]

            image_ext = base_image["ext"]

            mime_type = f"image/{image_ext}" if image_ext != "jpg" else "image/jpeg"

            media.append({
                "type": "image",
                "bytes": image_bytes,
                "mime_type": mime_type,
                "filename": f"page_{page_number + 1}_img_{img_idx}.{image_ext}",
                "metadata": {
                    "page": page_number + 1
                }
            })

    document.close()

    return "\n".join(text_parts), media


def load_pdf(file_path: str):

    documents = extract_pdf(file_path)

    return documents