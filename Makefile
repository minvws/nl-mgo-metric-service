.SILENT: help
all: help

lint: ## Check for linting errors
	uv run ruff check

lint-fix: ## Fix linting errors
	uv run ruff check --fix --show-fixes

format: ## Format code
	uv run ruff format

format-diff: ## Show formatting differences
	uv run ruff format --diff

type-check: ## Check for typing errors
	uv run mypy

test: ## Runs automated tests with code coverage and exports a code coverage report to an XML file
	uv run pytest --cov --cov-fail-under=100 --cov-branch --cov-report=xml

check: lint format-diff type-check test ## Runs all checks
fix: lint-fix format ## Runs all fixers

help: ## Display available commands
	echo "Available make commands:"
	echo
	grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m  %-30s\033[0m %s\n", $$1, $$2}'
