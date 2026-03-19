---
name: experiment-run
description: How to run LLM simulation experiments correctly. Load before running any experiment batch. Covers parameter settings, logging, reproducibility, and the experimental conditions from Manning & Horton.
---

# Running Experiments

## Experimental Conditions

From the project brief (Section 4):

| Condition | Description | Prompt Style |
|-----------|-------------|--------------|
| B (Bare) | Minimal prompt, no theory | "You are a participant... What do you choose?" |
| C (Theory) | Level-k persona prompt | "You assume opponent chooses randomly and best-respond..." |
| C+ (Calibrated) | Best prompt selected on calibration data | Multiple candidates, pick best on held-out |
| A (Agent) | Multi-step with tool access | Model can compute Nash, reason step-by-step |

## Parameters (Non-Negotiable)

- **Samples**: 200 per (model × condition × game)
- **Temperature**: 1.0 (matching original paper)
- **Response format**: Ask for "only a number" in 1-shot conditions
- **Model IDs**: Pin exact versions. Record in results metadata.

## Running a Batch

```bash
# Single condition
python src/simulate.py --game eleven_twenty --condition bare --model claude-opus-4-6 --samples 200

# All conditions for a model
python src/simulate.py --game eleven_twenty --condition all --model claude-opus-4-6 --samples 200
```

## Logging Requirements

Each batch produces a JSON file in `results/` containing:
```json
{
  "game": "eleven_twenty",
  "condition": "bare",
  "model_id": "claude-opus-4-6",
  "temperature": 1.0,
  "samples": 200,
  "timestamp": "2026-03-19T12:00:00Z",
  "prompt": "...",
  "responses": [17, 18, 20, ...],
  "raw_responses": ["17", "I would choose 18", ...],
  "parse_failures": 3,
  "parse_failure_rate": 0.015
}
```

## Reproducibility Checklist

- [ ] Model ID pinned (not "opus" but "claude-opus-4-6")
- [ ] Temperature = 1.0
- [ ] Sample count = 200
- [ ] Exact prompt text saved in `prompts/` and in results JSON
- [ ] Parse failure rate logged
- [ ] API response metadata logged (if available)

## Cost Awareness

Rough estimate for 11-20 game only:
- 200 samples × 4 conditions × 3 models = 2,400 calls
- ~200 tokens in, ~10 tokens out per call (1-shot)
- Total: ~500K tokens, < $5

For 1,500 games: ~750M tokens = $hundreds. Subsample if needed.

## Common Pitfalls

- **Output parsing**: LLMs add text around the number. Always parse robustly.
- **Temperature 0**: Do NOT use temperature=0. You need the stochastic distribution.
- **Overclaiming**: Frame as "spot-check replication" unless using the full 1,500-game dataset.
- **Zero-frequency smoothing**: Add Laplace smoothing when computing log-likelihoods to avoid -inf.
