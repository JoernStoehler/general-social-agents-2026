# Arad & Rubinstein (2012) — Empirical Data

**Source:** Arad, A. and Rubinstein, A. (2012). "The 11-20 Money Request Game: A Level-k Reasoning Study." *American Economic Review*, 102(7), 3561–3573.
**PDF:** https://arielrubinstein.org/papers/88.pdf
**DOI:** https://doi.org/10.1257/aer.102.7.3561
**Data retrieved from:** Full paper PDF (all tables read directly from pp. 3565–3569)

---

## Experiment Overview

- **Subject pool:** Undergraduate economics students at Tel Aviv University (had not studied game theory)
- **Total subjects across all three game versions:** 233
- **Design:** Three game versions randomly distributed in class; subjects played once (one-shot); forms collected and randomly matched for payment

---

## Table 1 — Basic Version (n = 108)

This is the canonical version used in the literature. Data from Table 1, p. 3565.

| Choice | Level-k | Equilibrium (%) | Results (%) | Implied count (approx.) |
|--------|---------|-----------------|-------------|--------------------------|
| 11     | L9      | —               | 4           | ~4                       |
| 12     | L8      | —               | 0           | 0                        |
| 13     | L7      | —               | 3           | ~3                       |
| 14     | L6      | —               | 6           | ~6–7                     |
| 15     | L5      | 25              | 1           | ~1                       |
| 16     | L4      | 25              | 6           | ~6–7                     |
| 17     | L3      | 20              | 32          | ~35                      |
| 18     | L2      | 15              | 30          | ~32                      |
| 19     | L1      | 10              | 12          | ~13                      |
| 20     | L0      | 5               | 6           | ~6–7                     |
| **Total** |      | **100**         | **100**     | **~108**                 |

**Notes on counts:** The paper reports percentages rounded to integers. Back-calculating n=108 × percentage gives non-integers; the implied counts above are approximate. The sum of rounded counts is ~106, with ~2 subjects absorbed in rounding. Do not treat implied counts as exact.

**Key summary statistics (Basic Version):**
- L1 + L2 + L3 (choices 17–19): **74%** of subjects
- L0 (choice 20): **6%**
- L4 and below (choices 11–16): **20%**
- Nash equilibrium prediction for 17–19: 45%
- Nash equilibrium prediction for 15–16: 50%

---

## Table 2 — Cycle Version (n = 72)

Variant where choosing 20 can also win the bonus (if opponent chooses 11), making 20 more salient as L0.

| Choice | Equilibrium (%) | Cycle (%) | Basic (%) |
|--------|-----------------|-----------|-----------|
| 11     | —               | 1         | 4         |
| 12     | —               | 1         | 0         |
| 13     | —               | 0         | 3         |
| 14     | —               | 1         | 6         |
| 15     | 25              | 0         | 1         |
| 16     | 25              | 4         | 6         |
| 17     | 20              | 10        | 32        |
| 18     | 15              | 22        | 30        |
| 19     | 10              | 47        | 12        |
| 20     | 5               | 13        | 6         |

Key finding: Enhancing L0 salience shifted within L1–L3 toward L1 (19 jumped from 12% to 47%), but did not increase total L1+L2+L3 (79% vs 74%, p=0.43).

---

## Table 3 — Costless Iterations Version (n = 53)

Variant where all choices 11–19 cost the same (17 shekels guaranteed vs 20 for choosing 20), eliminating the incremental cost of each level of reasoning.

| Choice | Equilibrium (%) | Results (%) |
|--------|-----------------|-------------|
| 11     | 10              | 0           |
| 12     | 15              | 4           |
| 13     | 15              | 0           |
| 14     | 15              | 4           |
| 15     | 15              | 4           |
| 16     | 15              | 4           |
| 17     | 15              | 9           |
| 18     | 15              | 21          |
| 19     | 15              | 40          |
| 20     | 15              | 15          |

Key finding: 84% chose L0–L3 strategies; the cost of iteration is not what limits depth.

---

## Comparison with Project Brief Approximations

The project brief listed approximate percentages: 20:~5%, 19:~10%, 18:~25%, 17:~30%, 16:~15%, 15:~8%, 14:~4%, 13–11:~3%.

**Corrections from actual Table 1 data (basic version):**

| Choice | Brief estimate | Actual (%) | Error |
|--------|---------------|------------|-------|
| 20     | ~5%           | 6%         | close |
| 19     | ~10%          | 12%        | close |
| 18     | ~25%          | 30%        | +5pp  |
| 17     | ~30%          | 32%        | close |
| 16     | ~15%          | 6%         | **-9pp** — substantial overestimate |
| 15     | ~8%           | 1%         | **-7pp** — substantial overestimate |
| 14     | ~4%           | 6%         | close |
| 13     | ~3% (pooled)  | 3%         | close |
| 12     | ~3% (pooled)  | 0%         | — |
| 11     | ~3% (pooled)  | 4%         | close |

The brief significantly overestimated choices 15 and 16 (which are in Nash equilibrium territory). The actual mass is much more concentrated in 17–19 (74% total) than the brief suggests (~65%).

---

## Level-k Type Estimates (from paper, footnote 6)

Best-fitting model (L0, L1, L2, L3 + noise):
- L0: 0.05 (5%)
- L1: 0.13 (13%)
- L2: 0.39 (39%)
- L3: 0.43 (43%)
- Error rate (uniform noise): 0.32

Cognitive Hierarchy model (Poisson): best-fit lambda = 2.36

---

## For Simulation Use

The canonical empirical distribution to replicate is **Table 1, basic version, n=108**:

```python
ARAD_RUBINSTEIN_2012_BASIC = {
    11: 0.04,
    12: 0.00,
    13: 0.03,
    14: 0.06,
    15: 0.01,
    16: 0.06,
    17: 0.32,
    18: 0.30,
    19: 0.12,
    20: 0.06,
}
# Source: Table 1, Arad & Rubinstein (2012), AER 102(7): 3561-3573
# n=108; percentages rounded to integers in the paper
```
