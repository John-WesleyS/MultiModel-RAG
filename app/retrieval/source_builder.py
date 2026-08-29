def build_sources(retrieved_chunks):

    sources = []

    for chunk in retrieved_chunks:

        metadata = chunk.get("metadata", {})

        source = {
            "document_id": metadata.get("document_id"),
            "filename": metadata.get("filename"),
            "chunk_index": metadata.get("chunk_index"),
            "chunk_type": metadata.get("chunk_type", "text"),
            "score": chunk.get("score")
        }

        # Include page/sheet/slide references
        if "page" in metadata:
            source["page"] = metadata["page"]

        if "sheet_name" in metadata:
            source["sheet_name"] = metadata["sheet_name"]

        if "slide_number" in metadata:
            source["slide_number"] = metadata["slide_number"]

        if "media_path" in metadata:
            source["media_path"] = metadata["media_path"]

        sources.append(source)

    return sources