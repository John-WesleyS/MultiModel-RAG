def build_rag_prompt(query, context):

    prompt = f"""
You are a helpful AI assistant.

You are answering questions using information retrieved
from the user's documents.

IMPORTANT RULES:

1. Answer the question using ONLY the provided context.
2. Do not use outside knowledge.
3. Do not make up information.
4. If the answer cannot be found in the context,
   clearly say that the information is not available
   in the provided documents.
5. Give a clear and concise answer.

====================
CONTEXT
====================

{context}

====================
USER QUESTION
====================

{query}

====================
ANSWER
====================
"""

    return prompt