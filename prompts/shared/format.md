# Output Format

For each game prediction, output a JSON object mapping each possible choice to its predicted probability. Probabilities must sum to 1.0.

Example for a game with choices 1-5:
```json
{"1": 0.05, "2": 0.15, "3": 0.40, "4": 0.30, "5": 0.10}
```

Output ONLY the JSON object, no other text.
