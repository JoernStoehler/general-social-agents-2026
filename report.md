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

We ran Claude Opus 4.6 via `claude -p` (Claude Code CLI in pipe mode) with default system prompt and tools enabled. The model read prompt files from a clean directory with no project context. We tested two system configurations:

- **V1 (bare)**: Game descriptions only
- **V2 (with context)**: Added a context file with general behavioral principles and a learnings file with diagnostic feedback from V1

### 3. Results

#### 11-20 Game

| System | KL divergence (lower = better) |
|--------|-------------------------------|
| GPT-4o raw (Manning & Horton) | 2.7 |
| Uniform random | 2.42 |
| **Claude Opus 4.6, one call** | **0.73** |
| Manning & Horton's optimized ensemble | 0.30 |

Opus is 3.7x better than raw GPT-4o. It puts 26% mass on 17-18 (vs humans' 62%) and 55% on 19-20 (vs humans' 18%). It applies level-k reasoning but anchors at level 0-1 — humans reason 2-3 levels deep.

The model spontaneously identified the game as "the well-known game studied by Arad and Rubinstein (2012)" despite receiving only the rules. It has the framework correct (level-k reasoning) but miscalibrates the depth.

#### Contamination Controls

We tested three variants of the 11-20 game (different bonus values) and a named condition (citing the paper explicitly):

| Condition | Mass at 19-20 | KL vs human |
|-----------|:---:|:---:|
| Unnamed, bonus=20 (original) | 55% | 0.73 |
| Unnamed, bonus=10 (weak) | 60% | 0.75 |
| Unnamed, bonus=50 (strong) | 70% | 0.82 |
| Named (cite paper) | 64% | 0.87 |

The model cited Arad & Rubinstein for *all* conditions, including variants with different parameters. With a stronger undercutting incentive (bonus=50), the model moved more mass *toward* 19-20 — the wrong direction. A stronger bonus should encourage more undercutting (leftward shift). This suggests template-matching rather than reasoning from game structure.

#### Charness-Rabin Games (20 games)

| Metric | Player A | Player B |
|--------|:---:|:---:|
| Correlation with human data | 0.73 | 0.83 |
| Mean absolute error | 0.14 | 0.14 |
| Mean KL divergence | 0.07 | 0.09 |

The model gets the direction right — it understands which games will produce more extreme choices. But it systematically **regresses predictions toward 50-50**. When humans show strong preferences (near 0% or 100%), the model predicts moderate ones (40-60%).

A telling signal: 7 of 20 Player B predictions were exactly 0.62, suggesting a "fairness heuristic" applied uniformly rather than per-game reasoning.

#### V2 (With Context) vs V1 (Bare)

Adding a context file ("humans reason deeper than level 0-1," "don't hedge to 50-50") had mixed effects:

| | Player A MAE | Player B MAE |
|---|:---:|:---:|
| V1 (bare) | 0.142 | 0.139 |
| V2 (context) | 0.132 | 0.158 |

Player A improved; Player B worsened. The generic advice over-corrected on some games. This suggests the system needs game-specific reasoning, not just calibration adjustments.

### 4. Discussion

**The model is a mediocre social scientist, not a bad one.** Its predictions are correlated with human behavior (r = 0.73-0.83 across 20 binary games) and dramatically better than naive game-theoretic predictions. But it has systematic biases:

1. **Level-k miscalibration**: It underestimates how deeply humans reason in strategic games.
2. **Regression to mean**: It predicts moderate proportions when humans show strong preferences.
3. **Template behavior**: It applies generic frameworks rather than reasoning about each game's specific structure.

These are the errors of a student who has read the textbook but hasn't run experiments. The model knows about level-k reasoning and social preferences, but it hasn't calibrated this knowledge against actual human data — or has calibrated poorly.

**Is the model recalling or reasoning?** It recognized the 11-20 game from its training data and cited the correct paper. But it got the distribution substantially wrong (predicted 35% on 20; actual is 6%). On the Charness-Rabin games, it used a small set of default predictions rather than game-specific values. This pattern is more consistent with "applying a learned framework incorrectly" than "recalling memorized data."

**Can we replace human experiments?** Not yet, at this accuracy level. A mean absolute error of 14 percentage points on binary games and KL = 0.73 on the 11-20 game means the predictions would be directionally useful but quantitatively unreliable. For the purpose of, say, pilot-testing whether a game design works, AI predictions might be sufficient. For actual scientific claims about human behavior, they are not.

**How much room for improvement?** The v2 experiment shows that naive prompt engineering has limited value — generic advice helps some games and hurts others. The Manning & Horton pipeline (KL = 0.30) demonstrates that systematic calibration does work, even with a weaker base model. A promising direction is iterative learning: accumulating prediction principles across runs while carefully avoiding overfitting to specific games.

### 5. Limitations

- **One model**: We tested only Claude Opus 4.6. Cross-model comparison (Sonnet, GPT-4o) would strengthen conclusions.
- **Limited game set**: 1 multi-choice game + 20 binary games. The paper tested 1,500 games with human data we don't have access to.
- **Single run per condition**: No repeated measurements to estimate variance.
- **Contamination**: The model's training data includes the source papers. We cannot fully separate learned knowledge from memorized data, only analyze the pattern of errors.
- **Prompt sensitivity**: Different phrasings could yield different predictions. We tested two prompt variants with mixed results.

### 6. Conclusion

Claude Opus 4.6, with zero engineering, predicts human game play 3.7x better than raw GPT-4o (KL 0.73 vs 2.7). It correlates well with human behavior across 20 diverse allocation games (r = 0.73-0.83). But it falls short of the engineered ensemble approach (KL 0.30) and shows systematic biases: underestimating human strategic depth and regressing predictions toward 50-50.

The gap between "decent correlation" and "accurate enough to replace experiments" remains real. Two years of model progress closed about 80% of the gap between GPT-4o's baseline and the optimized ensemble, but the last 20% — precisely calibrated social cognition — may require either more capable models or lightweight calibration techniques.

---

*Data and code: [github.com/JoernStoehler/general-social-agents-2026](https://github.com/JoernStoehler/general-social-agents-2026)*

*Human data: Arad & Rubinstein (2012) AER; Charness & Rabin (2002) QJE via Manning & Horton (2026) Table D2.*
