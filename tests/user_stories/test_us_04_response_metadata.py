"""User story test for US-04: response metadata is returned."""

from __future__ import annotations

import pytest

from myproject.router import route_query


@pytest.mark.user_story("US-04")
def test_us_04_response_metadata() -> None:
    """Given/When/Then.

    Given the Adaptive RAG application pipeline is available,
    When the user submits a valid question,
    Then the response includes the answer, routing decision, citations,
    retrieval step count, latency, and request ID.
    """
    result = route_query("What are the three routing labels in Adaptive RAG?")

    required_keys = {
        "request_id",
        "question",
        "complexity_label",
        "strategy",
        "answer",
        "citations",
        "retrieval_steps",
        "latency_ms",
    }

    assert required_keys.issubset(result.keys())
    assert result["request_id"]
    assert result["question"]
    assert result["complexity_label"] in {"A", "B", "C"}
    assert result["strategy"] in {"no_retrieval", "single_step", "multi_step"}
    assert result["answer"]
    assert isinstance(result["citations"], list)
    assert result["retrieval_steps"] >= 0
    assert result["latency_ms"] >= 0

    assert result["complexity_label"] == "B"
    assert result["strategy"] == "single_step"
    assert result["retrieval_steps"] == 1
    assert len(result["citations"]) >= 1

    citation = result["citations"][0]
    citation_keys = {"doc_id", "title", "snippet", "score"}

    assert citation_keys.issubset(citation.keys())
    assert citation["doc_id"]
    assert citation["title"]
    assert citation["snippet"]
    assert citation["score"] >= 0.0
