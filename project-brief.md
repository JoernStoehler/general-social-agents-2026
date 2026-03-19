# Project Brief: Do Modern LLMs Predict Human Game Play Better Than GPT-4o?

## Extending Manning & Horton (2026), "General Social Agents"

**Owner:** Jörn Stöhler (@JoernStoehler)
**Mode:** Fully autonomous agent team. Human overseer for infrastructure failures only.
**Deliverables:** Public GitHub repo, final report (markdown), Twitter/X thread draft.

---

## 1. What the Paper Actually Does

Manning & Horton (NBER WP 34937, arXiv:2508.17407) test whether LLM agents can predict how humans play economic games. Their method:

1. **Baseline GPT-4o is bad.** Asked to play the 11-20 Money Request Game, GPT-4o picks 19 approximately 87% of the time (KL divergence = 2.7 vs. human data). It does not predict human behavior.

2. **They build an ensemble system.** They define 100 "persona agents" — GPT-4o instances with theory-grounded system prompts (level-k thinkers, random choosers, etc.). Each persona is sampled 100 times at temperature=1 to produce a response distribution.

3. **They calibrate mixture weights.** Using the Arad & Rubinstein (2012) 11-20 game as training data (n=108 humans), they optimize a weighted mixture of the 100 persona distributions to minimize KL divergence against the human distribution. The optimized mixture achieves KL ≈ 0.3 in-sample.

4. **They test on held-out games.** They generated 883,320 novel allocation/coordination games, sampled 1,500, collected human data (3 subjects each via Prolific), and evaluated the calibrated ensemble. Result: the ensemble assigns 1.54× more probability to actual human choices than the baseline.

The contribution is the *pipeline* (personas + calibration + mixture), not the raw model. GPT-4o is just a component.

### Available Data

We have downloaded from arXiv and Expected Parrot:
- The full paper (TeX source + PDF)
- 100 agent/persona definitions with exact prompt text (JSON)
- 1,500 pre-registered game configurations (JSON)
- Their exact system prompt: *"You are answering questions as if you were a human. Do not break character."*
- Chain-of-thought structure: two sequential API calls per response

We do **not** have: their simulation code, raw AI response data, or human Prolific response data for the 1,500 games.

---

## 2. The Question We're Answering

Two years of model progress later: **can a modern LLM predict human game play without needing the elaborate persona-ensemble-calibration pipeline?**

Sub-questions:
- (a) Can a modern model (Claude Opus 4.6), asked directly to predict the human distribution, beat GPT-4o's baseline (KL = 2.7)?
- (b) Can it beat the *optimized ensemble* (KL ≈ 0.3)?
- (c) Does the persona/calibration pipeline still improve predictions when applied to a modern model, or has the model already internalized behavioral economics?

### Why This Matters

If a 2026 model can match or beat an engineered pipeline from 2024 in a single call, that's evidence that "world modeling of humans" is improving with scale — relevant for alignment, mechanism design, and social simulation.

---

## 3. The Flagship Game: 11-20 Money Request Game

Arad & Rubinstein (2012), *American Economic Review* 102(7), 3561-3573.

- Two players simultaneously request an integer between 11 and 20.
- Each player receives what they request.
- **Bonus:** If you request exactly 1 less than your opponent, you get +20.
- Tension: 20 is safe, but lower numbers give a chance at the bonus.

### Human Data (Basic Version, n=108)

| Choice | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 |
|--------|----|----|----|----|----|----|----|----|----|----|
| %      | 4  | 0  | 3  | 6  | 1  | 6  | 32 | 30 | 12 | 6  |

Most humans cluster at 17-18 (62%), consistent with level-1/level-2 reasoning.

Source: Table 1 of Arad & Rubinstein (2012), verified from the paper at arielrubinstein.org/papers/88.pdf.

---

## 4. Method

The method should fit the goal. We are **not** locked to the paper's sampling approach.

### Primary: Direct Distribution Prediction

Ask the model to predict the human distribution directly:

> "Here is a game: [description]. What probability distribution over choices {11, 12, ..., 20} do you predict for human participants? Return as JSON."

One call per model. Compare the predicted distribution to the known human distribution using KL divergence, total variation distance, and log-likelihood.

This is the most natural way to use a 2026 model. It tests explicit knowledge of human behavior.

### Secondary: Sampling (Replicating the Paper's Method)

For comparability with Manning & Horton, also run the sampling approach: call the model N times at temperature=1 with a role-play prompt, collect responses, build empirical distribution. This tests the model's *implicit* behavioral priors (what it does when role-playing vs. what it knows humans do).

Sample size: start with N=50. The human ground truth is only n=108, so matching its precision is sufficient. Increase if results are noisy.

### Conditions

- **Direct prediction**: Ask for the distribution explicitly (no role-play)
- **Bare role-play**: "You are a participant in this game. What do you choose?" (sampling)
- **Persona role-play**: Use Manning & Horton's persona prompts (sampling)

### Models

- Claude Opus 4.6 (primary)
- Claude Sonnet 4.6 (for model size comparison)
- GPT-4o (for direct comparison with paper, if budget allows)

### Metrics

- **KL divergence** of predicted distribution vs. human distribution (lower = better)
- **Total variation distance**
- **Log-likelihood** of human data under predicted distribution

Baselines: Nash equilibrium (mixed), level-k predictions, uniform random.

---

## 5. Deliverables

### GitHub Repo

```
src/
├── games.py           # Game definitions and human data
├── simulate.py        # LLM simulation harness
├── baselines.py       # Nash, level-k, uniform computations
├── metrics.py         # Log-likelihood, KL, TV distance
└── analysis.py        # Result aggregation and plotting
prompts/               # All prompts used, labeled
results/               # Raw outputs (JSON/CSV)
figures/               # Generated plots
report.md              # Full writeup
twitter_thread.md      # Draft thread
```

### Report (~1500-2500 words)

1. Motivation and what the original paper actually showed
2. Our approach (direct prediction + sampling comparison)
3. Results (distributions overlaid on human data, metric comparisons)
4. Discussion
5. Limitations

Key plot: overlay predicted distributions from each model/condition against human data for the 11-20 game.

### Twitter/X Thread (6-10 tweets)

Informative, not clickbait. For ML/econ audience. Tag the original authors.

---

## 6. Priorities

Cut from the bottom:

1. **11-20 game, direct prediction + bare role-play, Claude Opus 4.6** — minimum viable result
2. Add Claude Sonnet 4.6
3. Add persona role-play condition (using paper's exact prompts)
4. Add GPT-4o for direct comparison
5. Add more classic games if human data is available
6. Test on the paper's 1,500 novel games (requires their human response data, which we don't have)

---

## 7. What We Have

Research completed (saved in `results/reference/`):
- Paper TeX source and PDF
- 100 persona definitions with exact prompts (JSON from Expected Parrot)
- 1,500 game configurations (JSON from Expected Parrot)
- Arad & Rubinstein (2012) human data (verified from original paper)
- Prior work survey (Horton 2023 homo_silicus, Microsoft turing-experiments, etc.)
- EDSL evaluation (not worth using — caching hazard, 50+ deps, no N-samples support)
- Nash equilibria computed via nashpy
