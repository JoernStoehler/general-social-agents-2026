# Twitter Thread Draft

**1/**
Can a single LLM predict human behavior in economic games — without an elaborate multi-agent pipeline?

Manning & Horton (2026) needed 100 persona agents + calibration + mixture optimization for GPT-4o.

I tested Claude Opus 4.6 with one prompt, one API call. Thread:

**2/**
The game: Arad & Rubinstein's 11-20 Money Request Game. Pick 11-20, get what you pick. If you pick exactly 1 less than opponent, +20 bonus.

Humans cluster at 17-18 (62%). Raw GPT-4o puts ~87% on 19-20.

**3/**
Claude Opus 4.6, bare prompt: D_KL(h||q) = 0.47. Better than GPT-4o out of the box, but still anchors too high.

With a domain-informed prompt (accurate experiment description + level-k priming + structural analysis): D_KL(h||q) = 0.14. A 3.4x improvement. Deterministic across 5 runs.

**4/**
The engineered prompt puts 45% mass on 17-18 (human: 62%) and 25% on 19-20 (human: 18%). Shape is right, peak is right — but not peaked enough.

What changed? The bare model recalled the game but got the data WRONG — claimed humans "cluster around 20." The prompt fixes retrieval, not capability.

**5/**
Think of it like briefing a smart colleague: describe who the participants are (Israeli undergrads, one-shot, real money), prime relevant frameworks (level-k reasoning, bounded rationality), and spell out structural implications (2-3 levels from 20 implies peak around 17-18).

The model has the knowledge. The prompt ensures correct application.

**6/**
Important caveat: Manning & Horton report D_KL(q||h) = 2.7 for raw GPT-4o and 0.30 for their optimized ensemble. We report D_KL(h||q). These are different KL directions — direct numerical comparison is not meaningful without recomputing in the same direction.

What we can say: one call gets qualitatively similar predictions to their 10,000-call pipeline.

**7/**
Also tested 20 Charness-Rabin allocation games (fairness, reciprocity, social preferences).

Player A: r = 0.79, MAE = 0.12
Player B: r = 0.85, MAE = 0.13

Direction is right. But the model regresses toward moderate predictions when humans are extreme.

**8/**
A cautionary tale: during development, a "failure mode description" in the prompt accidentally included actual human data. Predictions improved — looked great but was tainted.

Caught and removed. All reported results are spoiler-free. But it shows how easily ground truth leaks into AI prediction prompts.

**9/**
Bottom line: one model, one prompt, one API call gets you surprisingly far on predicting human game play. The bottleneck is prompt engineering, not model capability.

The key is treating the model like a knowledgeable colleague who needs a good briefing — not a black box you throw questions at.

**10/**
Data, code, prompts, and reasoning traces: [repo link]

Paper: Manning & Horton (2026), "General Social Agents" arXiv:2508.17407
Human data: Arad & Rubinstein (2012) AER, Charness & Rabin (2002) QJE

@BenjaminManning @john_j_horton
