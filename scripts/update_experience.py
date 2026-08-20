#!/usr/bin/env python3
"""Update the public experience total in the profile README."""

from datetime import date
from pathlib import Path
import re

README = Path(__file__).resolve().parents[1] / "README.md"
CURRENT_ROLE_START = date(2025, 1, 1)
PRIOR_PROFESSIONAL_MONTHS = 5  # CuraStone, Aug-Dec 2023


def completed_months(start: date, end: date) -> int:
    months = (end.year - start.year) * 12 + end.month - start.month
    if end.day < start.day:
        months -= 1
    return max(months, 0)


total_months = PRIOR_PROFESSIONAL_MONTHS + completed_months(
    CURRENT_ROLE_START, date.today()
)
years, months = divmod(total_months, 12)
label = f"{years} year{'s' if years != 1 else ''}, {months} month{'s' if months != 1 else ''}"

text = README.read_text(encoding="utf-8")
updated, count = re.subn(
    r"(?<=<!-- EXPERIENCE:START -->).*?(?=<!-- EXPERIENCE:END -->)",
    label,
    text,
    count=1,
)

if count != 1:
    raise SystemExit("Experience markers were not found exactly once in README.md")

README.write_text(updated, encoding="utf-8")
