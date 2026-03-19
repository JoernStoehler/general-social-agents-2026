# Twitter Thread Draft

**1/**
Manning & Horton (2026) showed GPT-4o can't predict human game play without an elaborate pipeline (100 personas, calibration, mixture optimization).

Two years later: can Claude Opus 4.6 do it in one call?

We tested it. Results are interesting. Thread:

**2/**
The game: Arad & Rubinstein's 11-20 Money Request Game. Pick 11-20, get what you pick. If you pick exactly 1 less than your opponent, you get +20 bonus.

Humans cluster at 17-18 (62%). GPT-4o picks 19 almost 90% of the time.

**3/**
Claude Opus 4.6, one call, zero engineering:
- KL divergence: 0.73 (3.7x better than raw GPT-4o's 2.7)
- Still 2.4x worse than the paper's optimized ensemble (0.30)
- Predicts the right shape but anchors at 19-20 instead of 17-18

**4/**
We also tested on 20 Charness-Rabin allocation games (binary choices about fairness and reciprocity).

Correlation with human data: r = 0.73-0.83
Mean absolute error: 14 percentage points

It gets the direction right but hedges toward 50-50.

**5/**
The model spontaneously cited "Arad & Rubinstein (2012)" despite receiving only game rules. It knows the framework (level-k reasoning) but miscalibrates the depth.

It's a student who read the textbook but never ran the experiment.

**6/**
Contamination check: we changed the bonus from 20 to 10 and 50.

With a bigger bonus (stronger undercutting incentive), the model predicted MORE mass on 19-20. That's the wrong direction — it's template-matching, not reasoning from game structure.

**7/**
Adding behavioral context ("humans reason deeper than level 0-1", "don't hedge") had mixed effects: helped some games, hurt others. Generic prompt engineering isn't the fix.

The paper's calibration approach still matters — but a better base model means less engineering needed.

**8/**
Bottom line: 2 years of model progress closed ~80% of the gap between GPT-4o's baseline and the optimized ensemble.

The last 20% — precisely calibrated social cognition — remains open. Can we replace human experiments with AI? Not yet, but we're closer.

**9/**
Why this matters: if AI systems can accurately predict human behavior in games, that's cheap, fast social science. Pilot studies without Prolific. Behavioral predictions during rapid change. Mechanism design without the mechanism.

We're not there yet, but the trajectory is clear.

**10/**
Data, code, and full session logs (including model reasoning traces): [repo link]

Paper: Manning & Horton (2026), "General Social Agents" arXiv:2508.17407
Human data: Arad & Rubinstein (2012) AER, Charness & Rabin (2002) QJE

@BenjaminManning @john_j_horton
