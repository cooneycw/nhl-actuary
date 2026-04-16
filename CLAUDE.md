# nhl-actuary

## Overview

NHL playoff bracket predictor. Fetches current season standings from the NHL API, applies statistical models to predict playoff outcomes, and generates an HTML bracket visualization.

## Key Conventions

- Python project using uv for dependency management
- Source code in `src/nhl_actuary/`
- HTML templates in `templates/`
- Generated output in `output/`
- Uses NHL public API for data

## CI/CD Protocol

- Use Makefile targets for all build, test, and deploy operations
- Never run raw build commands - use `make lint`, `make test`, `make build`, `make deploy`
- The Makefile is the single source of truth for project commands
- If a Makefile target is missing for your operation, ADD the target rather than running raw commands

## Troubleshooting Protocol

- Before debugging manually, run `make lint` and `make test` to surface known issues
- When fixing errors, fix BOTH the application code AND the CI/CD process
- After any fix, verify through the full pipeline: `make verify`
- Never bypass quality gates - if `make lint` or `make test` fails, fix the root cause
- Use `make troubleshoot` for a single-command diagnostic pass

## Quality Gates

| Target | Purpose | When to Run |
|--------|---------|-------------|
| `make lint` | Run ruff linter | Before every commit |
| `make test` | Run pytest | Before every commit |
| `make verify` | Full check (lint + test) | Before deployment |
| `make build` | Generate HTML bracket | To produce output |
