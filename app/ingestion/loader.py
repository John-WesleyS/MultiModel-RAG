def load_document(
    file_bytes,
    filename,
    file_type,
    document_id
):

    media = []

    if file_type == "pdf":

        from app.ingestion.loaders.pdf_loader import extract_pdf_data

        text, media = extract_pdf_data(
            file_bytes
        )

    elif file_type == "docx":

        from app.ingestion.loaders.docx_loader import extract_docx_data

        text, media = extract_docx_data(
            file_bytes
        )

    elif file_type == "excel":

        from app.ingestion.loaders.excel_loader import extract_excel_data

        text, media = extract_excel_data(
            file_bytes
        )

    elif file_type == "pptx":

        from app.ingestion.loaders.pptx_loader import extract_pptx_data

        text, media = extract_pptx_data(
            file_bytes
        )

    elif file_type == "text":

        from app.ingestion.loaders.text_loader import extract_txt_text

        text = extract_txt_text(
            file_bytes
        )

    elif file_type == "csv":

        from app.ingestion.loaders.csv_loader import extract_csv_data

        text, media = extract_csv_data(
            file_bytes
        )

    elif file_type == "image":

        from app.ingestion.loaders.image_extractor import extract_image_data

        text, media = extract_image_data(
            file_bytes,
            filename
        )

    elif file_type == "video":

        from app.ingestion.extractors.vedio import extract_video_data

        text, media = extract_video_data(
            file_bytes,
            filename
        )

    elif file_type == "audio":

        from app.ingestion.processors.audio_processor import extract_audio_data

        text, media = extract_audio_data(
            file_bytes,
            filename
        )

    else:

        raise ValueError(
            f"Unsupported file type: {file_type}"
        )

    return {
        "text": text,
        "media": media,
        "metadata": {
            "document_id": document_id,
            "filename": filename,
            "file_type": file_type
        }
    }