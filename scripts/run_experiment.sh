#!/bin/bash
# Run an experiment: concatenate prompt files and pass to Claude CLI.
#
# Concatenates the given prompt files in order, appends a JSON-only output
# instruction, and runs the result through `claude -p`. Saves the full
# prompt, the list of input files, and the model output to results/runs/.
#
# Runs from /tmp to avoid CLAUDE.md influencing the model.
#
# Usage:
#   scripts/run_experiment.sh <prompt_files...>
#
# Examples:
#   scripts/run_experiment.sh prompts/task.md prompts/learnings.md prompts/game_1120_desc.md
#   scripts/run_experiment.sh prompts/task.md prompts/learnings.md prompts/games_cr.md

set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
CLAUDE_BIN="${CLAUDE_BIN:-$(which claude 2>/dev/null || echo "/home/codespace/.vscode-remote/extensions/anthropic.claude-code-2.1.79-linux-x64/resources/native-binary/claude")}"
TIMESTAMP="$(date +%Y%m%d_%H%M%S)"

if [ $# -eq 0 ]; then
    echo "Usage: scripts/run_experiment.sh <prompt_files...>"
    echo ""
    echo "Concatenates prompt files and passes them to claude -p."
    echo "Results saved to results/runs/<timestamp>/."
    exit 1
fi

# Concatenate all prompt files with --- separators
PROMPT=""
for f in "$@"; do
    PROMPT="${PROMPT}$(cat "$REPO_DIR/$f")

---

"
done

# Append output instruction
PROMPT="${PROMPT}
Output ONLY the JSON object/array, nothing else."

echo "=== Experiment ==="
echo "Files: $*"
echo "Timestamp: $TIMESTAMP"
echo "Prompt length: $(echo "$PROMPT" | wc -c) chars"
echo ""

# Run from /tmp to avoid CLAUDE.md
cd /tmp
RESULT=$(CLAUDE_CODE_DISABLE_AUTO_MEMORY=1 "$CLAUDE_BIN" -p "$PROMPT" --dangerously-skip-permissions 2>/dev/null)

echo "$RESULT"

# Save result
RESULT_DIR="$REPO_DIR/results/runs/$TIMESTAMP"
mkdir -p "$RESULT_DIR"
echo "$RESULT" > "$RESULT_DIR/output.txt"
echo "$*" > "$RESULT_DIR/files.txt"
echo "$PROMPT" > "$RESULT_DIR/full_prompt.txt"

echo ""
echo "=== Saved to: results/runs/$TIMESTAMP ==="
