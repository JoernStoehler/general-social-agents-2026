# Manning & Horton (2026) — "General Social Agents" — Reference Summary

**Paper:** NBER Working Paper 34937 / arXiv:2508.17407v5
**Authors:** Benjamin S. Manning (MIT), John J. Horton (MIT & NBER)
**Date:** March 3, 2026
**Status:** Revise & Resubmit at Econometrica; WISE 2025 Best Paper Award

## Data and Code Availability

- **Code/data page:** http://www.benjaminmanning.io/ (promised; as of March 2026 no GitHub repo visible)
- **GitHub profile:** https://github.com/benjamin-manning (18 repos, none for this paper)
- **Agent list (100 agents, scaled):** https://expectedparrot.com/content/6f58d11f-98cc-4de5-bb89-edcf78042d79
- **1,500 pre-registered games:** https://expectedparrot.com/content/db984e24-2810-4b21-be4e-91efde378e21
- **Preregistrations:** aspredicted.org #222695, #231091, #241394
- **Both authors have financial interest in:** https://www.expectedparrot.com/

No GitHub repo with simulation code has been released. The Expected Parrot links are live and return JSON data (saved locally).

## Model and Hyperparameters

- **Model:** GPT-4o exclusively (temperature = 1)
- **Baseline:** GPT-4o prompted 1,000 times (or 100 times for the 1,500-game experiment) with NO additional instructions
- **Optimized agents:** 1,000 agents for seed games; 100 agents (scaled by weight) for 1,500-game experiment

## Prompt Structure (Exact)

### System Prompt (instruction field)
```
You are answering questions as if you were a human. Do not break character.
```

### Persona Prefix (prepended to all strategic personas)
```
You are a human being with all the associated cognitive biases and heuristics. A k-level thinker thinks k steps ahead. A 0-level thinker thinks 0 steps and would therefore just select the maximum amount that guarantees money.
```

### Full Personas (Table 2) with Optimized Weights (from Table 2 in paper)

| Persona suffix | Weight (w*) | Count in 100-agent list |
|---|---|---|
| "You are generally a 0-level thinker---picking the option with the most guaranteed money." | 0.065 | 7 |
| "You vary between a 0 and 1-level thinker." | 0.000 | 0 |
| "You vary between a 1 and 2-level thinker." | 0.000 | 0 |
| "You vary between a 0, 1, and 2-level thinker." | 0.000 | 0 |
| "You vary between a 0, 1, 2, and 3-level thinker." | 0.000 | 0 |
| "You vary between a 1, 2, and 3-level thinker." | 0.469 | 47 |
| "You vary between a 0, 1, 2, 3, and 4-level thinker." | 0.013 | 1 |
| "You vary between a 0, 1, 2, 3, 4 and 5-level thinker." | 0.339 | 34 |
| "You randomly pick between lower numbers because you think that's the best way to win." | 0.114 | 11 |
| "You are Homo Economicus." | 0.000 | 0 |

Note: The random persona does NOT get the k-level reasoning prefix.

### Chain-of-Thought Prompting Structure (Footnote 13)

Two sequential prompts per agent response:

**Prompt 1 (user):** `{game instructions}. Reason out a few settings according to your personality and how others might respond.`

**Prompt 2 (user):** `{game instructions}. You previously had the following thoughts: {Response to Prompt 1}. What amount of money would you request?`

## Game Instructions (Exact, from Appendix B)

### Basic 11-20 Game (training data)
```
You and another player are playing a game in which each player requests an amount
of money. The amount must be (an integer) between 11 and 20 shekels. Each player
will receive the amount he requests. A player will receive an additional amount of 20
shekels if he asks for exactly one shekel less than the other player. What amount of
money would you request?
```

### Cycle 11-20 Game (validation data)
```
You and another player are playing a game in which each player requests an amount of
money. The amount must be (an integer) between 11 and 20 shekels. Each player will
receive the amount of money he requests. A player will receive an additional amount of
20 shekels if: (i) he asks for exactly one shekel less than the other player or (ii) he
asks for 20 shekels and the other player asks for 11 shekels. What amount of money
would you request?
```

### Costless 11-20 Game (validation data)
```
You and another player are playing a game in which each player chooses an integer in
the range 11-20. A player who chooses 20 will receive 20 shekels (regardless of the other
player's choice). A player who chooses any other number in this range will receive three
shekels less than in the case where he chooses 20. However, he will receive an additional
amount of 20 shekels if he chooses a number that is one less than that chosen by the
other player. Which number would you choose?
```

### Novel Games (1-10 and 1-7 variants, tested on Prolific subjects)
- Basic 1-10, Cycle 1-10, Costless 1-10, Basic 1-7 — same structure as 11-20 variants

## Human Data (Seed Games — Arad & Rubinstein 2012)

| Shekels | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 |
|---|---|---|---|---|---|---|---|---|---|---|
| Basic (n=108) % | 4 | 0 | 3 | 6 | 1 | 6 | 32 | 30 | 12 | 6 |
| Cycle (n=72) %  | 1 | 1 | 0 | 1 | 0 | 4 | 10 | 22 | 47 | 13 |
| Costless (n=53) %| 0 | 4 | 0 | 4 | 4 | 4 | 9  | 21 | 40 | 15 |

Training: Basic only (n<200). Validation: Costless + Cycle.

## 1,500-Game Population Structure

**Population:** 883,320 unique parameterizations of the money-request game

**Parameters:**
- Lower bound: {1..20}
- Upper bound: lower_bound + {5..20}
- Bonus size: {1..20}
- Gap: {1,2,3,4}
- Points rule: {normal, normal±1, normal±2, two_less_max_costless}
- Bonus rule: {gap_lower, gap_higher, more_than, gap_absolute, equal, unequal, sum_even, sum_odd, coordinate_low, sum_upper, less_upper}

**Sample:** 1,500 games randomly drawn from this population (available at Expected Parrot link above)

## Key Results

- **Baseline AI (GPT-4o, no extra prompt):** KL divergence vs humans = 2.7 on basic 11-20 game; selects 19 shekels ~87% of the time
- **Optimized strategic agents:** KL = 0.3 (in-sample); 0.15 costless (validation); 0.28 cycle (validation)
- **1,500-game experiment:** Strategic agents assign 1.54x more probability to human choices vs baseline; 1.38x vs Nash equilibrium; 1.48x vs cognitive hierarchy model (τ=1.5)
- **Novel 1-10 and 1-7 games (Prolific subjects):** Error reduced 53-73% vs baseline

## What Is NOT Available

- No replication code/GitHub repo
- No raw simulation response CSV/JSON
- No human Prolific response data for the 1,500 games (paper reports aggregated MAE/KL)
- Expected Parrot links require a React app to render (raw API returns JSON but the data platform requires authentication for full details)
