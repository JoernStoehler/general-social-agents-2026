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

We ran Claude Opus 4.6 via `claude -p` (Claude Code CLI in pipe mode) with default system prompt and thinking enabled. The model received the prompt as concatenated text with no project context.

For the 11-20 game, the prompt is a self-contained document with: (1) the task (predict human distributions, minimize KL), (2) complete experiment details (participants, setting, instructions), (3) structural analysis with epistemic hedging (facts, reasonable inferences, guesstimates), and (4) known AI failure modes. For the CR games, the prompt uses a shared system context and learnings file plus the game descriptions.

The prompts were designed following a key principle: don't outsource cognitive labor to the model when you can enumerate the implications once. Facts about the experimental setup (Israeli undergrads, one-shot, real money), structural implications (level-k reasoning starting from 20 implies the peak is 2-3 steps down), and known failure modes are stated explicitly rather than hoping the model recalls them. None of this is spoiler data — it's what a competent social scientist would derive before seeing results.

**KL methodology note**: We report D_KL(human || predicted), which measures how well the prediction covers where humans actually go (in nats, with ε = 10⁻¹⁰ smoothing for zero-mass bins). Manning & Horton report D_KL(predicted || human), which additionally penalizes mass at zero-human bins. We report their metric where comparable.

### 3. Results

#### 11-20 Game

| System | D_KL(h‖q) |
|--------|:---------:|
| GPT-4o raw (Manning & Horton) | ~1.8* |
| Opus 4.6, bare prompt (V1) | 0.47 |
| **Opus 4.6, engineered prompt** | **0.14** |

*Estimated from their reported distribution. Manning & Horton report D_KL(q‖h) = 2.7; we report D_KL(h‖q) throughout because it better measures how well the prediction covers human behavior.

The engineered prompt is 3.4x better than the bare prompt. It predicts 45% mass on 17-18 (humans: 62%) and 25% on 19-20 (humans: 18%). The shape is qualitatively correct — peak at the right place, correct ordering — but still insufficiently peaked.

**What changed?** Reasoning trace analysis of the bare prompt revealed the model recalled WRONG memorized data — it claimed humans "cluster around 20 with a significant secondary group choosing 19," essentially inverting the actual distribution. The engineered prompt fixed this by: (1) providing general knowledge about level-k reasoning depth (humans reason 2-3 levels), (2) describing the experiment completely so the model could reason about how real undergrads would behave, and (3) spelling out the structural implications (2-3 steps from 20 → peak around 17-18).

The result is deterministic: 5 parallel runs of the engineered prompt produced identical output.

**Spoiler note**: An earlier version inadvertently included actual human data in a failure mode description. It was caught and removed. All results above use the audited spoiler-free prompt.

#### Contamination Controls

We tested three variants of the 11-20 game (different bonus values) using the bare prompt:

| Condition | D_KL(h‖q) |
|-----------|:---------:|
| Unnamed, bonus=20 (original) | 0.47 |
| Unnamed, bonus=10 (weak) | 0.54 |
| Unnamed, bonus=50 (strong) | 0.78 |
| Named (cite paper) | 0.54 |

Note: KL values computed against the *original* human data (bonus=20), since human data for variant games doesn't exist. These measure whether the model adjusts its predictions when the game changes.

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

**Prompt engineering matters enormously.** The same model went from D_KL(h‖q) = 0.47 to 0.14 on the 11-20 game — a 3.4x improvement — purely through better prompting. No fine-tuning, no multi-agent pipeline, no calibration data. The key changes:

1. **Accurate experiment description**: Specifying that participants were Israeli undergrads playing one-shot for real shekels, with only the game rules and no game theory training.
2. **Concept priming**: Mentioning "level-k reasoning" and "bounded rationality" prompted the model to recall and correctly apply these frameworks.
3. **Structural implications**: Spelling out that 2-3 levels of reasoning from 20 implies concentration around 17-18 — derivable from general knowledge but not spontaneously derived by the model.

**The model has the knowledge but doesn't spontaneously apply it correctly.** Reasoning trace analysis of V1 showed the model recognized the 11-20 game, cited the correct paper, but recalled an *inverted* distribution (claiming humans cluster at 20 when they actually cluster at 17-18). It has internalized the relevant behavioral economics (level-k, social preferences, bounded rationality) but miscalibrates when left to its own devices. The prompt's job is to ensure correct retrieval and application.

**A simple system gets surprisingly close.** Our system (one API call, one prompt) achieved D_KL(h‖q) = 0.14 on the 11-20 game. Direct comparison with Manning & Horton's D_KL(q‖h) = 0.30 requires care since the metrics differ in direction and smoothing, but our prediction places mass in the right region (peak at 17-18) with one call vs their ten thousand.

**Can we replace human experiments?** Not yet, but the results are directionally promising. The model correctly identifies the peak region (17-18) and the rank order of preferences across CR games (r = 0.79-0.85). For screening game designs or testing hypotheses qualitatively, this level of accuracy may be useful. For quantitative claims, the systematic bias (regression toward moderate predictions, template behavior) remains a barrier.

**Spoiler contamination**: During development, the prompt inadvertently included actual human data in a failure mode description. This was caught and removed via systematic audit. All reported results use the audited spoiler-free prompt. This episode illustrates a general risk: ground truth can leak into prompts through "failure mode descriptions" that reference actual outcomes.

### 5. Limitations

- **Contamination cannot be fully ruled out.** The model's training data includes the source papers. The V1→V3 improvement suggests the model wasn't simply recalling data (it recalled the *wrong* data in V1), but partial memorization could inflate V3 accuracy. Testing on novel games with human data would be the cleanest test.
- **One model**: We tested only Claude Opus 4.6. Cross-model comparison would clarify how much is model capability vs prompt engineering.
- **Limited game set**: 1 multi-choice game + 20 binary games. The paper tested 1,500 games.
- **Prompt engineering is an intervention**: The prompt encodes behavioral economics knowledge (e.g., "humans reason 2-3 levels deep"). This is legitimate system design — like programming a tool with domain knowledge — but the system's predictions are only as good as the knowledge encoded in the prompt.
- **Metric comparability**: We report D_KL(h‖q); Manning & Horton report D_KL(q‖h). Direct numerical comparison across directions is not meaningful without re-computing in the same direction with the same smoothing.

### 6. Conclusion

A simple system — Claude Opus 4.6 with a domain-informed prompt, one API call — predicts human game play at D_KL(h‖q) = 0.14 on the 11-20 game. The key insight is that the model possesses the relevant behavioral economics knowledge but doesn't spontaneously apply it correctly; the prompt's job is to ensure correct retrieval and application.

The bottleneck is prompt engineering, not model capability. Better experiment descriptions, concept priming, and structural analysis produced a 3.4x improvement. These principles generalize beyond games.

---

*Data and code: [github.com/JoernStoehler/general-social-agents-2026](https://github.com/JoernStoehler/general-social-agents-2026)*

*Human data: Arad & Rubinstein (2012) AER; Charness & Rabin (2002) QJE via Manning & Horton (2026) Table D2.*
