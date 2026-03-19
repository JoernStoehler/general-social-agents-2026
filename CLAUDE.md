# CLAUDE.md

Extension of Manning & Horton (2026), "General Social Agents."
Owner: Jörn Stöhler (@JoernStoehler)
Mode: Fully autonomous agent team. Human overseer for infrastructure failures only.
Deliverables: Public GitHub repo, final report (markdown), Twitter/X thread draft.

## What This Project Does

We test whether modern LLMs (Claude Opus 4.6, Claude Sonnet 4.6) can predict human game play — potentially without the elaborate persona-ensemble-calibration pipeline that Manning & Horton needed for GPT-4o. The flagship game is Arad & Rubinstein (2012) "11-20 Money Request Game." See `project-brief.md` for full context including what the original paper actually does.

## Repo Structure

```
src/                  # Python: games, simulation harness, baselines, metrics, analysis
prompts/              # All system prompts used, labeled
results/              # Raw simulation outputs (JSON/CSV)
figures/              # Generated plots
```

## Experiment Integrity

- **Log everything**: raw API responses, parsed values, parse failure counts.
- **Pin model IDs** explicitly (e.g., `claude-opus-4-6`). Record in results metadata.
- **Never change prompts** without documenting the change and rationale in `prompts/`.
- Method details (sampling vs. direct prediction, sample sizes, temperature) are in `project-brief.md`.

## Work Quality

- **Verify before trusting.** Cross-check data across independent sources before committing or building on it. Subagent outputs are not pre-verified.
- **Never fabricate.** If you haven't read the primary source, say "to be verified" or leave it out. Silence beats confident falsehood.
- **Proactive wrap-up.** When a work phase completes, verify outputs, check for error propagation, and clean up — without waiting to be prompted.
- **Contamination awareness.** The 11-20 game is from a famous 2012 paper. Models may have memorized published data. Flag this when interpreting results.

## Communication with Jörn

- Investigate before requesting attention. Agent time is free.
- Number items so Jörn can respond "3 yes, 5 no."
- Push back on contradictions and oversights.
- Never take silence as confirmation.
- Adopt Jörn's exact phrasing when he corrects.

## Cost and Safety

- **NEVER make paid API calls without explicit permission.** `ANTHROPIC_API_KEY` and `OPENAI_API_KEY` are connected to Jörn's personal accounts. Estimate cost and get approval before any API usage.
- **Think before dangerous actions.** API calls, pushing code, installing packages, anything with real-world consequences — pause and verify it's authorized.

## Session Workflow

**Act freely:** writing code, investigation, committing to working branch.
**Discuss first:** scope changes, experiment methodology changes, prompt changes, any API calls that cost money.
**Never without instruction:** destructive operations, PRs, merging to `main`, paid API calls.

## Quick Commands

```bash
pip install -r requirements.txt
pytest tests/
ruff check src/ tests/
```

## Environment

- GitHub Codespace (Linux), Python 3.x
- API keys: `ANTHROPIC_API_KEY` (required), `OPENAI_API_KEY` (optional)
- Agent teams enabled
