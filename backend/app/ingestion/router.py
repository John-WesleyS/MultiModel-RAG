import os
from app.ingestion.file_detector import get_file_type, SUPPORTED_FILE_TYPES


def detect_file_type(filename: str) -> str:
    """Detect file type from filename extension."""
    return get_file_type(filename)