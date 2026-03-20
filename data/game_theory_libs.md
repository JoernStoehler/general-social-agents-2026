# Game Theory Libraries Reference

*Generated: 2026-03-19. Verified by running code in the project environment.*

---

## 1. nashpy (already in requirements.txt)

**Version in environment:** 0.0.43
**Scope:** Two-player games only. Educational focus, uses numpy/scipy. No C dependencies.
**Install:** `pip install nashpy` (already present)

### Minimal usage example

```python
import nashpy as nash
import numpy as np

# Rock-Paper-Scissors (zero-sum, pass one matrix)
A = np.array([[0, -1, 1], [1, 0, -1], [-1, 1, 0]], dtype=float)
game = nash.Game(A)  # zero-sum: B = -A assumed

# Non-zero-sum (pass two matrices)
B = -A
game = nash.Game(A, B)

# Find all Nash equilibria
# support_enumeration: exact but slow on large games (enumerates all support pairs)
for sigma_row, sigma_col in game.support_enumeration():
    print(sigma_row, sigma_col)  # numpy arrays summing to 1

# vertex_enumeration: faster in practice for larger games
for sigma_row, sigma_col in game.vertex_enumeration():
    eu = sigma_row @ A @ sigma_col  # expected utility calculation
    print(sigma_row, sigma_col, eu)
```

**Return type:** Iterator of `(np.ndarray, np.ndarray)` tuples. Each array is a probability
distribution over actions for that player.

**Warning:** `support_enumeration` on a 10x10 game is very slow (2^10 * 2^10 = ~1M pairs to check).
Use `vertex_enumeration` instead for games this size. Even vertex_enumeration may timeout;
for the 11-20 game it found 9 equilibria (not all symmetric).


---

## 2. pygambit

**Version in environment:** 16.5.0 (installed successfully)
**Scope:** N-player games, production-grade, multiple solvers. Requires C extension build.
**Install:** `pip install pygambit`

PyPI package is `pygambit` (not `gambit`). The package `gambit` on PyPI is an unrelated
Scheme interpreter.

### Minimal usage example

```python
import pygambit as gbt
import numpy as np

# Create from numpy arrays — cleanest for our use case
A = np.array([[0, -1, 1], [1, 0, -1], [-1, 1, 0]], dtype=float)
B = -A
g = gbt.Game.from_arrays(A, B)

# Enumerate all mixed strategy Nash equilibria (exact, using LRS vertex enumeration)
result = gbt.nash.enummixed_solve(g)
for eq in result.equilibria:
    for p in g.players:
        probs = [float(eq[s]) for s in p.strategies]
        print(f"Player {p.label}: {probs}")

# Other solvers available:
# gbt.nash.enumpure_solve(g)   — pure strategy equilibria only
# gbt.nash.lp_solve(g)         — linear programming (zero-sum games)
# gbt.nash.lcp_solve(g)        — linear complementarity (2-player)
# gbt.nash.logit_solve(g)      — quantal response equilibria
```

**Return type:** `result.equilibria` is a list of mixed strategy profiles. Access probabilities
via `eq[strategy_object]`, returning `Rational` (exact arithmetic).

### nashpy vs pygambit comparison

| Feature | nashpy | pygambit |
|---|---|---|
| Players | 2 only | N >= 2 |
| Install complexity | pip only, pure Python | pip + C extensions |
| Exact arithmetic | No (float64) | Yes (Rational via GMP) |
| Speed | Slow on large games | Fast (compiled) |
| Best for | Teaching, 2-player research | Production computation |
| Docs | readthedocs, well-documented | readthedocs, comprehensive |

For this project, **nashpy is sufficient** for 2-player games if we use `vertex_enumeration`.
pygambit gives exact rational arithmetic and is faster, but adds a binary dependency.


---

## 3. Level-k / Cognitive Hierarchy libraries

**Finding: No dedicated Python library exists.** The academic search found only custom
implementations in individual research papers. Standard approach is to implement from
scratch using numpy. See the implementation below.


---

## 4. The 11-20 Money Request Game

### Game definition

Two players simultaneously choose an integer in {11, 12, ..., 20}.
- Each player receives their chosen amount as a base payoff.
- If player A requests exactly 1 less than player B, player A receives an additional +20 bonus.
  (The undercut bonus is one-directional per pair: only the lower requester gets it.)

### Payoff matrix (row player)

Rows = row player's action, Columns = column player's action.

```
        11   12   13   14   15   16   17   18   19   20
  11:   11   31   11   11   11   11   11   11   11   11
  12:   12   12   32   12   12   12   12   12   12   12
  13:   13   13   13   33   13   13   13   13   13   13
  14:   14   14   14   14   34   14   14   14   14   14
  15:   15   15   15   15   15   35   15   15   15   15
  16:   16   16   16   16   16   16   36   16   16   16
  17:   17   17   17   17   17   17   17   37   17   17
  18:   18   18   18   18   18   18   18   18   38   18
  19:   19   19   19   19   19   19   19   19   19   39
  20:   20   20   20   20   20   20   20   20   20   20
```

Entry (i, j): row player gets `actions[i]` + 20 if `actions[i] == actions[j] - 1`, else just `actions[i]`.
The column player's payoff matrix B is the transpose-analog (B[i,j] = A[j,i]).

### Nash equilibrium (symmetric mixed strategy)

Derived analytically via indifference conditions. Verified computationally with nashpy and
by direct EU calculation.

The **unique symmetric Nash equilibrium** places positive probability only on {15, 16, 17, 18, 19, 20}:

| Action | Probability | Fraction |
|--------|-------------|----------|
| 11 | 0 | 0 |
| 12 | 0 | 0 |
| 13 | 0 | 0 |
| 14 | 0 | 0 |
| 15 | 0.25 | 5/20 |
| 16 | 0.25 | 5/20 |
| 17 | 0.20 | 4/20 |
| 18 | 0.15 | 3/20 |
| 19 | 0.10 | 2/20 |
| 20 | 0.05 | 1/20 |

**Derivation:** In a symmetric NE, all actions in the support must give equal expected utility.
Setting EU(x) = EU(20) = 20 for each x in {15,...,19}:
- EU(x) = x + 20 * P(opponent plays x+1) = 20
- => P(x+1) = (20 - x) / 20

So: P(16)=5/20, P(17)=4/20, P(18)=3/20, P(19)=2/20, P(20)=1/20.
P(15) = 1 - sum(others) = 5/20.

**Verification:** EU(14) = 14 + 20*(5/20) = 14 + 5 = 19 < 20. Actions 11-14 are not profitable
deviations, confirming they are correctly excluded from the support.

Note: The game has *multiple* Nash equilibria (nashpy vertex_enumeration found 9), but only
one is symmetric. Asymmetric equilibria exist but are not the behavioral baseline.

### Level-k predictions (standard: L0 = uniform)

The level-k model assumes a hierarchy of reasoning types:

| Level | Belief about opponent | Action chosen | Reasoning |
|-------|----------------------|---------------|-----------|
| L0 | (anchor, no strategic reasoning) | uniform over {11,...,20} | by definition |
| L1 | opponent plays L0 (uniform) | **19** | EU(19)=21 > EU(20)=20; x+20*(1/10) maximized at x=19 |
| L2 | opponent plays L1 (plays 19) | **18** | EU(18)=38 (gets 18+20 bonus); dominates all others |
| L3 | opponent plays L2 (plays 18) | **17** | EU(17)=37 (gets 17+20 bonus) |
| L4 | opponent plays L3 (plays 17) | **16** | EU(16)=36 |
| L5 | opponent plays L4 (plays 16) | **15** | EU(15)=35 |
| L6+ | opponent plays L5 (plays 15) | **14** | EU(14)=34; then chain continues down |

**Key insight from Arad & Rubinstein (2012):** Experimentally, ~74% of subjects play {17,18,19},
corresponding to L1-L3. Only ~6% play 20 (Nash equilibrium weight: 5%).
The data strongly favors the level-k model over Nash.

**Correspondence to experimental data (Arad & Rubinstein 2012):**
- 20 → ~6% of subjects (Nash predicts 5%, close)
- 19 → L1 prediction; high frequency
- 18 → L2 prediction; high frequency
- 17 → L3 prediction; high frequency
- 15,16 → Nash predicts 50% combined; observed only ~7% (model failure)

### Python code to build the game

```python
import numpy as np

def build_11_20_game():
    """Returns (A, B) payoff matrices for the 11-20 Money Request Game.

    Actions indexed 0-9 correspond to requests 11-20.
    A[i,j] = payoff to row player when row plays actions[i], col plays actions[j].
    """
    actions = list(range(11, 21))
    n = 10
    A = np.zeros((n, n))
    B = np.zeros((n, n))

    for i, ri in enumerate(actions):
        for j, rj in enumerate(actions):
            A[i, j] = ri + (20 if ri == rj - 1 else 0)
            B[i, j] = rj + (20 if rj == ri - 1 else 0)

    return A, B

def level_k_prediction(k, l0_dist=None):
    """Returns the pure strategy action (as integer 11-20) for level-k player.

    Args:
        k: reasoning level (0=uniform, 1=best-respond to L0, etc.)
        l0_dist: L0 distribution over actions[0..9]; defaults to uniform.
    Returns:
        For k=0: np.ndarray of probabilities (length 10).
        For k>=1: int in {11,...,20} (deterministic best response).
    """
    actions = list(range(11, 21))
    A, _ = build_11_20_game()

    if k == 0:
        return l0_dist if l0_dist is not None else np.ones(10) / 10

    # Recursively get L(k-1) distribution
    prev = level_k_prediction(k - 1, l0_dist)
    if isinstance(prev, int):
        # Convert pure strategy to distribution
        dist = np.zeros(10)
        dist[prev - 11] = 1.0
        prev = dist

    eu = A @ prev
    best = np.argmax(eu)
    return actions[best]

# Example usage:
# A, B = build_11_20_game()
# import nashpy as nash
# game = nash.Game(A, B)
# eqs = list(game.vertex_enumeration())

# Level-k predictions:
# level_k_prediction(0)  => uniform array
# level_k_prediction(1)  => 19
# level_k_prediction(2)  => 18
# level_k_prediction(3)  => 17
```

---

## Sources

- Arad, A. & Rubinstein, A. (2012). "The 11-20 Money Request Game: A Level-k Reasoning Study."
  *American Economic Review* 102(7): 3561-3573.
  https://www.aeaweb.org/articles?id=10.1257/aer.102.7.3561
- nashpy documentation: https://nashpy.readthedocs.io/en/stable/
- nashpy vs gambit discussion: https://nashpy.readthedocs.io/en/stable/discussion/gambit.html
- pygambit documentation: https://gambitproject.readthedocs.io/
- pygambit GitHub: https://github.com/gambitproject/gambit
