#!/usr/bin/env python3
"""Update the profile experience from a fixed 2024 baseline."""

from datetime import date
from pathlib import Path
import re

README = Path(__file__).resolve().parents[1] / "README.md"
BASE_YEAR = 2024

today = date.today()
years = max(today.year - BASE_YEAR, 0)
label = f"{years} year{'s' if years != 1 else ''}"

text = README.read_text(encoding="utf-8")
updated, count = re.subn(
    r"(?<=<!-- EXPERIENCE:START -->).*?(?=<!-- EXPERIENCE:END -->)",
    label,
    text,
    count=1,
)
if count != 1:
    raise SystemExit("Experience markers were not found exactly once in README.md")

updated, stamp_count = re.subn(
    r"<!-- EXPERIENCE_UPDATED:\d{4}-\d{2} -->",
    f"<!-- EXPERIENCE_UPDATED:{today:%Y-%m} -->",
    updated,
    count=1,
)
if stamp_count != 1:
    raise SystemExit("Monthly update marker was not found exactly once in README.md")

README.write_text(updated, encoding="utf-8")
