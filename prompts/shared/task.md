# Task

You are predicting how real humans played specific economic experiments. Your goal is to produce a probability distribution over the possible choices that minimizes KL divergence from the actual empirical distribution.

**This is a difficult prediction task.** Previous AI systems performed poorly:
- GPT-4o predicted ~87% of players choose 19 or 20 in one game, when only ~18% did (KL = 2.7)
- The main failure modes are: anchoring on game-theoretic "rational" reasoning instead of modeling human cognition, and hedging toward uniform distributions when uncertain

Your predictions should reflect how real people actually behave, not how a rational agent would behave.
