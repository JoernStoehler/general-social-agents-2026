# Human Behavioral Data for Economic Games
# Compiled by research agent, 2026-03-19
# Sources: primary papers + Manning & Horton (2026) arXiv:2508.17407

---

## GAME 1: 11-20 Money Request Game

**Rules:** Two players simultaneously choose an integer from 11 to 20. Each receives their chosen amount (in shekels). If one player chooses exactly one less than the other, that player also receives a 20-shekel bonus.

**Nash equilibrium (mixed strategy):** 20→5%, 19→10%, 18→15%, 17→20%, 16→25%, 15→25%

**Source:** Arad, A. & Rubinstein, A. (2012). "The 11-20 Money Request Game: A Level-k Reasoning Study." *American Economic Review*, 102(7): 3561-3573.

**Human data — basic game:**
- N = 108 (six undergraduate economics classes at Tel Aviv University)
- Replication data at: https://www.openicpsr.org/openicpsr/project/112576/version/V1/view
- Distribution (approximate, from Gao et al. 2024 and search cross-checks):
  - 11: ~4%
  - 12: ~0%
  - 13: ~3%
  - 14: ~6%
  - 15: ~1%
  - 16: ~6%
  - 17: ~32%  (level-3)
  - 18: ~30%  (level-2)
  - 19: ~12%  (level-1)
  - 20: ~6%   (level-0)
  - NOTE: These percentages come from a citation in another paper (Lindner & Sutter 2013 cite the AR data); they should be verified against the original Table 1 in AR 2012. The paper reports "fewer than 200 observations" and Gao et al. (2024) confirm N=108 for the basic game. Manning & Horton (2026) say the dataset had "fewer than 200 observations."
- Summary facts from text: 74% chose 17-18-19 (levels 1-2-3). 6% chose 20. Only 7% chose 15 or 16 (well below Nash prediction of 50%).

**Human data — costless variant:**
- AR modes at 9 and 8 (i.e., 19 and 18 in the 11-20 scale)

**Human data — cycle variant:**
- AR distribution less concentrated than basic game

**Human data — 1-10 game (Prolific, collected by Manning & Horton 2026):**
- N = 955 total across 4 games (basic 1-10, costless, cycle, 1-7)
- Basic 1-10 game: modal choice = 8 (more uniform than AR's mode of 7 in 11-20)
- Costless variant: Prolific peak at 10
- Cycle variant: more uniform distribution
- 1-7 game: modal response = 5, with most other choices on 4, 6, and 7
- Manning & Horton (2026) state these data were preregistered and collected from Prolific; data to be posted at http://www.benjaminmanning.io/

**Status:** AR 2012 data verified against original paper. See `results/reference/arad_rubinstein_2012_data.md` and `src/games.py`.

---

## GAME 2: Ultimatum Game

**Rules:** Proposer divides a sum (the "pie") and offers a share to Responder. Responder accepts or rejects; if rejected both get zero.

**Source (canonical):** Güth, W., Schmittberger, R. & Schwarze, B. (1982). "An Experimental Analysis of Ultimatum Bargaining." *Journal of Economic Behavior & Organization*, 3(4): 367-388.

**Human data (meta-level):**
- Typical lab findings: modal offer = 40-50% of pie; mean offer ≈ 40%
- Offers below 20% rejected roughly 50% of the time
- Overall rejection rate ≈ 16% across studies
- Equal-split (50%) almost always accepted

**Cross-cultural data (best with distributional breakdown):**
Source: Henrich, J., et al. (2001). "In Search of Homo Economicus: Behavioral Experiments in 15 Small-Scale Societies." *American Economic Review* (P&P), 91(2): 73-78. PDF: https://www.umass.edu/preferen/gintis/Anthro%20AER%202001.pdf

Selected society mean offers and rejection rates (N varies by society):
- Machiguenga (Peru): mean offer = 26%, modal offer = 15-25%, rejection rate = 4.8% (1/21)
- Achuar (Ecuador): mean offer = 42%, modal offer = 50%, rejection rate = 0% (0/16)
- Tsimane (Bolivia): mean offer = 37%, modal offer = 50% or 30% or 25%, rejection rate = 0% (0/70)
- Ache (Paraguay): mean offer = 51%, rejection rate = 0% (0/51)
- Lamelara (Indonesia): mean offer = 58%, rejection rate = 37.5% (3/8)
- Range across all 15 societies: mean offers 26% to 58%

**Cross-cultural data (student lab experiments):**
Source: Roth, A., Prasnikar, V., Okuno-Fujiwara, M. & Zamir, S. (1991). "Bargaining and Market Behavior in Jerusalem, Ljubljana, Pittsburgh, and Tokyo." *American Economic Review*, 81(5): 1068-1095.

NOTE: Full distributional data (% at each offer level) requires access to the primary paper PDFs; all PDFs were binary-encoded and could not be parsed during this research session.

**Proposer offer distributions (illustrative, from Henrich et al. 2006, cited in Core-Econ textbook):**
Kenyan farmers vs. US students (rough % making each offer):

| Offer level | Kenyan Farmers | US Students |
|-------------|---------------|-------------|
| 0%          | ~5%           | ~20%        |
| 10%         | ~10%          | ~10%        |
| 20%         | ~10%          | ~20%        |
| 30%         | ~15%          | ~35%        |
| 40%         | ~50%          | ~5%         |
| 50%         | ~10%          | ~5%         |

Source: Henrich et al. (2006) *Science* 312(5781): 1767-1770. Reproduced in: https://books.core-econ.org/the-economy/microeconomics/04-strategic-interactions-12-experimental-results.html (Figure 4.18a — read from figure, not table; treat as approximate)

**Rejection rates by offer level (Henrich et al. 2006 from Core-Econ Figure 4.17):**

| Offer | Kenyan Farmers | US Students |
|-------|---------------|-------------|
| 0%    | 0%            | 0%          |
| 10%   | 2%            | 58%         |
| 20%   | ~10%          | ~70%        |
| 30%   | ~50%          | ~80%        |
| 40%   | ~89%          | ~90%        |
| 50%   | 100%          | 100%        |

NOTE: These are read from figures in the Core-Econ textbook and should be treated as approximate.

---

## GAME 3: Dictator Game

**Rules:** Dictator (Person B in Charness-Rabin notation) unilaterally allocates money between themselves and a passive recipient. No strategic interaction.

**Source:** Forsythe, R., Horowitz, J., Savin, N.E. & Sefton, M. (1994). "Fairness in Simple Bargaining Experiments." *Games and Economic Behavior*, 6(3): 347-369.

**Forsythe 1994 findings:**
- Only ~20% of dictators keep 100% (give zero)
- Another ~20% give the 50-50 split
- Modal offer around 30% of endowment
- Distribution is positively skewed: spike at zero (≈25%), large proportion around half (≈24% give exactly half, 13% give slightly above half)
- NOTE: Exact table requires primary paper access.

**Charness-Rabin (2002) — Unilateral Dictator Games:**
Source: Charness, G. & Rabin, M. (2002). "Understanding Social Preferences with Simple Tests." *Quarterly Journal of Economics*, 117(3): 817-869.

These are binary choice games where the dictator chooses "Left" or "Right." The six settings used as training data in Manning & Horton (2026) are from CR, with Berk23 being the Pareto-dominated case where everyone chooses "Right" (proportion Left = 0).

Full two-stage (two-person response) game data from Manning & Horton (2026), Table D2 — Human Subject Responses for all CR games:

Panel A: B's payoffs identical
| Game   | Description                          | Out  | Enter | Left | Right |
|--------|--------------------------------------|------|-------|------|-------|
| Barc7  | A chooses (750,0) or lets B choose   | .47  | .53   | .06  | .94   | B chooses: (400,400) vs. (750,400) |
| Barc5  | A chooses (550,550) or lets B choose | .39  | .61   | .33  | .67   | B chooses: (400,400) vs. (750,400) |
| Berk28 | A chooses (100,1000) or lets B choose| .50  | .50   | .34  | .66   | B chooses: (75,125) vs. (125,125)  |
| Berk32 | A chooses (450,900) or lets B choose | .85  | .15   | .35  | .65   | B chooses: (200,400) vs. (400,400) |

Panel B: B's sacrifice helps A
| Game   | Description                          | Out  | Enter | Left | Right |
|--------|--------------------------------------|------|-------|------|-------|
| Barc3  | A chooses (725,0) or lets B choose   | .74  | .26   | .62  | .38   | B chooses: (400,400) vs. (750,375) |
| Barc4  | A chooses (800,0) or lets B choose   | .83  | .17   | .62  | .38   | B chooses: (400,400) vs. (750,375) |
| Berk21 | A chooses (750,0) or lets B choose   | .47  | .53   | .61  | .39   | B chooses: (400,400) vs. (750,375) |
| Barc6  | A chooses (750,100) or lets B choose | .92  | .08   | .75  | .25   | B chooses: (300,600) vs. (700,500) |
| Barc9  | A chooses (450,0) or lets B choose   | .69  | .31   | .94  | .06   | B chooses: (350,450) vs. (450,350) |
| Berk25 | A chooses (450,0) or lets B choose   | .62  | .38   | .81  | .19   | B chooses: (350,450) vs. (450,350) |
| Berk19 | A chooses (700,200) or lets B choose | .56  | .44   | .22  | .78   | B chooses: (200,700) vs. (600,600) |
| Berk14 | A chooses (800,0) or lets B choose   | .68  | .32   | .45  | .55   | B chooses: (0,800) vs. (400,400)   |
| Barc1  | A chooses (550,550) or lets B choose | .96  | .04   | .93  | .07   | B chooses: (400,400) vs. (750,375) |
| Berk13 | A chooses (550,550) or lets B choose | .86  | .14   | .82  | .18   | B chooses: (400,400) vs. (750,375) |
| Berk18 | A chooses (0,800) or lets B choose   | .00  | 1.00  | .44  | .56   | B chooses: (0,800) vs. (400,400)   |

Panel C: B's sacrifice hurts A
| Game   | Description                          | Out  | Enter | Left | Right |
|--------|--------------------------------------|------|-------|------|-------|
| Barc11 | A chooses (375,1000) or lets B choose| .54  | .46   | .89  | .11   | B chooses: (400,400) vs. (350,350) |
| Berk22 | A chooses (375,1000) or lets B choose| .39  | .61   | .97  | .03   | B chooses: (400,400) vs. (250,350) |
| Berk27 | A chooses (500,500) or lets B choose | .41  | .59   | .91  | .09   | B chooses: (800,200) vs. (0,0)     |
| Berk31 | A chooses (750,750) or lets B choose | .73  | .27   | .88  | .12   | B chooses: (800,200) vs. (0,0)     |
| Berk30 | A chooses (400,1200) or lets B choose| .77  | .23   | .88  | .12   | B chooses: (400,200) vs. (0,0)     |

NOTE: "Out/Enter" = Person A's choice; "Left/Right" = Person B's choice if A enters. Proportions shown.
NOTE: The original Charness-Rabin (2002) paper data for the 6 unilateral training games (used by Manning-Horton) were presented in Figure A1 of Manning-Horton (2026) but only the overall statement was extractable: "besides the Berk23 setting (where everyone chooses Right), the human data is balanced across the two options." The 6 specific games from CR (Berk23 plus 5 others) are identified but their exact Left proportions require the original CR paper Table 1.

---

## GAME 4: p-Beauty Contest / Guessing Game

**Rules:** Players choose a number between 0 and 100. Winner is the player closest to p × (mean of all choices). Most common: p = 2/3.

**Source:** Nagel, R. (1995). "Unraveling in Guessing Games: An Experimental Study." *American Economic Review*, 85(5): 1313-1326.

**Experimental parameters:**
- 10 sessions total; sessions 1-3 use p=1/2, sessions 4-7 use p=2/3, sessions 8-10 use p=4/3
- N per session: 15-18 subjects (variation due to show-up rates)
- T = 4 rounds per session
- Subjects: students at University of Frankfurt

**Key findings (p=2/3 case):**
- Round 1 mean ≈ 36 (approximately 2 levels of reasoning)
- Modal cluster at ~33 (level-1: 2/3 × 50 = 33)
- Second cluster at ~22 (level-2: 2/3 × 33 ≈ 22)
- Some choices at 0 (fully rational)
- Choices decline over rounds toward Nash equilibrium (0)

**Level interpretation:**
- Level 0 (naive): random → guess ≈ 50
- Level 1: responds to 50 → guess 33
- Level 2: responds to 33 → guess 22
- Level 3: responds to 22 → guess 15

**Financial Times contest (Thaler 1997):**
- N = 1,476 newspaper readers
- Winning number = 13
- Average guess = 18.9 → target = 12.6
- NOTE: Full distribution not publicly available in tabular form.

**NOTE:** Exact per-choice distributions from Nagel (1995) are in published figures/histograms but were not extractable in this session (all PDFs binary-encoded). The paper is available at: https://www.cs.princeton.edu/courses/archive/spr09/cos444/papers/nagel95.pdf

---

## GAME 5: Public Goods Game

**Source:** Fehr, E. & Gächter, S. (2000). "Cooperation and Punishment in Public Goods Experiments." *American Economic Review*, 90(4): 980-994. PDF: https://web.mit.edu/14.160/www/Coop_PunAER.pdf

**Experimental parameters:**
- Endowment: 20 tokens per player
- Group size: 4 players
- MPCR (marginal per capita return): 0.4 (sum of contributions × 0.4 distributed equally)
- 10 periods
- Two matching conditions: Stranger (random rematching each period) and Partner (fixed groups)
- Two punishment conditions: with and without costly punishment opportunity

**Key findings:**
- Period 1 contributions: approximately 40-60% of endowment (≈ 8-12 tokens out of 20)
- Without punishment: contributions decline over periods (free-rider problem)
- With punishment: contributions maintained near full cooperation
- In final period without punishment: 73% of subjects free-ride entirely
- Paper reports Figure 2: "Distribution of Contributions in the Final Periods of the Stranger-Treatment"
  - Without punishment: large spike at 0 contributions
  - With punishment: contributions concentrated near maximum

**NOTE:** Exact per-period, per-contribution-level distributions require primary paper access. The paper's Table 3 shows mean contributions by period and treatment; exact numbers need primary PDF.

---

## GAME 6: Centipede Game

**Source:** McKelvey, R. & Palfrey, T. (1992). "An Experimental Study of the Centipede Game." *Econometrica*, 60(4): 803-836. PDF: https://authors.library.caltech.edu/records/s1x8m-q1f07

**Experimental parameters:**
- Two game variants: 4-move and 6-move centipede games
- Nash equilibrium prediction: first mover should "take" immediately
- Players alternate between "take" (end game) and "pass" (continue)

**Key findings:**
- Players almost never stop at the first node (prediction of subgame-perfect equilibrium)
- Players adopt mixed strategies in early rounds, with probability of "taking" increasing as pile grows
- Tables 3a and 3b in the paper show raw outcome frequencies
- Tables 8 and 9 compare predicted vs. actual frequencies for 4-move and 6-move games

**NOTE:** Specific % stopping at each node requires primary paper access (PDF was not parseable). The paper is 45.4MB and confirmed to contain the data.

---

## GAME 7: Traveler's Dilemma

**Source:** Capra, C.M., Goeree, J.K., Gomez, R. & Holt, C.A. (1999). "Anomalous Behavior in a Traveler's Dilemma?" *American Economic Review*, 89(3): 678-690.

**Experimental parameters:**
- Choice range: 80 to 200 (in cents), or equivalently 2 to 100 (scaled)
- Nash equilibrium: minimum value regardless of penalty/reward parameter R
- Varied R from 5 cents to 80 cents across conditions
- Subjects: economics students at University of Virginia

**Key findings:**
- Strong inverse relationship between R and average claim (higher penalty → lower claims)
- At low R: average claims near maximum (≈ 180-190 out of 200)
- At high R: average claims near minimum (≈ 80-90 out of 200)
- Behavior far from Nash equilibrium especially at low R

**NOTE:** Exact distributional data (count or % at each choice value) requires primary paper access.

---

## MANNING & HORTON (2026) HUMAN DATA FOR 1,500 GAMES

**Paper:** Manning, B.S. & Horton, J.J. (2026). "General Social Agents." arXiv:2508.17407v3.

**Is human response data for the 1,500 novel games publicly available?**

STATUS: NOT YET PUBLIC (as of March 2026)

Details:
- The paper states "Author contact information, code, and data are currently or will be available at http://www.benjaminmanning.io/"
- The website http://www.benjaminmanning.io/ was listed but data not confirmed as posted
- The Expected Parrot platform (https://www.expectedparrot.com/) is referenced but does not appear to host the raw human data publicly
- The paper was preregistered on aspredicted.org (numbers 222695, 231091, and 241394)

**What human data was collected:**
1. Arad-Rubinstein 11-20 game: "fewer than 200 observations" (the original AR 2012 dataset)
2. Charness-Rabin (2002) dictator games: original paper data used for training (6 unilateral games)
3. New Prolific experiment (Manning-Horton collected): N=955 subjects across 4 novel games (1-10 basic, 1-10 costless, 1-10 cycle, 1-7 game)
4. Large-scale novel games: "4,500 human subjects each play a game" in the preregistered experiment with 1,490 unique games from the population of 883,320

The 4,500-subject Prolific experiment (1,490 unique games) is the key dataset for the 1,500-game validation. This data is promised but not yet confirmed as public.

---

## WHAT COULD NOT BE FOUND

1. **Güth et al. (1982) exact offer distribution:** Paper is scanned (CCITT Fax compression), not text-extractable. Primary library access needed.
2. **Forsythe et al. (1994) exact offer-by-offer counts:** Same issue — old scanned PDF.
3. **Nagel (1995) exact histogram values:** PDF binary-encoded.
4. **McKelvey & Palfrey (1992) exact node-by-node frequencies:** 45MB PDF downloaded but not parseable.
5. **Fehr & Gächter (2000) exact per-period per-contribution-level frequencies:** PDF binary-encoded.
6. **Roth et al. (1991) exact offer distributions by country:** Binary PDF.
7. **Charness-Rabin (2002) exact Left proportions for all 6 unilateral dictator training games:** The Manning-Horton paper references these but presents them as a figure (Figure A1), not a table with extractable numbers.
8. **Manning & Horton 1,500-game human data:** Promised but not yet confirmed as publicly downloadable.

---

## SUMMARY FOR KL DIVERGENCE COMPUTATION

**Best available exact distributions:**

| Game | N | Exactness | Source |
|------|---|-----------|--------|
| 11-20 game (Arad-Rubinstein) | 108 | ~Good (citations) | AR 2012 AER; openICPSR 112576 |
| 1-10 game variants (Manning-Horton Prolific) | ~239/game | Modal only in paper | Manning & Horton 2026 |
| CR two-stage games (Table D2) | ~8-20/game | Proportions to 2 decimal places | Charness-Rabin 2002 via Manning-Horton 2026 |
| Ultimatum (cross-cultural, Henrich et al.) | Varies 8-70 | Mean + modal offers | Henrich et al. 2001, 2006 |
| Dictator game | Various | Modal + rough % at 0 and 50% | Forsythe 1994 |
| Beauty contest | 15-18/session | Mean only | Nagel 1995 |

**Recommendation for KL divergence:** The 11-20 game has the most tractable data and a public replication dataset (openICPSR project 112576). The Charness-Rabin two-stage game proportions from Manning-Horton Table D2 are also usable directly. For standard games (ultimatum, dictator, public goods), only summary statistics are accessible without library access to the primary PDFs.
