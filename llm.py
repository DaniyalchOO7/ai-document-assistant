"""
llm.py — Gemini integration for AI Document Assistant

Takes retrieved chunks (from rag.py) + the user's question, builds a
grounded prompt, and calls Gemini. Includes a lightweight check so answers
that aren't actually grounded in the retrieved context get flagged.

Uses the new `google-genai` SDK (replaces the deprecated
`google-generativeai` package) — required for compatibility with the
newer "AQ." format API keys from Google AI Studio.
"""

import os
from dotenv import load_dotenv

load_dotenv()

from google import genai
print("GENAI MODULE PATH:", genai.__file__)

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

_MODEL_NAME = "gemini-3.8-flash"

_SYSTEM_INSTRUCTIONS = """You are a document assistant. Answer the user's question using ONLY \
the context provided below. Do not use outside knowledge.

If the context does not contain enough information to answer the question, \
say exactly: "I couldn't find that in the document." Do not guess or make \
anything up.

When you use information from a specific chunk, mention its chunk number \
in your answer, like: "According to Chunk 2, ..."
"""


def build_prompt(question, context):
    return f"""{_SYSTEM_INSTRUCTIONS}

Context:
{context}

Question: {question}

Answer:"""


def ask_gemini(question, context):
    """
    Send the grounded prompt to Gemini and return the raw answer text.
    """
    prompt = build_prompt(question, context)
    response = client.models.generate_content(
        model=_MODEL_NAME,
        contents=prompt,
    )
    return response.text.strip()


def is_grounded(answer, retrieved_chunks):
    """
    Lightweight check: does the answer reference at least one retrieved
    chunk, or explicitly say it couldn't find the info?

    This isn't a perfect hallucination detector, but it catches the most
    common failure mode: Gemini answering from general knowledge instead
    of the document. Good enough for a portfolio project, and a talking
    point in interviews about RAG reliability.
    """
    if "couldn't find that in the document" in answer.lower():
        return True

    chunk_ids = [str(c["chunk_id"]) for c in retrieved_chunks]
    return any(f"chunk {cid}" in answer.lower() for cid in chunk_ids)


def ask_with_grounding_check(question, retrieved_chunks, context):
    """
    Full flow: ask Gemini, check grounding, return a structured result
    so app.py can display a warning badge if the answer looks ungrounded.
    """
    answer = ask_gemini(question, context)
    grounded = is_grounded(answer, retrieved_chunks)

    return {
        "answer": answer,
        "grounded": grounded,
        "sources": [c["chunk_id"] for c in retrieved_chunks],
    }