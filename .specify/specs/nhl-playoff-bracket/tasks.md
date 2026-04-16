# Tasks: NHL Playoff Bracket Predictor

## Format
`[ID] [P?] [Story] Description`

## Wave 1: Data Layer
- [ ] **T001** [P1] [US2] Build NHL API client to fetch current standings from api-web.nhle.com
- [ ] **T002** [P1] [US2] Parse standings response into structured Team dataclass (name, abbrev, conference, division, points, wins, losses, otl, goal_diff, games_played)

## Wave 2: Seeding Logic
- [ ] **T003** [P1] [US1] Implement playoff qualification logic (top 3 per division + 2 wild cards per conference)
- [ ] **T004** [P1] [US1] Implement correct NHL playoff seeding and bracket placement (division winners vs wild cards, division 2nd vs 3rd)

## Wave 3: Prediction Model
- [ ] **T005** [P1] [US3] Implement Log5 prediction model for series win probability
- [ ] **T006** [P1] [US1] Predict series length based on win probability differential
- [ ] **T007** [P1] [US1] Build bracket advancement logic through all 4 rounds

## Wave 4: HTML Rendering
- [ ] **T008** [P1] [US1] Create Jinja2 HTML bracket template with inline CSS
- [ ] **T009** [P1] [US1] Implement renderer to populate template with bracket data
- [ ] **T010** [P2] [US1] Add team logos from NHL CDN
- [ ] **T011** [P2] [US3] Add methodology explanation section to HTML output

## Wave 5: Main Pipeline & Polish
- [ ] **T012** [P1] [US1] Create main.py entry point that orchestrates full pipeline
- [ ] **T013** [P2] [US2] Add generation timestamp and data freshness indicator
- [ ] **T014** [P2] [US1] Responsive CSS for mobile viewing

## Issue Sync
| Task | Issue | Status |
|------|-------|--------|
