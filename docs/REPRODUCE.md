# Reproducibility Procedure

> The TA runs `make reproduce` to verify the project can be rebuilt and tested from a clean checkout. This document tells the TA what to expect. The project is designed to run locally without paid API keys, external LLM calls, downloaded model checkpoints, or external dataset downloads.

## Procedure

```bash
# From a fresh clone with .env populated
make reproduce
```

`make reproduce` performs these steps in order:

1. `make download-data` confirms the local corpus listed in `docs/DATA.md` exists.
2. `make download-models` confirms no external model checkpoints are required.
3. Runs the application pipeline on sample Adaptive RAG questions.
4. Runs `make test` for unit, integration, user story, and edge tests.
5. Reports pass or fail per phase.
6. Regenerates reports under `reports/`.

## Hardware Profile

The headline numbers were measured on a standard local development machine.

Expected minimum hardware:

- CPU: Intel or AMD x86_64, 2 cores or higher
- Memory: 4 GB or higher
- Disk: 1 GB free
- Network: only required to clone the repository
- GPU: not required

The system does not require CUDA, GPU acceleration, or external model hosting.

## Software Profile

Expected software:

| Tool | Version |
|---|---|
| Python | 3.11 |
| Docker | Recent stable version |
| Docker Compose | Recent stable version |
| Git | Recent stable version |
| Operating system | Windows, macOS, or Linux |

## Expected Wall Clock

- Total `make reproduce` runtime: under 10 minutes on the documented hardware
- `docker compose up` to healthy: under 10 minutes
- Data download: no external download required
- Model download: no external download required
- Test suite: under 5 minutes

## Expected Outputs

After `make reproduce` completes, the following files should exist:

- `reports/unit.xml` — unit test results
- `reports/integration.xml` — integration test results
- `reports/user_stories.xml` — user story acceptance test results
- `reports/edge.xml` — edge case test results
- `reports/coverage.xml` — coverage report
- `reports/coverage_html/index.html` — coverage browser
- `reports/benchmarks.json` — benchmark timing and request summary, if benchmark target is run

## Expected Metric Values

These are the headline numbers reported in `README.md`. Because this project is deterministic and local, the TA's reproduction should match within the stated tolerance.

| Metric | Expected | Tolerance | Where measured |
|---|---:|---:|---|
| User story pass rate | 1.00 | ± 0.00 | `reports/user_stories.xml` |
| Route accuracy on local evaluation set | 0.85 | ± 0.05 | `reports/eval.json` |
| Citation present rate | 0.90 | ± 0.05 | `reports/eval.json` |
| Average adaptive retrieval steps | 1.20 | ± 0.30 | `reports/eval.json` |
| Average API latency | 250 ms | ± 100 ms | `reports/benchmarks.json` |

These metrics are intentionally lightweight because the project is a small deterministic reproduction and does not run the full benchmark datasets from the Adaptive-RAG paper.

## Expected Routing Behavior

The following examples should reproduce consistently:

| Question | Expected label | Expected strategy | Retrieval steps |
|---|---|---|---:|
| `What is Adaptive RAG?` | `A` | `no_retrieval` | 0 |
| `What are the three routing labels in Adaptive RAG?` | `B` | `single_step` | 1 |
| `How does Adaptive RAG balance accuracy and efficiency compared to always using multi-step retrieval?` | `C` | `multi_step` | 2 |
| `What is the maintenance schedule for the Mars colony water pump?` | `B` or `C` | retrieval strategy | safe fallback |

## Manual Reproduction Steps

If `make reproduce` is not available in the local shell, the same process can be run manually.

### 1. Clone the repository

```bash
git clone https://github.com/catylyst/cs6263-final-project.git
cd cs6263-final-project
```

### 2. Create environment file

```bash
cp .env.example .env
```

No paid API key is required.

### 3. Create and activate a Python environment

On macOS or Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

### 4. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -e ".[dev]"
```

If editable install is not available, install from requirements:

```bash
pip install -r requirements.txt
```

### 5. Run unit tests

```bash
python -m pytest tests/unit
```

### 6. Run integration tests

```bash
python -m pytest tests/integration
```

### 7. Run user story tests

```bash
python -m pytest tests/user_stories
```

### 8. Run edge case tests

```bash
python -m pytest tests/edge
```

### 9. Run all tests together

```bash
python -m pytest tests/unit tests/integration tests/user_stories tests/edge
```

### 10. Run the application locally

```bash
uvicorn myproject.api:app --host 0.0.0.0 --port 8080
```

The application should be available at:

```text
http://localhost:8080
```

The health endpoint should be available at:

```text
http://localhost:8080/health
```

The query endpoint is:

```text
POST /api/query
```

## Docker Reproduction

From a clean clone:

```bash
cp .env.example .env
docker compose up
```

The service should become available at:

```text
http://localhost:8080
```

Expected startup time:

```text
under 10 minutes
```

## Data Reproducibility

The project uses one local corpus:

```text
data/corpus.jsonl
```

No external data download is required.

The corpus should contain original project-authored summaries about Adaptive RAG, routing labels, retrieval strategies, fallback behavior, and response metadata.

## Model Reproducibility

No external model checkpoint is required.

The project uses:

1. Rule-based query complexity classifier.
2. TF-IDF retriever built from `data/corpus.jsonl`.
3. Deterministic answer strategies.

The following files define the model behavior:

```text
src/myproject/classifier.py
src/myproject/retriever.py
src/myproject/strategies.py
```

## Known Reproduction Notes

On Windows PowerShell, use:

```powershell
python -m pytest
```

instead of:

```powershell
pytest
```

This ensures that Pytest runs from the active Python environment.

If Python cannot find the `myproject` package, confirm that `pytest.ini` contains:

```ini
[pytest]
pythonpath = src
markers =
    user_story(id): marks tests as user story acceptance tests
testpaths =
    tests
```

## Outside Tolerance?

If a metric drifts outside the documented tolerance:

- The Reproducibility test row may receive partial credit instead of full credit.
- The team should investigate and document the cause in `reports/known_issues.md` if the deadline has not passed.
- Because this project is deterministic, large drift usually indicates a changed corpus, changed classifier rule, changed dependency version, or changed test environment.

## Reproduction Success Criteria

Reproduction is successful when:

1. The application starts.
2. `/health` returns `{"status": "healthy"}`.
3. The local corpus loads.
4. All tests pass.
5. The expected routing behavior matches the table above.
6. The system returns citations for retrieval-based questions.
7. The system returns a safe fallback for unsupported questions.
