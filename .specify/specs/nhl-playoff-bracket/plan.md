# Implementation Plan: NHL Playoff Bracket Predictor

## Summary
Build a Python pipeline that fetches NHL standings, computes playoff seedings, predicts series outcomes using Log5, and renders an HTML bracket via Jinja2.

## Architecture

```
src/nhl_actuary/
├── main.py          # Entry point - orchestrates the pipeline
├── api.py           # NHL API client - fetch standings
├── seeding.py       # Playoff seeding logic
├── predictor.py     # Log5 prediction model
├── bracket.py       # Bracket structure and advancement
└── renderer.py      # Jinja2 HTML rendering

templates/
└── bracket.html     # Jinja2 template for the bracket

output/
└── bracket.html     # Generated output (gitignored)
```

## Dependencies
| Package | Purpose |
|---------|---------|
| requests | HTTP client for NHL API |
| jinja2 | HTML template rendering |
| pytest | Testing |
| ruff | Linting |

## Phases
| Phase | Tasks | Dependencies |
|-------|-------|--------------|
| 1: Data Layer | API client, standings parser | None |
| 2: Seeding | Playoff qualification + seeding logic | Phase 1 |
| 3: Prediction | Log5 model, series simulation | Phase 2 |
| 4: Bracket | Bracket structure, advancement through rounds | Phase 3 |
| 5: Rendering | HTML template, CSS, output generation | Phase 4 |
| 6: Polish | Team logos, responsive layout, final testing | Phase 5 |
