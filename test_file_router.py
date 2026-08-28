from app.ingestion.router import detect_file_type


files = [
    "document.pdf",
    "notes.docx",
    "sales.xlsx",
    "data.csv",
    "presentation.pptx",
    "notes.txt",
    "diagram.png",
    "lecture.mp4",
]


for file in files:

    file_type = detect_file_type(file)

    print(
        f"{file} -> {file_type}"
    )