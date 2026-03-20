# Spoiler Audit Agent

Check prompt files for ground truth leakage that could inflate prediction accuracy.

## What to check

1. **Specific numbers matching human data**:
   - 11-20 game: {11:0.04, 12:0.00, 13:0.03, 14:0.06, 15:0.01, 16:0.06, 17:0.32, 18:0.30, 19:0.12, 20:0.06}
   - CR games: see data/cr_games.py for all 40 human data points
   - Any percentages like "62%", "18%", "32%", "30%", "94%", "96%" near game contexts

2. **Indirect leakage patterns**:
   - "in reality", "actual data shows", "empirically", "the real proportion"
   - Aggregates that constrain the distribution (e.g., "only 18% chose 19-20")
   - Failure mode descriptions that reference actual outcomes

3. **What is NOT a spoiler**:
   - General behavioral economics facts ("humans reason 2-3 levels deep")
   - Structural analysis derived from game rules ("undercutting costs 1 shekel for a chance at 20")
   - AI performance data ("GPT-4o put 87% on 19-20") — this is about the AI, not humans

## How to run

Read all files in prompts/ and check each against the criteria above. Report:
- File, line number, suspicious text
- Whether it's a clear spoiler, borderline, or clean
- Recommended fix if spoiler found
