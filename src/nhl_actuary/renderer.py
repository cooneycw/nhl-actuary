"""HTML bracket renderer using Jinja2."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from .models import Bracket

TEMPLATE_DIR = Path(__file__).resolve().parent.parent.parent / "templates"
OUTPUT_DIR = Path(__file__).resolve().parent.parent.parent / "output"


def render_bracket(bracket: Bracket, output_path: Path | None = None) -> Path:
    """Render the bracket to an HTML file.

    Returns the path to the generated file.
    """
    env = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)), autoescape=True)
    template = env.get_template("bracket.html")

    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    html = template.render(
        standings_date=bracket.standings_date,
        generated_at=generated_at,
        west_r1=bracket.western.round1,
        west_r2=bracket.western.round2,
        west_cf=bracket.western.conf_final,
        east_r1=bracket.eastern.round1,
        east_r2=bracket.eastern.round2,
        east_cf=bracket.eastern.conf_final,
        scf=bracket.stanley_cup_final,
    )

    if output_path is None:
        OUTPUT_DIR.mkdir(exist_ok=True)
        output_path = OUTPUT_DIR / "bracket.html"

    output_path.write_text(html, encoding="utf-8")
    return output_path
