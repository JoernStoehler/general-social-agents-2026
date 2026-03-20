# Manning & Horton (2026) "General Social Agents" — Key Details

Extracted verbatim from LaTeX source at `results/reference/manning_horton_2026_source/`.

---

## 1. Methodology

### Model and Hyperparameters

- **Model**: GPT-4o (referred to throughout as `\textsc{Gpt-4o}`)
- **Temperature**: 1 (explicitly set for all simulation calls)
- **Quote from paper**: "All simulations use \textsc{Gpt-4o} with the temperature set to 1, though the approach is agnostic to the choice of model and hyperparameters. \textsc{Gpt-4o}, among the most widely used LLMs, and the temperature setting are defaults for the software used to run our simulations."
- **Software platform**: EDSL (Expected Parrot), `https://www.expectedparrot.com/`

### Sample Sizes

- **Baseline elicitation (basic 11-20 game)**: GPT-4o prompted 1,000 times with no additional instructions
- **Candidate persona elicitation**: 100 responses per persona (10 personas × 100 = 1,000 total for optimization)
- **Optimized strategic sample**: 1,000 agents assigned by mixture weights (for validation games)
- **Large-scale experiment**: 100 agents per game × 1,500 games = ~150,000 per sample; ~300,000 total AI responses
- **Charness & Rabin (CR) appendix**: 1,000 responses per setting for baseline; 30 responses per agent for optimization search; 150 responses per game for validation

### Chain-of-Thought Prompting Structure

All persona responses in the 11-20 game use **two sequential prompts**:

**Prompt 1:**
> {11-20 game instructions}. Reason out a few settings according to your personality and how others might respond.

**Prompt 2:**
> {11-20 game instructions}. You previously had the following thoughts: {Response to prompt 1}. What amount of money would you request?

This implements chain-of-thought reasoning before the final answer. The paper cites Wei et al. (2024) for COT prompting.

---

## 2. Exact Game Instruction Text

### Basic 11-20 Game (original Arad & Rubinstein, used as training data)

> You and another player are playing a game in which each player requests an amount of money. The amount must be (an integer) between 11 and 20 shekels. Each player will receive the amount he requests. A player will receive an additional amount of 20 shekels if he asks for exactly one shekel less than the other player. What amount of money would you request?

### Cycle 11-20 Game (validation data)

> You and another player are playing a game in which each player requests an amount of money. The amount must be (an integer) between 11 and 20 shekels. Each player will receive the amount of money he requests. A player will receive an additional amount of 20 shekels if: (i) he asks for exactly one shekel less than the other player or (ii) he asks for 20 shekels and the other player asks for 11 shekels. What amount of money would you request?

### Costless 11-20 Game (validation data)

> You and another player are playing a game in which each player chooses an integer in the range 11-20. A player who chooses 20 will receive 20 shekels (regardless of the other player's choice). A player who chooses any other number in this range will receive three shekels less than in the case where he chooses 20. However, he will receive an additional amount of 20 shekels if he chooses a number that is one less than that chosen by the other player. Which number would you choose?

### Basic 1-10 Game (novel target game, Prolific participants)

> You are going to play a game where you must select a whole number between 1 and 10. You will receive a number of points equivalent to that number. For example, if you select 3, you will get 3 points. If you select 7, you will get 7 points, etc. After you tell us your number, we will randomly pair you with another Prolific worker who is also playing this game. They will also have chosen a number between 1 and 10. If either of you select a number exactly one less than the other player's number, than the player with the lower number will receive an additional 10 points. Please choose a number between 1 and 10.

### Cycle 1-10 Game

> You are going to play a game where you must select a whole number between 1 and 10. You will receive a number of points equivalent to that number. For example, if you select 3, you will get 3 points. If you select 7, you will get 7 points, etc. After you tell us your number, we will randomly pair you with another Prolific worker who is also playing this game. They will also have chosen a number between 1 and 10. There are 2 ways to win an additional 10 points based on both yours and the other player's choice: 1. If either of you select a number exactly one less than the other player's number, then the player with the lower number will receive an additional 10 points. 2. If either of you select 10 and the other selects 1, then the player who chose 10 will receive an additional 10 points. Please choose a number between 1 and 10.

### Costless 1-10 Game

> You are going to play a game where you must select a whole number between 1 and 10. You will receive 10 points if you select the number 10 and you will receive 7 points for selecting any other number. After you tell us your number, we will randomly pair you with another Prolific worker who is also playing this game. They will also have chosen a number between 1 and 10. If either of you select a number exactly one less than the other player's number, than the player with the lower number will receive an additional 10 points. Please choose a number between 1 and 10.

### 1-7 Game

> You are going to play a game where you must select a whole number between 1 and 7. You will receive a number of points equivalent to that number. For example, if you select 3, you will get 3 points. If you select 6, you will get 6 points, etc. After you tell us your number, we will randomly pair you with another Prolific worker who is also playing this game. They will also have chosen a number between 1 and 7. If either of you select a number exactly one less than the other player's number, than the player with the lower number will receive an additional 10 points. Please choose a number between 1 and 7.

---

## 3. Persona Definitions (Table 2 — the 10 Strategic Personas)

**Preamble prepended to ALL personas** (verbatim from paper notes):
> You are a human being with all the cognitive biases and heuristics that come with it.

**K-level explanation included for all personas except "random":**
> A k-level thinker thinks k steps ahead. A 0-level thinker thinks 0 steps and would, therefore, just select the maximum amount that guarantees money.

| Persona Text | Optimized Weight |
|---|---|
| You are generally a 0-level thinker---picking the option with the most guaranteed money. | 0.065 |
| You vary between a 0 and 1-level thinker. | 0.000 |
| You vary between a 1 and 2-level thinker. | 0.000 |
| You vary between a 0, 1, and 2-level thinker. | 0.000 |
| You vary between a 0, 1, 2, and 3-level thinker. | 0.000 |
| You vary between a 1, 2, and 3-level thinker. | 0.469 |
| You vary between a 0, 1, 2, 3, and 4-level thinker. | 0.013 |
| You vary between a 0, 1, 2, 3, 4 and 5-level thinker. | 0.339 |
| You randomly pick between lower numbers because you think that's the best way to win. | 0.114 |
| You are Homo Economicus. | 0.000 |

**Summary of weights**: Most mass on "L1–L3" (47%) and "L0–L5" (34%); random strategy gets 11%; pure L0 gets 6.5%; zero weight on several intermediate types and Homo Economicus.

### Atheoretical Personas (for comparison, Table A1)

**Historical Figures set** — each persona is "You are X" (e.g., "You are Julius Caesar"):
- Julius Caesar: 0.891, Confucius: 0.109, all others: 0.000

**MBTI set** — personas like "You are an ENFP" (also told the letters refer to the Myers-Briggs Type Indicator):
- ENFP: 1.000, all others: 0.000

**Always Pick N set** — "You always like to pick N" for N in {11,...,20}:
- 17: 0.324, 18: 0.296, 19: 0.120, 20: 0.065, 16: 0.065, 14: 0.056, 11: 0.037, 13: 0.028, 15: 0.009, 12: 0.000

---

## 4. Human Distribution (Training Data from Arad & Rubinstein 2012)

### Basic 11-20 Game Human Results (n=108, college students)

| Shekels | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 |
|---|---|---|---|---|---|---|---|---|---|---|
| Level-k | L9 | L8 | L7 | L6 | L5 | L4 | L3 | L2 | L1 | L0 |
| Nash Eq. (%) | 0 | 0 | 0 | 0 | 25 | 25 | 20 | 15 | 10 | 5 |
| Human (%) | 4 | 0 | 3 | 6 | 1 | 6 | 32 | 30 | 12 | 6 |

### Cycle 11-20 Game Human Results (n=72)

| Human (%) | 1 | 1 | 0 | 1 | 0 | 4 | 10 | 22 | 47 | 13 |

### Costless 11-20 Game Human Results (n=53)

Nash Eq. (different): 0 | 0 | 0 | 10 | 15 | 15 | 15 | 15 | 15 | 15

| Human (%) | 0 | 4 | 0 | 4 | 4 | 4 | 9 | 21 | 40 | 15 |

---

## 5. Baseline GPT-4o Distribution (Key Facts)

- **87%** of baseline GPT-4o responses (no persona) chose **19 shekels** in the basic 11-20 game
- This is consistent with Gao et al. (2024) findings — LLMs strongly index on 19 shekels even with diverse prompting, fine-tuning, or demographic traits

---

## 6. Calibration / Optimization Methodology

### Selection Method (used for 11-20 game personas)

**Objective**: Minimize absolute difference between CDFs of human distribution P and mixture distribution:

```
min_w  d(P, sum_theta w_theta * P_hat_theta)
subject to: sum w_theta = 1, w_theta >= 0
```

where d is CDF absolute difference (not KL divergence — they use mean absolute CDF distance for optimization, though KL is reported for performance).

**Process**:
1. Enumerate candidate personas (10 in this case)
2. Elicit 100 responses per persona using GPT-4o at temperature=1 (with COT prompting)
3. Solve the mixture weight optimization using nonlinear programming
4. Apply the weights to construct a sample of 1,000 agents

**Calibration data**: Human responses from the basic 11-20 game only (n=108 observations from Arad & Rubinstein 2012 original paper)

### Construction Method (used for Charness & Rabin allocation games, Appendix)

**Prompt template with numeric parameters**:
> On a scale from 1 to 10, your efficiency level is: {phi_eff}. 10 means you strongly prioritize maximizing combined payoffs, and 1 means you don't care. On a scale from 1 to 10, your self-interest level is: {phi_self}. 10 means you strongly prioritize your own payoffs, and 1 means you don't care. On a scale from 1 to 10, your inequity aversion level is: {phi_ineq}. 10 means you strongly prioritize fairness between players, and 1 means you don't care.

**Optimized parameters**: (phi_eff, phi_self, phi_ineq) = (7,10,10), (3,1,3), (1,10,2) for the three agents.

**Optimization procedure**: Bayesian optimization; 5 random initial samples + 15 additional iterations (20 total evaluations); 30 queries per agent per setting.

**Distance metric for CR**: Mean absolute error (MAE), not KL divergence.

---

## 7. All Quantitative Results

### 11-20 Game KL Divergences (forward KL, human distribution as reference)

| Comparison | KL Divergence |
|---|---|
| Baseline AI vs. human (basic game) | 2.70 |
| Optimized strategic AI vs. human (basic game) | 0.30 |
| Improvement over baseline (basic game) | 89% |
| Historical figures vs. human (basic game) | 2.16 |
| Myers-Briggs vs. human (basic game) | 2.36 |
| Always Pick N vs. human (basic game, in-sample) | 0.00 (perfect fit by construction) |
| Baseline AI vs. human (cycle game) | 0.95 |
| Optimized AI vs. human (cycle game) | 0.28 |
| Improvement over baseline (cycle game) | 71% |
| Baseline AI vs. human (costless game) | 0.93 |
| Optimized AI vs. human (costless game) | 0.15 |
| Improvement over baseline (costless game) | 84% |
| KL divergence between basic and costless human distributions | 1.26 |
| KL divergence between basic and cycle human distributions | 1.00 |
| Optimized AI vs. human (1-7 novel game) | 0.16 |

### 1-10 Novel Games: Improvement of Optimized AI over Baseline

| Game | Improvement |
|---|---|
| Basic 1-10 | 73% |
| Cycle 1-10 | 53% |
| Costless 1-10 | 73% |
| 1-7 game | 73% |
| Range (paper quote) | 53%–73% |

### Large-Scale Experiment: 1,500 Games, Log-Likelihood Ratios (epsilon=0.2)

The metric Lambda-bar is the average per-observation log-likelihood ratio of Strategic AI vs. benchmark (positive = Strategic AI better).

| Benchmark | Lambda-bar | exp(Lambda-bar) | SE | p-value | % Games Strategic AI Wins |
|---|---|---|---|---|---|
| Baseline AI | 0.43 | 1.54 | 0.019 | <0.001 | 71.5% |
| Cognitive Hierarchy (tau=1.5) | 0.39 | 1.48 | 0.029 | <0.001 | 64.0% |
| Harsanyi-Selten Nash | 0.32 | 1.38 | 0.027 | <0.001 | 62.2% |
| Uniform distribution | 0.20 | 1.22 | 0.016 | <0.001 | 64.3% |
| Random pure strategy | 1.44 | 4.21 | 0.026 | <0.001 | 90.2% |

**Interpretation**: The strategic AI assigns 1.54x more probability to actual human responses than baseline GPT-4o, 1.48x more than the cognitive hierarchy model, and 1.38x more than Nash equilibria.

**At epsilon=0.05** (stricter smoothing):

| Benchmark | Lambda-bar | SE | % Games Strategic AI Wins |
|---|---|---|---|
| Baseline AI | 0.668 | 0.027 | 72.6% |
| Cognitive Hierarchy | 0.302 | 0.030 | 59.6% |
| Harsanyi-Selten Nash | 0.924 | 0.039 | 73.0% |
| Uniform | 0.106 | 0.021 | 59.8% |
| Random Pure Strategy | 2.574 | 0.036 | 94.2% |

### Absolute Predictive Accuracy (no smoothing, epsilon=0)

| Metric | Strategic AI | Baseline AI | HS Nash Eq. | Cog. Hierarchy |
|---|---|---|---|---|
| % Humans Choose Max Prob. Strategy | 24.3% | 16.8% | 30.4% | 28.5% |
| % Humans Choose Top 3 Prob. Strategy | 52.9% | 39.1% | 49.6% | 49.5% |
| % Humans Choose Pos. Prob. Strategy | 94.3% | 81.9% | 46.4% | 100.0% |
| % Games Any Human Chooses Pos. Prob. Strategy | 99.3% | 93.7% | 74.7% | 100.0% |
| % Games All Humans Choose Pos. Prob. Strategy | 86.3% | 65.3% | 17.7% | 100.0% |

### Charness & Rabin (CR) Appendix Results

| Metric | Value |
|---|---|
| Baseline MAE (training, 6 settings) | 0.42 |
| Optimized AI MAE (training) | 0.20 |
| Atheoretical AI MAE (training) | 0.42 |
| Optimized AI MAE (validation, Player A) | 0.17 |
| Baseline MAE (validation, Player A) | 0.52 |
| Optimized AI MAE (validation, Player B) | 0.15 |
| Baseline MAE (validation, Player B) | 0.29 |
| Optimized AI MAE (novel 3-player games) | 0.206 |
| Baseline MAE (novel 3-player games) | 0.259 |
| Atheoretical AI MAE (novel 3-player games) | 0.264 |
| % improvement in novel games | ~21% |
| n participants (novel 3-player games) | 494 |
| Optimized AI better than baseline in validation (out of 40) | 31 of 40 settings |

---

## 8. Large-Scale Experiment Details (Section 4)

- **Population of games**: 883,320 unique strategic games (full factorial of parameters, de-duplicated)
- **Sample for experiment**: 1,500 games randomly drawn from population
- **Human subjects**: 4,500 Prolific workers recruited; 4,249 passed attention check; played across 1,490 unique games (some with 1–5 players each)
- **Payment**: $0.50 fixed + 1% chance of performance bonus (averaging $23; max $48)
- **Comprehension check**: Participants calculated correct points for a hypothetical outcome before making choice
- **Games converged for Nash**: 1,487 of 1,500 (fewer than 1% had degeneracy issues)
- **Unique symmetric Nash equilibria**: 467 games; payoff-dominant selected in 328; risk-dominant in 1,026; 59% pure strategy equilibria selected
- **Maximum symmetric Nash equilibria in a single game**: 10,051
- **Smoothing parameter main results**: epsilon=0.2 (80% follow model, 20% uniform random); robustness checks at epsilon in {0.05, 0.10, 0.30}
- **Cognitive hierarchy tau**: 1.5 (from Camerer et al. 2004 meta-analytic estimate)

### Game Parameter Space

| Parameter | Values |
|---|---|
| Lower Bound | {1, 2, ..., 20} |
| Upper Bound | Lower bound + {5, 6, ..., 20} |
| Bonus Size | {1, 2, ..., 20} points |
| Gap | {1, 2, 3, 4} |
| Points Rule | {# - 2, # - 1, #, # + 1, # + 2, costless - 2} |
| Bonus Rule | 11 rules (see below) |

**Bonus Rules**:
- Gap Low: select exactly {gap} less than opponent (competitive)
- Gap High: select exactly {gap} more than opponent (competitive)
- More Than: select more than {gap} above opponent (competitive)
- Gap Abs.: absolute difference from opponent equals {gap} (mutual)
- Equal: same number as opponent (mutual)
- Unequal: different number than opponent (mutual)
- Sum Even: sum of both numbers is even (mutual)
- Sum Odd: sum of both numbers is odd (mutual)
- Coord. Low: both select lower bound (mutual)
- Sum Upper: sum equals upper bound (mutual/not achievable)
- Less Upper: sum less than upper bound (mutual/not achievable)

---

## 9. Construction Method — Atheoretical Prompt (CR Appendix)

> On a scale from 1 to 10, you think the show New Girl is: {phi_ng}. 10 means you love New Girl, and 1 means you hate it. On a scale from 1 to 10, your passion for taxidermy is: {phi_tax}. 10 means you love taxidermy, and 1 means you hate it. On a scale from 1 to 10, your ability to swim is: {phi_swim}. 10 means you are a great swimmer, and 1 means you can't swim.

Optimized atheoretical parameters: (phi_ng, phi_tax, phi_swim) = (5,7,1), (9,9,5), (7,6,8). Result: failed to beat baseline even in-sample.

---

## 10. Key Methodological Notes for Replication

1. **Training data**: Only the basic 11-20 game human distribution (n=108) was used to optimize persona weights. The costless and cycle variants were held out for validation. The 1-10 and 1-7 games were novel target settings with no prior data used in construction.

2. **Preregistration**: All AI responses (prompts, weights) were locked in before human data was collected for the novel games. Preregistered on aspredicted.org (numbers 222695, 231091, 241394).

3. **Agents constructed months before**: The level-k agents used in the 1,500-game experiment were constructed before any of those games existed, using only the basic 11-20 game optimization.

4. **Invalid responses**: Less than 0.1% of AI responses were invalid at temperature=1; these were discarded without resampling per the preregistered plan.

5. **Distance metric**: KL divergence (forward, human as reference) is the primary reported metric for 11-20 games. MAE is used for the CR allocation games.

6. **Baseline definition**: "Off-the-shelf" GPT-4o with no system prompt or persona beyond the game instructions.

7. **The paper does NOT use Claude or any Anthropic model**: All simulations in the original paper use GPT-4o exclusively.
