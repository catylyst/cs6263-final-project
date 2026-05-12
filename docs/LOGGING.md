# Logging

> The Logging category is graded by tracing one request end to end through `docker compose logs -f app` using the request ID returned by the system. This document explains the log format, the expected events, and what the TA should look for during the trace.

## Format

All production log entries should be written to stdout as JSON, one entry per line.

Expected format:

```json
{
  "timestamp": "2026-05-11T20:00:00.000Z",
  "level": "INFO",
  "module": "myproject.api",
  "request_id": "req_a1b2c3d4",
  "message": "received query",
  "extra": {
    "event": "request_received",
    "text_length": 42
  }
}
```

Required fields:

```text
timestamp
level
module
request_id
message
```

Recommended fields inside `extra`:

```text
event
complexity_label
strategy
retrieval_steps
latency_ms
hits
status
```

The goal is simple: a grader should be able to copy one `request_id` from the response and follow the same request through the API, classifier, router, retriever, answer strategy, and final response.

## Levels

| Level | Use |
|---|---|
| `DEBUG` | Internal details used during development. Off by default. |
| `INFO` | Normal request flow, including request received, classification completed, retrieval completed, and response sent. |
| `WARNING` | Recoverable issue, such as no evidence found or fallback response used. |
| `ERROR` | Request failed and returned an error response. |

The application sets the log level with the `LOG_LEVEL` environment variable.

Default value:

```text
INFO
```

## Request ID Propagation

Every user request should receive a unique `request_id`.

The same `request_id` must appear in every log line for that request. This is what makes the request traceable during grading.

The request ID should be visible in the API response:

```json
{
  "request_id": "req_a1b2c3d4",
  "question": "What are the three routing labels in Adaptive RAG?",
  "complexity_label": "B",
  "strategy": "single_step",
  "answer": "The three Adaptive RAG routing labels are A, B, and C.",
  "citations": [],
  "retrieval_steps": 1,
  "latency_ms": 120
}
```

The same request ID should also appear in the logs.

## Expected Events

A successful request should show these events:

```text
request_received
classification_started
classification_completed
routing_completed
retrieval_started
retrieval_completed
answer_generated
response_sent
```

For no-retrieval requests, the retrieval events may be skipped because the system does not call the retriever.

For an error request, the trace should include:

```text
request_received
error_returned
```

## Worked Example: Single-Step Retrieval

Example question:

```text
What are the three routing labels in Adaptive RAG?
```

Expected behavior:

```text
complexity_label: B
strategy: single_step
retrieval_steps: 1
```

Command used to watch logs:

```bash
docker compose logs -f app | grep req_a1b2c3d4
```

PowerShell version:

```powershell
docker compose logs app | Select-String "req_a1b2c3d4"
```

Example trace:

```json
{"timestamp":"2026-05-11T20:00:00.000Z","level":"INFO","module":"myproject.api","request_id":"req_a1b2c3d4","message":"received query","extra":{"event":"request_received","text_length":55}}
{"timestamp":"2026-05-11T20:00:00.010Z","level":"INFO","module":"myproject.classifier","request_id":"req_a1b2c3d4","message":"classification started","extra":{"event":"classification_started"}}
{"timestamp":"2026-05-11T20:00:00.015Z","level":"INFO","module":"myproject.classifier","request_id":"req_a1b2c3d4","message":"classification completed","extra":{"event":"classification_completed","complexity_label":"B"}}
{"timestamp":"2026-05-11T20:00:00.018Z","level":"INFO","module":"myproject.router","request_id":"req_a1b2c3d4","message":"selected answer strategy","extra":{"event":"routing_completed","complexity_label":"B","strategy":"single_step"}}
{"timestamp":"2026-05-11T20:00:00.020Z","level":"INFO","module":"myproject.retriever","request_id":"req_a1b2c3d4","message":"retrieval started","extra":{"event":"retrieval_started","k":5}}
{"timestamp":"2026-05-11T20:00:00.060Z","level":"INFO","module":"myproject.retriever","request_id":"req_a1b2c3d4","message":"retrieval completed","extra":{"event":"retrieval_completed","hits":3,"ms":40}}
{"timestamp":"2026-05-11T20:00:00.070Z","level":"INFO","module":"myproject.strategies","request_id":"req_a1b2c3d4","message":"answer generated","extra":{"event":"answer_generated","strategy":"single_step","retrieval_steps":1}}
{"timestamp":"2026-05-11T20:00:00.080Z","level":"INFO","module":"myproject.api","request_id":"req_a1b2c3d4","message":"response sent","extra":{"event":"response_sent","status":200,"latency_ms":80}}
```

The TA should be able to read the trace from top to bottom and confirm:

1. The API received the request.
2. The classifier assigned a complexity label.
3. The router selected the strategy.
4. The retriever searched the local corpus.
5. The answer strategy generated a response.
6. The API returned the response.

## Worked Example: No-Retrieval Request

Example question:

```text
What is Adaptive RAG?
```

Expected behavior:

```text
complexity_label: A
strategy: no_retrieval
retrieval_steps: 0
```

Example trace:

```json
{"timestamp":"2026-05-11T20:03:00.000Z","level":"INFO","module":"myproject.api","request_id":"req_b2c3d4e5","message":"received query","extra":{"event":"request_received","text_length":21}}
{"timestamp":"2026-05-11T20:03:00.010Z","level":"INFO","module":"myproject.classifier","request_id":"req_b2c3d4e5","message":"classification completed","extra":{"event":"classification_completed","complexity_label":"A"}}
{"timestamp":"2026-05-11T20:03:00.015Z","level":"INFO","module":"myproject.router","request_id":"req_b2c3d4e5","message":"selected answer strategy","extra":{"event":"routing_completed","complexity_label":"A","strategy":"no_retrieval"}}
{"timestamp":"2026-05-11T20:03:00.020Z","level":"INFO","module":"myproject.strategies","request_id":"req_b2c3d4e5","message":"answer generated","extra":{"event":"answer_generated","strategy":"no_retrieval","retrieval_steps":0}}
{"timestamp":"2026-05-11T20:03:00.030Z","level":"INFO","module":"myproject.api","request_id":"req_b2c3d4e5","message":"response sent","extra":{"event":"response_sent","status":200,"latency_ms":30}}
```

For this request, retrieval logs are not expected because the selected strategy is `no_retrieval`.

## Worked Example: Error Request

Example input:

```text

```

Expected behavior:

```text
HTTP 400
error: input text is required
```

Example trace:

```json
{"timestamp":"2026-05-11T20:05:00.000Z","level":"INFO","module":"myproject.api","request_id":"req_error123","message":"received query","extra":{"event":"request_received","text_length":0}}
{"timestamp":"2026-05-11T20:05:00.005Z","level":"ERROR","module":"myproject.api","request_id":"req_error123","message":"input text is required","extra":{"event":"error_returned","status":400}}
```

The UI or API should not show a Python stack trace. It should return a clear user-facing error.

## How to Verify Logging

1. Start the app.

```bash
docker compose up
```

2. Submit a valid query.

```bash
curl -X POST "http://localhost:8080/api/query" \
  -H "Content-Type: application/json" \
  -d "{\"text\":\"What are the three routing labels in Adaptive RAG?\",\"max_results\":5}"
```

3. Copy the `request_id` from the response.

4. Search logs for that request ID.

```bash
docker compose logs app | grep req_a1b2c3d4
```

PowerShell:

```powershell
docker compose logs app | Select-String "req_a1b2c3d4"
```

5. Confirm the request can be followed from request received to response sent.

## What Full Credit Looks Like

The Logging category should receive full credit if:

1. Logs are JSON.
2. Logs are written to stdout.
3. Every log line has `timestamp`, `level`, `module`, `request_id`, and `message`.
4. A request ID is returned in the API response.
5. The same request ID appears across all components touched by the request.
6. The TA can trace request arrival, classification, routing, retrieval when used, answer generation, and response delivery from logs alone.

## Privacy and Safety

The system should not log:

1. API keys.
2. Secrets.
3. Private environment variables.
4. Credentials.
5. Sensitive user information.

The system may log:

1. Request ID.
2. Text length.
3. Complexity label.
4. Selected strategy.
5. Retrieval step count.
6. Status code.
7. Latency.

The system should avoid logging full user text when possible. For this course project, logging text length and routing metadata is enough for traceability.

## Implementation Location

Logging support is implemented in:

```text
src/myproject/logging_config.py
```

The FastAPI app and routing pipeline should use this logging setup so Docker logs can be inspected during grading.

## Notes

This project uses deterministic local routing and retrieval. The logs are meant to prove that the system is observable and traceable, not to debug a large external model. A clean request trace is enough for the TA to verify that the system behaves like a real deployed application.
