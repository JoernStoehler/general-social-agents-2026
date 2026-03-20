# Task: Predict human choices in 20 allocation games

## The experiments

These are 20 two-stage dictator games from Charness & Rabin (2002, Quarterly Journal of Economics). Human data from university students playing for real money.

**Game structure**: In each game:
- **Person A** chooses between "Out" (a fixed allocation) or "Enter" (lets Person B decide)
- **Person B** chooses between "Left" and "Right" (two different allocations)
- Person B chooses WITHOUT knowing what A chose (strategy method)
- Both players know all payoffs in advance

**Important**: Because B chooses without knowing A's decision (strategy method), B's choice reflects their unconditional preference between Left and Right. This is not a strategic response to A — it's a direct preference revelation.

**Key behavioral factors in these games**:
- **Self-interest**: People prefer more money for themselves, all else equal
- **Inequality aversion**: People dislike unfair outcomes, especially when they get less
- **Efficiency**: People often prefer the allocation with higher total payoff
- **Reciprocity**: B may "reward" or "punish" A by choosing allocations that help/hurt A, even at cost to self. But remember: B doesn't know A's choice, so reciprocity here is about B's general attitude toward the game structure, not a response to A's actual action
- **When multiple motives conflict**: Different people weigh these differently. Some are mostly selfish, some are fairness-oriented, some are efficiency-oriented. The DISTRIBUTION reflects this mixture of types in the population

**Critical patterns that past AI systems got wrong**:
- **"Free generosity"**: When B's payoff is IDENTICAL across Left and Right, the choice is costless to B. In this case, the vast majority of humans (85-95%) choose the option that helps A more. Being generous when it costs nothing is nearly universal — do NOT predict 50-50 here.
- **Risk aversion for A**: When Out gives A a decent, safe outcome, most humans take it — especially if Enter introduces risk. When Out gives (550, 550) or similar fair outcomes, 85-96% of A's choose Out. Don't underestimate how risk-averse humans are when the safe option is "good enough."
- **Extreme predictions are real**: In games where one option dominates on multiple dimensions, 80-95% of people choose it. Do NOT default to moderate predictions out of uncertainty.
- **Each game is different**: Do NOT copy predictions across games. Even if two games look structurally similar, small payoff differences can shift behavior substantially. Reason about each game independently.

## Games

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

## How to approach this

Work through each game individually. For each game:
1. Identify what motives (self-interest, fairness, efficiency, reciprocity) point which direction
2. Consider whether the motives align (→ extreme prediction) or conflict (→ moderate prediction)
3. Commit to a specific prediction — don't default to 0.50 or 0.60 out of uncertainty

Many games have one option that dominates on multiple dimensions. When that happens, predict 80-95% choosing it. Only predict moderate splits when motives genuinely conflict.

## Output format

Output a JSON array with 20 objects, one per game, in order:
```json
[
  {"game": "Barc7", "out": 0.XX, "enter": 0.XX, "left": 0.XX, "right": 0.XX},
  ...
]
```
Where "out"+"enter"=1.0 and "left"+"right"=1.0 for each game. Output ONLY the JSON array.
