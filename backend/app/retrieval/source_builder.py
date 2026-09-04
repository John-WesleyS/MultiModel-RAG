import os


def build_sources(retrieved_chunks):

    sources = []

    for chunk in retrieved_chunks:

        metadata = chunk.get("metadata", {})
        text = chunk.get("text", "")
        media_path = metadata.get("media_path")
        document_id = metadata.get("document_id")

        media_url = None
        if media_path:
            norm_path = media_path.replace("\\", "/")
            # Extract relative path inside media/
            if "media/" in norm_path:
                rel = norm_path.split("media/", 1)[1]
                media_url = f"/media/{rel}"
            else:
                media_url = f"/media/{os.path.basename(media_path)}"

        source = {
            "document_id": document_id,
            "filename": metadata.get("filename"),
            "chunk_index": metadata.get("chunk_index"),
            "chunk_type": metadata.get("chunk_type", "text"),
            "score": round(float(chunk.get("score", 0.0)), 4) if chunk.get("score") is not None else None,
            "snippet": (text[:200] + "...") if len(text) > 200 else text
        }

        # Include page/sheet/slide references
        if "page" in metadata:
            source["page"] = metadata["page"]

        if "sheet_name" in metadata:
            source["sheet_name"] = metadata["sheet_name"]

        if "slide_number" in metadata:
            source["slide_number"] = metadata["slide_number"]

        if media_path:
            source["media_path"] = media_path

        if media_url:
            source["media_url"] = media_url

        sources.append(source)

    return sources
