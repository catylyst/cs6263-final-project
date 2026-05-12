# Models

> This document lists every model, classifier, retrieval method, and scoring method used by the project. This project does not require a paid external LLM API or downloaded model checkpoint during grading.

## Model 1: Rule-Based Query Complexity Classifier

- **Name:** Adaptive RAG Query Complexity Classifier
- **Local module:** `src/myproject/classifier.py`
- **Model type:** Deterministic rule-based classifier
- **Version:** `classifier-v1`
- **External checkpoint:** None
- **Download required:** No
- **License:** Same license as this repository
- **Purpose:** Predict whether a user question should use no retrieval, single-step retrieval, or multi-step retrieval.

## Overview

The query complexity classifier predicts one of three labels:

| Label | Meaning | Selected strategy |
|---|---|---|
| A | Straightforward question | No retrieval |
| B | Moderate question | Single-step retrieval |
| C | Complex question | Multi-step retrieval |

The classifier is intentionally lightweight and deterministic. This makes the project easier to test, reproduce, and grade on a clean machine.

The classifier does not use a trained neural model. It uses transparent rules based on phrases, question length, and reasoning cues.

## Classification Rules

The classifier checks the normalized input question for complexity cues.

Examples that route to label `A`:

```text
What is Adaptive RAG?
Define Adaptive RAG.
What does Adaptive RAG mean?
```

Examples that route to label `B`:

```text
What are the three routing labels in Adaptive RAG?
What is single-step retrieval?
What is the query complexity classifier?
```

Examples that route to label `C`:

```text
How does Adaptive RAG balance accuracy and efficiency compared to always using multi-step retrieval?
Compare single-step retrieval and multi-step retrieval.
What is the relationship between retrieval overhead and question complexity?
```

## Model 2: TF-IDF Retriever

- **Name:** Local TF-IDF Retriever
- **Local module:** `src/myproject/retriever.py`
- **Model type:** TF-IDF vectorizer with cosine similarity
- **Library:** scikit-learn
- **External checkpoint:** None
- **Download required:** No
- **Purpose:** Search `data/corpus.jsonl` and return relevant evidence passages as citations.

## Retriever Details

The retriever loads the local JSONL corpus and builds a TF-IDF matrix from the `text` field of each corpus record.

At query time, the retriever:

1. Normalizes the user query.
2. Converts the query into the TF-IDF vector space.
3. Computes cosine similarity between the query and corpus documents.
4. Ranks documents by similarity score.
5. Returns the top matching documents as citations.

Each citation contains:

```text
doc_id
title
snippet
score
```

## Model 3: Deterministic Answer Strategies

- **Name:** Adaptive RAG Answer Strategies
- **Local module:** `src/myproject/strategies.py`
- **Model type:** Deterministic answer generation logic
- **External checkpoint:** None
- **Download required:** No
- **Purpose:** Generate answers using the selected retrieval strategy.

The project implements three answer strategies:

| Strategy | Retrieval steps | Description |
|---|---:|---|
| `no_retrieval` | 0 | Answers straightforward questions using built-in project knowledge |
| `single_step` | 1 | Retrieves evidence once and answers from the top passages |
| `multi_step` | 2 | Performs two retrieval passes and combines evidence |

## Why No External LLM Is Used

The original Adaptive-RAG paper uses large language models and a trained smaller language model classifier. This project recreates the core design idea in a smaller course-ready implementation.

A paid or downloaded LLM is not used because the project needs to be:

1. Reproducible on a clean grading machine.
2. Runnable without API keys.
3. Testable with deterministic outputs.
4. Small enough for Docker-based grading.
5. Aligned with the course software engineering rubric.

## Prompting

This project does not use prompt templates for an external LLM.

The answer generation logic is deterministic and evidence-based. Retrieval-based answers are generated from local citations, and unsupported questions return a safe fallback response.

Fallback response:

```text
I could not find enough evidence in the local corpus to answer the question.
```

## Reproducibility

No model downloads are required.

The system can be run from a fresh clone using the local source code and local corpus.

The required files are:

```text
src/myproject/classifier.py
src/myproject/retriever.py
src/myproject/strategies.py
data/corpus.jsonl
```

## Limitations

The rule-based classifier is easy to inspect, but it is less flexible than a trained query-complexity classifier.

Known limitations:

1. It may misclassify ambiguous questions.
2. It depends on phrase matching and simple heuristics.
3. It does not learn from new examples.
4. It does not use semantic embeddings.
5. It does not reproduce the full classifier training process from the Adaptive-RAG paper.

The TF-IDF retriever is also limited. It works well for a small local corpus, but it is not designed for large-scale open-domain retrieval.

## Future Work

Future work could replace the rule-based classifier with a trained classifier, add dense embeddings, add a larger corpus, compare more retrieval strategies, and evaluate on benchmark QA datasets.
