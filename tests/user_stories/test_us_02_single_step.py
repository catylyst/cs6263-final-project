"""User story test for US-02: single-step retrieval routing."""

from __future__ import annotations

import pytest

from myproject.router import route_query


@pytest.mark.user_story("US-02")
def test_us_02_single_step() -> None:
    """Given/When/Then.

    Given the Adaptive RAG application pipeline and local corpus are available,
    When the user asks about the three routing labels in Adaptive RAG,
    Then the system returns label B, uses the single_step strategy,
    uses one retrieval step, includes citations, and returns an answer.
    """
    result = route_query("What are the three routing labels in Adaptive RAG?")

    assert result["question"] == "What are the three routing labels in Adaptive RAG?"
    assert result["complexity_label"] == "B"
    assert result["strategy"] == "single_step"
    assert result["retrieval_steps"] == 1
    assert result["request_id"]
    assert result["answer"]
    assert "A" in result["answer"]
    assert "B" in result["answer"]
    assert "C" in result["answer"]
    assert isinstance(result["citations"], list)
    assert len(result["citations"]) >= 1

    first_citation = result["citations"][0]
    assert first_citation["doc_id"]
    assert first_citation["title"]
    assert first_citation["snippet"]
    assert first_citation["score"] >= 0.0
    assert result["latency_ms"] >= 0
