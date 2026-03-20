# Game: 11-20 Money Request Game

## Experiment details

**Source**: Arad & Rubinstein (2012), "The 11-20 Money Request Game: A Level-k Reasoning Study," American Economic Review 102(7): 3561-3573.

**Participants**: 108 undergraduate students at Tel Aviv University and the Technion (Israel). Not specially trained in game theory. Playing for real money (Israeli shekels).

**Setup**: One-shot (played exactly once). Anonymous. Random pairing. Simultaneous independent decisions. No communication between participants.

**Instructions shown to participants** (verbatim):
> You and another player are playing a game in which each player requests an amount of money. The amount must be (an integer) between 11 and 20 shekels. Each player will receive the amount he requests. A player will receive an additional amount of 20 shekels if he asks for exactly one shekel less than the other player.

That is all participants were told. No game theory terminology, no discussion of strategies.

## Structural analysis

- Choosing 20 gives 20 shekels guaranteed. Choosing 19 gives 19 guaranteed + a chance at the 20 bonus (total 39) if the opponent chose 20.
- The bonus (20 shekels) is very large relative to the 1-shekel cost of undercutting. Giving up 1 shekel for a chance at 20 is a very good deal. This makes undercutting highly attractive.
- A naive (level-0) player might choose 20 (maximum guaranteed). A level-1 player best-responds to level-0 by choosing 19. A level-2 player best-responds to the mix of level-0 and level-1 by choosing 18. Level-3 chooses 17. And so on.
- Since most humans reason 2-3 levels deep in strategic games, and level-0 starts at 20: level-1 chooses 19, level-2 chooses 18, level-3 chooses 17. So the bulk of choices should concentrate around 17-18 (the modal reasoning depth of 2-3 steps from 20).
- Very few participants would go as low as 11-14 — the guaranteed money lost is too large relative to the speculative bonus. Very few would stay at 20 — forgoing the bonus when undercutting costs only 1 shekel seems naive, and most people think at least one step ahead.
- The distribution should be peaked, not flat. One-shot games produce clustering around a few focal strategies.

## Predict

What probability distribution over choices {11, 12, 13, 14, 15, 16, 17, 18, 19, 20} would you predict for this experiment?

Output format:
```json
{"11": p11, "12": p12, "13": p13, "14": p14, "15": p15, "16": p16, "17": p17, "18": p18, "19": p19, "20": p20}
```
