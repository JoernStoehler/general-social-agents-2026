"""Game definitions and human data for the General Social Agents project."""

from dataclasses import dataclass
from typing import Callable

import numpy as np


@dataclass
class Game:
    """A game with human data for comparison."""

    name: str
    description: str  # Natural language rules (used in LLM prompts)
    action_space: list[int]
    human_data: dict[int, float]  # action -> probability
    payoff: Callable[[int, int], tuple[float, float]]  # (row_action, col_action) -> (row_payoff, col_payoff)

    def payoff_matrix(self) -> tuple[np.ndarray, np.ndarray]:
        """Build payoff matrices A (row player) and B (column player)."""
        n = len(self.action_space)
        A = np.zeros((n, n))
        B = np.zeros((n, n))
        for i, ai in enumerate(self.action_space):
            for j, aj in enumerate(self.action_space):
                A[i, j], B[i, j] = self.payoff(ai, aj)
        return A, B


def _eleven_twenty_payoff(row: int, col: int) -> tuple[float, float]:
    """Payoff for the 11-20 Money Request Game.

    Each player gets what they request. If you request exactly 1 less
    than your opponent, you get an additional +20 bonus.
    """
    row_pay = row + (20 if row == col - 1 else 0)
    col_pay = col + (20 if col == row - 1 else 0)
    return float(row_pay), float(col_pay)


# Game instruction text matching Arad & Rubinstein (2012), as used by
# Manning & Horton (2026) -- see paper_key_details.md section 2.
_ELEVEN_TWENTY_DESCRIPTION = (
    "You and another player are playing a game in which each player requests "
    "an amount of money. The amount must be (an integer) between 11 and 20 "
    "shekels. Each player will receive the amount he requests. A player will "
    "receive an additional amount of 20 shekels if he asks for exactly one "
    "shekel less than the other player."
)

# Human data: Table 1, Arad & Rubinstein (2012), AER 102(7): 3561-3573
# Basic version, n=108. Percentages as reported (integers, sum to 100).
ARAD_RUBINSTEIN_2012_BASIC: dict[int, float] = {
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

ELEVEN_TWENTY_GAME = Game(
    name="11-20 Money Request Game",
    description=_ELEVEN_TWENTY_DESCRIPTION,
    action_space=list(range(11, 21)),
    human_data=ARAD_RUBINSTEIN_2012_BASIC,
    payoff=_eleven_twenty_payoff,
)


if __name__ == "__main__":
    game = ELEVEN_TWENTY_GAME
    print(f"Game: {game.name}")
    print(f"Actions: {game.action_space}")
    print(f"Human data: {game.human_data}")
    print(f"Sum of human probs: {sum(game.human_data.values()):.2f}")

    A, B = game.payoff_matrix()
    print(f"\nPayoff matrix A (row player), shape {A.shape}:")
    print(A.astype(int))
