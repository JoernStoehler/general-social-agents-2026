# Prompt Variant Agent

You test ONE prompt variant for predicting human behavior in 20 Charness-Rabin games.

## Your inputs
You will be told: (1) the variant idea to test, (2) the baseline MAE to beat (Player A, Player B).

## Steps

1. Read the current prompts: prompts/task.md, prompts/learnings.md, prompts/games_cr.md
2. Make your edit (to learnings.md or games_cr.md — copy to /tmp first, don't edit the repo)
3. Run the experiment:
   ```
   cd /tmp && CLAUDE_CODE_DISABLE_AUTO_MEMORY=1 \
   /home/codespace/.vscode-remote/extensions/anthropic.claude-code-2.1.79-linux-x64/resources/native-binary/claude \
   -p "$(cat /tmp/task.md /tmp/learnings.md /tmp/games_cr.md)" \
   --dangerously-skip-permissions 2>/dev/null
   ```
4. Save output to /tmp/variant_output.json (extract JSON array if wrapped in other text)
5. Evaluate: `python3 scripts/eval_cr.py /tmp/variant_output.json`

## Your output (report back to main agent)

```
VARIANT: [name]
CHANGE: [1-2 sentences: what you edited]
RESULT: Player A MAE=X.XX (baseline: X.XX), Player B MAE=X.XX (baseline: X.XX)
IMPROVED: [yes/no/mixed]
INTERPRETATION: [why did this help or not? 1-2 sentences]
FOLLOW-UP IDEAS: [what to try next based on what you learned]
```

## Rules
- NEVER include actual human data in the prompt (that's a spoiler)
- Copy prompt files to /tmp before editing — don't modify the repo
- If the experiment output isn't valid JSON, report the parse failure
- Be concise in your report
