I'm# Twitter Thread Draft

**1/**
Manning & Horton (2026) showed GPT-4o can't predict human game play without an elaborate pipeline (100 personas, calibration, mixture optimization).

Can a simple system with Claude Opus 4.6 do better?

We tested it. Thread:

**2/**
The game: Arad & Rubinstein's 11-20 Money Request Game. Pick 11-20, get what you pick. If you pick exactly 1 less than opponent, +20 bonus.

Humans cluster at 17-18 (62%). Raw GPT-4o puts ~87% on 19-20. KL divergence = 2.7.

**3/**
Claude Opus 4.6, bare prompt: KL = 0.73. Better than GPT-4o, but still anchors at 19-20 instead of 17-18.

With a domain-informed prompt (experiment description + behavioral economics priming + structural analysis): KL ~0.20.

That's 1.5x better than the paper's optimized 100-persona ensemble (KL = 0.30). One API call.

**4/**
What changed? The bare model recalled the game but got the data wrong — claimed humans "cluster around 20." The fix:
- Describe the experiment accurately (Israeli undergrads, one-shot, real money)
- Prime relevant concepts (level-k reasoning, bounded rationality)
- Spell out structural implications the model should derive but doesn't

**5/**
Think of it like briefing a smart colleague: you wouldn't ask them to predict behavior without telling them who the participants are, what's at stake, and what game theory implies about reasoning depth.

The model has the knowledge. The prompt ensures correct retrieval and application.

**6/**
We also tested 20 Charness-Rabin allocation games (fairness, reciprocity, social preferences).

Correlation with human data: r = 0.76-0.81
Mean absolute error: ~13 percentage points

Direction is right. But the model still hedges toward moderate predictions when humans are extreme.

**7/**
Contamination check: we changed the 11-20 bonus from 20 to 10 and 50.

With bigger bonus (stronger undercutting incentive), the bare model predicted MORE mass on 19-20 — the wrong direction. Template-matching, not reasoning from game structure.

**8/**
A cautionary tale: during development, a "failure mode description" in the prompt accidentally included actual human data. KL dropped to 0.13 — looked great but was tainted. Caught and corrected, but illustrates how easily ground truth leaks into AI evaluation pipelines.

**9/**
Bottom line: a simple system (one model, one prompt, one call) outperforms a complex 100-persona pipeline — if the prompt is designed with domain knowledge.

The bottleneck is now prompt engineering, not model capability. These principles (accurate descriptions, concept priming) generalize beyond games.

**10/**
Data, code, prompts, and full reasoning traces: [repo link]

Paper: Manning & Horton (2026), "General Social Agents" arXiv:2508.17407
Human data: Arad & Rubinstein (2012) AER, Charness & Rabin (2002) QJE

@BenjaminManning @john_j_horton
