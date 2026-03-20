# Learnings: Predicting human behavior in economic games

These are general patterns and failure modes discovered from past prediction attempts. Apply them as appropriate to each specific game.

## Common AI failure modes

Previous AI systems performed very poorly on these tasks. Key failure modes:

- **Level-k anchoring**: AI systems anchor on level-0 or level-1 game-theoretic reasoning (e.g., "the rational choice is X"). Humans typically reason 2-3 levels deep, not 0-1. If your first instinct is "the obvious/rational choice is X," most humans have already thought past that.
- **Regression to 50-50**: When uncertain, AI systems predict moderate splits (40-60%). Real human distributions are often extreme — 80-95% choosing one option when it dominates on multiple dimensions. Commit to your best prediction; don't hedge.
- **Template predictions**: AI systems apply the same prediction to structurally similar games. Each game is different — small payoff changes can shift behavior substantially. Reason about each game independently.
- **Ignoring experiment context**: The specific participant population, stakes, and framing all matter. University students playing for real money behave differently than hypothetical rational agents.

## Key behavioral economics principles

- **Bounded rationality**: Humans satisfice, not optimize. They use heuristics and limited-depth reasoning.
- **Social preferences**: Humans care about fairness, reciprocity, and efficiency — not just their own payoff. Inequality aversion (Fehr & Schmidt), reciprocity (Rabin), and efficiency concerns all shape choices.
- **"Free generosity"**: When being generous costs nothing (identical personal payoff either way), the vast majority choose the prosocial option.
- **Risk aversion**: When a safe option gives a decent outcome, most humans take it. Don't underestimate how risk-averse people are when the safe option is "good enough."
- **Focal points**: People coordinate on salient options — round numbers, equal splits, symmetric outcomes.

## How to approach each game

1. Identify what motives (self-interest, fairness, efficiency, reciprocity) point which direction
2. Consider whether motives align (→ extreme prediction, 80-95%) or genuinely conflict (→ moderate prediction)
3. Consider the specific participant population and stakes
4. Commit to a specific prediction — don't default to moderate values out of uncertainty
