"""Unit tests for query complexity classifier."""

from __future__ import annotations

import pytest

from myproject.classifier import classify_query


def test_classify_simple_adaptive_rag_question() -> None:
    """A simple definition question should route to no retrieval."""
    assert classify_query("What is Adaptive RAG?") == "A"


def test_classify_routing_labels_question() -> None:
    """A routing labels question should route to single-step retrieval."""
    assert classify_query("What are the three routing labels in Adaptive RAG?") == "B"


def test_classify_accuracy_efficiency_question() -> None:
    """A comparison question should route to multi-step retrieval."""
    question = (
        "How does Adaptive RAG balance accuracy and efficiency compared to "
        "always using multi-step retrieval?"
    )

    assert classify_query(question) == "C"


def test_classify_empty_input_raises_error() -> None:
    """Empty input should raise a clear validation error."""
    with pytest.raises(ValueError, match="input text is required"):
        classify_query("")