.PHONY: install dev run test clean help

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies
	uv sync

dev: ## Run development server
	uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

run: ## Run production server
	uv run uvicorn app.main:app --host 0.0.0.0 --port 8000

test: ## Run tests
	uv run pytest -svx .

test-coverage: ## Run tests with coverage
	uv run pytest -svx . --cov=app --cov-report=html

clean: ## Clean cache and temporary files
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache
	rm -rf htmlcov

lint: ## Run code linting
	uv run ruff check app/
	uv run ruff format --check app/

format: ## Format code
	uv run ruff format app/

check: ## Run all checks (lint, format, test)
	make lint
	make test