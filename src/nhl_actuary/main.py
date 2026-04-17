"""Main entry point for the NHL playoff bracket predictor."""

from __future__ import annotations

from .api import fetch_standings
from .predictor import predict_bracket
from .renderer import render_bracket
from .seeding import build_bracket, parse_teams


def main() -> None:
    print("Fetching NHL standings...")
    raw = fetch_standings()
    standings_date = raw.get("standingsDateTimeUtc", "unknown")
    print(f"  Standings date: {standings_date}")

    print("Parsing teams...")
    teams = parse_teams(raw)
    print(f"  {len(teams)} teams loaded")

    print("Building playoff bracket...")
    bracket = build_bracket(teams, standings_date)

    print("Running predictions...")
    predict_bracket(bracket)

    # Print summary
    print("\n--- Predicted Bracket ---")
    for conf_bracket in [bracket.western, bracket.eastern]:
        print(f"\n{conf_bracket.conference} Conference:")
        print("  Round 1:")
        for s in conf_bracket.round1:
            print(
                f"    {s.higher_seed.abbrev} ({s.higher_seed.seed_label}) vs "
                f"{s.lower_seed.abbrev} ({s.lower_seed.seed_label}) -> "
                f"{s.predicted_winner.abbrev} in {s.series_length} "
                f"({s.win_prob:.0%})"
            )
        print("  Round 2:")
        for s in conf_bracket.round2:
            print(
                f"    {s.higher_seed.abbrev} vs {s.lower_seed.abbrev} -> "
                f"{s.predicted_winner.abbrev} in {s.series_length} "
                f"({s.win_prob:.0%})"
            )
        if conf_bracket.conf_final:
            s = conf_bracket.conf_final
            print(
                f"  Conference Final: {s.higher_seed.abbrev} vs {s.lower_seed.abbrev} -> "
                f"{s.predicted_winner.abbrev} in {s.series_length} ({s.win_prob:.0%})"
            )

    if bracket.stanley_cup_final:
        s = bracket.stanley_cup_final
        print(
            f"\nStanley Cup Final: {s.higher_seed.abbrev} vs {s.lower_seed.abbrev} -> "
            f"{s.predicted_winner.abbrev} in {s.series_length} ({s.win_prob:.0%})"
        )
        print(f"\n*** PREDICTED STANLEY CUP CHAMPION: {s.predicted_winner.name} ***")

    print("\nRendering HTML bracket...")
    output_path = render_bracket(bracket)
    print(f"  Bracket saved to: {output_path}")


if __name__ == "__main__":
    main()
