import os
from app.ingestion.cleaner import clean_text
from app.ingestion.splitter import split_text
from app.ingestion.metadata import create_metadata
from app.llm.llm import describe_media


def process_document(document):

    text = document.get("text", "")

    media_list = document.get("media", [])

    doc_metadata = document.get("metadata", {})

    filename = doc_metadata.get("filename", "Unknown")

    file_type = doc_metadata.get("file_type", "Unknown")

    document_id = doc_metadata.get("document_id", "Unknown")

    processed_chunks = []

    chunk_index = 0

    # 1. Clean and split text
    if text.strip():

        cleaned_text = clean_text(text)

        chunks = split_text(cleaned_text)

        for chunk in chunks:

            metadata = create_metadata(
                filename=filename,
                file_type=file_type,
                document_id=document_id,
                chunk_index=chunk_index,
                chunk_type="text"
            )

            processed_chunks.append({
                "text": chunk,
                "metadata": metadata
            })

            chunk_index += 1

    # 2. Process media attachments
    if media_list:

        media_dir = os.path.join(
            "media",
            document_id
        )

        os.makedirs(
            media_dir,
            exist_ok=True
        )

        for media_item in media_list:

            media_type = media_item.get(
                "type",
                "image"
            )

            media_bytes = media_item.get(
                "bytes"
            )

            mime_type = media_item.get(
                "mime_type",
                ""
            )

            orig_filename = media_item.get(
                "filename",
                "media_file"
            )

            item_metadata = media_item.get(
                "metadata",
                {}
            )

            # Define output filepath
            media_file_path = os.path.join(
                media_dir,
                orig_filename
            )

            # Save media locally
            try:

                with open(
                    media_file_path,
                    "wb"
                ) as f:

                    f.write(media_bytes)

            except Exception as e:

                print(
                    f"Error saving media file to {media_file_path}: {e}"
                )

            # Describe media with Gemini
            description = describe_media(
                media_bytes=media_bytes,
                mime_type=mime_type,
                media_type=media_type
            )

            # Generate metadata
            metadata = create_metadata(
                filename=filename,
                file_type=file_type,
                document_id=document_id,
                chunk_index=chunk_index,
                chunk_type=media_type,
                media_path=media_file_path,
                mime_type=mime_type,
                **item_metadata
            )

            processed_chunks.append({
                "text": description,
                "metadata": metadata
            })

            chunk_index += 1

    return processed_chunks