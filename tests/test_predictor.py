"""Tests for the prediction model."""

from nhl_actuary.predictor import log5, predict_series_length, series_win_probability


def test_log5_equal_teams():
    """Equal teams should have 50/50 probability."""
    assert abs(log5(0.5, 0.5) - 0.5) < 0.001


def test_log5_stronger_team():
    """Better team should have > 50% probability."""
    p = log5(0.7, 0.5)
    assert p > 0.5


def test_log5_weaker_team():
    """Worse team should have < 50% probability."""
    p = log5(0.4, 0.6)
    assert p < 0.5


def test_log5_extreme():
    """Very dominant team should have high probability."""
    p = log5(0.9, 0.3)
    assert p > 0.8


def test_series_win_probability_even():
    """Even matchup should be close to 50%."""
    p = series_win_probability(0.5)
    assert abs(p - 0.5) < 0.01


def test_series_win_probability_favorite():
    """Favorite should have series advantage greater than game advantage."""
    game_prob = 0.6
    series_prob = series_win_probability(game_prob)
    assert series_prob > game_prob


def test_series_win_probability_sum():
    """P(A wins series) + P(B wins series) should equal 1."""
    p = 0.6
    assert abs(series_win_probability(p) + series_win_probability(1 - p) - 1.0) < 0.001


def test_predict_series_length_lopsided():
    """Lopsided matchups should end faster."""
    assert predict_series_length(0.95) <= predict_series_length(0.55)


def test_predict_series_length_range():
    """Series length should be between 4 and 7."""
    for prob in [0.1, 0.3, 0.5, 0.7, 0.9]:
        length = predict_series_length(prob)
        assert 4 <= length <= 7
