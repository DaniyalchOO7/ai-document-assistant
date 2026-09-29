"""
doc_qa_metrics.py — Reliability metrics for AI Document Assistant (RAG)

Logs every question/answer interaction and computes the numbers that
actually matter for a RAG project: how often retrieval finds strong
matches, and how often the answer stays grounded in the source document.

Call log_interaction() right after ask_with_grounding_check() in app.py.
Run this file directly (or add a Streamlit "Stats" tab) to see results.
"""

import csv
import os
from collections import Counter
from datetime import datetime

LOG_FIELDS = [
    "timestamp", "question", "num_sources_retrieved",
    "top_retrieval_score", "grounded", "answer_length",
]


def log_interaction(question, retrieved_chunks, result, log_path="qa_log.csv"):
    """
    Call this after ask_with_grounding_check() returns.

    retrieved_chunks: the list from rag.retrieve() (has "score" per chunk —
    lower L2 distance means a closer match).
    result: the dict from ask_with_grounding_check() (has "answer", "grounded").
    """
    file_exists = os.path.isfile(log_path)

    top_score = retrieved_chunks[0]["score"] if retrieved_chunks else None

    with open(log_path, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=LOG_FIELDS)
        if not file_exists:
            writer.writeheader()
        writer.writerow({
            "timestamp": datetime.now().isoformat(),
            "question": question,
            "num_sources_retrieved": len(retrieved_chunks),
            "top_retrieval_score": round(top_score, 4) if top_score is not None else "",
            "grounded": result["grounded"],
            "answer_length": len(result["answer"]),
        })


def compute_stats(log_path="qa_log.csv"):
    """
    Returns the numbers worth putting on a resume/README:
    - % of answers that stayed grounded in the document
    - average retrieval confidence (lower score = better match)
    - % of questions where retrieval found nothing strong (weak-match rate)
    """
    if not os.path.isfile(log_path):
        return {"total": 0}

    with open(log_path, "r", newline="") as f:
        rows = list(csv.DictReader(f))

    total = len(rows)
    if total == 0:
        return {"total": 0}

    grounded_count = sum(1 for r in rows if r["grounded"] == "True")
    scores = [float(r["top_retrieval_score"]) for r in rows if r["top_retrieval_score"]]
    avg_score = sum(scores) / len(scores) if scores else None

    # Weak-match threshold: tune this once you've looked at real scores —
    # start high and lower it as you see what "good" retrieval looks like
    # for your document set.
    weak_match_threshold = 1.0
    weak_matches = sum(1 for s in scores if s > weak_match_threshold)

    return {
        "total": total,
        "grounded_pct": round(grounded_count / total * 100, 1),
        "avg_retrieval_score": round(avg_score, 4) if avg_score is not None else None,
        "weak_match_pct": round(weak_matches / len(scores) * 100, 1) if scores else None,
    }


if __name__ == "__main__":
    stats = compute_stats()
    print("Doc Q&A reliability stats:")
    for key, value in stats.items():
        print(f"  {key}: {value}")