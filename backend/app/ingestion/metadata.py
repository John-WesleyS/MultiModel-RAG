def create_metadata(
    filename,
    file_type,
    document_id,
    chunk_index,
    chunk_type="text",
    media_path=None,
    mime_type=None,
    **kwargs
):

    meta = {
        "document_id": document_id,
        "filename": filename,
        "file_type": file_type,
        "chunk_index": chunk_index,
        "chunk_type": chunk_type
    }

    if media_path:
        meta["media_path"] = media_path

    if mime_type:
        meta["mime_type"] = mime_type

    for k, v in kwargs.items():
        if v is not None:
            meta[k] = v

    return meta