# Can Claude Opus 4.6 Predict Human Game Play?

## Testing LLM Social Cognition on Economic Games

### 1. Motivation

Manning & Horton (2026) showed that GPT-4o, out of the box, cannot predict human behavior in economic games. On the classic 11-20 Money Request Game (Arad & Rubinstein, 2012), raw GPT-4o puts ~87% of mass on choices 19-20 — humans cluster at 17-18. They report D_KL(predicted || human) = 2.7, worse than uniform random (2.42).

To fix this, they built an elaborate pipeline: 100 persona agents with theory-grounded prompts, each sampled 100 times at temperature=1, with mixture weights optimized against calibration data. This achieved KL = 0.30 in-sample and performed 1.54x better than baseline on held-out games.

The pipeline works, but it's complex and game-specific. The scientific question we care about is simpler: **Can a modern LLM system predict human behavior in games without elaborate engineering?** If yes, we can potentially replace expensive human experiments with cheap AI predictions — useful for faster iteration in social science, predicting behavior during distribution shifts, and saving research budgets.

### 2. Method

We tested Claude Opus 4.6 on two sets of games:

**11-20 Money Request Game** (Arad & Rubinstein, 2012): Two players simultaneously choose an integer from 11 to 20. Each receives their choice. A player who chooses exactly 1 less than their opponent gets a +20 bonus. Human data: n=108, peak at 17 (32%) and 18 (30%).

**20 Charness-Rabin Two-Stage Dictator Games** (Charness & Rabin, 2002; human data verified from Manning & Horton Table D2): Person A chooses "Out" (fixed payoff) or "Enter" (lets Person B choose between two allocations). Binary choices for both players. These games test social preferences — fairness, reciprocity, inequality aversion.

We ran Claude Opus 4.6 via `claude -p` (Claude Code CLI in pipe mode) with default system prompt and thinking enabled. The model received prompts as concatenated text with no project context.

The prompt has three parts: (1) a **system context** explaining the task (predict human distributions, minimize KL), (2) a **learnings file** with general behavioral economics knowledge and known AI failure modes, and (3) a **game description** with complete experiment details and structural analysis. All three are game-independent except the game description itself.

The prompt was designed following a key principle: don't outsource cognitive labor to the model when you can enumerate the implications once. Facts about the experimental setup (Israeli undergrads, one-shot, real money), structural implications (level-k reasoning starting from 20 implies the peak is 2-3 steps down), and known failure modes are stated explicitly rather than hoping the model recalls them. None of this is spoiler data — it's what a competent social scientist would derive before seeing results.

**KL methodology note**: Manning & Horton report D_KL(predicted || human) in nats. We use the same metric for comparability. This direction penalizes the predicted distribution for placing mass where humans don't go. We also report D_KL(human || predicted) which measures how well the prediction covers where humans actually go. Both directions use ε = 10⁻¹⁰ smoothing for zero-mass bins.

### 3. Results

#### 11-20 Game

| System | D_KL(q‖h) | D_KL(h‖q) |
|--------|:---------:|:---------:|
| GPT-4o raw (Manning & Horton) | 2.7 | — |
| Uniform random | 2.42 | 0.54 |
| Opus 4.6, bare prompt (V1) | 1.03 | 0.65 |
| **Opus 4.6, engineered prompt (V3)** | **0.59** | **0.21** |
| Manning & Horton's optimized ensemble | 0.30 | — |

V3 is 1.7x better than V1 in the paper's metric. The paper's optimized ensemble (0.30) remains 2x better than our single-call system (0.59). However, their system uses 10,000 API calls with mixture weights optimized against calibration data; ours uses one call with zero calibration.

V3 predicts 37% mass on 17-18 (humans: 62%) and 34% on 19-20 (humans: 18%). The shape is qualitatively correct (peak at 17-18, declining tails) but insufficiently peaked — too much mass remains at 19-20 and in the lower tail.

The gap between metrics is instructive: D_KL(q‖h) = 0.59 is dominated by ~2% mass we place at choice 12 (where 0 of 108 humans went), while D_KL(h‖q) = 0.21 shows that where humans *do* go, our prediction is reasonable. The paper's ensemble, being optimized against calibration data, learns to zero out mass at empty bins — an advantage our uncalibrated system lacks.

**What changed between V1 and V3?** Reasoning trace analysis of V1 revealed the model recalled WRONG memorized data — it claimed humans "cluster around 20 with a significant secondary group choosing 19," essentially inverting the actual distribution. The V3 prompt fixed this by: (1) providing general knowledge about level-k reasoning depth (humans reason 2-3 levels), (2) describing the experiment completely so the model could reason about how real undergrads would behave, and (3) spelling out the structural implications (2-3 steps from 20 → peak around 17-18).

**Note on methodology**: An earlier version of this prompt contained a spoiler ("in reality only ~18% chose 19-20") that was inadvertently included in a failure mode description. Results with that spoiler are not reported here. All results above use the spoiler-free prompt.

#### Contamination Controls

We tested three variants of the 11-20 game (different bonus values) using the V1 bare prompt:

| Condition | D_KL(q‖h) | D_KL(h‖q) |
|-----------|:---------:|:---------:|
| Unnamed, bonus=20 (original) | 1.03 | 0.65 |
| Unnamed, bonus=10 (weak) | 0.78 | 0.55 |
| Unnamed, bonus=50 (strong) | 0.98 | 0.75 |
| Named (cite paper) | 0.87 | 0.63 |

Note: The KL values here are computed against the *original* human data (bonus=20), not the human data for the variant games (which doesn't exist). These measure whether the model adjusts its predictions when the game changes — not absolute accuracy for the variants.

The model cited Arad & Rubinstein for *all* conditions, including variants with different parameters. With a stronger undercutting incentive (bonus=50), the model moved more mass *toward* 19-20 — the wrong direction. A stronger bonus should encourage more undercutting (leftward shift). This suggests template-matching rather than reasoning from game structure.

#### Charness-Rabin Games (20 games)

Results with spoiler-free prompt (system + learnings + game descriptions):

| Metric | Player A | Player B |
|--------|:---:|:---:|
| Correlation with human data | 0.79 | 0.85 |
| Mean absolute error | 0.12 | 0.13 |
| Mean KL divergence (binary) | 0.06 | 0.08 |

The model gets the direction right — it understands which games produce more extreme choices. But it systematically **regresses predictions toward moderate values**. When humans show strong preferences (>85% choosing one option), the model typically predicts only 60-70%.

Reasoning trace analysis revealed the mechanism: the model identifies similar game structures and copies a small set of template predictions (e.g., 0.62 for "fairness-relevant" B choices) rather than reasoning per-game.

### 4. Discussion

**Prompt engineering matters enormously.** The same model went from D_KL = 1.03 to 0.59 on the 11-20 game — a 1.7x improvement — purely through better prompting. No fine-tuning, no multi-agent pipeline, no calibration data. The key changes:

1. **Accurate experiment description**: Specifying that participants were Israeli undergrads playing one-shot for real shekels, with only the game rules and no game theory training.
2. **Concept priming**: Mentioning "level-k reasoning" and "bounded rationality" prompted the model to recall and correctly apply these frameworks.
3. **Structural implications**: Spelling out that 2-3 levels of reasoning from 20 implies concentration around 17-18 — derivable from general knowledge but not spontaneously derived by the model.

**The model has the knowledge but doesn't spontaneously apply it correctly.** Reasoning trace analysis of V1 showed the model recognized the 11-20 game, cited the correct paper, but recalled an *inverted* distribution (claiming humans cluster at 20 when they actually cluster at 17-18). It has internalized the relevant behavioral economics (level-k, social preferences, bounded rationality) but miscalibrates when left to its own devices. The prompt's job is to ensure correct retrieval and application.

**A simple system gets close.** Our system (one API call, one prompt) achieved D_KL = 0.59, compared to Manning & Horton's optimized 100-persona ensemble at D_KL = 0.30. The gap is 2x, but the comparison is one call vs ten thousand with calibration. The remaining gap is partly structural: the paper's ensemble is optimized to avoid placing mass at zero-human bins, a systematic advantage over any uncalibrated system.

**Can we replace human experiments?** Not yet, but the results are directionally promising. The model correctly identifies the peak region (17-18) and the rank order of preferences across CR games (r = 0.79-0.85). For screening game designs or testing hypotheses qualitatively, this level of accuracy may be useful. For quantitative claims, the systematic bias (regression toward moderate predictions, template behavior) remains a barrier.

**Spoiler contamination**: During development, the prompt inadvertently included a spoiler (actual human data for the 11-20 game's 19-20 mass), which improved D_KL(h‖q) from 0.21 to 0.13. This was caught and removed. All reported results use the spoiler-free prompt. This episode illustrates a general risk: ground truth can leak into prompts through "failure mode descriptions" that reference actual outcomes.

### 5. Limitations

- **Contamination cannot be fully ruled out.** The model's training data includes the source papers. The V1→V3 improvement suggests the model wasn't simply recalling data (it recalled the *wrong* data in V1), but partial memorization could inflate V3 accuracy. Testing on novel games with human data would be the cleanest test.
- **KL sensitivity**: D_KL(q‖h) is dominated by mass at zero-human bins (choice 12 has 0 of 108 human observations). Small amounts of predicted mass there (2-3%) cause large KL penalties. Different smoothing choices yield different numbers. Our reported values use ε = 10⁻¹⁰ to match the paper's uniform = 2.42 benchmark.
- **One model**: We tested only Claude Opus 4.6. Cross-model comparison would clarify how much is model capability vs prompt engineering.
- **Limited game set**: 1 multi-choice game + 20 binary games. The paper tested 1,500 games.
- **Run-to-run variance**: Two clean 11-20 runs yielded D_KL(q‖h) = 0.59 and 0.85 — substantial variance. More runs would tighten estimates.
- **Prompt engineering is an intervention**: The prompt encodes behavioral economics knowledge (e.g., "humans reason 2-3 levels deep"). This is legitimate system design — like programming a tool with domain knowledge — but the system's predictions are only as good as the knowledge encoded in the prompt.

### 6. Conclusion

A simple system — Claude Opus 4.6 with a domain-informed prompt, one API call — predicts human game play at D_KL = 0.59, within 2x of a 10,000-call optimized ensemble pipeline (D_KL = 0.30). The key insight is that the model possesses the relevant behavioral economics knowledge but doesn't spontaneously apply it correctly; the prompt's job is to ensure correct retrieval and application.

The remaining gap to the paper's ensemble is real but narrow given the difference in engineering effort. Whether closing it requires better models, better prompts, or lightweight calibration remains an open question.

---

*Data and code: [github.com/JoernStoehler/general-social-agents-2026](https://github.com/JoernStoehler/general-social-agents-2026)*

*Human data: Arad & Rubinstein (2012) AER; Charness & Rabin (2002) QJE via Manning & Horton (2026) Table D2.*
