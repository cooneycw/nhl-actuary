"""Data models for NHL teams and series."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Team:
    name: str
    abbrev: str
    conference: str
    division: str
    points: int
    wins: int
    losses: int
    ot_losses: int
    games_played: int
    goal_differential: int
    regulation_wins: int
    regulation_plus_ot_wins: int
    point_pctg: float
    logo_url: str
    clinch_indicator: str = ""
    division_sequence: int = 0
    wildcard_sequence: int = 0
    conference_sequence: int = 0
    seed: int = 0
    seed_label: str = ""

    @property
    def record(self) -> str:
        return f"{self.wins}-{self.losses}-{self.ot_losses}"

    @classmethod
    def from_api(cls, data: dict) -> Team:
        return cls(
            name=data["teamName"]["default"],
            abbrev=data["teamAbbrev"]["default"],
            conference=data["conferenceName"],
            division=data["divisionName"],
            points=data["points"],
            wins=data["wins"],
            losses=data["losses"],
            ot_losses=data["otLosses"],
            games_played=data["gamesPlayed"],
            goal_differential=data["goalDifferential"],
            regulation_wins=data["regulationWins"],
            regulation_plus_ot_wins=data["regulationPlusOtWins"],
            point_pctg=data["pointPctg"],
            logo_url=data["teamLogo"],
            clinch_indicator=data.get("clinchIndicator", ""),
            division_sequence=data.get("divisionSequence", 0),
            wildcard_sequence=data.get("wildcardSequence", 0),
            conference_sequence=data.get("conferenceSequence", 0),
        )


@dataclass
class Series:
    higher_seed: Team
    lower_seed: Team
    win_prob: float = 0.0  # probability higher_seed wins
    predicted_winner: Team | None = None
    predicted_loser: Team | None = None
    series_length: int = 0
    round_num: int = 0
    round_name: str = ""


@dataclass
class ConferenceBracket:
    conference: str
    round1: list[Series] = field(default_factory=list)
    round2: list[Series] = field(default_factory=list)
    conf_final: Series | None = None


@dataclass
class Bracket:
    eastern: ConferenceBracket = field(default_factory=lambda: ConferenceBracket("Eastern"))
    western: ConferenceBracket = field(default_factory=lambda: ConferenceBracket("Western"))
    stanley_cup_final: Series | None = None
    standings_date: str = ""
