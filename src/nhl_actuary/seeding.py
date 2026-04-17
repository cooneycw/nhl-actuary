"""NHL playoff seeding logic.

NHL Playoff Format:
- 16 teams qualify (8 per conference)
- Top 3 from each division qualify automatically
- 2 wild card spots per conference go to next-best teams regardless of division
- Seeding within conference:
  - A1: Division winner with more points
  - A2: Other division winner
  - A1 vs WC2 (lower wild card)
  - A2 vs WC1 (higher wild card)
  - 2nd vs 3rd in A1's division
  - 2nd vs 3rd in A2's division
"""

from __future__ import annotations

from .models import Bracket, ConferenceBracket, Series, Team


def parse_teams(raw_standings: dict) -> list[Team]:
    """Parse API response into Team objects."""
    return [Team.from_api(t) for t in raw_standings["standings"]]


def _sort_key(team: Team) -> tuple:
    """Sort teams by points desc, regulation wins desc, regulation+OT wins desc, goal diff desc."""
    return (
        -team.points,
        -team.regulation_wins,
        -team.regulation_plus_ot_wins,
        -team.goal_differential,
    )


def seed_conference(teams: list[Team], conference: str) -> ConferenceBracket:
    """Determine seeding and first-round matchups for one conference.

    Returns a ConferenceBracket with round1 matchups populated.
    """
    conf_teams = [t for t in teams if t.conference == conference]

    # Get divisions in this conference
    divisions = sorted(set(t.division for t in conf_teams))
    assert len(divisions) == 2, f"Expected 2 divisions in {conference}, got {divisions}"

    # Top 3 from each division
    div_teams: dict[str, list[Team]] = {}
    for div in divisions:
        div_sorted = sorted([t for t in conf_teams if t.division == div], key=_sort_key)
        div_teams[div] = div_sorted

    # Division winners
    div_winners = {div: div_sorted[0] for div, div_sorted in div_teams.items()}

    # Determine A1 (better division winner) and A2
    winners_sorted = sorted(div_winners.values(), key=_sort_key)
    a1_team = winners_sorted[0]
    a2_team = winners_sorted[1]
    a1_div = a1_team.division
    a2_div = a2_team.division

    # Division qualifiers (2nd and 3rd in each division)
    div_qualifiers: dict[str, list[Team]] = {}
    for div in divisions:
        div_qualifiers[div] = div_teams[div][1:3]  # 2nd and 3rd place

    # Wild cards: remaining teams in conference sorted by points, take top 2
    qualified_so_far = {a1_team.abbrev, a2_team.abbrev}
    for div in divisions:
        for t in div_qualifiers[div]:
            qualified_so_far.add(t.abbrev)

    remaining = sorted(
        [t for t in conf_teams if t.abbrev not in qualified_so_far],
        key=_sort_key,
    )
    wc1 = remaining[0] if len(remaining) >= 1 else None
    wc2 = remaining[1] if len(remaining) >= 2 else None

    # Assign seeds
    a1_team.seed = 1
    a1_team.seed_label = f"{a1_div[0]}1"
    a2_team.seed = 2
    a2_team.seed_label = f"{a2_div[0]}2"

    for i, t in enumerate(div_qualifiers[a1_div]):
        t.seed = i + 2  # 2nd, 3rd in A1's division
        t.seed_label = f"{a1_div[0]}{i + 2}"
    for i, t in enumerate(div_qualifiers[a2_div]):
        t.seed = i + 2
        t.seed_label = f"{a2_div[0]}{i + 2}"

    if wc1:
        wc1.seed = 7
        wc1.seed_label = "WC1"
    if wc2:
        wc2.seed = 8
        wc2.seed_label = "WC2"

    # Build first-round matchups:
    # A1 vs WC2
    # A1's div 2nd vs A1's div 3rd
    # A2 vs WC1
    # A2's div 2nd vs A2's div 3rd
    round1 = []

    # Matchup 1: A1 vs WC2
    if wc2:
        round1.append(
            Series(
                higher_seed=a1_team,
                lower_seed=wc2,
                round_num=1,
                round_name="First Round",
            )
        )

    # Matchup 2: A1 div 2nd vs A1 div 3rd
    if len(div_qualifiers[a1_div]) >= 2:
        round1.append(
            Series(
                higher_seed=div_qualifiers[a1_div][0],
                lower_seed=div_qualifiers[a1_div][1],
                round_num=1,
                round_name="First Round",
            )
        )

    # Matchup 3: A2 vs WC1
    if wc1:
        round1.append(
            Series(
                higher_seed=a2_team,
                lower_seed=wc1,
                round_num=1,
                round_name="First Round",
            )
        )

    # Matchup 4: A2 div 2nd vs A2 div 3rd
    if len(div_qualifiers[a2_div]) >= 2:
        round1.append(
            Series(
                higher_seed=div_qualifiers[a2_div][0],
                lower_seed=div_qualifiers[a2_div][1],
                round_num=1,
                round_name="First Round",
            )
        )

    bracket = ConferenceBracket(conference=conference, round1=round1)
    return bracket


def build_bracket(teams: list[Team], standings_date: str) -> Bracket:
    """Build the full playoff bracket with seedings."""
    bracket = Bracket(standings_date=standings_date)
    bracket.eastern = seed_conference(teams, "Eastern")
    bracket.western = seed_conference(teams, "Western")
    return bracket
