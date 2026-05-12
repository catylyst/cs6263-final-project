"""User story test for US-06: no evidence fallback behavior."""

from __future__ import annotations

import pytest
from myproject.router import route_query
from myproject.strategies import FALLBACK_ANSWER


@pytest.mark.user_story("US-06")
def test_us_06_no_evidence_returns_safe_fallback() -> None:
    """Given/When/Then.

    Given the Adaptive RAG application pipeline and local corpus are available,
    When the user asks a question unrelated to the local corpus,
    Then the system returns a safe fallback response, no citations,
    no crash, and a request ID.
    """
    question = "What is the maintenance schedule for the Mars colony water pump?"

    result = route_query(question)

    assert result["question"] == question
    assert result["request_id"]
    assert result["answer"] == FALLBACK_ANSWER
    assert result["citations"] == []
    assert isinstance(result["citations"], list)
    assert result["retrieval_steps"] >= 0
    assert result["latency_ms"] >= 0
    assert result["complexity_label"] in {"A", "B", "C"}
    assert result["strategy"] in {"no_retrieval", "single_step", "multi_step"}
