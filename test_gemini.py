from app.llm.llm import generate_response


prompt = """
Explain Retrieval Augmented Generation
in simple terms.
"""


answer = generate_response(prompt)


print("\n==============================")
print("GEMINI RESPONSE")
print("==============================")

print(answer)