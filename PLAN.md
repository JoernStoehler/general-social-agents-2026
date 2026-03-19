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

## Contamination: Design, Not Detection

### The Problem

The 11-20 game is from Arad & Rubinstein (2012), a famous AER paper. If the human distribution is in the model's training data, any prediction on this game could be recall, not reasoning. A "contamination caveat" is worthless — contaminated results measure nothing.

### Why Detection Is Hard

Asking the model "do you know this data?" doesn't work. Implicit memorization doesn't require explicit recall. The contamination detection literature (Gao et al. 2024, Zhang et al. 2024) offers heuristics but no reliable way to distinguish memorized recall from genuine reasoning on a single data point. You cannot prove non-contamination.

### Our Approach: Experimental Controls

Instead of trying to detect contamination, we design around it using standard experimental controls.

**Control 1 — Structural variants (no published data exists):**

Modify game parameters to create games with identical structure but no published human data. The model can't recall what doesn't exist.

| Variant | Range | Bonus | What changes theoretically |
|---------|-------|-------|---------------------------|
| Original | 11-20 | 20 | (published human data exists) |
| Weak bonus | 11-20 | 10 | Weaker undercutting incentive → rightward shift |
| Strong bonus | 11-20 | 50 | Stronger undercutting incentive → leftward shift |
| Shifted range | 1-10 | 10 | Different numbers, same structure |

For each variant we compute Nash equilibrium and level-k predictions. Even without human data, we check:
1. Does the model's prediction shift when parameters change? (If not → recalling regardless of input)
2. Does it shift in the theoretically expected direction? (If yes → reasoning from game structure)
3. Is it internally consistent? (Support makes sense, sums to 1)

**Control 2 — Named vs. unnamed game:**

Two conditions with identical rules:
1. "Here is a game: [rules only]" (unnamed)
2. "This is the Arad & Rubinstein (2012) 11-20 Money Request Game: [same rules]" (named)

If naming shifts the prediction toward published data → contamination pathway exists and is active.
If predictions are identical → model processes game structure, not metadata.

**Control 3 — Theory comparison:**

Compare whether the model's prediction correlates more with published empirical data or with theoretical predictions (Nash, level-k mixture). If closer to empirical than any theory produces → suspicious. If closer to theory → reasoning from structure.

### Preliminary Evidence (subagent test, 2026-03-19)

A Claude Opus subagent tested informally:
- **Recall test:** Could NOT produce the published distribution. Got the modal choice wrong (said 20; actual is 17).
- **Prediction test:** 35% on 20, 30% on 19 — classic level 0-1 reasoning.
- **Actual humans:** 32% on 17, 30% on 18 — level 2-3 reasoning.

This matches Gao et al. (2024) "Scylla Ex Machina" (arXiv:2410.19599), which found all advanced LLMs (including Claude 3) cluster at 19-20 on this game with near-0% instruction recall. Suggests the model is reasoning (poorly), not recalling. But one informal test is not rigorous evidence — the controls above are needed.

### What This Means

The original 11-20 game is a calibration point. Variants are where the clean evidence lives. The main finding of the project comes from variant results, not the original game.

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
| Direct prediction (unnamed) | Game rules only | Full distribution (JSON) | 1 call | Explicit knowledge of human behavior |
| Direct prediction (named) | Game rules + paper citation | Full distribution (JSON) | 1 call | Contamination: does naming shift prediction? |
| Direct prediction (variants) | Variant rules only | Full distribution (JSON) | 1 call each | Reasoning vs recall (no published data exists) |
| Bare role-play | Game rules, "you are a participant" | Single choice | N=50, temp=1 | Implicit behavioral priors |
| Persona role-play | Paper's exact persona prompts | Single choice | N=50, temp=1 | Does persona pipeline still help? |

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

1. Direct prediction (unnamed): Opus on original 11-20 game — 1 call
2. Direct prediction (named): Opus on same game with citation — 1 call
3. Direct prediction (variants): Opus on 3 parameter variants — 3 calls
4. Compute metrics, compare named/unnamed/variants to theory and published data
5. Bare role-play: Opus on original game, N=50 — assess implicit vs explicit gap
6. Repeat steps 1-5 with Sonnet (tests capability scaling)
7. Persona role-play (if results from steps 1-5 are interesting)
8. Write report and Twitter thread

**Cost note:** All calls can run via `claude -p` under Max subscription (officially supported by Anthropic TOS for automation via CLI). No paid API key needed. Steps 1-4 are ~7 calls total. Step 5 is 50 calls. Weekly token limits apply (Max = 20× Pro).

## What We Have

### Verified Data
- Arad & Rubinstein (2012) human data: n=108, cross-checked across 4 sources
- Manning & Horton persona prompts: extracted from TeX source, verified against paper
- 1,500 novel game configurations: pulled from Expected Parrot via EDSL
- Paper TeX source with full methodology details

### Code (reviewed, 25 tests passing)
- src/games.py — 11-20 game definition with verified human data
- src/simulate.py — direct prediction + sampling methods (needs rewrite for `claude -p`)
- src/metrics.py — KL, TV, log-likelihood (14 tests)
- src/baselines.py — Nash, level-k, uniform (11 tests)
- src/analysis.py — plotting and comparison

### Missing
- Human response data for the 1,500 novel games (collected via Prolific, not publicly released)
- GPT-4o API access (optional)

## Open Questions for Jörn

1. **Contact authors:** Should we email Manning & Horton asking for the human response data on the 1,500 games? (Would give us clean ground truth for novel games.)
2. **Scope of variant testing:** 3 variants sufficient, or more? (More variants = stronger evidence but more calls against Max weekly limit.)

## Deliverables

1. GitHub repo (public)
2. Report (report.md, ~1500-2500 words)
3. Twitter/X thread draft (6-10 tweets)

## Priorities (cut from bottom)

1. Direct prediction on original + variants + named/unnamed, Claude Opus 4.6 (core result)
2. Add bare role-play on original game (explicit vs implicit comparison)
3. Add Sonnet (capability scaling)
4. Add persona role-play condition (is the pipeline still needed?)
5. Add GPT-4o (direct paper comparison — requires API key)
6. Test on 1,500 novel games (requires human data from authors)
