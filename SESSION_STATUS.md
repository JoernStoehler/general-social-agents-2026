# Session Status (2026-03-19, session 2, continued)

## Project Goal (clarified by Jörn)
How good is a system powered by Opus 4.6 and sota techniques at predicting human behavior, exemplified on simple games? Downstream: can we replace gathering empirical social data with just asking an AI?

## Key Results

### 11-20 Money Request Game
- **Opus 4.6 direct prediction: KL = 0.73** (1 call, no engineering)
- GPT-4o raw baseline (paper): KL = 2.7
- Paper's 100-persona optimized ensemble: KL = 0.30
- Opus is 3.7× better than raw GPT-4o, but 2.4× worse than the pipeline
- Model predicts peak at 19-20 (55%), humans peak at 17-18 (62%)
- Model applies level-k reasoning but anchors at level 0-1 (humans at level 2-3)

### Contamination Controls (11-20 variants)
- Model cited Arad & Rubinstein (2012) for ALL conditions including variants with different bonuses
- Weak bonus (b=10): 60% at 19-20
- Strong bonus (b=50): 70% at 19-20 — WRONG direction (should shift left with stronger incentive)
- Named condition: KL = 0.87, slightly worse than unnamed
- Conclusion: model applies a template, doesn't reason from game structure

### Charness-Rabin Games (20 binary choice games)
- Player A predictions: correlation r=0.731, MAE=0.142, mean KL=0.073
- Player B predictions: correlation r=0.826, MAE=0.138, mean KL=0.086
- Model regresses predictions toward 0.5 (hedges)
- 8/20 Player B predictions are exactly 0.62 — default heuristic, not per-game reasoning
- Misses extreme behavior badly (where humans are near 0% or 100%)
- Gets direction right most of the time

## Technical Findings
- `claude -p` reads CLAUDE.md from working directory (run from /tmp to isolate)
- Prepends "You are a Claude agent, built on Anthropic's Claude Agent SDK."
- Injects date via system-reminder in user message
- Thinking: adaptive mode, effort: high, max_tokens: 64000
- Using `--system-prompt` to replace default makes system WORSE (removes useful context)
- Best approach: `cd /tmp/folder && claude -p "Read prompt.md and write to output.md"`

## What Jörn Said (key insights from this session)
1. Goal is about the SYSTEM, not the raw model. Simple system > complex pipeline (more reusable)
2. "Contamination" is wrong frame — model has knowledge like humans have education. Question is whether it generalizes
3. The experiment folder IS the system — put helpful context in it
4. Test fame gradient: does model predict better on well-known games? If yes → memorization
5. Prompt must accurately describe what experiment subjects experienced
6. Delegate focused analysis (reasoning traces) to expert subagents
7. learnings.md: models accumulate knowledge across runs, carefully pruned for overfitting

## Files Changed This Session
- src/cr_games.py — 20 CR games with verified human data from paper Table D2
- results/session2_results.json — all experiment results
- results/reference/human_data_other_games.md — research agent findings on available human data

## Remaining Work
1. Try improved system (better prompting, theory-of-mind context, learnings.md)
2. Analyze reasoning traces (what does model do wrong? delegate to subagent)
3. Test fame gradient if possible (need games at different fame levels)
4. Write report (~1500-2500 words)
5. Write Twitter thread (6-10 tweets)
6. Quota: ~4% used, must stay <100%
7. ~5 hours remaining to deadline
