"""Baseline predictions: Nash equilibrium, level-k, uniform random."""

import numpy as np

from src.games import Game


def nash_equilibrium_symmetric(game: Game) -> dict[int, float]:
    """Return the unique symmetric Nash equilibrium for the 11-20 game.

    Derived analytically via indifference conditions. For actions in
    {15,...,20}, P(x+1) = (20-x)/20. Actions 11-14 have zero probability.

    See results/reference/game_theory_libs.md for the full derivation.
    """
    # The analytic solution for the 11-20 game
    nash_dist = {
        11: 0.00, 12: 0.00, 13: 0.00, 14: 0.00,
        15: 0.25, 16: 0.25, 17: 0.20, 18: 0.15,
        19: 0.10, 20: 0.05,
    }
    # Verify it covers the game's action space
    assert set(nash_dist.keys()) == set(game.action_space)
    return nash_dist


def nash_equilibrium_computed(game: Game) -> dict[int, float]:
    """Compute the symmetric Nash equilibrium using nashpy.

    Falls back to the analytic solution if nashpy doesn't find a
    symmetric equilibrium (which can happen with floating-point issues).
    """
    import nashpy as nash

    A, B = game.payoff_matrix()
    ng = nash.Game(A, B)

    # Search for symmetric equilibria among all found
    for sigma_row, sigma_col in ng.vertex_enumeration():
        if np.allclose(sigma_row, sigma_col, atol=1e-6):
            dist = {}
            for i, action in enumerate(game.action_space):
                dist[action] = float(sigma_row[i])
            return dist

    # Fallback to analytic
    return nash_equilibrium_symmetric(game)


def level_k_distribution(game: Game, k: int) -> dict[int, float]:
    """Return the level-k prediction as a probability distribution.

    L0 = uniform over action space.
    L1 = best response to L0 (deterministic).
    L2 = best response to L1, etc.

    For the 11-20 game: L1->19, L2->18, L3->17, L4->16, ...
    """
    actions = game.action_space
    n = len(actions)
    A, _ = game.payoff_matrix()

    if k == 0:
        return {a: 1.0 / n for a in actions}

    # Build the belief distribution (what level k-1 plays)
    prev = level_k_distribution(game, k - 1)
    prev_vec = np.array([prev[a] for a in actions])

    # Best response: action maximizing expected utility
    eu = A @ prev_vec
    best_idx = int(np.argmax(eu))

    dist = {a: 0.0 for a in actions}
    dist[actions[best_idx]] = 1.0
    return dist


def uniform_distribution(game: Game) -> dict[int, float]:
    """Uniform random baseline over the action space."""
    n = len(game.action_space)
    return {a: 1.0 / n for a in game.action_space}


if __name__ == "__main__":
    from src.games import ELEVEN_TWENTY_GAME

    game = ELEVEN_TWENTY_GAME

    print("Nash equilibrium (symmetric, analytic):")
    nash = nash_equilibrium_symmetric(game)
    for a in game.action_space:
        print(f"  {a}: {nash[a]:.2f}")

    print("\nNash equilibrium (computed via nashpy):")
    nash_c = nash_equilibrium_computed(game)
    for a in game.action_space:
        print(f"  {a}: {nash_c[a]:.4f}")

    for k in range(4):
        lk = level_k_distribution(game, k)
        nonzero = {a: p for a, p in lk.items() if p > 0}
        print(f"\nLevel-{k}: {nonzero}")

    print(f"\nUniform: { {a: f'{p:.2f}' for a, p in uniform_distribution(game).items()} }")
