"""Charness-Rabin two-stage dictator games with human data.

Data source: Manning & Horton (2026), Table D2 (Appendix),
verified against paper TeX source (optimize.tex lines 1713-1759).
Original data from Charness & Rabin (2002), QJE 117(3): 817-869.

Each game has two stages:
- Stage 1: Person A chooses "Out" (a fixed allocation) or "Enter" (lets B choose)
- Stage 2: Person B chooses "Left" or "Right" (two different allocations)
B chooses without knowing A's decision.

Human data is the proportion choosing each option.
"""

from dataclasses import dataclass


@dataclass
class CRGame:
    """A Charness-Rabin two-stage dictator game."""

    name: str
    panel: str  # A, B, or C
    # Stage 1: A chooses Out (fixed allocation) or Enter (B decides)
    out_payoff: tuple[int, int]  # (A's payoff, B's payoff) if A chooses Out
    # Stage 2: B chooses Left or Right
    left_payoff: tuple[int, int]  # (A's payoff, B's payoff)
    right_payoff: tuple[int, int]  # (A's payoff, B's payoff)
    # Human data: proportions
    human_out: float  # P(A chooses Out)
    human_enter: float  # P(A chooses Enter)
    human_left: float  # P(B chooses Left)
    human_right: float  # P(B chooses Right)

    def prompt_player_a(self) -> str:
        """Generate prediction prompt for Player A's decision."""
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
        """Generate prediction prompt for Player B's decision."""
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


# Panel A: B's payoffs identical
CR_GAMES = [
    CRGame("Barc7", "A", (750, 0), (400, 400), (750, 400), 0.47, 0.53, 0.06, 0.94),
    CRGame("Barc5", "A", (550, 550), (400, 400), (750, 400), 0.39, 0.61, 0.33, 0.67),
    CRGame("Berk28", "A", (100, 1000), (75, 125), (125, 125), 0.50, 0.50, 0.34, 0.66),
    CRGame("Berk32", "A", (450, 900), (200, 400), (400, 400), 0.85, 0.15, 0.35, 0.65),
    # Panel B: B's sacrifice helps A
    CRGame("Barc3", "B", (725, 0), (400, 400), (750, 375), 0.74, 0.26, 0.62, 0.38),
    CRGame("Barc4", "B", (800, 0), (400, 400), (750, 375), 0.83, 0.17, 0.62, 0.38),
    CRGame("Berk21", "B", (750, 0), (400, 400), (750, 375), 0.47, 0.53, 0.61, 0.39),
    CRGame("Barc6", "B", (750, 100), (300, 600), (700, 500), 0.92, 0.08, 0.75, 0.25),
    CRGame("Barc9", "B", (450, 0), (350, 450), (450, 350), 0.69, 0.31, 0.94, 0.06),
    CRGame("Berk25", "B", (450, 0), (350, 450), (450, 350), 0.62, 0.38, 0.81, 0.19),
    CRGame("Berk19", "B", (700, 200), (200, 700), (600, 600), 0.56, 0.44, 0.22, 0.78),
    CRGame("Berk14", "B", (800, 0), (0, 800), (400, 400), 0.68, 0.32, 0.45, 0.55),
    CRGame("Barc1", "B", (550, 550), (400, 400), (750, 375), 0.96, 0.04, 0.93, 0.07),
    CRGame("Berk13", "B", (550, 550), (400, 400), (750, 375), 0.86, 0.14, 0.82, 0.18),
    CRGame("Berk18", "B", (0, 800), (0, 800), (400, 400), 0.00, 1.00, 0.44, 0.56),
    # Panel C: B's sacrifice hurts A
    CRGame("Barc11", "C", (375, 1000), (400, 400), (350, 350), 0.54, 0.46, 0.89, 0.11),
    CRGame("Berk22", "C", (375, 1000), (400, 400), (250, 350), 0.39, 0.61, 0.97, 0.03),
    CRGame("Berk27", "C", (500, 500), (800, 200), (0, 0), 0.41, 0.59, 0.91, 0.09),
    CRGame("Berk31", "C", (750, 750), (800, 200), (0, 0), 0.73, 0.27, 0.88, 0.12),
    CRGame("Berk30", "C", (400, 1200), (400, 200), (0, 0), 0.77, 0.23, 0.88, 0.12),
]


if __name__ == "__main__":
    print(f"Total CR games: {len(CR_GAMES)}")
    print(f"Total prediction tasks: {len(CR_GAMES) * 2} (Player A + Player B for each)")
    print()
    for game in CR_GAMES[:3]:
        print(f"--- {game.name} (Panel {game.panel}) ---")
        print(f"Out payoff: {game.out_payoff}")
        print(f"Left: {game.left_payoff}, Right: {game.right_payoff}")
        print(f"Human A: Out={game.human_out:.2f}, Enter={game.human_enter:.2f}")
        print(f"Human B: Left={game.human_left:.2f}, Right={game.human_right:.2f}")
        print()
