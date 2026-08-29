import mimetypes


def extract_image_data(file_bytes, filename):

    mime_type, _ = mimetypes.guess_type(filename)

    if not mime_type:

        ext = filename.split(".")[-1].lower()

        if ext in ["png", "webp", "gif"]:

            mime_type = f"image/{ext}"

        else:

            mime_type = "image/jpeg"

    media = [{
        "type": "image",
        "bytes": file_bytes,
        "mime_type": mime_type,
        "filename": filename,
        "metadata": {}
    }]

    return "", media
