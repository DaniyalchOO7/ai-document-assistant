"""
rag.py — Chunking + semantic retrieval for AI Document Assistant

Upgrade from "basic vector-style chunk retrieval" to real embedding-based
semantic search using sentence-transformers + FAISS.
"""

from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Loaded once and reused across the app — small, fast, runs locally (no API cost)
_MODEL_NAME = "all-MiniLM-L6-v2"
_model = SentenceTransformer(_MODEL_NAME)


def chunk_text(text, chunk_size=800, overlap=150):
    """
    Split raw document text into overlapping chunks.

    chunk_size / overlap are character counts, not tokens — simple and good
    enough for this project. Overlap keeps context from being cut mid-idea
    at chunk boundaries.

    Returns a list of dicts: {"text": str, "chunk_id": int}
    """
    if not text:
        return []

    chunks = []
    start = 0
    chunk_id = 0
    text_len = len(text)

    while start < text_len:
        end = min(start + chunk_size, text_len)
        chunk_str = text[start:end].strip()

        if chunk_str:
            chunks.append({"text": chunk_str, "chunk_id": chunk_id})
            chunk_id += 1

        if end == text_len:
            break
        start = end - overlap  # step forward, keeping overlap

    return chunks


def build_index(chunks):
    """
    Embed every chunk and build a FAISS index over them.

    chunks: list of dicts from chunk_text(), each with a "text" key.

    Returns (index, chunks) — keep both together, since the index only
    stores vectors and you need `chunks` to map results back to text.
    """
    if not chunks:
        raise ValueError("No chunks to index — document may be empty or failed to extract text.")

    texts = [c["text"] for c in chunks]
    embeddings = _model.encode(texts, show_progress_bar=False)
    embeddings = np.array(embeddings).astype("float32")

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    return index, chunks


def retrieve(query, index, chunks, top_k=4):
    """
    Given a user question, return the top_k most relevant chunks.

    Returns a list of dicts: {"text": str, "chunk_id": int, "score": float}
    score is L2 distance — lower means more relevant.
    """
    if index is None or not chunks:
        return []

    query_embedding = _model.encode([query]).astype("float32")
    distances, indices = index.search(query_embedding, min(top_k, len(chunks)))

    results = []
    for rank, idx in enumerate(indices[0]):
        if idx == -1:  # FAISS pads with -1 if fewer than top_k results exist
            continue
        chunk = chunks[idx]
        results.append({
            "text": chunk["text"],
            "chunk_id": chunk["chunk_id"],
            "score": float(distances[0][rank]),
        })

    return results


def format_context(retrieved_chunks):
    """
    Turn retrieved chunks into a single context string for the LLM prompt,
    each one labeled so the model (and your citation display) can reference it.
    """
    if not retrieved_chunks:
        return "No relevant context found in the document."

    parts = []
    for r in retrieved_chunks:
        parts.append(f"[Chunk {r['chunk_id']}]\n{r['text']}")

    return "\n\n".join(parts)