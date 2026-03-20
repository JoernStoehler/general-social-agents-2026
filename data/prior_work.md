# Prior Work: LLMs as Human Behavior Simulators

Compiled 2026-03-19 for the General Social Agents replication project.

---

## 1. Horton, Filippas & Manning (2023) — Homo Silicus

**Citation:** "Large Language Models as Simulated Economic Agents: What Can We Learn from Homo Silicus?"
NBER Working Paper 31122. Published at ACM EC 2024.

**URLs:**
- Paper: https://arxiv.org/abs/2301.07543
- PDF (direct): https://john-joseph-horton.com/papers/llm_ask.pdf
- Official replication code: https://github.com/johnjosephhorton/homo_silicus
- Community Python package: https://github.com/yachty66/EconomicAgents

**What they did:**
Argued that LLMs are implicit computational models of humans ("Homo silicus") and can be given endowments, preferences, and information to simulate economic behavior. Ran LLMs through four classic behavioral economics experiments: Charness-Rabin dictator games, Kahneman status quo bias (Zeckhauser), an "Horton" task, and a fairness/pricing experiment. Used OpenAI API (GPT-3/3.5 era). Results were qualitatively consistent with human data.

**Experimental method:**
Prompt the LLM with the game framing, elicit a choice, repeat N times to build a distribution, compare to human data from the original papers. Results stored in SQLite databases (JSON).

**Reusable code:** Yes. The official repo (`johnjosephhorton/homo_silicus`) contains Python + R code for all four experiments. The community package (`yachty66/EconomicAgents`) wraps each experiment as a Python class with `.play()` and `.create_plot()` methods.

**Relevance to us:** Direct ancestor. Manning is a co-author. The simulation-as-distribution methodology is exactly what we are replicating.

---

## 2. Manning & Horton (2026) — General Social Agents (the paper we are replicating)

**Citation:** "General Social Agents," Benjamin S. Manning & John J. Horton (MIT).
arXiv:2508.17407. NBER Working Paper w34937. Revise & Resubmit at Econometrica.

**URLs:**
- arXiv: https://arxiv.org/abs/2508.17407
- HTML version: https://arxiv.org/html/2508.17407v3
- NBER: https://www.nber.org/papers/w34937
- Author page: https://benjaminmanning.io/project/optimize_agents/

**What they did:**
Built "general" LLM agents using theory-grounded natural language instructions, calibrated on human data from "seed" games, and tested whether they could predict human behavior in 1,500 novel games out-of-sample. Flagship game: Arad & Rubinstein (2012) 11-20 money request game and a population of 883,320 variants. Also used Charness-Rabin dictator games. Compared against cognitive hierarchy models, Nash equilibrium, and out-of-the-box GPT-4o (temperature=1). Experiments preregistered on AsPredicted.

**Key numbers:**
- 883,320 novel game variants generated
- 1,500 games sampled for preregistered evaluation
- Human subjects recruited on Prolific
- GPT-4o at temperature=1 as the baseline ("out-of-the-box" condition)

**Reusable code:** No public GitHub found. Authors mention code availability at benjaminmanning.io but no repository link confirmed. A public notebook "demonstrating agent construction from behavioral economics papers" is mentioned.

**Relevance to us:** This is our target paper. The key claim we test: do Claude Opus 4.6 / Claude Sonnet 4.6 predict human play better than GPT-4o did as the out-of-the-box baseline?

---

## 3. Aher, Arriaga & Kalai (2022/2023) — Turing Experiments

**Citation:** "Using Large Language Models to Simulate Multiple Humans and Replicate Human Subject Studies."
arXiv:2208.10264. Published at ICML 2023.

**URLs:**
- arXiv: https://arxiv.org/abs/2208.10264
- Official code: https://github.com/microsoft/turing-experiments
- Author repo: https://github.com/GatiAher/Using-Large-Language-Models-to-Replicate-Human-Subject-Studies

**What they did:**
Introduced "Turing Experiments" (TEs): evaluate an LLM by having it simulate a representative *sample* of participants (not one individual), then test whether the resulting distribution matches the human distribution. Applied to four experiments: Ultimatum Game, Garden Path Sentences, Milgram Shock Experiment, Wisdom of Crowds. Used GPT-3/ChatGPT/GPT-4. Three of four experiments replicated successfully; GPT-4 showed "hyper-accuracy distortion" on Wisdom of Crowds.

**Experimental method:**
Run LLM N times per scenario, collect response distribution, compare to human data using statistical tests. This is the most direct methodological precedent for the sampling approach we use.

**Reusable code:** Yes, Microsoft-hosted. Python code for all four experiments available at https://github.com/microsoft/turing-experiments.

**Relevance to us:** Establishes the "run N times, compare distributions" methodology explicitly. Good reference for how to frame statistical comparisons.

---

## 4. Akata et al. (2023/2025) — Playing Repeated Games with LLMs

**Citation:** "Playing Repeated Games with Large Language Models."
arXiv:2305.16867. Published in *Nature Human Behaviour* 9, 1380-1390 (2025).

**URLs:**
- arXiv: https://arxiv.org/abs/2305.16867
- Nature: https://www.nature.com/articles/s41562-025-02172-y
- PDF: https://hcai-munich.com/pubs/Akata2025Games.pdf

**What they did:**
Had LLMs play finitely-repeated 2x2 games against each other and against human players. Games included iterated Prisoner's Dilemma (and variants) and Battle of the Sexes. Tested GPT-4. Found LLMs perform well in self-interested games but fail at coordination games. GPT-4 retaliates too rapidly (defects after a single defection). Introduced "social chain-of-thought" prompting to improve coordination with human players.

**Reusable code:** Not confirmed in abstract; TeX source on arXiv. No GitHub found in search.

**Relevance to us:** Relevant for understanding where LLMs diverge from human strategic behavior, and specifically the role of prompt framing — directly applicable to designing our conditions.

---

## 5. LLMs Replicating Human Cooperation (arxiv 2511.04500, 2025)

**Citation:** "Large Language Models Replicate and Predict Human Cooperation Across Experiments in Game Theory."
arXiv:2511.04500 (submitted November 2025).

**URL:** https://arxiv.org/html/2511.04500v2

**What they did:**
Built a "digital twin of game-theoretic experiments." Tested Llama, Mistral, and Qwen on cooperative game experiments. Achieved "population-level behavioral replication without persona-based prompting" — meaning aggregate human distributions matched without per-agent personas. Extended tests to novel game configurations outside the original parameter grid.

**Reusable code:** Not confirmed in abstract.

**Relevance to us:** Confirms population-level (aggregate distribution) matching without personas is feasible. Directly parallels our experimental approach.

---

## Visualization: Grouped Bar Chart for Predicted vs. Observed

For overlaying predicted (LLM) vs. observed (human) discrete distributions, the standard approach is a grouped bar chart using matplotlib with offset bar positions.

### Pattern (matplotlib, pure):

```python
import numpy as np
import matplotlib.pyplot as plt

def plot_predicted_vs_observed(categories, human_dist, llm_dist,
                                xlabel="Choice", ylabel="Proportion",
                                title="LLM vs. Human Distribution",
                                human_label="Human (Arad & Rubinstein 2012)",
                                llm_label="LLM (Claude Sonnet 4.6)"):
    x = np.arange(len(categories))
    width = 0.35

    fig, ax = plt.subplots(figsize=(9, 5))
    bars_human = ax.bar(x - width/2, human_dist, width,
                        label=human_label, color="#4C72B0", alpha=0.85)
    bars_llm   = ax.bar(x + width/2, llm_dist,   width,
                        label=llm_label,  color="#DD8452", alpha=0.85)

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.legend()
    ax.yaxis.grid(True, linestyle="--", alpha=0.5)
    ax.set_axisbelow(True)
    fig.tight_layout()
    return fig
```

For the 11-20 game specifically: categories = [11, 12, 13, 14, 15, 16, 17, 18, 19, 20], both distributions are proportions summing to 1.

### Seaborn alternative (tidy-data format):

```python
import pandas as pd
import seaborn as sns

# Build long-form dataframe
rows = []
for val, p in zip(categories, human_dist):
    rows.append({"choice": val, "proportion": p, "source": "Human"})
for val, p in zip(categories, llm_dist):
    rows.append({"choice": val, "proportion": p, "source": "LLM"})
df = pd.DataFrame(rows)

fig, ax = plt.subplots(figsize=(9, 5))
sns.barplot(data=df, x="choice", y="proportion", hue="source",
            palette=["#4C72B0", "#DD8452"], ax=ax)
ax.set_title("LLM vs. Human Distribution")
fig.tight_layout()
```

**Reference:** Seaborn grouped barplot pattern: https://seaborn.pydata.org/examples/grouped_barplot.html
**Matplotlib stacked/grouped gist:** https://gist.github.com/ctokheim/6435202a1a880cfecd71

---

## Gaps and What Was Not Found

1. **Manning & Horton (2026) code:** No public repository confirmed. Authors mention a public notebook but no URL was found. Possible it will be released upon journal acceptance.

2. **Exact GPT-4o prompts** from the original paper: Not extractable from the binary PDF; full paper text would need to be accessed via NBER (paywalled) or arXiv HTML.

3. **Arad & Rubinstein human data file:** Raw CSV of the original 11-20 game human choices is not in a public repo — must be extracted from the paper's figures or requested from authors.

4. **Playing Repeated Games (Akata et al.) code:** Not confirmed public.

5. **Replication attempts of Manning & Horton (2026) specifically:** None found as of March 2026, which is expected given the paper only appeared on arXiv in August 2025.

---

## Key Takeaway

The "run LLM N times, compare output distribution to human data" methodology is well-established (Horton 2023, Aher 2022). Official replication code exists for Horton (2023) at `johnjosephhorton/homo_silicus` and for Aher (2022) at `microsoft/turing-experiments`. Manning & Horton (2026) is the direct target; its out-of-the-box GPT-4o baseline (temperature=1) is what we are trying to beat with newer Claude models.
