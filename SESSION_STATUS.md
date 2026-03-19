# Session Status (2026-03-19)

## What's Done

### Infrastructure (committed)
- Settings.json: agent teams enabled, permissions, session-start hook
- CLAUDE.md: project context, work quality rules, cost/safety rules
- Skills: experiment-run, output-parsing
- Agent: research.md
- Hooks: session-start.sh (env forwarding, pip install)

### Research (committed)
- Paper TeX source downloaded and extracted
- Arad & Rubinstein (2012) human data verified across 4 sources (n=108)
- 100 persona prompts extracted from TeX, verified against paper
- 1,500 novel game configurations pulled via EDSL
- Nash equilibria and level-k predictions computed
- EDSL evaluated (not worth using as dependency)
- Prior work surveyed

### Code Harness (committed, reviewed, 25 tests passing)
- src/games.py — 11-20 game with verified human data
- src/simulate.py — direct prediction + sampling methods
- src/metrics.py — KL, TV, log-likelihood
- src/baselines.py — Nash, level-k, uniform
- src/analysis.py — plotting and comparison
- tests/test_metrics.py — 14 tests
- tests/test_baselines.py — 11 tests

### Project Plan (committed)
- PLAN.md with methodology, conditions, execution order
- project-brief.md rewritten to accurately describe the paper

## Key Design Decisions (from conversation with Jörn)

1. **Direct distribution prediction is the primary method** — ask the model for the full distribution in one call, don't sample 200 times
2. **The paper built an ensemble pipeline, not just a prompted model** — baseline GPT-4o is terrible (KL=2.7)
3. **Contamination is a real concern** — the 11-20 game is likely memorized by modern models
4. **Test contamination empirically** — compare "recall published data" vs "predict from rules"
5. **Parameter variants** for clean tests (change bonus, range) where no published data exists
6. **NEVER make paid API calls without explicit permission** — costs real Jörn's money

## Unresolved Questions (need Jörn's input)

1. Can we use Max subscription (subagents / `claude -p`) instead of paid API calls?
2. Budget approval for any API calls
3. Whether to contact Manning & Horton for human data on 1,500 games
4. Is the 11-20 game sufficient with contamination caveat, or do we need novel games?

## Session Learnings (saved to memories + CLAUDE.md)

- Never fabricate claims about papers without reading the source
- Verify subagent outputs before committing or building on them
- Proactive wrap-up at phase boundaries
- Never make paid API calls without permission
- Wire learnings into CLAUDE.md (not just memories) so subagents see them
- Use background agents for mechanical work, don't block conversation
- Ask short clarifying questions rather than making wrong assumptions
