"""Unit tests for Adaptive RAG answer strategies."""

from __future__ import annotations

from myproject.retriever import Retriever
from myproject.strategies import (
    FALLBACK_ANSWER,
    multi_step_answer,
    no_retrieval_answer,
    single_step_answer,
)


def test_no_retrieval_answer_uses_zero_steps() -> None:
    """The no-retrieval strategy should return an answer with zero retrieval steps."""
    result = no_retrieval_answer("What is Adaptive RAG?")

    assert result["answer"]
    assert "Adaptive RAG" in result["answer"]
    assert result["citations"] == []
    assert result["retrieval_steps"] == 0


def test_single_step_answer_returns_citations() -> None:
    """The single-step strategy should retrieve evidence once."""
    retriever = Retriever("data/corpus.jsonl")

    result = single_step_answer(
        query="What are the three routing labels in Adaptive RAG?",
        retriever=retriever,
        max_results=3,
    )

    assert result["answer"]
    assert "A" in result["answer"]
    assert "B" in result["answer"]
    assert "C" in result["answer"]
    assert result["retrieval_steps"] == 1
    assert isinstance(result["citations"], list)
    assert len(result["citations"]) >= 1


def test_multi_step_answer_returns_two_steps() -> None:
    """The multi-step strategy should use two retrieval steps."""
    retriever = Retriever("data/corpus.jsonl")

    result = multi_step_answer(
        query=(
            "How does Adaptive RAG balance accuracy and efficiency compared to "
            "always using multi-step retrieval?"
        ),
        retriever=retriever,
        max_results=3,
    )

    assert result["answer"]
    assert "accuracy" in result["answer"].lower()
    assert "efficiency" in result["answer"].lower()
    assert result["retrieval_steps"] == 2
    assert isinstance(result["citations"], list)
    assert len(result["citations"]) >= 1


def test_single_step_answer_returns_fallback_when_no_evidence() -> None:
    """The single-step strategy should return a safe fallback with no evidence."""

    class EmptyRetriever:
        def search(self, query: str, k: int = 5) -> list[dict]:
            return []

    result = single_step_answer(
        query="What is the maintenance schedule for the Mars colony water pump?",
        retriever=EmptyRetriever(),  # type: ignore[arg-type]
        max_results=3,
    )

    assert result["answer"] == FALLBACK_ANSWER
    assert result["citations"] == []
    assert result["retrieval_steps"] == 1


def test_multi_step_answer_returns_fallback_when_no_evidence() -> None:
    """The multi-step strategy should return a safe fallback with no evidence."""

    class EmptyRetriever:
        def search(self, query: str, k: int = 5) -> list[dict]:
            return []

    result = multi_step_answer(
        query="What is the maintenance schedule for the Mars colony water pump?",
        retriever=EmptyRetriever(),  # type: ignore[arg-type]
        max_results=3,
    )

    assert result["answer"] == FALLBACK_ANSWER
    assert result["citations"] == []
    assert result["retrieval_steps"] == 2
