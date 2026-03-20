# Can a Simple LLM System Predict Human Behavior in Games?

## Research question

Manning & Horton (2026) showed that GPT-4o cannot predict human behavior in economic games out of the box. They built an elaborate pipeline — 100 persona agents, calibration, mixture optimization — to close the gap.

**We ask: does a simple system (one model, one prompt, one API call) with modern LLMs and good prompt engineering get you close?**

This matters because if cheap AI predictions approximate human behavior, social scientists can iterate faster, test hypotheses before running expensive experiments, and predict behavior during distribution shifts.

## Results

### 20 Charness-Rabin allocation games (the paper's main benchmark)

The paper uses MAE (mean absolute error) on 40 binary predictions (20 games × 2 players).

| System | Player A MAE | Player B MAE |
|--------|:-----------:|:-----------:|
| GPT-4o baseline (Manning & Horton) | 0.52 | 0.29 |
| GPT-4o optimized ensemble (Manning & Horton) | 0.17 | 0.15 |
| **Opus 4.6, one prompt, one call** | **0.12** | **0.13** |

The model captures the rank order of human preferences well (r = 0.79 / 0.85) but systematically regresses toward moderate predictions when humans show strong preferences.

## What we learned

**Prompt engineering is the bottleneck.** The same model goes from much worse to competitive purely through better prompting. The key: describe the experiment accurately (who the participants are, what's at stake), prime relevant concepts (level-k reasoning, bounded rationality, social preferences), and spell out structural implications that the model should derive but doesn't.

**The model has the knowledge but misapplies it.** Reasoning trace analysis shows Opus 4.6 recognizes the games, cites the right papers, and knows the relevant behavioral economics. But without guidance it miscalibrates — anchoring on game-theoretic rationality instead of modeling bounded human cognition.

**Template behavior is the main remaining failure.** On CR games, the model copies similar predictions across structurally different games rather than reasoning per-game. When humans show 90%+ preference for one option, the model predicts 60-70%.

**A simple system is scientifically more valuable.** A complex pipeline tuned to one domain is a one-time thing. A simple system that works across games is reusable — and the failure modes are interpretable and fixable.

## Method

Claude Opus 4.6 via `claude -p` (Claude Code CLI, pipe mode). One call per game set. Default system prompt with thinking enabled. No fine-tuning, no multi-agent pipeline, no calibration against human data.

The prompt encodes behavioral economics knowledge (level-k reasoning, social preferences, bounded rationality) and describes the experiment completely. This is legitimate system design — like programming a tool with domain knowledge — not data leakage. A [spoiler audit](.claude/agents/audit-spoilers.md) verified no ground truth leaked into prompts.

Human data: Arad & Rubinstein (2012) AER for the 11-20 game; Charness & Rabin (2002) QJE via Manning & Horton (2026) Table D2 for the CR games.

## Repo structure

```
prompts/          Prompt files (task framing, learnings, game descriptions)
scripts/          Evaluation, experiment runner, JSONL extraction, spoiler audit
data/             Human data, game definitions, paper summaries
results/          Experiment outputs (timestamped runs, session logs)
paper/            Manning & Horton (2026) PDF and TeX source
report.md         Detailed report
twitter_thread.md Thread draft
```

## Running experiments

```bash
pip install -r requirements.txt
scripts/run_experiment.sh prompts/game_1120.md
python3 scripts/eval_cr.py results/runs/20260320_101421/output.txt
python3 scripts/extract_session.py results/sessions/*.jsonl
```

## References

- Manning & Horton (2026), "General Social Agents," arXiv:2508.17407
- Arad & Rubinstein (2012), "The 11-20 Money Request Game," AER 102(7)
- Charness & Rabin (2002), "Understanding Social Preferences," QJE 117(3)
