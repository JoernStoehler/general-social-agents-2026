# Session Status (2026-03-19, session 2, latest)

## Project Goal (clarified by Jörn)
How good is a system powered by Opus 4.6 and sota techniques at predicting human behavior, exemplified on simple games? Downstream: can we replace gathering empirical social data with just asking an AI? Simpler systems are more scientifically valuable since they can be reused.

## Key Results So Far

### 11-20 Money Request Game (Arad & Rubinstein 2012)
| System | KL divergence |
|--------|:---:|
| GPT-4o raw (paper) | 2.7 |
| Uniform random | 2.42 |
| **Opus 4.6, one call, zero engineering** | **0.73** |
| Paper's 100-persona optimized ensemble | 0.30 |

- Model predicts peak at 19-20 (55%), humans peak at 17-18 (62%)
- Model applies level-k reasoning but anchors at level 0-1 (humans at 2-3)
- Model spontaneously cited Arad & Rubinstein (2012) from training data

### Contamination Controls (11-20 variants)
- Cited A&R for ALL conditions including different bonus values
- Strong bonus (50): 70% at 19-20 — WRONG direction (should shift left)
- Template-matching, not reasoning from game structure

### Charness-Rabin Games (20 binary choice games, data from paper Table D2)
- Player A: r=0.731, MAE=0.142, mean KL=0.073
- Player B: r=0.826, MAE=0.138, mean KL=0.086
- Model regresses predictions toward 50-50, misses extremes
- 7/20 Player B predictions are exactly 0.62 (template behavior)

### V2 (context+learnings) vs V1 (bare)
- Player A improved (MAE 0.142→0.132)
- Player B worsened (MAE 0.139→0.158)
- Generic prompt engineering had mixed effects

## Technical Setup
- `claude -p` from clean /tmp directory (no CLAUDE.md)
- CLAUDE_CODE_DISABLE_AUTO_MEMORY=1
- Claude Code prepends "You are a Claude agent, built on Anthropic's Claude Agent SDK." and injects date
- Thinking: adaptive mode, effort: high, max_tokens: 64000
- Best approach: `cd /tmp/folder && claude -p "Read prompt.md and write to output.md"` with --dangerously-skip-permissions
- Session JSONL files saved in results/sessions/

## Jörn's Key Insights This Session
1. **Goal clarification**: Not "replicate the paper" — test how good a SIMPLE system is at predicting human behavior. Simpler = more valuable scientifically.
2. **Downstream purpose**: Replacing empirical social data collection. Faster social science, predictions during distribution shifts, saving money.
3. **"Contamination" is wrong frame**: Model has knowledge like humans have education. Question is whether it GENERALIZES (theory of mind) or is narrow pattern-matching.
4. **Fame gradient idea**: Test whether model predicts better on well-known games. If yes → memorization driving results.
5. **The folder IS the system**: Put useful context files in the experiment directory. learnings.md accumulates knowledge across runs, pruned to avoid overfitting.
6. **Prompt engineering matters**: Describe the experiment accurately. AIs don't magically know what experiment you want them to predict. Omitting relevant context misleads them.
7. **Analyze reasoning traces**: Extract thinking from JSONL to diagnose what the model does wrong. Delegate this to focused subagents.
8. **Ask sooner**: Don't waste project time to save Jörn 5 seconds. 1h agent time = 16% of remaining project.
9. **Don't use quota when Jörn is away** (but "not use up" = "don't exhaust", some usage is fine)
10. **Keep repo up to date**: Commit regularly so nothing is lost at compaction.

## Deliverables Status
- [x] report.md — drafted (~1800 words), needs refinement
- [x] twitter_thread.md — drafted (10 tweets), needs refinement
- [x] results/session2_results.json — all raw results
- [x] results/analysis_patterns.md — diagnostic analysis
- [x] results/sessions/ — JSONL session logs
- [x] src/cr_games.py — 20 CR games with verified human data
- [ ] Improved predictions (prompt engineering — Jörn offered to help, not yet applied)
- [ ] Final polish on report and thread

## Quota
- ~5-6% used (estimate)
- Budget: stay under 100%
- ~3.5h remaining to Twitter deadline (estimate as of last Jörn message)

## Open Items
1. Jörn offered to help with prompt engineering — not yet taken up. The key question: how to fix level-k anchoring and regression to mean?
2. Fame gradient experiment (need games at different fame levels — hard without more human data)
3. Reasoning trace analysis (delegate to subagent)
4. Final report/thread polish

## Key Files
- PLAN.md — project plan (needs updating to reflect actual results)
- report.md — report draft
- twitter_thread.md — thread draft
- src/games.py — 11-20 game + variants
- src/cr_games.py — 20 CR games with human data
- src/simulate.py — CLI + SDK backends
- results/session2_results.json — all results
- results/sessions/ — JSONL session logs
- /tmp/experiment/ — clean experiment directory with prompt files, context.md, learnings.md
