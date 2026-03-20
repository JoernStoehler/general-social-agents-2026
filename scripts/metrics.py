"""Metrics for comparing predicted distributions to human data.

All metrics take two dicts mapping action -> probability.
The 'human' distribution is always the reference/ground truth.
"""

import math


def _align_distributions(
    predicted: dict[int, float],
    human: dict[int, float],
    laplace_alpha: float = 0.0,
) -> tuple[list[float], list[float]]:
    """Align two distributions over the same action space.

    Returns (p_pred, p_human) as lists in the same action order.
    Applies Laplace smoothing if alpha > 0.
    """
    actions = sorted(set(predicted.keys()) | set(human.keys()))
    n = len(actions)

    p = [predicted.get(a, 0.0) for a in actions]
    q = [human.get(a, 0.0) for a in actions]

    if laplace_alpha > 0:
        p = [(pi + laplace_alpha) / (sum(p) + n * laplace_alpha) for pi in p]
        q = [(qi + laplace_alpha) / (sum(q) + n * laplace_alpha) for qi in q]

    return p, q


def kl_divergence(
    predicted: dict[int, float],
    human: dict[int, float],
    laplace_alpha: float = 1e-10,
) -> float:
    """KL divergence D_KL(human || predicted).

    This is the "forward KL" with human as the reference distribution,
    matching the metric used in Manning & Horton (2026).

    KL(human || predicted) = sum_x human(x) * log(human(x) / predicted(x))

    Uses Laplace smoothing (default alpha=1e-10) to avoid log(0).
    """
    p_pred, p_human = _align_distributions(predicted, human, laplace_alpha)

    kl = 0.0
    for qi, pi in zip(p_human, p_pred):
        if qi > 0:
            kl += qi * math.log(qi / pi)
    return kl


def total_variation(
    predicted: dict[int, float],
    human: dict[int, float],
) -> float:
    """Total variation distance: TV(P, Q) = 0.5 * sum|P(x) - Q(x)|."""
    p_pred, p_human = _align_distributions(predicted, human)
    return 0.5 * sum(abs(pi - qi) for pi, qi in zip(p_pred, p_human))


def log_likelihood(
    predicted: dict[int, float],
    human: dict[int, float],
    n: int = 108,
    laplace_alpha: float = 1e-10,
) -> float:
    """Log-likelihood of human data under the predicted distribution.

    Treats human_data as observed frequencies (proportions * n) and
    computes sum_x count(x) * log(predicted(x)).

    Higher is better (less negative).
    """
    p_pred, p_human = _align_distributions(predicted, human, laplace_alpha)

    ll = 0.0
    for qi, pi in zip(p_human, p_pred):
        count = qi * n
        if count > 0:
            ll += count * math.log(pi)
    return ll


if __name__ == "__main__":
    from games import ARAD_RUBINSTEIN_2012_BASIC

    human = ARAD_RUBINSTEIN_2012_BASIC

    # Self-comparison (KL should be ~0)
    print(f"KL(human || human) = {kl_divergence(human, human):.6f}")
    print(f"TV(human, human) = {total_variation(human, human):.6f}")
    print(f"LL(human | human) = {log_likelihood(human, human):.2f}")

    # Uniform baseline
    uniform = {a: 0.1 for a in range(11, 21)}
    print(f"\nKL(human || uniform) = {kl_divergence(uniform, human):.4f}")
    print(f"TV(human, uniform) = {total_variation(uniform, human):.4f}")
    print(f"LL(human | uniform) = {log_likelihood(uniform, human):.2f}")

    # GPT-4o baseline (87% on 19)
    gpt4o = {a: 0.013 for a in range(11, 21)}
    gpt4o[19] = 0.87
    gpt4o_total = sum(gpt4o.values())
    gpt4o = {a: p / gpt4o_total for a, p in gpt4o.items()}
    print(f"\nKL(human || GPT-4o baseline) = {kl_divergence(gpt4o, human):.4f}")
    print(f"TV(human, GPT-4o baseline) = {total_variation(gpt4o, human):.4f}")
