.PHONY: help install install-dev test clean lint format run-app run-jupyter docker-build docker-run

# Default target
help:
	@echo "PlotlyVizPro - Available Commands"
	@echo "=================================="
	@echo "make install       - Create venv and install production dependencies"
	@echo "make install-dev   - Install development dependencies (includes testing tools)"
	@echo "make test          - Run test suite with pytest"
	@echo "make test-cov      - Run tests with coverage report"
	@echo "make lint          - Run code quality checks (flake8, black, isort)"
	@echo "make format        - Auto-format code with black and isort"
	@echo "make clean         - Remove cache files and build artifacts"
	@echo "make run-app       - Launch Streamlit app"
	@echo "make run-jupyter   - Launch JupyterLab"
	@echo "make docker-build  - Build Docker image"
	@echo "make docker-run    - Run Docker container"
	@echo "make all           - Install, test, and lint"

# Installation targets
install:
	@echo "Creating virtual environment..."
	python3 -m venv venv
	@echo "Installing production dependencies..."
	./venv/bin/pip install --upgrade pip
	./venv/bin/pip install -r requirements.txt
	@echo "✓ Installation complete! Activate with: source venv/bin/activate"

install-dev: install
	@echo "Installing development dependencies..."
	./venv/bin/pip install -r requirements_dev.txt
	./venv/bin/pip install pytest pytest-cov black flake8 isort mypy pre-commit
	@echo "✓ Development environment ready!"

# Testing targets
test:
	@echo "Running test suite..."
	pytest tests/ -v

test-cov:
	@echo "Running tests with coverage..."
	pytest tests/ -v --cov=utils --cov=pages --cov-report=html --cov-report=term
	@echo "✓ Coverage report generated in htmlcov/"

# Code quality targets
lint:
	@echo "Running code quality checks..."
	@echo "\n→ Checking with flake8..."
	flake8 utils/ pages/ tests/ --max-line-length=120 --exclude=venv,env,.venv
	@echo "\n→ Checking with black..."
	black --check utils/ pages/ tests/
	@echo "\n→ Checking with isort..."
	isort --check-only utils/ pages/ tests/
	@echo "✓ All checks passed!"

format:
	@echo "Auto-formatting code..."
	black utils/ pages/ tests/ generate_datasets.py app.py
	isort utils/ pages/ tests/ generate_datasets.py app.py
	@echo "✓ Code formatted!"

# Cleanup targets
clean:
	@echo "Cleaning up cache files..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ipynb_checkpoints" -exec rm -rf {} + 2>/dev/null || true
	rm -rf htmlcov/ .coverage coverage.xml
	@echo "✓ Cleanup complete!"

# Application targets
run-app:
	@echo "Launching Streamlit app..."
	streamlit run app.py

run-jupyter:
	@echo "Launching JupyterLab..."
	jupyter lab

# Docker targets
docker-build:
	@echo "Building Docker image..."
	docker build -t plotlyvizpro .
	@echo "✓ Docker image built successfully!"

docker-run:
	@echo "Running Docker container..."
	@echo "JupyterLab will be available at http://localhost:8888"
	docker run -p 8888:8888 plotlyvizpro

# Generate datasets
generate-data:
	@echo "Generating synthetic datasets..."
	python generate_datasets.py
	@echo "✓ Datasets generated in datasets/"

# Combined target
all: install-dev test lint
	@echo "✓ All tasks completed successfully!"

# Pre-commit setup
setup-hooks:
	@echo "Setting up pre-commit hooks..."
	pre-commit install
	@echo "✓ Pre-commit hooks installed!"
