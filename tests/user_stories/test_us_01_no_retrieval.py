"""User story test for US-01: no retrieval routing."""

from __future__ import annotations

import pytest
from myproject.router import route_query


@pytest.mark.user_story("US-01")
def test_us_01_no_retrieval() -> None:
    """Given/When/Then.

    Given the Adaptive RAG application pipeline is available,
    When the user submits a straightforward question about Adaptive RAG,
    Then the system returns label A, uses the no_retrieval strategy,
    uses zero retrieval steps, includes a request ID, and returns an answer.
    """
    result = route_query("What is Adaptive RAG?")

    assert (
        result["question"] == "What is Adaptive RAG?"
    )  # The original user query is included in the response under the "question" key, allowing for traceability and verification of the input that was processed by the system.
    assert (
        result["complexity_label"] == "A"
    )  # The complexity label assigned to the query is "A", indicating that the system classified the question as straightforward and suitable for the no_retrieval strategy.
    assert (
        result["strategy"] == "no_retrieval"
    )  # The strategy used to answer the query is "no_retrieval", which means that the system generated an answer without performing any retrieval steps, relying solely on the information available in the query and its internal knowledge.
    assert (
        result["retrieval_steps"] == 0
    )  # The number of retrieval steps taken to answer the query is 0, confirming that the no_retrieval strategy was used and that no evidence passages were retrieved from the corpus.
    assert result[
        "request_id"
    ]  # A unique identifier for the request is included in the response under the "request_id" key, which can be used for tracing and debugging purposes to track the specific request that was processed.
    assert result[
        "answer"
    ]  # An answer is included in the response under the "answer" key, indicating that the system successfully generated a response to the user's question based on the no_retrieval strategy.
    assert isinstance(
        result["citations"], list
    )  # The "citations" key in the response contains a list, which is expected to be empty for the no_retrieval strategy since no evidence passages were retrieved. This confirms that the system did not perform any retrieval steps and did not include any citations in the answer.
    assert (
        result["citations"] == []
    )  # The "citations" key in the response is an empty list, confirming that no evidence passages were retrieved or cited in the answer, which is consistent with the expected behavior of the no_retrieval strategy for a straightforward question.
    assert (
        result["latency_ms"] >= 0
    )  # The latency of the request is included in the response under the "latency_ms" key, and it is expected to be a non-negative integer representing the total time taken to process the request in milliseconds. This allows for performance monitoring and analysis of the system's response times.
