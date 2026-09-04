from pathlib import Path


SUPPORTED_FILE_TYPES = {
    # Documents
    ".pdf": "pdf",
    ".docx": "docx",
    ".txt": "text",

    # Spreadsheets
    ".xlsx": "excel",
    ".xls": "excel",
    ".csv": "csv",

    # Presentations
    ".pptx": "pptx",

    # Images
    ".jpg": "image",
    ".jpeg": "image",
    ".png": "image",
    ".webp": "image",

    # Videos
    ".mp4": "video",
    ".avi": "video",
    ".mov": "video",
    ".mkv": "video",

    # Audio
    ".mp3": "audio",
    ".wav": "audio",
    ".m4a": "audio",
}


def get_file_type(filename: str) -> str:

    extension = Path(filename).suffix.lower()

    file_type = SUPPORTED_FILE_TYPES.get(extension)

    if file_type is None:
        raise ValueError(
            f"Unsupported file type: {extension}"
        )

    return file_type