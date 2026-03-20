"""Result aggregation, comparison, and plotting."""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from games import Game
from metrics import kl_divergence, log_likelihood, total_variation


def plot_distributions(
    game: Game,
    distributions: dict[str, dict[int, float]],
    title: str | None = None,
    save_path: str | None = None,
) -> plt.Figure:
    """Grouped bar chart overlaying multiple distributions against human data.

    Args:
        game: The game (provides action_space and human_data).
        distributions: Maps label -> {action: probability}.
            Should include "Human" if you want the ground truth shown.
        title: Plot title. Defaults to game name.
        save_path: If provided, save the figure to this path.

    Returns:
        The matplotlib Figure.
    """
    actions = game.action_space
    labels = list(distributions.keys())
    n_groups = len(actions)
    n_bars = len(labels)

    fig, ax = plt.subplots(figsize=(12, 6))

    bar_width = 0.8 / n_bars
    x = np.arange(n_groups)

    colors = plt.cm.Set2(np.linspace(0, 1, max(n_bars, 3)))

    for i, label in enumerate(labels):
        dist = distributions[label]
        values = [dist.get(a, 0.0) for a in actions]
        offset = (i - n_bars / 2 + 0.5) * bar_width
        ax.bar(
            x + offset, values, bar_width,
            label=label, color=colors[i], edgecolor="white", linewidth=0.5,
        )

    ax.set_xlabel("Choice", fontsize=12)
    ax.set_ylabel("Probability", fontsize=12)
    ax.set_title(title or game.name, fontsize=14)
    ax.set_xticks(x)
    ax.set_xticklabels([str(a) for a in actions])
    ax.legend(loc="upper left", fontsize=10)
    ax.set_ylim(0, max(0.45, ax.get_ylim()[1]))
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight")

    return fig


def compare_all(
    game: Game,
    distributions: dict[str, dict[int, float]],
    n_human: int = 108,
) -> pd.DataFrame:
    """Compute KL, TV, and log-likelihood for each distribution vs human data.

    Args:
        game: The game (provides human_data).
        distributions: Maps label -> {action: probability}.
            "Human" entry is used as reference; it is also compared to itself.
        n_human: Sample size for log-likelihood computation.

    Returns:
        DataFrame with columns: Label, KL_divergence, Total_variation, Log_likelihood.
    """
    human = game.human_data

    rows = []
    for label, dist in distributions.items():
        kl = kl_divergence(dist, human)
        tv = total_variation(dist, human)
        ll = log_likelihood(dist, human, n=n_human)
        rows.append({
            "Label": label,
            "KL_divergence": round(kl, 4),
            "Total_variation": round(tv, 4),
            "Log_likelihood": round(ll, 2),
        })

    df = pd.DataFrame(rows)
    return df


if __name__ == "__main__":
    from baselines import (
        level_k_distribution,
        nash_equilibrium_symmetric,
        uniform_distribution,
    )
    from games import ELEVEN_TWENTY_GAME

    game = ELEVEN_TWENTY_GAME

    distributions = {
        "Human": game.human_data,
        "Nash (symmetric)": nash_equilibrium_symmetric(game),
        "Level-1 (pure)": level_k_distribution(game, 1),
        "Level-2 (pure)": level_k_distribution(game, 2),
        "Uniform": uniform_distribution(game),
    }

    # Compare
    df = compare_all(game, distributions)
    print(df.to_string(index=False))

    # Plot
    fig = plot_distributions(
        game, distributions,
        title="11-20 Money Request Game: Baselines vs Human Data",
        save_path="figures/baselines_vs_human.png",
    )
    print("\nPlot saved to figures/baselines_vs_human.png")
