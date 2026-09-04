import re


def clean_text(text):

    if not text:
        return ""

    # Remove excessive spaces
    text = re.sub(
        r"[ \t]+",
        " ",
        text
    )

    # Reduce excessive newlines
    text = re.sub(
        r"\n\s*\n+",
        "\n\n",
        text
    )

    # Remove leading/trailing whitespace
    text = text.strip()

    return text