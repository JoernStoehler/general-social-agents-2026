#!/usr/bin/env python3
"""Audit prompt files for ground truth leakage (spoilers).

Checks prompt files for numbers, percentages, and phrases that could leak
human experimental data into prediction prompts — which would contaminate
any evaluation of LLM prediction ability.

Data sources checked:
  - 11-20 game human distribution (Arad & Rubinstein 2012)
  - Charness-Rabin game human proportions (from src/cr_games.py)

Usage:
    python3 src/audit_spoilers.py                      # defaults to prompts/**
    python3 src/audit_spoilers.py prompts/**/*.md
    python3 src/audit_spoilers.py prompts/1120/prompt.md prompts/cr/games.md
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Ground truth data
# ---------------------------------------------------------------------------

# 11-20 game: human distribution from Arad & Rubinstein (2012)
HUMAN_1120: dict[int, float] = {
    11: 0.04,
    12: 0.00,
    13: 0.03,
    14: 0.06,
    15: 0.01,
    16: 0.06,
    17: 0.32,
    18: 0.30,
    19: 0.12,
    20: 0.06,
}

# Charness-Rabin games: human proportions (from cr_games.py)
# Collected as (game_name, human_out, human_enter, human_left, human_right)
CR_HUMAN_PROPORTIONS: list[tuple[str, float, float, float, float]] = [
    ("Barc7", 0.47, 0.53, 0.06, 0.94),
    ("Barc5", 0.39, 0.61, 0.33, 0.67),
    ("Berk28", 0.50, 0.50, 0.34, 0.66),
    ("Berk32", 0.85, 0.15, 0.35, 0.65),
    ("Barc3", 0.74, 0.26, 0.62, 0.38),
    ("Barc4", 0.83, 0.17, 0.62, 0.38),
    ("Berk21", 0.47, 0.53, 0.61, 0.39),
    ("Barc6", 0.92, 0.08, 0.75, 0.25),
    ("Barc9", 0.69, 0.31, 0.94, 0.06),
    ("Berk25", 0.62, 0.38, 0.81, 0.19),
    ("Berk19", 0.56, 0.44, 0.22, 0.78),
    ("Berk14", 0.68, 0.32, 0.45, 0.55),
    ("Barc1", 0.96, 0.04, 0.93, 0.07),
    ("Berk13", 0.86, 0.14, 0.82, 0.18),
    ("Berk18", 0.00, 1.00, 0.44, 0.56),
    ("Barc11", 0.54, 0.46, 0.89, 0.11),
    ("Berk22", 0.39, 0.61, 0.97, 0.03),
    ("Berk27", 0.41, 0.59, 0.91, 0.09),
    ("Berk31", 0.73, 0.27, 0.88, 0.12),
    ("Berk30", 0.77, 0.23, 0.88, 0.12),
]

# ---------------------------------------------------------------------------
# Build lookup sets
# ---------------------------------------------------------------------------

# Collect all distinctive human proportions as decimal strings and percentages.
# Exclude very common values (0.00, 1.00, 0.50) that appear in normal text.
TRIVIAL_PROPORTIONS = {0.00, 1.00, 0.50, 0.25, 0.75}


def _build_suspicious_numbers() -> tuple[set[str], set[str]]:
    """Return (decimal_strings, percentage_strings) of human data values.

    Decimal strings like "0.32", percentage strings like "32%".
    Excludes trivially common values.
    """
    decimals: set[str] = set()
    percentages: set[str] = set()

    # 11-20 game
    for _choice, prob in HUMAN_1120.items():
        if prob not in TRIVIAL_PROPORTIONS:
            decimals.add(f"{prob:.2f}")
            pct = int(round(prob * 100))
            if pct not in (0, 100, 50, 25, 75):
                percentages.add(f"{pct}%")

    # CR games
    for _name, h_out, h_enter, h_left, h_right in CR_HUMAN_PROPORTIONS:
        for val in (h_out, h_enter, h_left, h_right):
            if val not in TRIVIAL_PROPORTIONS:
                decimals.add(f"{val:.2f}")
                pct = int(round(val * 100))
                if pct not in (0, 100, 50, 25, 75):
                    percentages.add(f"{pct}%")

    return decimals, percentages


SUSPICIOUS_DECIMALS, SUSPICIOUS_PERCENTAGES = _build_suspicious_numbers()

# Phrases that, near numbers, suggest ground truth leakage
LEAKAGE_PHRASES = [
    r"in\s+reality",
    r"actual\s+data",
    r"human\s+data\s+shows?",
    r"empirically",
    r"the\s+real\s+proportion",
    r"observed\s+proportion",
    r"observed\s+frequency",
    r"experimental\s+result",
    r"actual\s+distribution",
    r"ground\s+truth",
    r"true\s+distribution",
    r"human\s+subjects?\s+chose",
    r"participants?\s+chose",
    r"human\s+choices?\s+(?:were|was|are|is)",
]

LEAKAGE_RE = re.compile(
    r"|".join(LEAKAGE_PHRASES),
    re.IGNORECASE,
)

# Pattern for the full 11-20 distribution (e.g. {11: 0.04, 12: 0.00, ...})
# Detects a JSON/dict-like structure with at least 3 entries from 11-20 range
DIST_PATTERN = re.compile(
    r"[{\[]\s*"
    r'(?:"?1[1-9]"?\s*[:=]\s*0?\.\d+\s*[,;]\s*){3,}'
)


# ---------------------------------------------------------------------------
# Scanning logic
# ---------------------------------------------------------------------------

@dataclass
class Flag:
    file: str
    line_no: int
    text: str
    reason: str


from dataclasses import dataclass  # noqa: E402 (kept near usage for clarity)


def scan_file(path: Path) -> list[Flag]:
    """Scan a single file for spoiler indicators."""
    flags: list[Flag] = []

    try:
        content = path.read_text(encoding="utf-8", errors="replace")
    except (OSError, UnicodeDecodeError) as exc:
        flags.append(Flag(str(path), 0, "", f"Could not read file: {exc}"))
        return flags

    lines = content.splitlines()

    for line_no_0, line in enumerate(lines):
        line_no = line_no_0 + 1

        # Check 1: Full distribution pattern
        if DIST_PATTERN.search(line):
            flags.append(Flag(
                str(path), line_no, line.strip(),
                "Looks like a full numeric distribution (possible ground truth)",
            ))

        # Check 2: Suspicious decimal proportions
        for dec in SUSPICIOUS_DECIMALS:
            if dec in line:
                flags.append(Flag(
                    str(path), line_no, line.strip(),
                    f"Contains suspicious proportion {dec} matching human data",
                ))

        # Check 3: Suspicious percentages
        for pct in SUSPICIOUS_PERCENTAGES:
            if pct in line:
                flags.append(Flag(
                    str(path), line_no, line.strip(),
                    f"Contains suspicious percentage {pct} matching human data",
                ))

        # Check 4: Leakage phrases near any number
        if LEAKAGE_RE.search(line) and re.search(r"\d", line):
            flags.append(Flag(
                str(path), line_no, line.strip(),
                "Leakage phrase near a number",
            ))

    # Check 5: Multi-line context — leakage phrase within 3 lines of a number
    for line_no_0, line in enumerate(lines):
        if not LEAKAGE_RE.search(line):
            continue
        # Look at surrounding lines for numbers
        start = max(0, line_no_0 - 3)
        end = min(len(lines), line_no_0 + 4)
        context = "\n".join(lines[start:end])
        # Check for suspicious decimals or percentages in context
        for dec in SUSPICIOUS_DECIMALS:
            if dec in context and dec not in line:
                flags.append(Flag(
                    str(path), line_no_0 + 1, line.strip(),
                    f"Leakage phrase within 3 lines of suspicious value {dec}",
                ))
                break
        for pct in SUSPICIOUS_PERCENTAGES:
            if pct in context and pct not in line:
                flags.append(Flag(
                    str(path), line_no_0 + 1, line.strip(),
                    f"Leakage phrase within 3 lines of suspicious value {pct}",
                ))
                break

    return flags


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    # Determine files to scan
    if len(sys.argv) > 1:
        paths = []
        for arg in sys.argv[1:]:
            p = Path(arg)
            if p.is_file():
                paths.append(p)
            elif p.is_dir():
                paths.extend(sorted(p.rglob("*")))
            else:
                # Might be a glob that the shell didn't expand (no matches)
                print(f"Warning: {arg} is not a file or directory, skipping")
        paths = [p for p in paths if p.is_file() and p.suffix in (
            ".md", ".txt", ".json", ".yaml", ".yml", ".py", ".j2", ".jinja",
            ".jinja2", ".tmpl", ".template", ".prompt",
        )]
    else:
        prompts_dir = Path("prompts")
        if not prompts_dir.exists():
            print("Error: prompts/ directory not found and no paths given")
            return 2
        paths = sorted(
            p for p in prompts_dir.rglob("*")
            if p.is_file() and p.name != ".gitkeep"
        )

    if not paths:
        print("No files to scan.")
        return 0

    all_flags: list[Flag] = []
    for path in paths:
        all_flags.extend(scan_file(path))

    # Deduplicate: same file + line + reason
    seen: set[tuple[str, int, str]] = set()
    unique_flags: list[Flag] = []
    for f in all_flags:
        key = (f.file, f.line_no, f.reason)
        if key not in seen:
            seen.add(key)
            unique_flags.append(f)

    # Report
    print(f"Scanned {len(paths)} file(s)")
    if not unique_flags:
        print("CLEAN: No spoiler indicators found.")
        return 0

    print(f"FLAGGED: {len(unique_flags)} potential spoiler(s) found:\n")
    for f in unique_flags:
        loc = f"{f.file}:{f.line_no}" if f.line_no else f.file
        print(f"  {loc}")
        print(f"    Reason: {f.reason}")
        if f.text:
            preview = f.text[:120] + ("..." if len(f.text) > 120 else "")
            print(f"    Text:   {preview}")
        print()

    return 1


if __name__ == "__main__":
    sys.exit(main())
