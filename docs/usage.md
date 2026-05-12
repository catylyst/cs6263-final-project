# Usage Guide

> Every feature listed in `docs/STORIES.md` has a matching section here. The TA can use this guide with `docs/STORIES.md` to walk through the running application without reading the source code.

## Submitting a No-Retrieval Question (US-01)

This story verifies that a simple question is routed to the no-retrieval strategy.

### UI Steps

1. Visit:

```text
http://localhost:8080
```

2. Type this question into the question box:

```text
What is Adaptive RAG?
```

3. Click `Submit`.
4. Review the response shown below the input box.

### Expected Result

The response should show:

```text
complexity_label: A
strategy: no_retrieval
retrieval_steps: 0
```

The response should also include:

```text
answer
request_id
latency_ms
```

The citations list should be empty because no retrieval is used for this story.

### API Example

```bash
curl -X POST "http://localhost:8080/api/query" \
  -H "Content-Type: application/json" \
  -d "{\"text\":\"What is Adaptive RAG?\",\"max_results\":5}"
```

---

## Submitting a Single-Step Retrieval Question (US-02)

This story verifies that a moderate question is routed to one retrieval step.

### UI Steps

1. Visit:

```text
http://localhost:8080
```

2. Type this question into the question box:

```text
What are the three routing labels in Adaptive RAG?
```

3. Click `Submit`.
4. Review the answer, routing label, strategy, retrieval steps, and citations.

### Expected Result

The response should show:

```text
complexity_label: B
strategy: single_step
retrieval_steps: 1
```

The answer should mention:

```text
A
B
C
```

The response should include at least one citation. Each citation should show:

```text
doc_id
title
snippet
score
```

### API Example

```bash
curl -X POST "http://localhost:8080/api/query" \
  -H "Content-Type: application/json" \
  -d "{\"text\":\"What are the three routing labels in Adaptive RAG?\",\"max_results\":5}"
```

---

## Submitting a Multi-Step Retrieval Question (US-03)

This story verifies that a more complex question is routed to the multi-step strategy.

### UI Steps

1. Visit:

```text
http://localhost:8080
```

2. Type this question into the question box:

```text
How does Adaptive RAG balance accuracy and efficiency compared to always using multi-step retrieval?
```

3. Click `Submit`.
4. Review the answer and metadata.

### Expected Result

The response should show:

```text
complexity_label: C
strategy: multi_step
retrieval_steps: 2
```

The answer should discuss both:

```text
accuracy
efficiency
```

The response should include citations because retrieval is used.

### API Example

```bash
curl -X POST "http://localhost:8080/api/query" \
  -H "Content-Type: application/json" \
  -d "{\"text\":\"How does Adaptive RAG balance accuracy and efficiency compared to always using multi-step retrieval?\",\"max_results\":5}"
```

---

## Reviewing Evidence, Routing Decision, Latency, and Request ID (US-04)

This story verifies that every successful response includes the metadata needed for grading and traceability.

### UI Steps

1. Visit:

```text
http://localhost:8080
```

2. Submit this question:

```text
What are the three routing labels in Adaptive RAG?
```

3. Review the response section.

### Expected Result

The response should show these fields:

```text
request_id
question
complexity_label
strategy
answer
citations
retrieval_steps
latency_ms
```

For this specific question, the expected routing result is:

```text
complexity_label: B
strategy: single_step
retrieval_steps: 1
```

The `request_id` should be visible. The same request ID can be used to trace the request in logs.

### Log Verification

With Docker running, copy the `request_id` from the response and search logs:

```bash
docker compose logs app | grep <request_id>
```

PowerShell:

```powershell
docker compose logs app | Select-String "<request_id>"
```

---

## Empty Input Handling (US-05)

This story verifies that the system returns a clear error when the user submits an empty question.

### UI Steps

1. Visit:

```text
http://localhost:8080
```

2. Leave the question box empty.
3. Click `Submit`.
4. Review the error message.

### Expected Result

The UI should show either:

```text
input text is required
```

or:

```text
Please enter a question
```

The UI should not show:

```text
blank answer
Python stack trace
server error page
```

### API Example

```bash
curl -X POST "http://localhost:8080/api/query" \
  -H "Content-Type: application/json" \
  -d "{\"text\":\"\",\"max_results\":5}"
```

Expected API response:

```json
{
  "error": "input text is required"
}
```

Expected HTTP status:

```text
400
```

---

## No Evidence Fallback (US-06)

This story verifies that the system gives a safe fallback when the local corpus does not contain enough evidence.

### UI Steps

1. Visit:

```text
http://localhost:8080
```

2. Type this unrelated question:

```text
What is the maintenance schedule for the Mars colony water pump?
```

3. Click `Submit`.
4. Review the answer and citations.

### Expected Result

The system should not crash.

The answer should be:

```text
I could not find enough evidence in the local corpus to answer the question.
```

The citations list should be empty.

The response should still include:

```text
request_id
complexity_label
strategy
retrieval_steps
latency_ms
```

### API Example

```bash
curl -X POST "http://localhost:8080/api/query" \
  -H "Content-Type: application/json" \
  -d "{\"text\":\"What is the maintenance schedule for the Mars colony water pump?\",\"max_results\":5}"
```

Expected response behavior:

```text
safe fallback answer
empty citations list
no stack trace
request_id included
```

---

## Configuration Notes

This project does not require an external LLM API key.

The `.env` file may include:

```text
APP_ENV=local
CORPUS_PATH=data/corpus.jsonl
LOG_LEVEL=INFO
MAX_QUERY_CHARS=1000
DEFAULT_TOP_K=5
```

The local corpus must exist at:

```text
data/corpus.jsonl
```

If the corpus is missing, retrieval-based questions will fail because the retriever cannot load evidence.

---

## Running the API Locally

Start the API with:

```bash
uvicorn myproject.api:app --host 0.0.0.0 --port 8080
```

Then open:

```text
http://localhost:8080
```

Health check:

```text
http://localhost:8080/health
```

Query endpoint:

```text
POST /api/query
```

---

## Running with Docker

From the project root:

```bash
cp .env.example .env
docker compose up
```

The application should be available at:

```text
http://localhost:8080
```

---

## Tips

Use full questions instead of short keyword fragments.

Good examples:

```text
What is Adaptive RAG?
What are the three routing labels in Adaptive RAG?
How does Adaptive RAG balance accuracy and efficiency compared to always using multi-step retrieval?
```

Avoid expecting the system to answer general world knowledge questions. The project is scoped to the local Adaptive RAG corpus. Unsupported questions should return the safe fallback response.
