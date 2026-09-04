from app.llm.llm import generate_response


prompt = """
You are a helpful AI assistant.

Answer the following question briefly.

Question:
What is machine learning?
"""


answer = generate_response(prompt)


print("\n==============================")
print("LLM RESPONSE")
print("==============================")

print(answer)