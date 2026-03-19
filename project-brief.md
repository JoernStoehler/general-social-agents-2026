# Project Brief: Do Modern LLMs Predict Human Game Play Better Than GPT-4o?

## Replicating & Extending Manning & Horton (2026), "General Social Agents"

**Owner:** Jörn Stöhler (@JStoehler)  
**Mode:** Fully autonomous agent team. No human data collection. Human overseer available for infrastructure failures only.  
**Deliverables:** Public GitHub repo, final report (markdown), Twitter/X thread draft.

---

## 0. How to Use Subagents (Read Before Starting)

You can and should spin up subagents for research and retrieval tasks. This saves tokens in the main agent's context and parallelizes the initial information-gathering phase. Here's what to delegate early:

### Research Tasks (Do These First, In Parallel)

1. **Find the paper's data & code release.** Check http://www.benjaminmanning.io/, the NBER page (https://www.nber.org/papers/w34937), the arXiv page (https://arxiv.org/abs/2508.17407), and any linked GitHub repos. Download whatever is available. Key targets: their exact prompts, game generation code, human response data, and simulation code. Summarize what exists and what doesn't.

2. **Get the Arad & Rubinstein (2012) human data.** The paper is "The 11-20 Money Request Game: A Level-k Reasoning Study," *American Economic Review* 102(7), 3561-3573. Find the exact empirical distribution of human choices (the histogram). This is the ground truth for our primary evaluation. Check the paper itself, its online appendix, and any replication packages on the AER website or the authors' pages.

3. **Find game theory Python libraries.** Specifically: libraries that compute Nash equilibria for normal-form games (nashpy, gambit, etc.), and any existing implementations of level-k / cognitive hierarchy models. We need these for baselines and for Condition A. Summarize: which library, how to install, minimal usage example for a 2-player game with known payoff matrix.

4. **Find prior LLM-as-human-simulator work.** Search for repos, blog posts, or papers that already implement the pattern of "run an LLM N times on a game and compare the output distribution to human data." Someone may have built a harness we can adapt rather than writing from scratch. Keywords: "LLM simulation human behavior," "homo silicus," "LLM behavioral economics," expectedparrot.com (the authors' company — they may have an open-source tool for exactly this).

5. **Check expectedparrot.com / EDSL.** Manning and Horton have a financial interest in Expected Parrot, which appears to be a platform/library for running LLM experiments. If they have an open-source SDK or DSL for LLM-based social simulation, it may be the fastest path to a working harness. Evaluate whether it's worth using vs. building our own.

### External Resources to Look For

- **Prompt engineering guides for behavioral simulation.** There's a growing literature on persona prompting, simulated participants, etc. A subagent can skim 3-5 relevant papers/posts and extract any prompt templates or best practices.
- **Existing replication attempts** of Manning & Horton or the related Horton (2023) "Homo Silicus" paper. Someone may have already done part of this work.
- **Visualization examples** for overlaying predicted vs. observed discrete distributions. Find a clean matplotlib/seaborn/plotly example we can adapt for the key results plot.

### What to Bring Back to Main Agent

For each subagent task: a **short summary** (what was found, what wasn't, key URLs, key numbers) plus any **downloaded files** (data CSVs, code files, prompt text). Don't dump full papers into context — summarize and excerpt.

---

## 1. What This Is About (Read This First)

Manning & Horton (NBER WP 34937, March 2026) showed that GPT-4o, given the right system prompt, can predict how humans play novel economic games better than Nash equilibrium, cognitive hierarchy models, and unprompted LLMs.

Their key finding: the *prompt* matters enormously. A GPT-4o agent told "you are a level-1 thinker who best-responds to a uniform opponent" predicts human behavior far better than a bare GPT-4o told "you are a human." They select/mix prompts grounded in behavioral economics theory (level-k thinking, quantal response equilibrium, etc.) using a small calibration dataset, then test on held-out games.

All their simulations used **GPT-4o (May 2024) at temperature=1**. They note the approach is model-agnostic. They did not test other models.

**The question we're answering:** Two years of model progress later, how do modern LLMs (Claude Opus 4.6, Claude Sonnet 4.6, and ideally GPT-4o for direct comparison) perform on the same task? Specifically:

- (a) Does a bare modern LLM already match or beat GPT-4o-with-optimized-prompt?
- (b) Does prompt optimization still help on top of modern models, or have they internalized the relevant behavioral economics?
- (c) Does giving the model a reasoning scratchpad (chain-of-thought) or tool access (e.g., computing Nash equilibria) help, or is raw intuition better for predicting irrational humans?

**Why this matters:** If modern LLMs are substantially better at predicting human behavior out-of-the-box, that's a strong signal that general "world modeling of humans" is improving with scale — relevant for alignment, mechanism design, and social simulation.

---

## 2. The Paper's Setup (What You Need to Reproduce)

### 2.1 The Flagship Game: Arad & Rubinstein (2012) "11-20 Money Request Game"

- Two players simultaneously request an integer amount between 11 and 20.
- Each player receives the amount they request.
- **Bonus:** If a player requests exactly 1 less than the opponent, they get an additional 20.
- This creates a tension: requesting 20 is safe, but requesting lower gives a chance at the bonus if you correctly predict the opponent.
- Human data (N ≈ 178 from original paper): most humans cluster around 17-18, consistent with level-1 / level-2 reasoning.
- The Nash equilibrium (mixed) and the level-k predictions are well-known for this game.

**This game alone is sufficient for a meaningful spot-check.** The human data is published in the original Arad & Rubinstein (2012) paper and is likely included in Manning & Horton's replication package.

### 2.2 The Large-Scale Evaluation (If Feasible)

Manning & Horton constructed a population of 883,320 novel allocation/coordination games and sampled 1,500 for human evaluation (3 human subjects each = 4,500 responses). The game generation code and human data may be available at:

- http://www.benjaminmanning.io/ (author page)
- The paper's GitHub / replication package (check the paper's footnotes and data availability statement)
- AsPredicted preregistrations: #222695, #231091, #241394

**If the 1,500-game human dataset is available,** a larger evaluation is possible and much more publishable. If not, the 11-20 game alone is still a valid and interesting comparison.

### 2.3 Their Prompting Strategy

They maintain a library of "persona prompts" grounded in behavioral economics theory:

- **Level-0:** "You choose uniformly at random."
- **Level-1:** "You best-respond to an opponent who chooses uniformly at random."
- **Level-2:** "You best-respond to an opponent who best-responds to uniform."
- **QRE-flavored:** "You choose probabilistically, favoring higher-payoff strategies but with noise."
- Other theory-grounded variants.

They use a **selection method**: try all candidate prompts on a calibration dataset, pick the one (or mixture) that minimizes prediction error, then evaluate on held-out data.

### 2.4 Their Metric

Primary: **log-likelihood of observed human responses** under the model's predicted distribution.

To compute: run the LLM N times (e.g., 200) at temperature > 0 on the same game. Count the frequency of each response. This empirical distribution is the model's prediction. Evaluate the log-probability it assigns to each observed human response. Average.

Higher (less negative) = better prediction.

---

## 3. What to Build

### 3.1 Evaluation Harness (Core)

A Python framework that:

1. **Defines games** in a structured format (players, strategies, payoff matrices, natural-language descriptions).
2. **Runs LLM simulations**: calls an LLM API N times with a given (game description + system prompt), collects the distribution of responses.
3. **Computes metrics**: log-likelihood of human data under the predicted distribution, KL divergence, and total variation distance.
4. **Supports multiple models**: at minimum Claude Opus 4.6 and Claude Sonnet 4.6 via Anthropic API. GPT-4o via OpenAI API if budget allows (for direct comparison). Models are configured via simple config, not hardcoded.
5. **Supports multiple prompting conditions** (see Section 4).

### 3.2 Game Library

At minimum:
- The 11-20 money request game with known human data.
- A few other classic games with published human data (Ultimatum Game, Public Goods Game, p-Beauty Contest) if time allows.

Stretch goal:
- Import the Manning & Horton game population if their code/data is available.

### 3.3 Baselines

For each game, compute:
- Nash equilibrium (mixed strategy) — there are Python packages for this, or compute analytically for simple games.
- Level-k predictions (analytical for simple games).
- Uniform random baseline.

These are compared against the LLM predictions.

---

## 4. Experimental Conditions

Run each model under these conditions. Label them clearly in results.

### Condition B: Bare LLM (1-shot)

System prompt: minimal. Something like "You are playing the following game. What do you choose?" No theory, no persona. This tests raw out-of-the-box human prediction.

### Condition C: Theory-Grounded Prompt (1-shot)

Replicate Manning & Horton's approach: provide a level-k persona or other behavioral economics framing in the system prompt. If you can find their exact prompts (check paper appendix / repo), use those. Otherwise, construct reasonable equivalents.

Run with multiple candidate prompts and report which works best (this IS their method).

### Condition C+: Calibrated Prompt (1-shot, uses calibration data)

If multiple games with human data are available: use a subset for calibration (try all prompts, pick best), evaluate on the rest. This is the full Manning & Horton pipeline.

### Condition A: Agent with Tools (multi-step)

Give the model a system prompt that says: "You have access to a Python interpreter. You may compute Nash equilibria, level-k best responses, expected payoffs, or any other analysis before making your prediction of what a human would choose." Let the model think step-by-step and use tools, then give a final answer. This tests whether analytical reasoning helps predict irrational humans.

### Samples Per Condition

200 samples per (model × condition × game) at temperature=1. This gives a reasonable empirical distribution. For each model-condition pair, also record raw response counts.

---

## 5. Deliverables

### 5.1 GitHub Repo

Public repo. Structure suggestion:
```
general-social-agents-replication/
├── README.md              # Project overview, how to run, key findings
├── src/
│   ├── games.py           # Game definitions and human data
│   ├── simulate.py        # LLM simulation harness
│   ├── baselines.py       # Nash, level-k, uniform computations
│   ├── metrics.py         # Log-likelihood, KL, TV distance
│   └── analysis.py        # Result aggregation and plotting
├── prompts/               # All system prompts used, labeled
├── results/               # Raw simulation outputs (JSON/CSV)
├── figures/               # Generated plots
├── report.md              # Full writeup
└── twitter_thread.md      # Draft thread
```

### 5.2 Report (report.md)

Target length: ~1500-2500 words. Sections:
1. Motivation (why this replication matters, link to original paper)
2. Setup (games, models, conditions, metrics)
3. Results (tables + plots: distributions overlaid on human data, metric comparisons)
4. Discussion (what improved, what didn't, implications)
5. Limitations (small N of games, no new human data, etc.)

Key plot: for the 11-20 game, overlay the predicted distributions from each (model × condition) against the known human distribution. This is the most visually compelling result.

### 5.3 Twitter/X Thread (twitter_thread.md)

6-10 tweets. Structure:
- Hook: "GPT-4o can predict human game play better than Nash equilibrium. But that was 2024. What about 2026 models?"
- Key finding (1-2 tweets)
- The most compelling plot (the 11-20 game overlay)
- What it means
- Link to repo and original paper
- Tag @BenSManning and Horton's handle (look it up)

Tone: informative, not clickbait. This is for an ML/econ audience. No hype, let the results speak.

---

## 6. Starter Ideas & Pitfalls (Clearly Marked — Use or Discard)

### STARTER: Getting Human Data for the 11-20 Game

The original Arad & Rubinstein (2012) data is approximately:
- Request 20: ~5%, 19: ~10%, 18: ~25%, 17: ~30%, 16: ~15%, 15: ~8%, 14: ~4%, 13-11: ~3%
(These are rough from memory — **verify against the actual paper.** The paper is: Arad, A. and Rubinstein, A. (2012). "The 11-20 Money Request Game: A Level-k Reasoning Study." *American Economic Review*, 102(7), 3561-3573.)

If you can't access the original paper's exact distribution, Manning & Horton likely reproduce it or cite exact numbers. Check their paper's figures and appendix.

### STARTER: Prompt Templates

For Condition B (bare):
```
You are a participant in an experiment. [Game description]. What integer do you choose? Respond with only a number.
```

For Condition C (level-1):
```
You are a participant in an experiment. You tend to think simply: you assume your opponent will choose randomly, and you pick the best response to that assumption. [Game description]. What integer do you choose? Respond with only a number.
```

For Condition C (level-2):
```
You are a participant in an experiment. You think strategically: you assume your opponent will best-respond to random play, and you best-respond to that. [Game description]. What integer do you choose? Respond with only a number.
```

For Condition A (agent):
```
You are predicting what a typical human participant would choose in the following game. You have access to a Python interpreter. Before predicting, you may analyze the game: compute Nash equilibria, expected payoffs, level-k best responses, or any other analysis. Then predict what a human — who is boundedly rational and may not compute equilibria — would most likely choose. [Game description]
```

### STARTER: API Costs

Rough estimate for the 11-20 game only:
- 200 samples × 4 conditions × 3 models = 2,400 API calls
- Each call is ~200 tokens in, ~10 tokens out (for 1-shot conditions)
- Total: ~500K tokens. Cost: negligible (<$5 even at Opus pricing).

For 1,500 games: multiply by 1,500 → ~750M tokens. That's $hundreds-to-low-thousands depending on model. Budget accordingly or subsample.

### STARTER: The Key Analytical Question

The most interesting possible finding is a **crossover**: if bare Opus 4.6 (Condition B) matches or beats GPT-4o-with-optimized-prompt (their best result), that means two years of scaling has internalized what previously required explicit behavioral-economics prompting. This would be a clean, tweetable result.

The second most interesting finding: if Condition A (agent with tools) does *worse* than Condition B or C, that's evidence that analytical game-theoretic reasoning actively hurts human prediction — because humans aren't analytical. Also very tweetable.

### PITFALL: Output Parsing

LLMs often wrap their response in explanatory text even when asked for "just a number." Build robust parsing: try int() first, then regex for first integer in response, then flag failures. Log and report the failure rate per condition — it's informative (agent conditions will have higher parse complexity).

### PITFALL: Temperature and Sampling

Use temperature=1 for all conditions to match the original paper. Do NOT use temperature=0 — you need the stochastic distribution, not the mode.

### PITFALL: Don't Overclaim

You have human data for a few classic games, not 1,500 novel ones. Frame results as a "spot-check replication" or "pilot extension," not a full replication. Be explicit that new human data collection was out of scope.

---

## 7. Priorities

If you have to cut scope, cut in this order (keep the top, drop the bottom):

1. **The 11-20 game, Conditions B and C, Claude Opus 4.6** — this alone is a publishable spot-check
2. Add Claude Sonnet 4.6 for model size comparison
3. Add Condition A (agent with tools)
4. Add GPT-4o for direct comparison with the original paper
5. Add more classic games (Ultimatum, Beauty Contest)
6. Attempt to obtain and use the full Manning & Horton dataset of 1,500 games
7. Add Condition C+ (calibrated prompt selection across multiple games)

---

## 8. One More Thing

The original paper's data, code, and samples should be at http://www.benjaminmanning.io/ and/or linked from the NBER page at https://www.nber.org/papers/w34937. **Start by checking what's actually available.** The entire project scoping depends on whether you can get (a) exact prompts they used, (b) human data beyond the 11-20 game.

If nothing is publicly available yet (the paper says "currently or will be available"), the 11-20 game from Arad & Rubinstein (2012) is fully self-contained and sufficient.
