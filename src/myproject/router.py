"""Query router for the Adaptive RAG project.

The router connects the classifier, retriever, and answer strategies.
It is the main Python interface used by the API and user story tests.
"""

from __future__ import annotations

import os
import time
import uuid
from pathlib import Path

from myproject.classifier import classify_query
from myproject.retriever import Retriever
from myproject.strategies import (
    multi_step_answer,
    no_retrieval_answer,
    single_step_answer,
)

DEFAULT_CORPUS_PATH = "data/corpus.jsonl"
MAX_QUERY_CHARS = int(os.getenv("MAX_QUERY_CHARS", "1000"))


def route_query(text: str, max_results: int = 5) -> dict:
    """Validate, classify, route, and answer a user query.

    Parameters
    ----------
    text:
        User question.
    max_results:
        Maximum number of evidence passages to retrieve.

    Returns
    -------
    dict
        Complete response dictionary matching docs/SPEC.md.
    """
    start_time = time.perf_counter()
    request_id = str(uuid.uuid4())

    cleaned_text = " ".join(text.strip().split())

    if not cleaned_text:
        raise ValueError("input text is required")

    if len(cleaned_text) > MAX_QUERY_CHARS:
        raise ValueError("input text exceeds maximum length")

    complexity_label = classify_query(cleaned_text)

    if complexity_label == "A":
        strategy = "no_retrieval"
        strategy_result = no_retrieval_answer(cleaned_text)

    elif complexity_label == "B":
        strategy = "single_step"
        retriever = _build_retriever()
        strategy_result = single_step_answer(
            query=cleaned_text,
            retriever=retriever,
            max_results=max_results,
        )

    elif complexity_label == "C":
        strategy = "multi_step"
        retriever = _build_retriever()
        strategy_result = multi_step_answer(
            query=cleaned_text,
            retriever=retriever,
            max_results=max_results,
        )

    else:
        raise ValueError(f"Unsupported complexity label: {complexity_label}")

    latency_ms = int((time.perf_counter() - start_time) * 1000)

    return {
        "request_id": request_id,
        "question": cleaned_text,
        "complexity_label": complexity_label,
        "strategy": strategy,
        "answer": strategy_result["answer"],
        "citations": strategy_result["citations"],
        "retrieval_steps": strategy_result["retrieval_steps"],
        "latency_ms": latency_ms,
    }


def _build_retriever() -> Retriever:
    """Build the retriever from the configured local corpus path."""
    corpus_path = os.getenv("CORPUS_PATH", DEFAULT_CORPUS_PATH)
    resolved_path = Path(corpus_path)

    if not resolved_path.exists():
        project_root_path = Path(__file__).resolve().parents[2] / corpus_path
        resolved_path = project_root_path

    return Retriever(str(resolved_path))
