# Datasets

> Every dataset or corpus used by the project must be listed here with source, version, license, and reproducibility notes. This project uses a small local JSONL corpus that is committed to the repository because it is original project-authored text and is required for deterministic grading.

## Dataset 1: Adaptive RAG Local Corpus

- **Source URL:** Not applicable. The corpus was written specifically for this course project.
- **Local path:** `data/corpus.jsonl`
- **Version:** `local-corpus-v1`
- **sha256:** To be computed after final corpus edits.
- **License:** Same license as this repository.
- **Size:** Approximately 12 JSONL records.
- **Cite as:** Project-authored local corpus for the CS 6263 Adaptive RAG Question Answering System.

## Overview

This project uses a small local JSONL corpus for retrieval. The corpus supports the Adaptive RAG Question Answering System by providing short evidence passages about Adaptive RAG, query complexity, routing labels, retrieval strategies, response metadata, fallback behavior, and structured logging.

The corpus is intentionally small so the project can run locally during grading without external downloads, paid APIs, large datasets, or large model dependencies.

## Dataset Location

The local corpus is stored at:

```text
data/corpus.jsonl
```

## Dataset Format

Each line in `data/corpus.jsonl` is one complete JSON object. The file is not wrapped in square brackets.

Each record uses this structure:

```json
{
  "doc_id": "string",
  "title": "string",
  "text": "string",
  "source": "string"
}
```

## Fields

| Field | Description |
|---|---|
| `doc_id` | Stable document identifier used in citations |
| `title` | Human-readable document title |
| `text` | Short evidence passage used by the retriever |
| `source` | Source label for provenance |

## Corpus Contents

The corpus contains short original summaries about:

1. Adaptive RAG overview
2. Adaptive RAG routing labels
3. No retrieval strategy
4. Single-step retrieval strategy
5. Multi-step retrieval strategy
6. Accuracy and efficiency tradeoff
7. Retrieval overhead
8. Query complexity classification
9. Local corpus behavior
10. Safe fallback behavior
11. Structured logging
12. Response metadata

## Provenance

The corpus was written specifically for this course project. It is based on the general Adaptive RAG concept described in the project specification and paper summary, but it does not copy long-form text from the Adaptive-RAG paper or the original Adaptive-RAG GitHub repository.

The source value used in each record is:

```text
original_course_summary
```

This means the passage is original project documentation text written for this implementation.

## Download

No external data download is required.

The corpus is included in the repository at:

```text
data/corpus.jsonl
```

The `make download-data` target should confirm the local corpus exists. Since the dataset is project-authored and small, it does not download external data.

Expected behavior:

```bash
make download-data
```

The command should complete successfully if `data/corpus.jsonl` exists.

## Manual Verification

To verify the corpus manually:

```bash
python -m json.tool data/corpus.jsonl
```

Because this is JSONL, another useful validation command is:

```bash
python -c "import json; [json.loads(line) for line in open('data/corpus.jsonl', encoding='utf-8') if line.strip()]; print('corpus valid')"
```

## Preprocessing

No separate preprocessing step is required.

At runtime, the retriever loads `data/corpus.jsonl`, reads each JSONL record, extracts the `text` field, and builds a TF-IDF matrix using scikit-learn. This process is deterministic.

The retrieval process is:

1. Load JSONL records from `data/corpus.jsonl`.
2. Validate each record using the `CorpusDocument` schema.
3. Extract document text.
4. Build a TF-IDF matrix.
5. Transform the user query.
6. Rank documents by cosine similarity.
7. Return citations containing `doc_id`, `title`, `snippet`, and `score`.

## Reproducibility

No external services, API keys, or downloads are needed for this dataset.

A fresh clone of the repository should include:

```text
data/corpus.jsonl
```

The test suite and application expect this file to exist.

## Limitations

The corpus is small and focused only on the Adaptive RAG project. It is not a general-purpose knowledge base. It does not include Wikipedia-scale data, benchmark QA datasets, private documents, or real-time information.

Questions outside the local corpus may return a safe fallback response instead of a supported answer.

## Data Not Used

This project does not use the full benchmark datasets from the Adaptive-RAG paper, such as SQuAD, Natural Questions, TriviaQA, MuSiQue, HotpotQA, or 2WikiMultiHopQA. Those datasets are out of scope for this smaller reproducible course implementation.
