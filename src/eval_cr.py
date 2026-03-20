"""Evaluate CR games predictions against human data.

Usage: python src/eval_cr.py results/cr_output.json
"""

import json
import math
import sys
from pathlib import Path

# Human data from cr_games.py
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
    """KL divergence for binary distribution."""
    eps = 1e-10
    p, q = p_human, max(min(p_pred, 1 - eps), eps)
    kl = 0.0
    if p > eps:
        kl += p * math.log(p / q)
    if (1 - p) > eps:
        kl += (1 - p) * math.log((1 - p) / (1 - q))
    return kl


def eval_cr(predictions: list[dict]) -> dict:
    """Evaluate CR game predictions."""
    pred_by_name = {p["game"]: p for p in predictions}

    a_errors, b_errors = [], []
    a_kls, b_kls = [], []
    a_human, a_pred = [], []
    b_human, b_pred = [], []

    print(f"{'Game':<8} {'A_hum':>5} {'A_pred':>6} {'A_err':>6} {'A_KL':>6} | {'B_hum':>5} {'B_pred':>6} {'B_err':>6} {'B_KL':>6}")
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

        print(f"{name:<8} {h['human_out']:5.2f} {p_out:6.2f} {a_err:6.3f} {a_kl:6.3f} | {h['human_left']:5.2f} {p_left:6.2f} {b_err:6.3f} {b_kl:6.3f}")

    # Correlation
    def corr(x, y):
        n = len(x)
        mx, my = sum(x)/n, sum(y)/n
        cov = sum((a-mx)*(b-my) for a,b in zip(x,y)) / n
        sx = (sum((a-mx)**2 for a in x) / n) ** 0.5
        sy = (sum((b-my)**2 for b in y) / n) ** 0.5
        return cov / (sx * sy) if sx > 0 and sy > 0 else 0

    print()
    print(f"Player A: MAE={sum(a_errors)/len(a_errors):.3f}  mean_KL={sum(a_kls)/len(a_kls):.4f}  r={corr(a_human, a_pred):.3f}")
    print(f"Player B: MAE={sum(b_errors)/len(b_errors):.3f}  mean_KL={sum(b_kls)/len(b_kls):.4f}  r={corr(b_human, b_pred):.3f}")

    return {
        "player_a": {"mae": sum(a_errors)/len(a_errors), "mean_kl": sum(a_kls)/len(a_kls), "r": corr(a_human, a_pred)},
        "player_b": {"mae": sum(b_errors)/len(b_errors), "mean_kl": sum(b_kls)/len(b_kls), "r": corr(b_human, b_pred)},
    }


if __name__ == "__main__":
    path = Path(sys.argv[1])
    text = path.read_text().strip()
    # Strip markdown code fences if present
    if text.startswith("```"):
        text = text.split("\n", 1)[1]
    if text.endswith("```"):
        text = text.rsplit("```", 1)[0]
    predictions = json.loads(text.strip())
    eval_cr(predictions)
