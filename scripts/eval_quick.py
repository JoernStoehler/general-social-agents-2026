"""Quick eval: parse model output and compare to human data.

Usage:
  python src/eval_quick.py results/output_1120.json
  python src/eval_quick.py results/output_cr.json --cr
"""

import json
import sys
import math
from pathlib import Path


def kl_divergence(human: dict[int, float], predicted: dict[int, float]) -> float:
    """D_KL(human || predicted). Lower = better."""
    eps = 1e-10
    kl = 0.0
    for k, p in human.items():
        q = predicted.get(k, eps)
        if p > 0:
            kl += p * math.log(p / max(q, eps))
    return kl


def parse_1120_distribution(text: str) -> dict[int, float] | None:
    """Try to extract a distribution over 11-20 from model output text."""
    # Try JSON first
    import re
    # Look for a JSON object with number keys
    json_match = re.search(r'\{[^{}]*\}', text)
    if json_match:
        try:
            d = json.loads(json_match.group())
            # Convert string keys to int
            result = {}
            for k, v in d.items():
                try:
                    result[int(k)] = float(v)
                except (ValueError, TypeError):
                    continue
            if len(result) >= 5:  # at least half the actions
                return result
        except json.JSONDecodeError:
            pass

    # Try line-by-line "17: 0.32" or "17 - 32%" patterns
    result = {}
    for line in text.split('\n'):
        m = re.search(r'(\d+)\s*[:=\-–]\s*([\d.]+)\s*%?', line)
        if m:
            action = int(m.group(1))
            val = float(m.group(2))
            if 11 <= action <= 20:
                if val > 1:  # percentage
                    val /= 100
                result[action] = val
    if len(result) >= 5:
        return result
    return None


# Human data: Arad & Rubinstein 2012, Table 1, n=108
HUMAN_1120 = {
    11: 0.04, 12: 0.00, 13: 0.03, 14: 0.06, 15: 0.01,
    16: 0.06, 17: 0.32, 18: 0.30, 19: 0.12, 20: 0.06,
}


def eval_1120(predicted: dict[int, float]) -> dict:
    total = sum(predicted.values())
    if abs(total - 1.0) > 0.05:
        predicted = {k: v / total for k, v in predicted.items()}

    kl = kl_divergence(HUMAN_1120, predicted)
    mae = sum(abs(HUMAN_1120.get(k, 0) - predicted.get(k, 0)) for k in range(11, 21)) / 10

    # Key diagnostics
    human_peak = sum(HUMAN_1120.get(k, 0) for k in [17, 18])
    pred_peak = sum(predicted.get(k, 0) for k in [17, 18])
    human_high = sum(HUMAN_1120.get(k, 0) for k in [19, 20])
    pred_high = sum(predicted.get(k, 0) for k in [19, 20])

    return {
        "kl": round(kl, 4),
        "mae": round(mae, 4),
        "mass_17_18_human": round(human_peak, 2),
        "mass_17_18_pred": round(pred_peak, 2),
        "mass_19_20_human": round(human_high, 2),
        "mass_19_20_pred": round(pred_high, 2),
        "predicted": {k: round(v, 4) for k, v in sorted(predicted.items())},
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python src/eval_quick.py <output_file_or_text>")
        sys.exit(1)

    path = Path(sys.argv[1])
    if path.exists():
        text = path.read_text()
    else:
        text = sys.argv[1]

    dist = parse_1120_distribution(text)
    if dist:
        result = eval_1120(dist)
        print(json.dumps(result, indent=2))
    else:
        print("Could not parse distribution from output")
        sys.exit(1)
