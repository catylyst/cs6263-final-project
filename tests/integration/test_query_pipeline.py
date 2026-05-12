"""Integration tests for the Adaptive RAG query pipeline.

These tests verify the full local pipeline through the router, classifier,
retriever, and answer strategies without requiring an external LLM API.
"""

from __future__ import annotations

import pytest
from myproject.router import route_query
from myproject.strategies import FALLBACK_ANSWER


def test_pipeline_handles_no_retrieval_question() -> None:
    """The full pipeline should handle a simple no-retrieval question."""
    result = route_query("What is Adaptive RAG?")

    assert result["complexity_label"] == "A"
    assert result["strategy"] == "no_retrieval"
    assert result["retrieval_steps"] == 0
    assert result["answer"]
    assert result["request_id"]
    assert result["citations"] == []


def test_pipeline_handles_single_step_question() -> None:
    """The full pipeline should handle a single-step retrieval question."""
    result = route_query("What are the three routing labels in Adaptive RAG?")

    assert result["complexity_label"] == "B"
    assert result["strategy"] == "single_step"
    assert result["retrieval_steps"] == 1
    assert result["answer"]
    assert len(result["citations"]) >= 1


def test_pipeline_handles_multi_step_question() -> None:
    """The full pipeline should handle a multi-step retrieval question."""
    question = (
        "How does Adaptive RAG balance accuracy and efficiency compared to "
        "always using multi-step retrieval?"
    )

    result = route_query(question)

    assert result["complexity_label"] == "C"
    assert result["strategy"] == "multi_step"
    assert result["retrieval_steps"] == 2
    assert result["answer"]
    assert len(result["citations"]) >= 1


def test_pipeline_handles_empty_input() -> None:
    """The full pipeline should reject empty input with a clear error."""
    with pytest.raises(ValueError, match="input text is required"):
        route_query("")


def test_pipeline_handles_no_evidence_question() -> None:
    """The full pipeline should return a safe fallback when evidence is missing."""
    result = route_query("What is the maintenance schedule for the Mars colony water pump?")

    assert result["answer"] == FALLBACK_ANSWER
    assert result["citations"] == []
    assert result["request_id"]
