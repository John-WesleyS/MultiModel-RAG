import os
import time
import random

from dotenv import load_dotenv
from google import genai


load_dotenv()


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set")


GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-2.5-flash"
)


client = genai.Client(
    api_key=GEMINI_API_KEY
)


def generate_response(prompt):

    max_retries = 3

    for attempt in range(max_retries):

        try:

            response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt
            )

            return response.text

        except Exception as e:

            error_message = str(e).lower()

            is_429 = (
                "429" in error_message
                or "resource_exhausted" in error_message
                or "quota" in error_message
            )

            is_503 = (
                "503" in error_message
                or "unavailable" in error_message
                or "overloaded" in error_message
            )

            # ------------------------------------------
            # Daily quota exhausted
            # ------------------------------------------

            if is_429 and (
                "perday" in error_message
                or "free_tier" in error_message
                or "daily" in error_message
            ):

                print(
                    "Gemini daily free-tier quota exhausted."
                )

                return (
                    "Gemini daily free-tier quota has been "
                    "exhausted. Please try again later."
                )

            # ------------------------------------------
            # Retry temporary 429 / 503 errors
            # ------------------------------------------

            if is_429 or is_503:

                if attempt == max_retries - 1:

                    return (
                        "Gemini is temporarily unavailable. "
                        "Please try again later."
                    )

                delay = (
                    2 ** attempt
                    + random.uniform(0, 1)
                )

                print(
                    f"Gemini error detected. "
                    f"Retrying in {delay:.2f} seconds..."
                )

                time.sleep(delay)

                continue

            # ------------------------------------------
            # Other errors
            # ------------------------------------------

            print(
                f"Gemini generation error: {e}"
            )

            return (
                "An error occurred while generating "
                "the answer."
            )

    return "Unable to generate an answer."