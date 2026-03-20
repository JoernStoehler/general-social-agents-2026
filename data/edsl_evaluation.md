# EDSL / Expected Parrot — Evaluation for This Project

**Date:** 2026-03-19
**Evaluator:** Research agent (Claude Sonnet 4.6)
**Purpose:** Decide whether to use EDSL as the LLM simulation harness, or write ~100 lines of Python directly.

---

## What Is EDSL?

EDSL (Expected Parrot Domain-Specific Language) is an open-source Python library developed by
Expected Parrot (founded by Benjamin Manning and John J. Horton, authors of the target paper).
It is designed for conducting surveys and experiments with LLM agents at scale.

- **GitHub:** https://github.com/expectedparrot/edsl (MIT license, ~7,400 commits as of early 2026)
- **PyPI:** `pip install edsl` (latest: v1.0.6, released 2026-01-28; wheel ~2.3 MB)
- **Docs:** https://docs.expectedparrot.com
- **Conflict of interest:** Manning & Horton have a financial interest in Expected Parrot.
  Their paper is listed first on EDSL's "Papers & Citations" page.

---

## Key Findings

### 1. Open source? Yes.
MIT license. Active development (~7,400 commits). Public GitHub. Available on PyPI.

### 2. Multi-provider LLM support? Yes.
Supports 13 inference providers: Anthropic, OpenAI, Azure, Google GenAI, Mistral, Groq,
DeepSeek, Together, Perplexity, xAI, Deep Infra, Bedrock, Ollama. Both Anthropic and OpenAI
are first-class supported.

### 3. Temperature control? Yes.
Temperature is a parameter on the `Model` object. Example:

```python
from edsl import Model
m = Model("claude-opus-4-6", service_name="anthropic", temperature=1.0)
```

Default temperature is 0.5 — so this **must** be explicitly overridden to match our
experiment design (temperature=1).

### 4. Running N iterations of the same prompt? Indirect, fragile.
This is the critical gap. EDSL does not have a first-class `n=200` or `n_trials` parameter.
The pattern for getting N fresh responses is:

- Run with `cache=False` (bypasses caching, gets fresh responses)
- Or create N dummy `Scenario` objects and use `.by(scenarios)`
- Or call `.run()` in a loop N times

The caching system is actually a hazard here: EDSL caches by (model, params, prompt,
iteration). If you run the same prompt twice without `cache=False`, you get the **same
cached response** — the opposite of what we want. For collecting response distributions,
you must explicitly disable caching or use `run(fresh=True)`.

None of the documentation or tutorials show a clean `survey.by(model).run(n=200)` pattern.
The "right" way appears to be running in a loop or using a `ScenarioList` with N identical
scenarios as a workaround.

### 5. Does Manning & Horton's paper use EDSL? Unclear.
The paper reports: "All simulations use GPT-4o with temperature set to 1. We elicit response
distributions for each candidate prompt by prompting GPT-4o 100 times per prompt."
No specific tools or code library are named in the abstract or publicly available excerpts.
The paper is listed on the EDSL papers page, consistent with the authors' financial connection,
but this does not confirm they ran simulations through EDSL.

### 6. Complexity and dependency weight?
EDSL has ~50+ dependencies including aiohttp, httpx, pydantic, jinja2, rich, pyyaml, and
optional extras for Anthropic, OpenAI, pandas, altair, and visualization libraries.
This is a substantial dependency tree for a project that needs to call an API N=200 times
and parse integers.

### 7. Any behavioral economics / game theory examples in EDSL docs? None found.
No notebooks or examples in the EDSL documentation specifically target game-theoretic
experiments, response distributions, or the kind of integer-parsing use case we need.

---

## Summary Assessment

EDSL is a mature, multi-provider LLM survey library optimized for parameterized surveys
with diverse agent personas, scenario injection, and result analysis pipelines. It handles
the general case well.

For our specific use case — call one prompt 200 times at temperature=1, collect raw text
responses, parse an integer, compute a frequency distribution — EDSL adds complexity without
adding value:

| Criterion | EDSL | Custom 100-line harness |
|---|---|---|
| Supports Anthropic + OpenAI | Yes | Yes (via SDK directly) |
| temperature=1 | Yes (explicit override needed) | Yes (trivial) |
| N=200 iterations | Indirect / workaround needed | Trivial (`for _ in range(200)`) |
| Parse integer from response | Not built-in | Trivial regex |
| Caching hazard | Yes (must disable for distributions) | N/A |
| Dependency footprint | ~50+ packages | anthropic + openai only |
| Learning curve | Medium (new DSL, docs to read) | None |
| Audit / transparency | Abstracted | Full visibility |

---

## Recommendation

**Build our own simple harness. Do not use EDSL.**

Rationale:
1. Our use case is simpler than EDSL's design target. EDSL shines for heterogeneous agent
   panels and multi-scenario surveys; we just need N iid samples from a fixed prompt.
2. The caching behavior is a correctness hazard — it could silently return the same response
   200 times if not carefully configured.
3. A ~100-line harness using the Anthropic and OpenAI SDKs directly is more auditable,
   requires no learning curve, and perfectly matches the project's KISS principle.
4. Manning & Horton's conflict of interest is worth noting: EDSL may be recommended by the
   paper's authors partly for commercial reasons, not solely technical merit.
5. The paper itself reports calling GPT-4o 100 times per prompt — a loop, not a DSL.

The right tool here is:
```python
import anthropic, json
client = anthropic.Anthropic()
responses = []
for _ in range(200):
    r = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=64,
        temperature=1,
        messages=[{"role": "user", "content": PROMPT}]
    )
    responses.append(r.content[0].text)
# then parse integers from responses
```

That is ~20 lines. Add logging, parse failures, and metadata: still well under 100 lines.

---

## Sources Checked

- https://github.com/expectedparrot/edsl
- https://pypi.org/project/edsl/
- https://docs.expectedparrot.com/en/latest/language_models.html
- https://docs.expectedparrot.com/en/latest/data.html
- https://docs.expectedparrot.com/en/latest/notebooks/edsl_polling.html
- https://docs.expectedparrot.com/en/latest/papers
- https://arxiv.org/abs/2508.17407 (Manning & Horton 2026)
- https://benjaminmanning.io/project/optimize_agents/
