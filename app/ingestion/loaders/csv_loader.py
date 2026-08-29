import csv
from io import StringIO


def extract_csv_text(file_bytes):

    try:

        decoded = file_bytes.decode(
            "utf-8",
            errors="ignore"
        )

        reader = csv.reader(
            StringIO(decoded)
        )

        rows = []

        for row in reader:

            if any(
                cell.strip()
                for cell in row
            ):

                rows.append(
                    " | ".join([
                        cell.strip()
                        for cell in row
                    ])
                )

        return "\n".join(rows)

    except Exception as e:

        print(f"Error reading CSV: {e}")

        return ""


def extract_csv_data(file_bytes):

    text = extract_csv_text(file_bytes)

    return text, []