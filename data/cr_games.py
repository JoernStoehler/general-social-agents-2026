#!/usr/bin/env python3
"""Charness-Rabin two-stage dictator games with human data.

20 games from Charness & Rabin (2002), QJE 117(3): 817-869.
Data source: Manning & Horton (2026), Table D2 (Appendix),
verified against paper TeX source (optimize.tex lines 1713-1759).

Each game has two stages:
    Stage 1: Person A chooses "Out" (a fixed allocation) or "Enter" (B decides).
    Stage 2: Person B chooses "Left" or "Right" (two allocations).
    B chooses without knowing A's decision.

Human data is the proportion choosing each option.

Usage:
    python3 data/cr_games.py             # print summary of all games
    python3 data/cr_games.py --prompts   # print prediction prompts for first 3 games
"""

import argparse
from dataclasses import dataclass


@dataclass
class CRGame:
    """A Charness-Rabin two-stage dictator game.

    Attributes:
        name: Game identifier (e.g. "Barc7", "Berk28").
        panel: Classification from the paper -- A, B, or C.
        out_payoff: (A's payoff, B's payoff) if A chooses Out.
        left_payoff: (A's payoff, B's payoff) if B chooses Left.
        right_payoff: (A's payoff, B's payoff) if B chooses Right.
        human_out: Proportion of human Player As who chose Out.
        human_enter: Proportion who chose Enter (= 1 - human_out).
        human_left: Proportion of human Player Bs who chose Left.
        human_right: Proportion who chose Right (= 1 - human_left).
    """

    name: str
    panel: str
    out_payoff: tuple[int, int]
    left_payoff: tuple[int, int]
    right_payoff: tuple[int, int]
    human_out: float
    human_enter: float
    human_left: float
    human_right: float

    def prompt_player_a(self) -> str:
        """Generate a prediction prompt for Player A's decision."""
        return (
            f"Here is a two-player game.\n\n"
            f"Person A chooses between two options:\n"
            f"- Option 'Out': The payoffs are ({self.out_payoff[0]} to A, {self.out_payoff[1]} to B)\n"
            f"- Option 'Enter': Person B gets to choose between two allocations\n\n"
            f"If A chooses Enter, Person B chooses between:\n"
            f"- 'Left': ({self.left_payoff[0]} to A, {self.left_payoff[1]} to B)\n"
            f"- 'Right': ({self.right_payoff[0]} to A, {self.right_payoff[1]} to B)\n\n"
            f"Person B makes their choice without knowing what A chose.\n\n"
            f"What proportion of human participants playing as Person A would choose 'Out'?\n"
            f"Return ONLY a JSON object: {{\"out\": <probability>, \"enter\": <probability>}} "
            f"where probabilities sum to 1."
        )

    def prompt_player_b(self) -> str:
        """Generate a prediction prompt for Player B's decision."""
        return (
            f"Here is a two-player game.\n\n"
            f"Person A has already made a choice (unknown to B).\n"
            f"Person B must choose between:\n"
            f"- 'Left': ({self.left_payoff[0]} to A, {self.left_payoff[1]} to B)\n"
            f"- 'Right': ({self.right_payoff[0]} to A, {self.right_payoff[1]} to B)\n\n"
            f"What proportion of human participants playing as Person B would choose 'Left'?\n"
            f"Return ONLY a JSON object: {{\"left\": <probability>, \"right\": <probability>}} "
            f"where probabilities sum to 1."
        )


# fmt: off
# Panel A: B's payoffs identical across Left/Right
CR_GAMES: list[CRGame] = [
    CRGame("Barc7",  "A", (750, 0),    (400, 400), (750, 400), 0.47, 0.53, 0.06, 0.94),
    CRGame("Barc5",  "A", (550, 550),  (400, 400), (750, 400), 0.39, 0.61, 0.33, 0.67),
    CRGame("Berk28", "A", (100, 1000), (75, 125),  (125, 125), 0.50, 0.50, 0.34, 0.66),
    CRGame("Berk32", "A", (450, 900),  (200, 400), (400, 400), 0.85, 0.15, 0.35, 0.65),
    # Panel B: B's sacrifice helps A
    CRGame("Barc3",  "B", (725, 0),    (400, 400), (750, 375), 0.74, 0.26, 0.62, 0.38),
    CRGame("Barc4",  "B", (800, 0),    (400, 400), (750, 375), 0.83, 0.17, 0.62, 0.38),
    CRGame("Berk21", "B", (750, 0),    (400, 400), (750, 375), 0.47, 0.53, 0.61, 0.39),
    CRGame("Barc6",  "B", (750, 100),  (300, 600), (700, 500), 0.92, 0.08, 0.75, 0.25),
    CRGame("Barc9",  "B", (450, 0),    (350, 450), (450, 350), 0.69, 0.31, 0.94, 0.06),
    CRGame("Berk25", "B", (450, 0),    (350, 450), (450, 350), 0.62, 0.38, 0.81, 0.19),
    CRGame("Berk19", "B", (700, 200),  (200, 700), (600, 600), 0.56, 0.44, 0.22, 0.78),
    CRGame("Berk14", "B", (800, 0),    (0, 800),   (400, 400), 0.68, 0.32, 0.45, 0.55),
    CRGame("Barc1",  "B", (550, 550),  (400, 400), (750, 375), 0.96, 0.04, 0.93, 0.07),
    CRGame("Berk13", "B", (550, 550),  (400, 400), (750, 375), 0.86, 0.14, 0.82, 0.18),
    CRGame("Berk18", "B", (0, 800),    (0, 800),   (400, 400), 0.00, 1.00, 0.44, 0.56),
    # Panel C: B's sacrifice hurts A
    CRGame("Barc11", "C", (375, 1000), (400, 400), (350, 350), 0.54, 0.46, 0.89, 0.11),
    CRGame("Berk22", "C", (375, 1000), (400, 400), (250, 350), 0.39, 0.61, 0.97, 0.03),
    CRGame("Berk27", "C", (500, 500),  (800, 200), (0, 0),     0.41, 0.59, 0.91, 0.09),
    CRGame("Berk31", "C", (750, 750),  (800, 200), (0, 0),     0.73, 0.27, 0.88, 0.12),
    CRGame("Berk30", "C", (400, 1200), (400, 200), (0, 0),     0.77, 0.23, 0.88, 0.12),
]
# fmt: on


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Charness-Rabin game definitions with human data."
    )
    parser.add_argument(
        "--prompts", action="store_true",
        help="Also print example prediction prompts for the first 3 games",
    )
    args = parser.parse_args()

    print(f"Total CR games: {len(CR_GAMES)}")
    print(f"Total prediction tasks: {len(CR_GAMES) * 2} (Player A + Player B each)")
    print()

    for game in CR_GAMES[:3]:
        print(f"--- {game.name} (Panel {game.panel}) ---")
        print(f"Out payoff: {game.out_payoff}")
        print(f"Left: {game.left_payoff}, Right: {game.right_payoff}")
        print(f"Human A: Out={game.human_out:.2f}, Enter={game.human_enter:.2f}")
        print(f"Human B: Left={game.human_left:.2f}, Right={game.human_right:.2f}")
        if args.prompts:
            print(f"\nPlayer A prompt:\n{game.prompt_player_a()}")
            print(f"\nPlayer B prompt:\n{game.prompt_player_b()}")
        print()


if __name__ == "__main__":
    main()
