from docx import Document


def extract_docx(file_path: str):

    document = Document(file_path)

    paragraphs = []

    for paragraph in document.paragraphs:

        text = paragraph.text.strip()

        if text:
            paragraphs.append(text)

    text = "\n".join(paragraphs)

    return [
        {
            "text": text,
            "metadata": {
                "source_type": "docx"
            }
        }
    ]