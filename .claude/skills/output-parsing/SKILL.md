---
name: output-parsing
description: Robust LLM output parsing for game responses. Load when implementing or debugging the response parser in simulate.py. Covers the parsing cascade, edge cases, and failure logging.
---

# Output Parsing

## The Problem

LLMs frequently wrap responses in explanatory text even when instructed to respond with "only a number." Each experimental condition has different response patterns:

- **Bare/Theory (1-shot):** Usually just a number, sometimes with brief explanation
- **Agent (multi-step):** Extended reasoning followed by a final answer

## Parsing Cascade

Apply in order. Stop at first success.

### Step 1: Direct parse
```python
try:
    value = int(response.strip())
    if game.min_choice <= value <= game.max_choice:
        return value
except ValueError:
    pass
```

### Step 2: First valid integer in response
```python
import re
matches = re.findall(r'\b(\d+)\b', response)
for match in matches:
    value = int(match)
    if game.min_choice <= value <= game.max_choice:
        return value
```

### Step 3: Final answer patterns (for agent condition)
```python
patterns = [
    r'(?:I choose|I predict|My answer|My prediction|I would choose|Final answer)[:\s]+(\d+)',
    r'(?:choose|predict|select)\s+(\d+)',
    r'(\d+)\s*$',  # last number in response
]
for pattern in patterns:
    match = re.search(pattern, response, re.IGNORECASE)
    if match:
        value = int(match.group(1))
        if game.min_choice <= value <= game.max_choice:
            return value
```

### Step 4: Failure
```python
return None  # Log as parse failure
```

## Logging

For each batch, track:
- `parse_failures`: count of None returns
- `parse_failure_rate`: failures / total samples
- `raw_responses`: list of raw response strings (for debugging)

A parse failure rate above 5% in 1-shot conditions suggests the prompt needs revision. Above 15% in agent condition is expected but worth investigating.

## Edge Cases

- Response contains multiple valid integers (e.g., "17 or 18"): take the first.
- Response is empty or whitespace-only: parse failure.
- Response contains the number in words ("seventeen"): not currently handled — log as failure. Consider adding word-to-int if failure rate is high.
- Response is a float (e.g., "17.0"): parse as int via `int(float(response.strip()))`.
