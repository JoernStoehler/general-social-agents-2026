# Twitter Thread Draft

**1/**
I'm interested in whether modern LLMs can predict human behavior in economic games without elaborate pipelines.

Manning & Horton (2026) needed 100 persona agents + calibration + mixture optimization for GPT-4o to get decent predictions.

Tested Claude Opus 4.6 with just a single prompt. Thread:

**2/**
The game: Arad & Rubinstein's 11-20 Money Request Game. Pick 11-20, get what you pick. If you pick exactly 1 less than opponent, +20 bonus.

Humans cluster at 17-18 (62%). Raw GPT-4o puts ~87% on 19-20. D_KL = 2.7, worse than random.

**3/**
Claude Opus 4.6, bare prompt: D_KL = 1.03. Better than GPT-4o, but still anchors at 19-20 instead of 17-18.

With a domain-informed prompt (accurate experiment description + behavioral economics priming + structural analysis): D_KL = 0.59.

Manning & Horton's optimized ensemble: D_KL = 0.30. So we're within 2x — with one call vs ten thousand.

**4/**
What changed? The bare model recalled the game but got the data WRONG — claimed humans "cluster around 20." The fix:
- Describe the experiment accurately (Israeli undergrads, one-shot, real money)
- Prime relevant concepts (level-k reasoning, bounded rationality)
- Spell out structural implications the model should derive but doesn't

**5/**
Think of it like briefing a smart colleague: you wouldn't ask them to predict behavior without telling them who the participants are, what's at stake, and what game theory implies about reasoning depth.

The model has the knowledge. The prompt ensures correct retrieval and application.

**6/**
Also tested 20 Charness-Rabin allocation games (fairness, reciprocity, social preferences).

Correlation with human data: r = 0.79-0.85
Mean absolute error: ~12-13 percentage points

Direction is right. But the model hedges toward moderate predictions when humans are extreme.

**7/**
Contamination check: changed the 11-20 bonus from 20 to 10 and 50.

With bigger bonus (stronger undercutting incentive), the bare model predicted MORE mass on 19-20 — the wrong direction. Template-matching, not reasoning from game structure.

**8/**
A cautionary tale: during development, a "failure mode description" in the prompt accidentally included actual human data. Predictions improved — looked great but was tainted. Caught and corrected, but illustrates how easily ground truth leaks into AI prediction prompts.

**9/**
Bottom line: a simple system (one model, one prompt, one call) gets within 2x of a complex 100-persona pipeline.

The bottleneck is prompt engineering, not model capability. Two years of model improvement (GPT-4o → Opus 4.6) closed most of the gap that previously required elaborate calibration.

**10/**
Data, code, prompts, and reasoning traces: [repo link]

Paper: Manning & Horton (2026), "General Social Agents" arXiv:2508.17407
Human data: Arad & Rubinstein (2012) AER, Charness & Rabin (2002) QJE

@BenjaminManning @john_j_horton
