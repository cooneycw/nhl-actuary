"""Log5 prediction model for NHL playoff series."""

from __future__ import annotations

import math

from .models import Bracket, ConferenceBracket, Series

HOME_ICE_BONUS = 0.015  # slight boost for higher seed (home ice advantage)


def log5(p_a: float, p_b: float) -> float:
    """Calculate probability that team A beats team B using Log5.

    p_a: team A's point percentage (proxy for win rate)
    p_b: team B's point percentage
    Returns: probability A wins a single game
    """
    if p_a + p_b == 0:
        return 0.5
    denom = p_a + p_b - 2 * p_a * p_b
    if denom == 0:
        return 0.5
    return (p_a - p_a * p_b) / denom


def series_win_probability(game_win_prob: float, wins_needed: int = 4) -> float:
    """Calculate probability of winning a best-of-7 series given per-game win probability.

    Uses the negative binomial distribution:
    P(win series) = sum over i=0..3 of C(3+i, i) * p^4 * (1-p)^i
    """
    p = game_win_prob
    q = 1 - p
    total = 0.0
    for losses in range(wins_needed):
        # Team needs exactly 'wins_needed' wins and 'losses' losses
        # Last game is a win; choose 'losses' from the first (wins_needed-1+losses) games
        n = wins_needed - 1 + losses
        combos = math.comb(n, losses)
        total += combos * (p**wins_needed) * (q**losses)
    return total


def predict_series_length(series_win_prob: float) -> int:
    """Estimate most likely series length based on win probability.

    More lopsided matchups tend to end quicker.
    """
    # Expected series length approximation
    dominance = abs(series_win_prob - 0.5) * 2  # 0 = even, 1 = total mismatch
    if dominance > 0.6:
        return 4
    elif dominance > 0.4:
        return 5
    elif dominance > 0.2:
        return 6
    else:
        return 7


def predict_series(series: Series) -> None:
    """Fill in predictions for a single series."""
    p_a = series.higher_seed.point_pctg + HOME_ICE_BONUS
    p_b = series.lower_seed.point_pctg

    # Clamp to valid range
    p_a = min(max(p_a, 0.01), 0.99)
    p_b = min(max(p_b, 0.01), 0.99)

    game_prob = log5(p_a, p_b)
    series.win_prob = series_win_probability(game_prob)
    series.series_length = predict_series_length(series.win_prob)

    if series.win_prob >= 0.5:
        series.predicted_winner = series.higher_seed
        series.predicted_loser = series.lower_seed
    else:
        series.predicted_winner = series.lower_seed
        series.predicted_loser = series.higher_seed


def advance_conference(conf: ConferenceBracket) -> None:
    """Predict all rounds within a conference."""
    # Round 1
    for s in conf.round1:
        predict_series(s)

    # Round 2: winners of matchups 0+1 play each other, winners of 2+3 play each other
    if len(conf.round1) == 4:
        r2_s1 = Series(
            higher_seed=conf.round1[0].predicted_winner,
            lower_seed=conf.round1[1].predicted_winner,
            round_num=2,
            round_name="Second Round",
        )
        r2_s2 = Series(
            higher_seed=conf.round1[2].predicted_winner,
            lower_seed=conf.round1[3].predicted_winner,
            round_num=2,
            round_name="Second Round",
        )
        predict_series(r2_s1)
        predict_series(r2_s2)
        conf.round2 = [r2_s1, r2_s2]

        # Conference Final
        conf.conf_final = Series(
            higher_seed=r2_s1.predicted_winner,
            lower_seed=r2_s2.predicted_winner,
            round_num=3,
            round_name="Conference Final",
        )
        predict_series(conf.conf_final)


def predict_bracket(bracket: Bracket) -> None:
    """Run predictions through the entire bracket."""
    advance_conference(bracket.eastern)
    advance_conference(bracket.western)

    # Stanley Cup Final
    if bracket.eastern.conf_final and bracket.western.conf_final:
        east_champ = bracket.eastern.conf_final.predicted_winner
        west_champ = bracket.western.conf_final.predicted_winner
        # Higher point team gets home ice in the final
        if east_champ.points >= west_champ.points:
            higher, lower = east_champ, west_champ
        else:
            higher, lower = west_champ, east_champ
        bracket.stanley_cup_final = Series(
            higher_seed=higher,
            lower_seed=lower,
            round_num=4,
            round_name="Stanley Cup Final",
        )
        predict_series(bracket.stanley_cup_final)
