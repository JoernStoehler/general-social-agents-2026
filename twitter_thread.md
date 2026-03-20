# Twitter Thread Draft

**1/**
Manning & Horton (2026) showed GPT-4o can't predict human game play without an elaborate pipeline (100 personas, calibration, mixture optimization).

Two years later: can a simple system with Claude Opus 4.6 do better?

We tested it. Results surprised us. Thread:

**2/**
The game: Arad & Rubinstein's 11-20 Money Request Game. Pick 11-20, get what you pick. If you pick exactly 1 less than opponent, +20 bonus.

Humans cluster at 17-18 (62%). Raw GPT-4o puts ~87% on 19-20. KL divergence = 2.7.

**3/**
Claude Opus 4.6 with zero engineering: KL = 0.73. Better than GPT-4o, but still bad — it anchors at 19-20 instead of 17-18.

But here's the key finding: with a well-engineered prompt? KL = 0.13.

That's 2.3x BETTER than the paper's optimized 100-persona ensemble (KL = 0.30).

One API call. ~4000 characters of prompt.

**4/**
What changed? Reasoning trace analysis showed the bare model recalled WRONG memorized data — it claimed humans "cluster around 20." The fix wasn't complex:
- Describe the experiment accurately (Israeli undergrads, one-shot, real money)
- Prime relevant concepts (level-k reasoning, bounded rationality)
- Warn about known AI failure modes

**5/**
Think of it like briefing a smart colleague: you wouldn't ask them to predict behavior without telling them who the participants are, what's at stake, and what errors to avoid.

The model has the behavioral economics knowledge. The prompt's job is to ensure correct retrieval and application.

**6/**
We also tested 20 Charness-Rabin allocation games (fairness, reciprocity, social preferences).

Correlation with human data: r = 0.76-0.81
Mean absolute error: ~13 percentage points

Direction is right. But the model still regresses toward moderate predictions when humans are extreme.

**7/**
Contamination check: we changed the 11-20 bonus from 20 to 10 and 50.

With bigger bonus (stronger undercutting incentive), the bare model predicted MORE mass on 19-20 — the wrong direction. Template-matching, not reasoning.

The engineered prompt fixed this by making the model reason from game structure.

**8/**
Bottom line: a simple system (one model, one prompt, one call) can outperform a complex 100-persona pipeline — if the prompt is designed with domain knowledge.

Two years of model progress didn't just improve the baseline. It made the elaborate calibration machinery obsolete.

**9/**
Why this matters: if AI can accurately predict human behavior in games, that's cheap, fast social science. Pilot studies without Prolific. Behavioral predictions during rapid change. Mechanism design without the mechanism.

KL = 0.13 is getting close to useful. The bottleneck is now prompt engineering, not model capability.

**10/**
Data, code, prompts, and full reasoning traces: [repo link]

Paper: Manning & Horton (2026), "General Social Agents" arXiv:2508.17407
Human data: Arad & Rubinstein (2012) AER, Charness & Rabin (2002) QJE

@BenjaminManning @john_j_horton
