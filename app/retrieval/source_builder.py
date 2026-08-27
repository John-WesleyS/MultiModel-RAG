def build_sources(retrieved_chunks):

    sources = []

    for chunk in retrieved_chunks:

        metadata = chunk.get("metadata", {})

        source = {
            "document_id": metadata.get("document_id"),
            "filename": metadata.get("filename"),
            "chunk_index": metadata.get("chunk_index"),
            "score": chunk.get("score")
        }

        sources.append(source)

    return sources