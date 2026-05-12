# Makefile for the CS 6263 final project.
#
# Every target here is referenced by the rubric. The TA runs these targets
# during grading. Do not rename them.
#
# This project is a local Adaptive RAG reproduction. It does not require
# external datasets, external model checkpoints, or paid LLM API keys.

.PHONY: help test test-unit test-integration test-user-stories test-edge \
        lint format reproduce loadtest demo \
        download-data download-models \
        clean preflight regenerate reports

PYTHON ?= python
PIP ?= pip
PYTEST ?= python -m pytest

# Where source lives. The course pins this; do not change.
PACKAGE := myproject
SRC := src/$(PACKAGE)

# ---------------------------------------------------------------------------
help:
	@echo "Common targets:"
	@echo "  make test            run all test suites and write JUnit XML + coverage to reports/"
	@echo "  make lint            run ruff + black --check + mypy"
	@echo "  make format          apply ruff fixes and black formatting in place"
	@echo "  make reproduce       full replay: verify data/models, run demo, run tests"
	@echo "  make loadtest        run the load test against the live app"
	@echo "  make demo            exercise the Adaptive RAG pipeline locally"
	@echo "  make download-data   verify local corpus exists"
	@echo "  make download-models confirm no external model checkpoints are required"
	@echo "  make regenerate      regenerate source from spec via LLM rubric script"
	@echo "  make preflight       run every automated grading check locally"
	@echo "  make clean           remove generated artifacts"

# ---------------------------------------------------------------------------
# Testing
# ---------------------------------------------------------------------------
test: reports
	$(PYTEST) tests/unit --junitxml=reports/unit.xml
	$(PYTEST) tests/integration --junitxml=reports/integration.xml
	$(PYTEST) tests/user_stories --junitxml=reports/user_stories.xml
	$(PYTEST) tests/edge --junitxml=reports/edge.xml
	$(PYTEST) --cov=src/$(PACKAGE) \
	          --cov-report=xml:reports/coverage.xml \
	          --cov-report=html:reports/coverage_html \
	          --cov-fail-under=70 \
	          tests/unit tests/integration tests/user_stories tests/edge

test-unit: reports
	$(PYTEST) tests/unit --junitxml=reports/unit.xml

test-integration: reports
	$(PYTEST) tests/integration --junitxml=reports/integration.xml

test-user-stories: reports
	$(PYTEST) tests/user_stories --junitxml=reports/user_stories.xml

test-edge: reports
	$(PYTEST) tests/edge --junitxml=reports/edge.xml

# ---------------------------------------------------------------------------
# Lint / format / static checks
# ---------------------------------------------------------------------------
lint:
	ruff check $(SRC) tests/
	black --check $(SRC) tests/
	mypy $(SRC)

format:
	ruff check --fix $(SRC) tests/
	black $(SRC) tests/

# ---------------------------------------------------------------------------
# Reproduce: full clean replay
# ---------------------------------------------------------------------------
reproduce: reports
	@echo "[reproduce] starting local Adaptive RAG reproduction"
	$(MAKE) download-data
	$(MAKE) download-models
	$(MAKE) demo
	$(MAKE) test
	@echo "[reproduce] complete. Compare reports/ values to README and docs/REPRODUCE.md."

# ---------------------------------------------------------------------------
# Data and model download
# ---------------------------------------------------------------------------
download-data:
	@echo "[download-data] verifying local corpus"
	$(PYTHON) -c "from pathlib import Path; p=Path('data/corpus.jsonl'); assert p.exists(), 'data/corpus.jsonl is missing'; assert p.stat().st_size > 0, 'data/corpus.jsonl is empty'; print('local corpus found:', p)"

download-models:
	@echo "[download-models] no external model checkpoints required"
	$(PYTHON) -c "print('Rule-based classifier, TF-IDF retriever, and deterministic strategies are local source code.')"

# ---------------------------------------------------------------------------
# Stress and load
# ---------------------------------------------------------------------------
loadtest: reports
	@echo "[loadtest] requires the app to be running with docker compose up"
	locust -f tests/load/locustfile.py \
	  --headless -u 20 -r 5 -t 60s \
	  --host=$${APP_URL:-http://localhost:8080} \
	  --csv=reports/loadtest \
	  || true
	$(PYTHON) -c "import json,csv,pathlib; p=pathlib.Path('reports/loadtest_stats.csv'); rows=list(csv.DictReader(open(p))) if p.exists() else []; pathlib.Path('reports/benchmarks.json').write_text(json.dumps(rows or {'loadtest':'completed_or_skipped'}, indent=2))"

# ---------------------------------------------------------------------------
# Demo and regeneration
# ---------------------------------------------------------------------------
demo:
	$(PYTHON) -m $(PACKAGE).app

regenerate:
	bash scripts/regenerate.sh

preflight:
	bash scripts/preflight.sh

# ---------------------------------------------------------------------------
# Housekeeping
# ---------------------------------------------------------------------------
reports:
	@mkdir -p reports

clean:
	rm -rf reports regenerated .pytest_cache .ruff_cache .mypy_cache
	find . -type d -name __pycache__ -exec rm -rf {} +