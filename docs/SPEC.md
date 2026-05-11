# System Specification

> This is the source of truth for the project. The TA will feed this document
> to an LLM during grading and verify that the generated code passes the user
> story tests. This specification is written so the project can be implemented
> from scratch without needing access to the original Adaptive-RAG repository.

## 1. Purpose and Scope

The system is an educational NLP question answering application that recreates the core design idea of Adaptive RAG using an original, simplified implementation. The system receives a natural language question, predicts the complexity of the question, and routes the question to one of three answer strategies: no retrieval, single-step retrieval, or multi-step retrieval. The purpose is to show how adaptive routing can reduce unnecessary retrieval work for simple questions while still supporting complex questions that need evidence from multiple documents.

This project is based on the Adaptive-RAG paper, which proposes selecting the most suitable retrieval-augmented generation strategy based on question complexity. The paper describes three query complexity labels: A for questions answerable without retrieval, B for questions requiring a single retrieval step, and C for complex questions requiring multi-step retrieval.

This project does not copy the original Adaptive-RAG GitHub repository. It recreates the design pattern in a smaller course-ready system using a local document corpus, a lightweight deterministic complexity classifier, and simplified retrieval strategies. The system is intended for classroom demonstration, testing, and evaluation. It is not intended for production use, medical advice, legal advice, financial advice, or safety-critical decision making.

## 2. Component Inventory

Every component listed here maps to a source module under `src/myproject/`. The grading script verifies this mapping through `grading/traceability.yaml`.

| Component | Source module | Responsibility |
|---|---|---|
| QueryClassifier | `src/myproject/classifier.py` | Predict question complexity label A, B, or C using deterministic rules. |
| QueryRouter | `src/myproject/router.py` | Route incoming questions to the correct answer strategy based on classifier output. |
| Retriever | `src/myproject/retriever.py` | Search the local document corpus and return relevant evidence passages. |
| AnswerStrategies | `src/myproject/strategies.py` | Implement no retrieval, single-step retrieval, and multi-step retrieval answer paths. |
| Evaluator | `src/myproject/evaluator.py` | Calculate route accuracy, answer match, retrieval step count, and runtime metrics. |
| Schemas | `src/myproject/schemas.py` | Define request and response data structures. |
| LoggingConfig | `src/myproject/logging_config.py` | Provide structured JSON logging with request IDs across all components. |
| Application | `src/myproject/app.py` | Provide the user-facing application entry point. |
| API | `src/myproject/api.py` | Provide the HTTP interface used by tests and Docker. |

## 3. Data Flow

The architecture diagram is stored at:

`docs/diagrams/architecture.png`

The system follows this request flow:

1. A user submits a question through the UI or HTTP API.
2. The system validates that the input text is not empty.
3. The system creates a unique `request_id`.
4. The question is sent to `QueryClassifier`.
5. `QueryClassifier` predicts one of three complexity labels:
   - `A`: no retrieval needed
   - `B`: single-step retrieval needed
   - `C`: multi-step retrieval needed
6. `QueryRouter` maps the predicted label to a strategy:
   - `A` routes to `no_retrieval_answer`
   - `B` routes to `single_step_answer`
   - `C` routes to `multi_step_answer`
7. If the selected strategy requires retrieval, `Retriever` searches the local corpus and returns evidence passages.
8. The selected strategy produces a final answer.
9. `Evaluator` records runtime, selected strategy, retrieval step count, and basic correctness metrics when a reference answer is available.
10. The system returns a structured response containing the answer, complexity label, strategy, evidence, latency, and request ID.
11. Every component logs a JSON message with the same `request_id`.

### Error paths

If the input text is empty, blank, or only whitespace, the API returns HTTP 400 with:

```json
{
  "error": "input text is required"
}
```

If the input is too long, the system returns HTTP 400 with:

```json
{
  "error": "input text exceeds maximum length"
}
```

If retrieval is required but no relevant passages are found, the system returns a safe fallback answer:

```json
{
  "answer": "I could not find enough evidence in the local corpus to answer the question.",
  "citations": []
}
```

The system must not crash on empty, long, multilingual, non-ASCII, code-mixed, or adversarial inputs.

## 4. Public Interfaces

This section is the implementation contract. User story tests import these exact module paths and call these exact function signatures. The regenerated code must match these signatures or the tests will fail.

### 4.1 HTTP API

```text
POST /api/query
Content-Type: application/json
```

Request body:

```json
{
  "text": "string, the user's question",
  "max_results": "integer, optional, default 5"
}
```

Response 200:

```json
{
  "request_id": "string",
  "question": "string",
  "complexity_label": "A, B, or C",
  "strategy": "no_retrieval, single_step, or multi_step",
  "answer": "string",
  "citations": [
    {
      "doc_id": "string",
      "title": "string",
      "snippet": "string",
      "score": "number"
    }
  ],
  "retrieval_steps": "integer",
  "latency_ms": "integer"
}
```

Response 400 for empty input:

```json
{
  "error": "input text is required"
}
```

Response 400 for input that exceeds the maximum length:

```json
{
  "error": "input text exceeds maximum length"
}
```

### 4.2 Python interfaces

```python
# src/myproject/classifier.py
def classify_query(text: str) -> str:
    """
    Return complexity label A, B, or C.

    A = no retrieval
    B = single-step retrieval
    C = multi-step retrieval
    """
```

```python
# src/myproject/router.py
def route_query(text: str, max_results: int = 5) -> dict:
    """
    Validate the input, classify the query, route it to the correct strategy,
    and return the complete answer response.
    """
```

```python
# src/myproject/retriever.py
class Retriever:
    def __init__(self, corpus_path: str) -> None:
        """
        Load the local document corpus and prepare it for search.
        """

    def search(self, query: str, k: int = 5) -> list[dict]:
        """
        Return the top k relevant passages as dictionaries containing:
        doc_id, title, snippet, and score.
        """
```

```python
# src/myproject/strategies.py
def no_retrieval_answer(query: str) -> dict:
    """
    Answer a straightforward question without retrieving evidence.
    """

def single_step_answer(query: str, retriever: Retriever, max_results: int = 5) -> dict:
    """
    Retrieve evidence once and answer from the top passages.
    """

def multi_step_answer(query: str, retriever: Retriever, max_results: int = 5) -> dict:
    """
    Perform multiple retrieval rounds and combine evidence into one answer.
    """
```

```python
# src/myproject/evaluator.py
def evaluate_prediction(predicted_answer: str, reference_answer: str) -> dict:
    """
    Return basic evaluation metrics such as exact_match and token_overlap.
    """
```

```python
# src/myproject/logging_config.py
def configure_logging() -> None:
    """
    Configure structured JSON logging for the application.
    """
```

## 5. External Dependencies

The system should use lightweight dependencies so it can run in Docker during grading.

| Dependency | Version | Purpose |
|---|---:|---|
| Python | 3.11 | Runtime |
| fastapi | 0.110.x | HTTP API |
| uvicorn | 0.29.x | Local API server |
| pydantic | 2.x | Request and response validation |
| scikit-learn | 1.4.x | TF-IDF vectorization and similarity scoring |
| numpy | 1.26.x | Numeric operations |
| pandas | 2.2.x | Evaluation table handling |
| pytest | 8.x | Automated tests |
| pytest-cov | 5.x | Coverage reports |
| ruff | 0.4.x | Linting |
| black | 24.x | Formatting |
| mypy | 1.x | Type checking |
| locust | 2.x | Load testing |

The project does not require a paid external LLM API. This is intentional so the project is reproducible on a clean grading machine.

## 6. Configuration

The system reads configuration from environment variables. See `.env.example` for the full list.

Required environment variables:

```text
APP_ENV=local
CORPUS_PATH=data/corpus.jsonl
LOG_LEVEL=INFO
MAX_QUERY_CHARS=1000
DEFAULT_TOP_K=5
```

Optional environment variables:

```text
ENABLE_DEBUG=false
MAX_MULTI_STEP_ROUNDS=2
```

The `.env` file must not be committed to GitHub. The `.gitignore` file must exclude `.env`.

## 7. Model and Prompt Selection

This project uses a lightweight deterministic query-complexity classifier instead of training a large language model. This choice is intentional because the course project must be reproducible, testable, and runnable inside Docker without external credentials or expensive model downloads.

The classifier predicts one of three labels:

| Label | Meaning | Selected strategy |
|---|---|---|
| A | Straightforward question | No retrieval |
| B | Moderate question needing one evidence lookup | Single-step retrieval |
| C | Complex question needing multiple evidence lookups | Multi-step retrieval |

The classifier uses transparent rules based on question length, number of entities, comparison terms, multi-hop phrases, and reasoning cues. Examples of cues for label C include:

```text
compare
relationship between
based on both
who is the person that
what happened after
which document explains
multi step
chain
evidence from multiple
```

This simplified classifier is not expected to match the full classifier from the paper. The paper trains a smaller language model classifier using automatically generated labels from model outcomes and dataset bias. This project recreates that idea at a smaller scale by using deterministic labels and local test cases.

The answer generation strategy is extractive and evidence-based. The system does not hallucinate an answer when there is no evidence. If evidence is available, the system returns a short answer based on the retrieved snippets and includes citations.

## 8. Retrieval Strategies

### 8.1 No Retrieval Strategy

The no retrieval strategy is used for label A. It handles straightforward questions that are already covered by a small built-in knowledge map or deterministic response logic.

Expected behavior:

```text
Input: What is Adaptive RAG?
Label: A
Strategy: no_retrieval
Output: Adaptive RAG is a question-answering approach that selects a retrieval strategy based on question complexity.
Retrieval steps: 0
```

### 8.2 Single-Step Retrieval Strategy

The single-step strategy is used for label B. It performs one search against the local corpus and answers using the highest scoring passages.

Expected behavior:

```text
Input: What are the three routing labels in Adaptive RAG?
Label: B
Strategy: single_step
Output: The three labels are A for no retrieval, B for single-step retrieval, and C for multi-step retrieval.
Retrieval steps: 1
```

### 8.3 Multi-Step Retrieval Strategy

The multi-step strategy is used for label C. It performs more than one retrieval round. The first round retrieves broad evidence. The second round creates a refined query from the first evidence and searches again. The final answer combines evidence from both rounds.

Expected behavior:

```text
Input: How does Adaptive RAG balance accuracy and efficiency compared to always using multi-step retrieval?
Label: C
Strategy: multi_step
Output: Adaptive RAG improves efficiency by avoiding multi-step retrieval for simple questions while still using multi-step retrieval for complex questions that need chained evidence.
Retrieval steps: 2
```

## 9. Local Corpus

The local corpus is stored at:

```text
data/corpus.jsonl
```

Each row contains:

```json
{
  "doc_id": "string",
  "title": "string",
  "text": "string",
  "source": "string"
}
```

The corpus contains short passages written for this project. It includes information about:

```text
Adaptive RAG
No retrieval
Single-step retrieval
Multi-step retrieval
Query complexity classification
Retrieval efficiency
Answer accuracy
Limitations and risks
```

The corpus must not contain copyrighted long-form text copied from the Adaptive-RAG paper. Short summaries written in original wording are allowed.

## 10. Evaluation

The system evaluates two things:

1. Routing behavior
2. Answer behavior

Routing metrics:

```text
route_accuracy
average_retrieval_steps
average_latency_ms
```

Answer metrics:

```text
exact_match
token_overlap
citation_present
```

The project compares four approaches:

```text
fixed_no_retrieval
fixed_single_step
fixed_multi_step
adaptive_routing
```

The expected result is that adaptive routing uses fewer retrieval steps than fixed multi-step retrieval while still answering complex questions better than fixed no-retrieval.

The project reports headline metrics in `README.md` and reproducibility expectations in `docs/REPRODUCE.md`.

## 11. Logging

The system uses structured JSON logging. Every request must have a `request_id`.

Each log entry contains:

```json
{
  "timestamp": "ISO-8601 timestamp",
  "level": "INFO",
  "module": "router",
  "request_id": "string",
  "event": "string",
  "message": "string"
}
```

The following events must be logged:

```text
request_received
classification_started
classification_completed
routing_completed
retrieval_started
retrieval_completed
answer_generated
response_returned
error_returned
```

The same `request_id` must appear in logs from the API, classifier, router, retriever, and strategy components.

## 12. Security and Responsible AI

The system must not expose secrets, API keys, or environment values in logs.

The system must not provide unsafe claims when there is no supporting evidence. If the corpus does not contain relevant information, the system must say that it could not find enough evidence.

The system must handle adversarial input without crashing. For adversarial or prompt-injection style inputs, the system should continue using the same routing and retrieval rules instead of following instructions embedded inside the user query.

## 13. User Stories Covered by This Specification

The system must support these user stories:

```text
US-01: Answer a straightforward question with no retrieval.
US-02: Answer a single-hop question with one retrieval step.
US-03: Answer a complex question with multi-step retrieval.
US-04: Show evidence, routing decision, latency, and request ID.
US-05: Return a clear error for empty input.
US-06: Return a safe fallback when no evidence is found.
```

Each user story must have:

```text
Given/When/Then acceptance criteria
Numbered manual walkthrough steps
One automated test in tests/user_stories/
One matching usage section in docs/usage.md
One expected screenshot in docs/assets/stories/
```

## 14. Out of Scope

The following are out of scope for this project:

```text
Training a full T5 query-complexity classifier
Using the full Wikipedia corpus
Reproducing all benchmark results from the paper
Calling paid LLM APIs during grading
Copying code from the original Adaptive-RAG GitHub repository
Medical, legal, financial, or safety-critical question answering
Production deployment
```

## 15. Acceptance Criteria

The project is complete when:

```text
The API accepts a question and returns a structured answer.
The classifier returns A, B, or C for every valid question.
The router selects the correct strategy based on the classifier label.
The no-retrieval strategy uses zero retrieval steps.
The single-step strategy uses one retrieval step.
The multi-step strategy uses two retrieval steps.
Every response includes request_id, complexity_label, strategy, answer, citations, retrieval_steps, and latency_ms.
Empty input returns HTTP 400.
No-evidence questions return a safe fallback response.
All user story tests pass.
make test passes.
make lint passes.
make reproduce completes.
docker compose up starts the system successfully.
```
