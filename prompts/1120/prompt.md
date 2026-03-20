# Task: Predict the distribution of human choices in an economic game

You are predicting how real humans played a specific economic experiment. Your goal is to produce a probability distribution over the possible choices that minimizes KL divergence from the actual empirical distribution.

**This is a difficult prediction task.** Previous AI systems performed poorly — for example, GPT-4o predicted that ~87% of players choose 19 or 20, when in reality only ~18% did. The main failure modes are:
- Anchoring on game-theoretic "rational" reasoning (level-0 or level-1) instead of modeling how humans actually think
- Underestimating how deeply humans reason strategically (humans typically reason 2-3 levels, not 0-1)
- Hedging predictions toward uniform/50-50 when uncertain, rather than committing to a peaked distribution that matches human behavioral tendencies

## The experiment (factual description)

This is the **11-20 Money Request Game**, run by Arad & Rubinstein (2012, American Economic Review).

**Participants**: 108 undergraduate students at Tel Aviv University and the Technion. These are smart but not specially trained in game theory. They are Israeli students playing for real money (shekels).

**Instructions given to participants** (verbatim):
> You and another player are playing a game in which each player requests an amount of money. The amount must be (an integer) between 11 and 20 shekels. Each player will receive the amount he requests. A player will receive an additional amount of 20 shekels if he asks for exactly one shekel less than the other player.

**Setup**: One-shot game (played exactly once, no learning). Anonymous. Each participant was randomly paired with one other participant. Participants did not communicate. They made their choices independently and simultaneously.

**What participants knew**: Only the rules above. They did not know game theory terminology. They were not told about "level-k reasoning" or Nash equilibria. They simply read the rules and chose a number.

## Key implications for prediction (facts and reasoning)

The following are implications I want you to consider:

**Fact**: Choosing 20 gives 20 shekels guaranteed. Choosing 19 gives 19 guaranteed + a chance at the 20 bonus (total 39) if the opponent chose 20. Choosing lower gives less guaranteed money but a chance at the bonus if the opponent chose exactly one higher.

**Fact**: The Nash equilibrium of this game involves mixing, with substantial mass below 20. A rational player who believes their opponent plays 20 should choose 19. A rational player who believes their opponent reasons this way should choose 18. And so on.

**Reasonable inference**: Most undergraduate participants would not choose 20 (the "naive" choice). The stakes matter: the bonus (20 shekels) is large relative to the difference between adjacent choices (1 shekel). This makes undercutting very attractive — giving up 1 shekel for a chance at 20 is a good deal. Most participants likely reason at least 1-2 steps: "others might pick 20, so I should pick 19... but others will think that too, so maybe 18..."

**Reasonable inference**: The distribution should be peaked, not flat. Humans in one-shot games tend to cluster around a few focal strategies, not spread uniformly across options.

**Guesstimate**: Participants probably reason about 2-3 steps deep on average. Very few would go all the way down to 11-14 (giving up too much guaranteed money). Very few would stay at 20 (foregoing the bonus entirely seems naive). The mass should be concentrated in the 16-19 range, with the peak likely around 17-18 (2-3 steps of reasoning from 20).

## Your output

Provide your predicted probability distribution as a JSON object mapping each choice (11-20) to its probability. Probabilities must sum to 1.0.

Think carefully about how real undergraduate students would approach this game. They are not game theorists — they are regular people reasoning informally about what their opponent might do.

Output format:
```json
{"11": p11, "12": p12, "13": p13, "14": p14, "15": p15, "16": p16, "17": p17, "18": p18, "19": p19, "20": p20}
```
