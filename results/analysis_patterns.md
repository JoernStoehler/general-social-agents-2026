# Analysis: What Opus 4.6 Gets Right and Wrong

> **Note**: This analysis is from the V1 (bare prompt) run in session 2 (2026-03-19). Numbers here reflect V1 predictions, not the current V3 engineered prompt. See report.md for current results.

## Key Diagnostic Patterns

### 1. Level-k Anchoring Error (11-20 game)
- Model puts 55% mass on 19-20 (level 0-1 reasoning)
- Humans put 62% mass on 17-18 (level 2-3 reasoning)
- Model underestimates human strategic depth by ~2 levels
- This matches Gao et al. (2024) finding that all advanced LLMs cluster at 19-20

### 2. Regression to Mean (CR games)
- 16/20 Player A predictions fall in [0.4, 0.7]
- 15/20 Player B predictions fall in [0.4, 0.7]
- But actual human proportions < 0.2 or > 0.8 in 6/20 (A) and 10/20 (B) games
- Model hedges toward 50-50 instead of predicting strong preferences
- Worst misses: Barc1 A (predicted 0.55, actual 0.96), Barc7 B (predicted 0.48, actual 0.06)

### 3. Template Behavior (CR games)
- 7/20 Player B predictions are exactly 0.62
- Model appears to use ~3 default values rather than reasoning per-game
- Suggests "fairness heuristic" (around 60% choose the "fair" option) applied uniformly

### 4. Direction is Correct
- Player A correlation: r = 0.731
- Player B correlation: r = 0.826
- Model understands WHICH games will have more extreme choices, just not HOW extreme

## What Could Help

### Immediate (prompt engineering)
- Instruct model to reason step-by-step about the game before predicting
- Tell it that humans often show strong preferences (don't hedge to 50-50)
- Describe experimental context more accurately (lab setting, real money, student subjects)

### System design (Jörn's suggestion)
- Add context files with general principles of human behavior (not game-specific)
- Use learnings.md to accumulate reasoning principles across runs
- Analyze reasoning traces to diagnose specific errors

### Remaining questions
- Does the model predict better on more famous games? (fame gradient)
- Would extended thinking improve level-k reasoning?
- Would self-critique ("what would humans say about your prediction?") help?
