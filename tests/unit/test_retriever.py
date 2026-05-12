"""Unit tests for the local corpus retriever."""

from __future__ import annotations

from pathlib import Path

from myproject.retriever import Retriever


def test_retriever_loads_local_corpus() -> None:
    """The retriever should load documents from data/corpus.jsonl."""
    retriever = Retriever("data/corpus.jsonl")

    assert len(retriever.documents) >= 1
    assert retriever.documents[0].doc_id
    assert retriever.documents[0].title
    assert retriever.documents[0].text


def test_retriever_returns_results_for_routing_labels() -> None:
    """A relevant query should return at least one citation."""
    retriever = Retriever("data/corpus.jsonl")

    results = retriever.search("What are the three routing labels in Adaptive RAG?", k=3)

    assert len(results) >= 1

    first = results[0]
    assert first["doc_id"]
    assert first["title"]
    assert first["snippet"]
    assert first["score"] >= 0.0


def test_retriever_returns_empty_for_blank_query() -> None:
    """A blank query should return no results."""
    retriever = Retriever("data/corpus.jsonl")

    assert retriever.search("", k=3) == []


def test_retriever_missing_file_raises_error(tmp_path: Path) -> None:
    """A missing corpus path should raise FileNotFoundError."""
    missing_file = tmp_path / "missing.jsonl"

    try:
        Retriever(str(missing_file))
    except FileNotFoundError as exc:
        assert "Corpus file not found" in str(exc)
    else:
        raise AssertionError("Expected FileNotFoundError")