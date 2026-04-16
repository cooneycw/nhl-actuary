.PHONY: lint test build clean verify troubleshoot deploy

lint:
	uv run ruff check src/ tests/
	uv run ruff format --check src/ tests/

lint-fix:
	uv run ruff check --fix src/ tests/
	uv run ruff format src/ tests/

test:
	uv run pytest tests/ -v

build:
	uv run python -m nhl_actuary.main

clean:
	rm -rf dist/ build/ *.egg-info/ .pytest_cache/ .ruff_cache/ output/*.html
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true

verify: lint test

troubleshoot: clean lint test

deploy: verify build
