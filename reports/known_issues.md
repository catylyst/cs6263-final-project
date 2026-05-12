# Known Issues

## scripts/regenerate.sh requires ANTHROPIC_API_KEY

The Adaptive RAG application does not require Anthropic, OpenAI, HuggingFace, or any paid external LLM API. The project uses local deterministic routing, a local JSONL corpus, TF-IDF retrieval, and deterministic answer strategies.

The course-provided `scripts/regenerate.sh` script requires `ANTHROPIC_API_KEY` for the spec-to-code regeneration check. That key is not committed to the repository and must be provided by the grader, instructor, or local user running the regeneration script.

All application tests, Docker startup, reproduction, and load testing can be run without this key.