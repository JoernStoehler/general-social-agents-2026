#!/usr/bin/env python3
"""Evaluate Charness-Rabin game predictions against human data.

Reads a JSON file of model predictions and computes per-game and aggregate
metrics (MAE, KL divergence, Pearson r) for both Player A and Player B.

Usage:
    python3 scripts/eval_cr.py results/runs/cr_pergame/combined.json
    python3 scripts/eval_cr.py results/runs/20260320_101421/output.txt
"""

import argparse
import json
import math
import sys
from pathlib import Path

# Human data from Charness & Rabin (2002), via Manning & Horton (2026) Table D2.
# Each entry: game name, P(A chooses Out), P(B chooses Left).
HUMAN_DATA = [
    {"game": "Barc7",  "human_out": 0.47, "human_left": 0.06},
    {"game": "Barc5",  "human_out": 0.39, "human_left": 0.33},
    {"game": "Berk28", "human_out": 0.50, "human_left": 0.34},
    {"game": "Berk32", "human_out": 0.85, "human_left": 0.35},
    {"game": "Barc3",  "human_out": 0.74, "human_left": 0.62},
    {"game": "Barc4",  "human_out": 0.83, "human_left": 0.62},
    {"game": "Berk21", "human_out": 0.47, "human_left": 0.61},
    {"game": "Barc6",  "human_out": 0.92, "human_left": 0.75},
    {"game": "Barc9",  "human_out": 0.69, "human_left": 0.94},
    {"game": "Berk25", "human_out": 0.62, "human_left": 0.81},
    {"game": "Berk19", "human_out": 0.56, "human_left": 0.22},
    {"game": "Berk14", "human_out": 0.68, "human_left": 0.45},
    {"game": "Barc1",  "human_out": 0.96, "human_left": 0.93},
    {"game": "Berk13", "human_out": 0.86, "human_left": 0.82},
    {"game": "Berk18", "human_out": 0.00, "human_left": 0.44},
    {"game": "Barc11", "human_out": 0.54, "human_left": 0.89},
    {"game": "Berk22", "human_out": 0.39, "human_left": 0.97},
    {"game": "Berk27", "human_out": 0.41, "human_left": 0.91},
    {"game": "Berk31", "human_out": 0.73, "human_left": 0.88},
    {"game": "Berk30", "human_out": 0.77, "human_left": 0.88},
]


def kl_binary(p_human: float, p_pred: float) -> float:
    """KL divergence D_KL(human || pred) for a binary distribution."""
    eps = 1e-10
    p, q = p_human, max(min(p_pred, 1 - eps), eps)
    kl = 0.0
    if p > eps:
        kl += p * math.log(p / q)
    if (1 - p) > eps:
        kl += (1 - p) * math.log((1 - p) / (1 - q))
    return kl


def pearson_r(x: list[float], y: list[float]) -> float:
    """Pearson correlation coefficient between two equal-length sequences."""
    n = len(x)
    mx, my = sum(x) / n, sum(y) / n
    cov = sum((a - mx) * (b - my) for a, b in zip(x, y)) / n
    sx = (sum((a - mx) ** 2 for a in x) / n) ** 0.5
    sy = (sum((b - my) ** 2 for b in y) / n) ** 0.5
    return cov / (sx * sy) if sx > 0 and sy > 0 else 0.0


def eval_cr(predictions: list[dict]) -> dict:
    """Evaluate CR game predictions against human data.

    Args:
        predictions: List of dicts with keys "game", "out", "left".

    Returns:
        Summary dict with per-player MAE, mean KL, and Pearson r.
    """
    pred_by_name = {p["game"]: p for p in predictions}

    a_errors: list[float] = []
    b_errors: list[float] = []
    a_kls: list[float] = []
    b_kls: list[float] = []
    a_human: list[float] = []
    a_pred: list[float] = []
    b_human: list[float] = []
    b_pred: list[float] = []

    header = (
        f"{'Game':<8} {'A_hum':>5} {'A_pred':>6} {'A_err':>6} {'A_KL':>6}"
        f" | {'B_hum':>5} {'B_pred':>6} {'B_err':>6} {'B_KL':>6}"
    )
    print(header)
    print("-" * 75)

    for h in HUMAN_DATA:
        name = h["game"]
        p = pred_by_name.get(name)
        if not p:
            print(f"  Missing: {name}")
            continue

        p_out = p.get("out", 0.5)
        p_left = p.get("left", 0.5)

        a_err = abs(h["human_out"] - p_out)
        b_err = abs(h["human_left"] - p_left)
        a_kl = kl_binary(h["human_out"], p_out)
        b_kl = kl_binary(h["human_left"], p_left)

        a_errors.append(a_err)
        b_errors.append(b_err)
        a_kls.append(a_kl)
        b_kls.append(b_kl)
        a_human.append(h["human_out"])
        a_pred.append(p_out)
        b_human.append(h["human_left"])
        b_pred.append(p_left)

        print(
            f"{name:<8} {h['human_out']:5.2f} {p_out:6.2f} {a_err:6.3f} {a_kl:6.3f}"
            f" | {h['human_left']:5.2f} {p_left:6.2f} {b_err:6.3f} {b_kl:6.3f}"
        )

    print()
    a_mae = sum(a_errors) / len(a_errors)
    a_mkl = sum(a_kls) / len(a_kls)
    a_r = pearson_r(a_human, a_pred)
    b_mae = sum(b_errors) / len(b_errors)
    b_mkl = sum(b_kls) / len(b_kls)
    b_r = pearson_r(b_human, b_pred)

    print(f"Player A: MAE={a_mae:.3f}  mean_KL={a_mkl:.4f}  r={a_r:.3f}")
    print(f"Player B: MAE={b_mae:.3f}  mean_KL={b_mkl:.4f}  r={b_r:.3f}")

    return {
        "player_a": {"mae": a_mae, "mean_kl": a_mkl, "r": a_r},
        "player_b": {"mae": b_mae, "mean_kl": b_mkl, "r": b_r},
    }


def _strip_markdown_fences(text: str) -> str:
    """Remove leading/trailing markdown code fences (```json ... ```)."""
    text = text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1]
    if text.endswith("```"):
        text = text.rsplit("```", 1)[0]
    return text.strip()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Evaluate CR game predictions against human data."
    )
    parser.add_argument(
        "predictions_file",
        type=Path,
        help="JSON file with model predictions (list of {game, out, left})",
    )
    args = parser.parse_args()

    text = _strip_markdown_fences(args.predictions_file.read_text())
    predictions = json.loads(text)
    eval_cr(predictions)


if __name__ == "__main__":
    main()
