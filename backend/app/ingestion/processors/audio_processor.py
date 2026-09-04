import mimetypes


def extract_audio_data(file_bytes, filename):

    mime_type, _ = mimetypes.guess_type(filename)

    if not mime_type:

        ext = filename.split(".")[-1].lower()

        if ext in ["mp3", "wav", "m4a", "ogg", "flac"]:

            mime_type = f"audio/{ext}" if ext != "mp3" else "audio/mpeg"

        else:

            mime_type = "audio/mpeg"

    media = [{
        "type": "audio",
        "bytes": file_bytes,
        "mime_type": mime_type,
        "filename": filename,
        "metadata": {}
    }]

    return "", media
