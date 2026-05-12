"""User story test for US-03: multi-step retrieval routing."""

from __future__ import annotations

import pytest
from myproject.router import route_query


@pytest.mark.user_story("US-03")
def test_us_03_multi_step() -> None:
    """Given/When/Then.

    Given the Adaptive RAG application pipeline and local corpus are available,
    When the user asks a complex question about balancing accuracy and efficiency,
    Then the system returns label C, uses the multi_step strategy,
    uses two retrieval steps, includes citations, and returns an answer.
    """
    question = (
        "How does Adaptive RAG balance accuracy and efficiency compared to "
        "always using multi-step retrieval?"
    )

    result = route_query(question)

    assert result["question"] == question
    assert result["complexity_label"] == "C"
    assert result["strategy"] == "multi_step"
    assert result["retrieval_steps"] == 2
    assert result["request_id"]
    assert result["answer"]
    assert "accuracy" in result["answer"].lower()
    assert "efficiency" in result["answer"].lower()
    assert isinstance(result["citations"], list)
    assert len(result["citations"]) >= 1

    first_citation = result["citations"][0]
    assert first_citation["doc_id"]
    assert first_citation["title"]
    assert first_citation["snippet"]
    assert first_citation["score"] >= 0.0
    assert result["latency_ms"] >= 0
