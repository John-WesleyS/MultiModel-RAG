from pathlib import Path


SUPPORTED_EXTENSIONS = {
    ".pdf": "pdf",
    ".docx": "docx",
    ".xlsx": "excel",
    ".xls": "excel",
    ".csv": "csv",
    ".pptx": "pptx",
    ".txt": "text",
    ".png": "image",
    ".jpg": "image",
    ".jpeg": "image",
    ".webp": "image",
    ".mp4": "video",
    ".mov": "video",
    ".avi": "video",
    ".mkv": "video",
}


def detect_file_type(filename: str):

    extension = Path(filename).suffix.lower()

    if extension not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            f"Unsupported file type: {extension}"
        )

    return SUPPORTED_EXTENSIONS[extension]