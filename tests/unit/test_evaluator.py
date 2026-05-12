"""Unit tests for Adaptive RAG evaluation helpers."""

from __future__ import annotations

from myproject.evaluator import (
    citation_present,
    evaluate_prediction,
    exact_match,
    normalize_text,
    summarize_route_result,
    token_overlap_score,
)


def test_normalize_text_lowercases_and_removes_punctuation() -> None:
    """normalize_text should lowercase text and remove punctuation."""
    result = normalize_text("Adaptive-RAG, Works!")

    assert result == "adaptive rag works"


def test_exact_match_true_for_normalized_equivalent_answers() -> None:
    """exact_match should compare normalized answers."""
    assert exact_match("Adaptive RAG.", "adaptive rag") is True


def test_exact_match_false_for_different_answers() -> None:
    """exact_match should return False when answers differ."""
    assert exact_match("single step", "multi step") is False


def test_token_overlap_score_returns_partial_overlap() -> None:
    """token_overlap_score should return a value between 0 and 1."""
    score = token_overlap_score(
        predicted_answer="Adaptive RAG uses retrieval routing",
        reference_answer="Adaptive RAG uses multi step retrieval",
    )

    assert 0.0 < score < 1.0


def test_evaluate_prediction_returns_expected_keys() -> None:
    """evaluate_prediction should return exact_match and token_overlap."""
    result = evaluate_prediction(
        predicted_answer="Adaptive RAG uses routing.",
        reference_answer="Adaptive RAG uses routing.",
    )

    assert result["exact_match"] is True
    assert result["token_overlap"] == 1.0


def test_citation_present_true_when_citations_exist() -> None:
    """citation_present should return True when citations are available."""
    citations = [
        {
            "doc_id": "adaptive_rag_labels",
            "title": "Adaptive RAG Routing Labels",
            "snippet": "Labels A, B, and C are used.",
            "score": 0.9,
        }
    ]

    assert citation_present(citations) is True


def test_citation_present_false_when_empty() -> None:
    """citation_present should return False for an empty citation list."""
    assert citation_present([]) is False


def test_summarize_route_result_returns_benchmark_fields() -> None:
    """summarize_route_result should extract routing and benchmark fields."""
    result = {
        "complexity_label": "B",
        "strategy": "single_step",
        "retrieval_steps": 1,
        "latency_ms": 120,
        "citations": [
            {
                "doc_id": "adaptive_rag_labels",
                "title": "Adaptive RAG Routing Labels",
                "snippet": "Labels A, B, and C are used.",
                "score": 0.9,
            }
        ],
    }

    summary = summarize_route_result(result)

    assert summary == {
        "complexity_label": "B",
        "strategy": "single_step",
        "retrieval_steps": 1,
        "latency_ms": 120,
        "citation_present": True,
    }