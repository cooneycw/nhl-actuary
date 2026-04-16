# Project Constitution

> Governing principles for nhl-actuary.
> All specifications and implementations must align with these principles.

---

## Core Principles

### P1: Data-Driven Predictions

All playoff predictions must be grounded in real NHL statistics from the current season. No hardcoded picks or subjective bias. The model's inputs and methodology must be transparent and auditable.

### P2: Self-Contained Output

The HTML bracket output must be a single, self-contained file that can be opened in any modern browser without a web server. All CSS and JS inline. No external dependencies at runtime.

### P3: Reproducible Results

Given the same input data (standings snapshot), the model must produce the same predictions. Stochastic elements (if any) must use a fixed seed by default.

---

## Development Workflow

1. Write specification before code
2. Review spec for completeness
3. Create technical plan
4. Break into tasks
5. Sync tasks to issues
6. Implement with tests

---

*Created: 2026-04-16*
