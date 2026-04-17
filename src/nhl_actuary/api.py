"""NHL API client for fetching standings data."""

from __future__ import annotations

import requests

STANDINGS_URL = "https://api-web.nhle.com/v1/standings/now"
USER_AGENT = "nhl-actuary/0.1.0"


def fetch_standings() -> dict:
    """Fetch current NHL standings from the public API.

    Returns the raw JSON response as a dict.
    """
    resp = requests.get(STANDINGS_URL, headers={"User-Agent": USER_AGENT}, timeout=10)
    resp.raise_for_status()
    return resp.json()
