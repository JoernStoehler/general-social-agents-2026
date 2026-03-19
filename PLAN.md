# Project Plan

## Goal

Test whether modern LLMs (Claude Opus 4.6, Claude Sonnet 4.6) can predict human game play — potentially without the elaborate persona-ensemble-calibration pipeline that Manning & Horton (2026) needed for GPT-4o.

## What the Original Paper Actually Does

Manning & Horton (2026) did NOT show that "GPT-4o predicts human behavior." They showed:

1. **Baseline GPT-4o is terrible.** It picks 19 ~87% of the time (KL = 2.7 vs humans).
2. **An engineered pipeline works.** They defined 100 persona agents with theory-grounded prompts, sampled each 100 times at temperature=1, optimized mixture weights against calibration data, and tested on 1,500 novel games.
3. **The pipeline gets KL = 0.3** in-sample, 1.54× better than baseline on held-out games.

The contribution is the *pipeline*, not the raw model. The sampling-at-temperature-1 approach was a workaround for extracting predictions from a model that couldn't express distributions directly.

## Why Our Approach Is Different

A 2026 model (Opus 4.6) can reason about and express probability distributions directly. It doesn't need to be sampled 200 times like a slot machine to reveal its implicit beliefs. The natural approach is to just ask it.

This changes the fundamental question from "how do we extract predictions from a dumb model?" to "does a smart model already know what humans do?"

## Method Design

### Primary: Direct Distribution Prediction

**Input:** Game rules only. Natural language description of the game. No behavioral economics hints, no persona framing, no "you are a human."

**Output:** Full probability distribution over the action space as JSON.

**Why this way:**
- One call per model per game. Efficient.
- Tests the model's explicit knowledge of human behavior.
- The cleaner the input, the more we learn about what the model actually knows vs. what we told it.
- No persona framing means the model isn't being steered toward a particular behavioral theory.

**Prompt sketch** (to be finalized):
> "Here is a game: [rules]. What probability distribution over choices {11, ..., 20} do you predict for human participants? Return as JSON."

### Secondary: Sampling (for comparability with paper)

Call the model N times at temperature=1 with a role-play prompt. Build empirical distribution. This tests the model's *implicit* behavioral priors — what it does when acting as a human, which may differ from what it explicitly predicts humans would do.

N=50 to start. The human ground truth is n=108, so there's no point in higher precision than that.

### Why Both Methods Matter

The gap between "what the model predicts humans do" (direct) and "what the model does when role-playing a human" (sampling) is itself interesting. If they differ, that tells us something about the model's self-knowledge.

## Contamination

### The Problem

The 11-20 game is from Arad & Rubinstein (2012), a famous AER paper. Modern models have almost certainly seen the human distribution in training. A model that outputs "17: 32%, 18: 30%" might be recalling a table, not predicting behavior.

### How to Test It

Ask the model two questions:
1. "What is the published distribution from Arad & Rubinstein (2012)?" (tests recall)
2. "Here is a game: [rules]. Predict human behavior." (tests prediction)

If the answers are identical, it's likely recall. If they differ, the model is doing something beyond memorization.

### How to Mitigate It

1. **Acknowledge it.** The 11-20 game result has a contamination caveat. Report it honestly.
2. **Test parameter variants.** Change the bonus from 20 to 10, change the range from 11-20 to 1-10, etc. No published human data exists for these variants, so the model can't recall.
3. **Test on novel games.** We have 1,500 game configurations from the paper. If human response data becomes available (it's collected but not publicly released), those are clean tests.

### Is the 11-20 Game Sufficient?

For a first result with contamination caveat: yes. It gives us concrete KL numbers to compare against the paper.

For a valid scientific claim: no. We need games where the human data isn't in training. Parameter variants are our best bet without needing external human data.

## What Constitutes Cheating

This matters for the validity and interest of the result.

**Cheating (makes result meaningless):**
- Web access during prediction (model could look up published data)
- Giving the model the paper or any human data
- Giving the model the name of the game or paper (enables recall)

**Not cheating but reduces interest:**
- Persona framing / behavioral economics hints (tells the model what theory to apply)
- This is the paper's approach — legitimate to test as a condition but less impressive than bare prediction

**Fine (part of the model's capability):**
- Extended thinking / chain-of-thought
- Tool use (calculator, Python for computing Nash equilibria)
- The model's training data (unavoidable, handle via contamination testing)

## Experimental Conditions

| Condition | Input | Output | Method | What it tests |
|-----------|-------|--------|--------|---------------|
| Direct prediction | Game rules only | Full distribution (JSON) | 1 call | Explicit knowledge of human behavior |
| Bare role-play | Game rules, "you are a participant" | Single choice | N=50, temp=1 | Implicit behavioral priors |
| Persona role-play | Paper's exact persona prompts | Single choice | N=50, temp=1 | Does persona pipeline still help? |
| Contamination check | "What does the published data say?" | Distribution | 1 call | Is direct prediction just recall? |

## Models

1. Claude Opus 4.6 (primary — most capable, tests ceiling)
2. Claude Sonnet 4.6 (tests whether capability scales with model size)
3. GPT-4o (direct comparison with paper — only if budget approved)

## Metrics

- **KL divergence**: D_KL(human || predicted). Lower = better. Paper's primary metric.
- **Total variation distance**: TV(P, Q) = 0.5 × Σ|P(x) - Q(x)|.
- **Log-likelihood**: of human data under predicted distribution.

## Reference Numbers (what we're comparing against)

| Prediction | KL (11-20 game) | Source |
|------------|-----------------|--------|
| GPT-4o baseline (87% on 19) | 2.7 | Paper |
| Paper's optimized ensemble | 0.3 | Paper |
| Nash equilibrium (symmetric) | 2.86 | Computed |
| Uniform random | 0.54 | Computed |
| **Claude Opus (direct)** | **?** | **Our experiment** |
| **Claude Opus (bare role-play)** | **?** | **Our experiment** |

## Execution Order

1. Contamination test (recall vs predict, 2 calls, free if using subscription)
2. Direct prediction: Opus and Sonnet on 11-20 game
3. Bare role-play: Opus and Sonnet (N=50 each)
4. Compute metrics, compare to reference numbers
5. If contamination detected: test on parameter variants (change bonus to 10, range to 1-10)
6. Persona role-play using paper's exact prompts (if results from steps 2-3 are interesting)
7. Write report and Twitter thread

**Cost note:** Steps 1-2 require Anthropic API calls. Must get explicit cost approval from Jörn before running. Estimated cost for direct prediction: negligible (<$0.10). For sampling N=50: ~$1-2 at Opus pricing.

## What We Have

### Verified Data
- Arad & Rubinstein (2012) human data: n=108, cross-checked across 4 sources
- Manning & Horton persona prompts: extracted from TeX source, verified against paper
- 1,500 novel game configurations: pulled from Expected Parrot via EDSL
- Paper TeX source with full methodology details

### Code (built by subagent, needs review)
- src/games.py — 11-20 game definition with verified human data
- src/simulate.py — direct prediction + sampling methods (default model needs fix)
- src/metrics.py — KL, TV, log-likelihood (14 tests passing)
- src/baselines.py — Nash, level-k, uniform
- src/analysis.py — plotting and comparison

### Missing
- Human response data for the 1,500 novel games (collected via Prolific, not publicly released)
- GPT-4o API access (optional)

## Open Questions for Jörn

1. **Budget for API calls:** Direct prediction is ~$0.10. Sampling (N=50 × 2 models) is ~$2. Full experiment including variants maybe $10-20. What's approved?
2. **Contamination tolerance:** Is the 11-20 game result publishable with a contamination caveat, or do we need clean novel-game results?
3. **Contact authors:** Should we email Manning & Horton asking for the human response data on the 1,500 games?

## Deliverables

1. GitHub repo (public)
2. Report (report.md, ~1500-2500 words)
3. Twitter/X thread draft (6-10 tweets)

## Priorities (cut from bottom)

1. 11-20 game, direct prediction + contamination test, Claude Opus 4.6
2. Add bare role-play, add Sonnet
3. Test on parameter variants if contamination detected
4. Add persona role-play condition
5. Add GPT-4o
6. Test on 1,500 novel games (requires human data)
