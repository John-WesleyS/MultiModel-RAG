import fitz


def extract_pdf(file_path: str):

    document = fitz.open(file_path)

    pages = []

    for page_number, page in enumerate(document):

        text = page.get_text()

        pages.append({
            "text": text,
            "metadata": {
                "page": page_number + 1
            }
        })

    document.close()

    return pages