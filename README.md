# general-social-agents-2026

Can a simple LLM system (Claude Opus 4.6, one prompt, one call) predict human behavior in economic games — without the elaborate 100-persona pipeline from Manning & Horton (2026)?

**Result**: D_KL = 0.59 vs the paper's optimized ensemble at 0.30. Within 2x, using one API call instead of ten thousand.

See [report.md](report.md) for the full writeup and [twitter_thread.md](twitter_thread.md) for a summary.

## Quick start

```bash
pip install -r requirements.txt
pytest tests/
./run_experiment.sh prompts/shared/system.md prompts/shared/learnings.md prompts/1120/game.md
```

## Repo structure

- `prompts/` — All prompts used (system context, learnings, game descriptions)
- `results/` — Raw outputs, human data references, experiment runs
- `src/` — Game definitions, metrics, evaluation scripts
- `report.md` — Full report
- `project-brief.md` — Original project brief and experimental design
