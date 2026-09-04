import mimetypes


def extract_video_data(file_bytes, filename):

    mime_type, _ = mimetypes.guess_type(filename)

    if not mime_type:

        ext = filename.split(".")[-1].lower()

        if ext in ["mp4", "avi", "mov", "mkv", "webm"]:

            mime_type = f"video/{ext}" if ext != "mov" else "video/quicktime"

        else:

            mime_type = "video/mp4"

    media = [{
        "type": "video",
        "bytes": file_bytes,
        "mime_type": mime_type,
        "filename": filename,
        "metadata": {}
    }]

    return "", media
