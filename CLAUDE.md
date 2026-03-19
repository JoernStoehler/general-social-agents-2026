# CLAUDE.md

Replication & extension of Manning & Horton (2026), "General Social Agents."
Owner: Jörn Stöhler (@JoernStoehler)
Mode: Fully autonomous agent team. Human overseer for infrastructure failures only.
Deliverables: Public GitHub repo, final report (markdown), Twitter/X thread draft.

## What This Project Does

We test whether modern LLMs (Claude Opus 4.6, Claude Sonnet 4.6, optionally GPT-4o) predict human game play better than GPT-4o did in the original paper. The flagship game is Arad & Rubinstein (2012) "11-20 Money Request Game." See `project-brief.md` for the full brief including experiment design, conditions, and priority ordering.

## Repo Structure

```
src/                  # Python: games, simulation harness, baselines, metrics, analysis
prompts/              # All system prompts used, labeled
results/              # Raw simulation outputs (JSON/CSV)
figures/              # Generated plots
```

## Experiment Integrity

- **temperature=1** for all LLM simulation calls (matching the original paper). Never temperature=0.
- **200 samples** per (model × condition × game).
- **Log everything**: raw API responses, parsed values, parse failure counts.
- **Pin model IDs** explicitly (e.g., `claude-opus-4-6`). Record in results metadata.
- **Never change prompts** without documenting the change and rationale in `prompts/`.

## Communication with Jörn

- Investigate before requesting attention. Agent time is free.
- Number items so Jörn can respond "3 yes, 5 no."
- Push back on contradictions and oversights.
- Never take silence as confirmation.
- Adopt Jörn's exact phrasing when he corrects.

## Session Workflow

**Act freely:** writing code, investigation, committing to working branch.
**Discuss first:** scope changes, experiment methodology changes, prompt changes.
**Never without instruction:** destructive operations, PRs, merging to `main`.

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
