import os


SUPPORTED_FILE_TYPES = {
    ".pdf": "pdf",
    ".docx": "docx",
    ".xlsx": "xlsx",
    ".pptx": "pptx",
    ".txt": "txt",
    ".csv": "csv"
}


def get_file_type(filename):

    extension = os.path.splitext(
        filename
    )[1].lower()

    if extension not in SUPPORTED_FILE_TYPES:

        raise ValueError(
            f"Unsupported file type: {extension}"
        )

    return SUPPORTED_FILE_TYPES[
        extension
    ]