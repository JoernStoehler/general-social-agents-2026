#!/bin/bash
# Run an experiment: concatenates prompt files and passes directly to claude -p.
#
# Usage: ./run_experiment.sh <prompt_files...>
#   Files are concatenated in order and passed as the prompt.
#
# Examples:
#   ./run_experiment.sh prompts/shared/system.md prompts/shared/learnings.md prompts/1120/game.md
#   ./run_experiment.sh prompts/shared/system.md prompts/shared/learnings.md prompts/cr/games.md

set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
CLAUDE_BIN="${CLAUDE_BIN:-$(which claude 2>/dev/null || echo "/home/codespace/.vscode-remote/extensions/anthropic.claude-code-2.1.79-linux-x64/resources/native-binary/claude")}"
TIMESTAMP="$(date +%Y%m%d_%H%M%S)"

if [ $# -eq 0 ]; then
    echo "Usage: ./run_experiment.sh <prompt_files...>"
    exit 1
fi

# Concatenate all prompt files
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
