#!/bin/bash
set -euo pipefail

# Forward API keys from host environment into Claude Code sessions.
# Keys should be set in the codespace secrets or .env (gitignored).
if [ -n "${CLAUDE_ENV_FILE:-}" ]; then
  for var in ANTHROPIC_API_KEY OPENAI_API_KEY; do
    if [ -n "${!var:-}" ]; then
      echo "export $var=${!var}" >> "$CLAUDE_ENV_FILE"
    fi
  done
fi

# Ensure Python dependencies are available
if [ -f "$CLAUDE_PROJECT_DIR/requirements.txt" ]; then
  pip install -q -r "$CLAUDE_PROJECT_DIR/requirements.txt" 2>/dev/null || true
fi
