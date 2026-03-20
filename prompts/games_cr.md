# Games: 20 Charness-Rabin Two-Stage Dictator Games

## Experiment details

**Source**: Charness & Rabin (2002), "Understanding Social Preferences with Simple Tests," Quarterly Journal of Economics 117(3): 817-869.

**Participants**: University students playing for real money.

**Game structure**: In each game:
- **Person A** chooses between "Out" (a fixed allocation) or "Enter" (lets Person B decide)
- **Person B** chooses between "Left" and "Right" (two different allocations)
- Person B chooses WITHOUT knowing what A chose (strategy method)
- Both players know all payoffs in advance

**Important**: Because B chooses without knowing A's decision (strategy method), B's choice reflects their unconditional preference between Left and Right. This is not a strategic response to A — it's a direct preference revelation.

## Predict

For each game below, predict P(A chooses Out) and P(B chooses Left).

### Game 1: Barc7 (Panel A)
Out: (750 to A, 0 to B). Enter → B chooses: Left (400 to A, 400 to B) or Right (750 to A, 400 to B).

### Game 2: Barc5 (Panel A)
Out: (550 to A, 550 to B). Enter → B chooses: Left (400 to A, 400 to B) or Right (750 to A, 400 to B).

### Game 3: Berk28 (Panel A)
Out: (100 to A, 1000 to B). Enter → B chooses: Left (75 to A, 125 to B) or Right (125 to A, 125 to B).

### Game 4: Berk32 (Panel A)
Out: (450 to A, 900 to B). Enter → B chooses: Left (200 to A, 400 to B) or Right (400 to A, 400 to B).

### Game 5: Barc3 (Panel B)
Out: (725 to A, 0 to B). Enter → B chooses: Left (400 to A, 400 to B) or Right (750 to A, 375 to B).

### Game 6: Barc4 (Panel B)
Out: (800 to A, 0 to B). Enter → B chooses: Left (400 to A, 400 to B) or Right (750 to A, 375 to B).

### Game 7: Berk21 (Panel B)
Out: (750 to A, 0 to B). Enter → B chooses: Left (400 to A, 400 to B) or Right (750 to A, 375 to B).

### Game 8: Barc6 (Panel B)
Out: (750 to A, 100 to B). Enter → B chooses: Left (300 to A, 600 to B) or Right (700 to A, 500 to B).

### Game 9: Barc9 (Panel B)
Out: (450 to A, 0 to B). Enter → B chooses: Left (350 to A, 450 to B) or Right (450 to A, 350 to B).

### Game 10: Berk25 (Panel B)
Out: (450 to A, 0 to B). Enter → B chooses: Left (350 to A, 450 to B) or Right (450 to A, 350 to B).

### Game 11: Berk19 (Panel B)
Out: (700 to A, 200 to B). Enter → B chooses: Left (200 to A, 700 to B) or Right (600 to A, 600 to B).

### Game 12: Berk14 (Panel B)
Out: (800 to A, 0 to B). Enter → B chooses: Left (0 to A, 800 to B) or Right (400 to A, 400 to B).

### Game 13: Barc1 (Panel B)
Out: (550 to A, 550 to B). Enter → B chooses: Left (400 to A, 400 to B) or Right (750 to A, 375 to B).

### Game 14: Berk13 (Panel B)
Out: (550 to A, 550 to B). Enter → B chooses: Left (400 to A, 400 to B) or Right (750 to A, 375 to B).

### Game 15: Berk18 (Panel B)
Out: (0 to A, 800 to B). Enter → B chooses: Left (0 to A, 800 to B) or Right (400 to A, 400 to B).

### Game 16: Barc11 (Panel C)
Out: (375 to A, 1000 to B). Enter → B chooses: Left (400 to A, 400 to B) or Right (350 to A, 350 to B).

### Game 17: Berk22 (Panel C)
Out: (375 to A, 1000 to B). Enter → B chooses: Left (400 to A, 400 to B) or Right (250 to A, 350 to B).

### Game 18: Berk27 (Panel C)
Out: (500 to A, 500 to B). Enter → B chooses: Left (800 to A, 200 to B) or Right (0 to A, 0 to B).

### Game 19: Berk31 (Panel C)
Out: (750 to A, 750 to B). Enter → B chooses: Left (800 to A, 200 to B) or Right (0 to A, 0 to B).

### Game 20: Berk30 (Panel C)
Out: (400 to A, 1200 to B). Enter → B chooses: Left (400 to A, 200 to B) or Right (0 to A, 0 to B).

## Output format

Output a JSON array with 20 objects, one per game, in order:
```json
[
  {"game": "Barc7", "out": 0.XX, "enter": 0.XX, "left": 0.XX, "right": 0.XX},
  ...
]
```
Where "out"+"enter"=1.0 and "left"+"right"=1.0 for each game.
