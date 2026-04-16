# Feature Specification: NHL Playoff Bracket Predictor

## Overview

Fetch current NHL standings from the public NHL API, determine playoff seedings, apply a statistical model to predict series outcomes through all four rounds, and render the complete bracket as a self-contained HTML file.

## User Stories

### US1: View Predicted Bracket
**As a** hockey fan, **I want** to see a complete predicted NHL playoff bracket, **So that** I can see which teams are likely to advance in each round.

**Acceptance Criteria:**
- [ ] Bracket shows all 16 playoff teams correctly seeded
- [ ] Each matchup shows the predicted winner and series length
- [ ] Win probability is displayed for each series
- [ ] Bracket advances winners through all 4 rounds to a Stanley Cup champion
- [ ] Output is a single HTML file viewable in any browser

### US2: Data Freshness
**As a** user, **I want** the bracket to use current season standings, **So that** predictions reflect the latest results.

**Acceptance Criteria:**
- [ ] Standings are fetched from the NHL API at runtime
- [ ] The date/time of the data fetch is displayed on the bracket
- [ ] If the regular season is incomplete, remaining games are noted

### US3: Prediction Transparency
**As a** user, **I want** to understand why a team is predicted to win, **So that** I can evaluate the prediction quality.

**Acceptance Criteria:**
- [ ] Each team's key stats (points, goal differential, record) are shown
- [ ] The prediction methodology is briefly explained on the page
- [ ] Win probabilities are shown as percentages

## Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| R1 | Fetch 2025-26 NHL standings from api-web.nhle.com | Must |
| R2 | Correctly determine 16 playoff teams with proper seeding | Must |
| R3 | Apply probability model based on regular season performance | Must |
| R4 | Predict series winners and lengths for all 4 rounds | Must |
| R5 | Generate single self-contained HTML bracket file | Must |
| R6 | Display team names, seeds, records, and logos | Must |
| R7 | Show win probabilities and predicted series lengths | Must |
| R8 | Include generation timestamp and data source | Should |
| R9 | Responsive layout for desktop and mobile | Should |
| R10 | Team color theming in the bracket | Could |

## Technical Design

### Data Source
- NHL API: `https://api-web.nhle.com/v1/standings/now`
- No authentication required
- Returns current standings with points, wins, losses, OTL, goal differential, etc.

### Playoff Seeding Rules (NHL Format)
- 16 teams qualify (8 per conference)
- Top 3 from each division qualify (12 teams)
- 2 wild card spots per conference (4 teams)
- Division winners are seeds 1-2 (by points)
- Division runners-up are seeds 3-4 (by points, but stay in their division matchup? No - they are re-seeded)
- Actually: Division winners get top 2 seeds. Remaining 6 teams are seeded 3-8 by points. But bracket is: 1v8/WC2, 2v7/WC1, 3v6, 4v5 — NO. Let me be precise:

**Correct NHL Playoff Format:**
- Each conference: 2 division winners get seeds A1, A2 (by points)
- Remaining 6 playoff teams (3rd in each division + 2 wild cards) are NOT traditionally seeded 3-8
- Instead: Top wild card plays A1's division runner-up path, second wild card plays A2's division
- Actually the bracket is: A1 vs WC2, A2 vs WC1, then the remaining division matchups are 2nd vs 3rd within each division
- **Simplified:** Division winners play wild cards. 2nd and 3rd place in each division play each other.

### Prediction Model (MVP)
- **Log5 method**: P(A beats B) = (pA - pA*pB) / (pA + pB - 2*pA*pB) where pA, pB are regular season point percentages
- **Series length**: Based on win probability — closer matchups go longer
- **Home ice**: Higher seed gets home ice (slight boost factored into point %)

### HTML Output
- Single file with inline CSS/JS
- Visual bracket layout (left conference flows right, right conference flows left, meeting in center)
- Team names, seeds, records, win probabilities
- Team logo URLs from NHL CDN
- Dark theme for readability
- Timestamp of generation

## Success Criteria
- [ ] All acceptance criteria met across all user stories
- [ ] Tests passing for seeding logic, prediction model, and HTML generation
- [ ] HTML output renders correctly in Chrome, Firefox, Safari
- [ ] Predictions are reproducible given same standings data
