# nhl-actuary

NHL playoff bracket predictor that fetches live standings from the NHL API, applies statistical models to predict every round of the playoffs, and generates a self-contained HTML bracket visualization.

## How It Works

1. **Fetches standings** from the NHL public API (`api-web.nhle.com/v1/standings/now`)
2. **Seeds the bracket** using division winners, wildcards, and conference matchups per NHL playoff format
3. **Predicts outcomes** using the [Log5 method](https://en.wikipedia.org/wiki/Log5) — a formula developed by Bill James for estimating head-to-head win probabilities from each team's overall winning percentage
4. **Renders an HTML bracket** with team logos, records, win probabilities, and connector lines linking rounds

### Statistical Model

- **Per-game probability:** `P(A) = (pA - pA*pB) / (pA + pB - 2*pA*pB)` where pA and pB are regular-season point percentages. The higher seed receives a +1.5% home-ice advantage bonus.
- **Series probability:** Computed via the negative binomial distribution — the probability of reaching exactly 4 wins before the opponent in a best-of-7 format.
- **Series length:** Estimated from the dominance differential — lopsided matchups tend to end in fewer games.

## Quick Start

### Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) package manager

### Generate the Bracket

```bash
# Install dependencies and build
uv sync
uv run python -m nhl_actuary.main

# Or use the Makefile
make build
```

Open `output/bracket.html` in a browser to view the bracket.

## Project Structure

```
nhl-actuary/
├── src/nhl_actuary/
│   ├── api.py          # NHL API client
│   ├── models.py       # Team, Series, Bracket data classes
│   ├── seeding.py      # Playoff seeding logic (divisions, wildcards)
│   ├── predictor.py    # Log5 model + series probability calculations
│   ├── renderer.py     # Jinja2 HTML rendering
│   └── main.py         # Orchestration entry point
├── templates/
│   └── bracket.html    # Jinja2 template with CSS bracket layout
├── output/             # Generated HTML output (git-ignored)
├── tests/              # Pytest test suite
├── Makefile            # Build, lint, test, deploy targets
└── pyproject.toml      # Project config (hatchling build system)
```

## Makefile Targets

| Target | Description |
|--------|-------------|
| `make build` | Fetch standings and generate bracket HTML |
| `make lint` | Run ruff linter and format check |
| `make lint-fix` | Auto-fix lint and formatting issues |
| `make test` | Run pytest suite |
| `make verify` | Full quality check (lint + test) |
| `make deploy` | Verify then build |
| `make clean` | Remove generated files and caches |
| `make troubleshoot` | Clean + lint + test diagnostic pass |

## Development

```bash
# Install with dev dependencies
uv sync --dev

# Run quality checks
make verify

# Fix lint issues
make lint-fix
```

## License

MIT
