def extract_txt_text(file_bytes):

    return file_bytes.decode(
        "utf-8",
        errors="ignore"
    )