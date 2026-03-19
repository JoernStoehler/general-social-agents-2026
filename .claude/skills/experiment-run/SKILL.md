---
name: experiment-run
description: How to run LLM experiments correctly. Load before running any experiment batch. Covers logging, reproducibility, and cost awareness.
---

# Running Experiments

## Methods

See `project-brief.md` Section 4 for the current experimental design. The two main approaches are:

1. **Direct distribution prediction**: Ask the model to predict the human distribution in one call. Returns a probability distribution over actions.
2. **Sampling (for comparability with Manning & Horton)**: Call the model N times at temperature=1 with a role-play prompt, build empirical distribution.

The specific conditions, sample sizes, and parameters are defined in the project brief and may evolve.

## Logging Requirements

Each experiment produces a JSON file in `results/` containing:
```json
{
  "game": "eleven_twenty",
  "method": "direct_prediction | sampling",
  "condition": "direct | bare_roleplay | persona_roleplay",
  "model_id": "claude-opus-4-6",
  "temperature": 1.0,
  "n_samples": 50,
  "timestamp": "2026-03-19T12:00:00Z",
  "prompt": "...",
  "predicted_distribution": {"17": 0.32, "18": 0.30, ...},
  "raw_responses": ["...", "..."],
  "parse_failures": 0,
  "parse_failure_rate": 0.0
}
```

## Reproducibility Checklist

- [ ] Model ID pinned (not "opus" but "claude-opus-4-6")
- [ ] Exact prompt text saved in `prompts/` and in results JSON
- [ ] Method and parameters recorded
- [ ] Parse failure rate logged (for sampling method)
- [ ] API response metadata logged (if available)

## Cost Awareness

For direct prediction: 1 call per model per game. Negligible cost.

For sampling (11-20 game): N samples × conditions × models calls. At N=50 with 3 conditions and 2 models = 300 calls. ~200 tokens in, ~10 tokens out per call. Total: ~60K tokens, < $1.

For 1,500 games with sampling: multiply accordingly. Budget before running.

## Common Pitfalls

- **Output parsing** (sampling method): LLMs add text around the number. Always parse robustly. See the output-parsing skill.
- **Zero-frequency smoothing**: Add Laplace smoothing when computing log-likelihoods to avoid -inf.
- **Contamination**: The 11-20 game is from a famous 2012 paper. Models may have memorized human data. Flag this limitation.
- **Overclaiming**: Frame as "spot-check" unless using novel games with human data the model couldn't have seen in training.
