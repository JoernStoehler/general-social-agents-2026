# Experiment Session Logs

Each JSONL file is a Claude Code session containing the full message chain,
including thinking blocks, tool calls, and raw API requests.

- `fad82708-d6d2-4a9d-85a2-dfd27b603d68.jsonl` — 11-20 game, full system (default prompt, tools enabled) (12KB)
- `1b9eeba6-3084-4196-98b8-719a9b20a92a.jsonl` — CR games batch v1 (bare, no context files) (87KB)
- `67c46c91-5434-42fe-a3f9-c3147f931322.jsonl` — CR games batch v2 (with context.md + learnings.md) (89KB)

## How to extract thinking blocks

```python
import json
with open('SESSION_ID.jsonl') as f:
    for line in f:
        obj = json.loads(line)
        if obj.get('type') == 'assistant':
            for block in obj.get('message', {}).get('content', []):
                if block.get('type') == 'thinking':
                    print(block['thinking'])
```
