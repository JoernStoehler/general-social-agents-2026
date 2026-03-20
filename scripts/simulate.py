"""LLM simulation harness for predicting human game play.

Two methods:
1. predict_distribution — asks the model to directly output a probability distribution
2. sample_responses — calls the model N times with role-play, builds empirical distribution

Two backends:
- "cli": Uses `claude -p` (free under Max subscription). Default.
- "sdk": Uses Anthropic Python SDK (requires ANTHROPIC_API_KEY, costs money).
"""

import json
import logging
import re
import shutil
import subprocess
import time
from pathlib import Path

from games import Game

logger = logging.getLogger(__name__)

RESULTS_DIR = Path(__file__).parent.parent / "results"

DEFAULT_MODEL = "claude-opus-4-6"
DEFAULT_BACKEND = "cli"

# Locate the claude CLI binary (may be installed globally or via npx)
_CLAUDE_BIN: str | None = shutil.which("claude")


def _claude_cmd() -> list[str]:
    """Return the command prefix for invoking claude CLI."""
    if _CLAUDE_BIN:
        return [_CLAUDE_BIN]
    # Fallback to npx
    return ["npx", "@anthropic-ai/claude-code"]


def _save_result(filename: str, data: dict) -> Path:
    """Save a result dict as JSON to the results directory."""
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    path = RESULTS_DIR / filename
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    logger.info(f"Saved result to {path}")
    return path


def _parse_json_from_text(raw_text: str) -> dict:
    """Extract and parse a JSON object from model response text.

    Handles: raw JSON, markdown code fences, surrounding prose.
    """
    text = raw_text.strip()

    # Try extracting from code fences first
    if "```" in text:
        match = re.search(r"```(?:\s*json)?\s*\n(.*?)\n?```", text, re.DOTALL)
        if match:
            text = match.group(1).strip()

    # Try parsing as-is
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Try finding a JSON object in the text
    match = re.search(r"\{[^{}]*\}", text)
    if match:
        return json.loads(match.group())

    raise ValueError(f"Could not parse JSON from response: {raw_text[:200]}")


def _normalize_distribution(raw: dict, action_space: list[int]) -> dict[int, float]:
    """Convert parsed JSON to a normalized distribution over the action space."""
    distribution = {int(k): float(v) for k, v in raw.items()}
    total = sum(distribution.values())
    if total > 0:
        distribution = {k: v / total for k, v in distribution.items()}
    return distribution


# ---------------------------------------------------------------------------
# CLI backend (claude -p, free under Max subscription)
# ---------------------------------------------------------------------------


def _call_cli(
    prompt: str,
    model: str = DEFAULT_MODEL,
    system_prompt: str | None = None,
    timeout: int = 180,
) -> str:
    """Call claude -p and return the raw text response."""
    cmd = [
        *_claude_cmd(),
        "-p",
        "--model", model,
        "--tools", "",  # Disable all tools — just answer the question
        "--output-format", "text",
        "--no-session-persistence",
    ]
    if system_prompt:
        cmd.extend(["--system-prompt", system_prompt])

    logger.info(f"Calling claude -p with model={model}")
    result = subprocess.run(
        cmd,
        input=prompt,
        capture_output=True,
        text=True,
        timeout=timeout,
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"claude -p exited with code {result.returncode}: {result.stderr[:500]}"
        )

    return result.stdout


# ---------------------------------------------------------------------------
# SDK backend (Anthropic Python SDK, requires API key)
# ---------------------------------------------------------------------------


def _call_sdk(
    prompt: str,
    model: str = DEFAULT_MODEL,
    temperature: float = 0,
    max_tokens: int = 1024,
) -> str:
    """Call Anthropic API via Python SDK and return the raw text response."""
    import anthropic

    client = anthropic.Anthropic()
    response = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def _default_predict_prompt(game: Game) -> str:
    """Default prompt for direct distribution prediction."""
    return (
        f"Here is a game: {game.description}\n\n"
        f"What probability distribution over choices "
        f"{{{', '.join(str(a) for a in game.action_space)}}} "
        f"do you predict for human participants?\n\n"
        f"Return ONLY a JSON object mapping each choice (as string key) "
        f"to its probability (as a number between 0 and 1, summing to 1). "
        f"Example format: {{\"11\": 0.05, \"12\": 0.03, ...}}"
    )


def _default_sample_prompt(game: Game) -> str:
    """Default prompt for sampling a single choice."""
    return (
        "You are answering questions as if you were a human. "
        "Do not break character.\n\n"
        f"{game.description}\n\n"
        "What amount of money would you request? "
        "Reply with just the number."
    )


def predict_distribution(
    game: Game,
    model: str = DEFAULT_MODEL,
    prompt: str | None = None,
    backend: str = DEFAULT_BACKEND,
    save: bool = True,
) -> dict[int, float]:
    """Ask the model to directly predict the human distribution as JSON.

    One call. Returns a dict of action -> probability.

    Args:
        backend: "cli" (claude -p, free under Max) or "sdk" (API key, costs money).
    """
    if prompt is None:
        prompt = _default_predict_prompt(game)

    if backend == "cli":
        raw_text = _call_cli(prompt, model=model)
    elif backend == "sdk":
        raw_text = _call_sdk(prompt, model=model, temperature=0)
    else:
        raise ValueError(f"Unknown backend: {backend}")

    logger.info(f"Raw response (predict_distribution): {raw_text[:500]}")

    parsed = _parse_json_from_text(raw_text)
    distribution = _normalize_distribution(parsed, game.action_space)

    if save:
        _save_result(
            f"predict_{model}_{game.name.replace(' ', '_')}_{int(time.time())}.json",
            {
                "method": "predict_distribution",
                "backend": backend,
                "model": model,
                "game": game.name,
                "prompt": prompt,
                "raw_response": raw_text,
                "distribution": {str(k): v for k, v in distribution.items()},
            },
        )

    return distribution


def _parse_action(text: str, action_space: list[int]) -> int | None:
    """Parse an integer action from model response text.

    Strategy: try int(text) first, then regex for first valid integer.
    """
    text = text.strip()

    # Try direct integer parse
    try:
        val = int(text)
        if val in action_space:
            return val
    except ValueError:
        pass

    # Regex: find all integers, return first one in action space
    for match in re.finditer(r"\b(\d+)\b", text):
        val = int(match.group(1))
        if val in action_space:
            return val

    return None


def sample_responses(
    game: Game,
    model: str = DEFAULT_MODEL,
    prompt: str | None = None,
    n: int = 50,
    temperature: float = 1.0,
    backend: str = DEFAULT_BACKEND,
    save: bool = True,
) -> dict[int, float]:
    """Call the model N times with a role-play prompt, build empirical distribution.

    Each call asks the model to play the game as a human participant.
    Responses are parsed to extract integer choices.

    Note: CLI backend ignores the temperature parameter (claude -p has no
    temperature control). Variance comes from the model's internal sampling.
    """
    if prompt is None:
        prompt = _default_sample_prompt(game)

    raw_responses: list[str] = []
    parsed_actions: list[int | None] = []
    failures = 0

    for i in range(n):
        if backend == "cli":
            raw = _call_cli(prompt, model=model)
        elif backend == "sdk":
            raw = _call_sdk(
                prompt, model=model, temperature=temperature, max_tokens=256
            )
        else:
            raise ValueError(f"Unknown backend: {backend}")

        raw_responses.append(raw)
        action = _parse_action(raw, game.action_space)
        parsed_actions.append(action)
        if action is None:
            failures += 1
            logger.warning(f"Parse failure on sample {i}: {raw[:100]}")

    # Build empirical distribution from valid responses
    valid = [a for a in parsed_actions if a is not None]
    distribution = {a: 0.0 for a in game.action_space}
    if valid:
        for a in valid:
            distribution[a] += 1.0
        total = sum(distribution.values())
        distribution = {a: c / total for a, c in distribution.items()}

    logger.info(
        f"sample_responses: {len(valid)}/{n} valid, {failures} failures"
    )

    if save:
        _save_result(
            f"sample_{model}_{game.name.replace(' ', '_')}_{int(time.time())}.json",
            {
                "method": "sample_responses",
                "backend": backend,
                "model": model,
                "game": game.name,
                "prompt": prompt,
                "n_requested": n,
                "n_valid": len(valid),
                "n_failures": failures,
                "temperature": temperature if backend == "sdk" else None,
                "raw_responses": raw_responses,
                "parsed_actions": parsed_actions,
                "distribution": {str(k): v for k, v in distribution.items()},
            },
        )

    return distribution


if __name__ == "__main__":
    from games import ELEVEN_TWENTY_GAME

    logging.basicConfig(level=logging.INFO)

    game = ELEVEN_TWENTY_GAME

    # Test parsing
    assert _parse_action("17", game.action_space) == 17
    assert _parse_action("I would request 18 shekels.", game.action_space) == 18
    assert _parse_action("My choice is 20.", game.action_space) == 20
    assert _parse_action("banana", game.action_space) is None
    print("Parsing tests passed.")

    # Uncomment to run actual experiments:
    # dist = predict_distribution(game, backend="cli")
    # print(f"Direct prediction (CLI): {dist}")
    #
    # dist = predict_distribution(game, backend="sdk")
    # print(f"Direct prediction (SDK): {dist}")
