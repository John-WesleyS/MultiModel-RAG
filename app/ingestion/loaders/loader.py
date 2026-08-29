from app.ingestion.router import route_file


def load_document(file_path: str, filename: str):

    return route_file(
        file_path=file_path,
        filename=filename
    )