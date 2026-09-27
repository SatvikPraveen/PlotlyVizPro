.DEFAULT_GOAL := help
PY ?= .venv/bin/python
PIP ?= .venv/bin/pip

.PHONY: help venv install install-dev test test-fast test-notebooks coverage lint format typecheck check bench \
        docs docs-serve run-app run-jupyter generate-data verify-data demo docker-build docker-run clean

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-16s\033[0m %s\n", $$1, $$2}'

venv: ## Create a virtual environment in .venv
	python3 -m venv .venv && $(PIP) install --upgrade pip

install: venv ## Install the package with runtime extras
	$(PIP) install -e ".[all]"

install-dev: venv ## Install the package with development and docs extras
	$(PIP) install -e ".[dev,docs,notebooks]"
	.venv/bin/pre-commit install

test: ## Run the test suite (excludes notebook execution)
	$(PY) -m pytest -m "not notebook"

test-fast: ## Run tests excluding slow, kaleido and notebook markers
	$(PY) -m pytest -m "not notebook and not slow and not kaleido" -x -q

test-notebooks: ## Execute every notebook end-to-end
	$(PY) -m pytest -m notebook -q

coverage: ## Run tests with the coverage gate and an HTML report
	$(PY) -m pytest -m "not notebook" --cov --cov-report=html --cov-report=term-missing

lint: ## Ruff lint + format check
	.venv/bin/ruff check . && .venv/bin/ruff format --check .

format: ## Auto-fix lint findings and format
	.venv/bin/ruff check --fix . && .venv/bin/ruff format .

typecheck: ## mypy in strict mode
	.venv/bin/mypy

check: lint typecheck test ## Everything CI runs

bench: ## Run micro-benchmarks
	$(PY) -m pytest benchmarks/ --benchmark-only --benchmark-sort=mean

docs: ## Build the documentation site
	.venv/bin/mkdocs build --strict

docs-serve: ## Serve docs locally with live reload
	.venv/bin/mkdocs serve

run-app: ## Launch the Streamlit gallery
	.venv/bin/streamlit run app.py

run-jupyter: ## Launch JupyterLab
	.venv/bin/jupyter lab

generate-data: ## Regenerate synthetic datasets and manifest
	.venv/bin/plotlyvizpro generate-data

verify-data: ## Verify dataset checksums against the manifest
	.venv/bin/plotlyvizpro verify-data

demo: ## Render the showcase figure into exports/
	.venv/bin/plotlyvizpro demo --formats html,json,png

docker-build: ## Build the Docker image
	docker build -t plotlyvizpro .

docker-run: ## Run JupyterLab from the image on :8888
	docker run --rm -p 8888:8888 -p 8501:8501 plotlyvizpro

clean: ## Remove caches and build artefacts
	rm -rf build dist *.egg-info .pytest_cache .mypy_cache .ruff_cache .hypothesis htmlcov .coverage coverage.xml site
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
	find . -type d -name .ipynb_checkpoints -prune -exec rm -rf {} +
