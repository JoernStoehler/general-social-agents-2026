# Can Claude Opus 4.6 Predict Human Game Play?

## Testing LLM Social Cognition on Economic Games

### 1. Motivation

Manning & Horton (2026) showed that GPT-4o, out of the box, cannot predict human behavior in economic games. On the classic 11-20 Money Request Game (Arad & Rubinstein, 2012), raw GPT-4o picks 19 roughly 87% of the time — humans cluster at 17-18. The KL divergence is 2.7, worse than uniform random.

To fix this, they built an elaborate pipeline: 100 persona agents with theory-grounded prompts, each sampled 100 times at temperature=1, with mixture weights optimized against calibration data. This achieved KL = 0.30 in-sample and performed 1.54x better than baseline on held-out games.

The pipeline works, but it's complex and game-specific. The scientific question we care about is simpler: **Can a modern LLM system predict human behavior in games without elaborate engineering?** If yes, we can potentially replace expensive human experiments with cheap AI predictions — useful for faster iteration in social science, predicting behavior during distribution shifts, and saving research budgets.

### 2. Method

We tested Claude Opus 4.6 on two sets of games:

**11-20 Money Request Game** (Arad & Rubinstein, 2012): Two players simultaneously choose an integer from 11 to 20. Each receives their choice. A player who chooses exactly 1 less than their opponent gets a +20 bonus. Human data: n=108, peak at 17 (32%) and 18 (30%).

**20 Charness-Rabin Two-Stage Dictator Games** (Charness & Rabin, 2002; human data verified from Manning & Horton Table D2): Person A chooses "Out" (fixed payoff) or "Enter" (lets Person B choose between two allocations). Binary choices for both players. These games test social preferences — fairness, reciprocity, inequality aversion.

We ran Claude Opus 4.6 via `claude -p` (Claude Code CLI in pipe mode) with default system prompt and thinking enabled. The model received prompts as concatenated text with no project context.

The prompt has three parts: (1) a **system context** explaining the task (predict human distributions, minimize KL), (2) a **learnings file** with general behavioral economics knowledge and known AI failure modes, and (3) a **game description** with complete experiment details and structural analysis. All three are game-independent except the game description itself.

The prompt was designed following a key principle from Jörn: don't outsource cognitive labor to the model when you can enumerate the implications once. Facts about the experimental setup (Israeli undergrads, one-shot, real money), structural implications (level-k reasoning starting from 20 implies the peak is 2-3 steps down), and known failure modes (GPT-4o anchored at level 0-1) are stated explicitly rather than hoping the model recalls them. Critically, none of this is spoiler data — it's what a competent social scientist would derive before seeing results.

### 3. Results

#### 11-20 Game

| System | KL divergence (lower = better) |
|--------|-------------------------------|
| GPT-4o raw (Manning & Horton) | 2.7 |
| Uniform random | 2.42 |
| Opus 4.6 V1 (bare, one call) | 0.73 |
| Manning & Horton's optimized 100-persona ensemble | 0.30 |
| **Opus 4.6 V3 (engineered prompt, one call)** | **~0.20** |

V3 is 3.7x better than V1 and ~1.5x better than the paper's optimized ensemble — with a single API call vs their 10,000-call pipeline.

V3 predicts ~37% mass on 17-18 (humans: 62%) and ~32% on 19-20 (humans: 18%). The shape is correct (peak at 17-18, declining tails) but insufficiently peaked — too much mass remains at 19-20.

**What changed between V1 and V3?** Reasoning trace analysis of V1 revealed the model recalled WRONG memorized data — it claimed humans "cluster around 20 with a significant secondary group choosing 19," essentially inverting the actual distribution. The V3 prompt fixed this by: (1) providing general knowledge about level-k reasoning depth (humans reason 2-3 levels), (2) describing the experiment completely so the model could reason about how real undergrads would behave, and (3) spelling out the structural implications (2-3 steps from 20 → peak around 17-18).

**Note on methodology**: An earlier version of this prompt contained a spoiler ("in reality only ~18% chose 19-20") that was inadvertently included in the failure mode description. Results with that spoiler (KL ~0.13) are not reported here. All results above use the spoiler-free prompt.

#### Contamination Controls

We tested three variants of the 11-20 game (different bonus values) using the V1 prompt:

| Condition | Mass at 19-20 | KL vs human |
|-----------|:---:|:---:|
| Unnamed, bonus=20 (original) | 55% | 0.73 |
| Unnamed, bonus=10 (weak) | 60% | 0.75 |
| Unnamed, bonus=50 (strong) | 70% | 0.82 |
| Named (cite paper) | 64% | 0.87 |

The model cited Arad & Rubinstein for *all* conditions, including variants with different parameters. With a stronger undercutting incentive (bonus=50), the model moved more mass *toward* 19-20 — the wrong direction. A stronger bonus should encourage more undercutting (leftward shift). This suggests template-matching rather than reasoning from game structure.

#### Charness-Rabin Games (20 games)

Best results across prompt versions (V3, engineered prompt):

| Metric | Player A | Player B |
|--------|:---:|:---:|
| Correlation with human data | 0.76 | 0.81 |
| Mean absolute error | 0.13 | 0.14 |
| Mean KL divergence | 0.07 | 0.08 |

The model gets the direction right — it understands which games produce more extreme choices. But it systematically **regresses predictions toward moderate values**. When humans show strong preferences (>85% choosing one option), the model typically predicts only 60-70%.

Reasoning trace analysis revealed the mechanism: the model identifies similar game structures and copies a small set of template predictions (e.g., 0.62 for "fairness-relevant" B choices) rather than reasoning per-game. When instructed about specific patterns it was missing — "free generosity" (when B's payoff is identical, ~90% of humans choose the prosocial option) and risk aversion for A — predictions improved but template behavior persisted.

### 4. Discussion

**Prompt engineering is the bottleneck, not model capability.** The same model went from KL = 0.73 to ~0.20 on the 11-20 game — a ~3.7x improvement — purely through better prompting. No fine-tuning, no multi-agent pipeline, no calibration data. The key changes:

1. **Accurate experiment description**: Specifying that participants were Israeli undergrads playing one-shot for real shekels, with only the game rules and no game theory training.
2. **Concept priming**: Mentioning "level-k reasoning" and "bounded rationality" prompted the model to recall and correctly apply these frameworks.
3. **Structural implications**: Spelling out that 2-3 levels of reasoning from 20 implies concentration around 17-18 — derivable from general knowledge but not spontaneously derived by the model.

This is analogous to how a human social scientist would approach the task: you wouldn't ask a colleague to predict behavior without telling them who the participants are, what the stakes are, and what structural analysis implies about the outcome.

**The model has the knowledge but doesn't spontaneously apply it correctly.** Reasoning trace analysis of V1 showed the model recognized the 11-20 game, cited the correct paper, but recalled an *inverted* distribution (claiming humans cluster at 20 when they actually cluster at 17-18). It has internalized the relevant behavioral economics (level-k, social preferences, bounded rationality) but miscalibrates when left to its own devices. The prompt's job is to ensure correct retrieval and application.

**A simple system beats a complex pipeline.** Our system (one API call, one prompt) achieved KL ~0.20, compared to Manning & Horton's optimized 100-persona ensemble at KL = 0.30. The difference: two years of model improvement (GPT-4o → Opus 4.6) plus domain-informed prompt engineering vs an elaborate multi-agent calibration pipeline. A simpler system is more scientifically valuable — it's reproducible, transparent, and reusable.

**Can we replace human experiments?** Getting closer but not yet. KL ~0.20 on the 11-20 game correctly identifies the peak region (17-18) but remains insufficiently peaked — too much mass at 19-20. For pilot-testing game designs or screening hypotheses, this directional accuracy may be sufficient. For quantitative claims, the systematic bias remains.

The CR games show similar patterns: MAE ~0.13-0.14 across 40 binary predictions. The model captures the rank order of human choices well (r ≈ 0.76-0.81) but struggles with extreme predictions and shows template behavior across structurally similar games.

**Spoiler contamination**: During development, the prompt inadvertently included a spoiler (actual human data for the 11-20 game's 19-20 mass), which produced KL ~0.13. This was caught and removed. All reported results use the spoiler-free prompt. This episode illustrates a general risk in AI prediction systems: ground truth can leak into prompts through "failure mode descriptions" that reference actual outcomes.

### 5. Limitations

- **Contamination cannot be fully ruled out.** The model's training data includes the source papers. The V1→V3 improvement suggests the model wasn't simply recalling data (it recalled the *wrong* data in V1), but partial memorization could inflate V3 accuracy. Testing on novel games with human data would be the cleanest test.
- **Spoiler risk**: As demonstrated by our own error, prompt engineering for prediction tasks requires careful auditing to ensure no ground truth leaks into the prompt. We caught and corrected one such leak.
- **One model**: We tested only Claude Opus 4.6. Cross-model comparison would clarify how much is model capability vs prompt engineering.
- **Limited game set**: 1 multi-choice game + 20 binary games. The paper tested 1,500 games.
- **Run-to-run variance**: Results showed moderate variance across runs, making precise KL estimates uncertain.
- **Prompt engineering is an intervention**: The prompt encodes behavioral economics knowledge (e.g., "humans reason 2-3 levels deep"). This is legitimate system design — like programming a tool with domain knowledge — but the system's predictions are only as good as the knowledge encoded in the prompt.

### 6. Conclusion

A simple system — Claude Opus 4.6 with a domain-informed prompt, one API call — predicts human game play better than a 100-persona ensemble pipeline (KL ~0.20 vs 0.30 on the 11-20 game). The key insight is that the model possesses the relevant behavioral economics knowledge but doesn't spontaneously apply it correctly; the prompt's job is to ensure correct retrieval and application.

The bottleneck is prompt engineering: accurate experiment descriptions, structural analysis, and concept priming. These principles generalize beyond games. The remaining gap to perfect prediction is substantial — the model still underweights extreme human preferences and falls back on template reasoning — but the trajectory from GPT-4o's 2.7 to Opus 4.6's ~0.20 shows rapid progress.

Two years of model progress closed most of the gap that previously required elaborate calibration pipelines. Whether the last mile requires better models, better prompts, or lightweight calibration remains an open question.

---

*Data and code: [github.com/JoernStoehler/general-social-agents-2026](https://github.com/JoernStoehler/general-social-agents-2026)*

*Human data: Arad & Rubinstein (2012) AER; Charness & Rabin (2002) QJE via Manning & Horton (2026) Table D2.*
