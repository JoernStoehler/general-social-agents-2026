"""LLM simulation harness for predicting human game play.

Two methods:
1. predict_distribution — asks the model to directly output a probability distribution
2. sample_responses — calls the model N times with role-play, builds empirical distribution
"""

import json
import logging
import re
import time
from pathlib import Path

import anthropic

from src.games import Game

logger = logging.getLogger(__name__)

RESULTS_DIR = Path(__file__).parent.parent / "results"

DEFAULT_MODEL = "claude-opus-4-6"


def _get_client() -> anthropic.Anthropic:
    """Create an Anthropic client. Requires ANTHROPIC_API_KEY env var."""
    return anthropic.Anthropic()


def _save_result(filename: str, data: dict) -> Path:
    """Save a result dict as JSON to the results directory."""
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    path = RESULTS_DIR / filename
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    logger.info(f"Saved result to {path}")
    return path


def predict_distribution(
    game: Game,
    model: str = DEFAULT_MODEL,
    prompt: str | None = None,
    save: bool = True,
) -> dict[int, float]:
    """Ask the model to directly predict the human distribution as JSON.

    One API call. Returns a dict of action -> probability.
    """
    if prompt is None:
        prompt = (
            f"Here is a game: {game.description}\n\n"
            f"What probability distribution over choices "
            f"{{{', '.join(str(a) for a in game.action_space)}}} "
            f"do you predict for human participants?\n\n"
            f"Return ONLY a JSON object mapping each choice (as string key) "
            f"to its probability (as a number between 0 and 1, summing to 1). "
            f"Example format: {{\"11\": 0.05, \"12\": 0.03, ...}}"
        )

    client = _get_client()
    response = client.messages.create(
        model=model,
        max_tokens=1024,
        temperature=0,  # Direct prediction: we want the model's best estimate
        messages=[{"role": "user", "content": prompt}],
    )

    raw_text = response.content[0].text
    logger.info(f"Raw response (predict_distribution): {raw_text[:500]}")

    # Parse JSON from response (handle markdown code blocks)
    text = raw_text.strip()
    if "```" in text:
        # Extract content between code fences
        match = re.search(r"```(?:json)?\s*\n?(.*?)\n?```", text, re.DOTALL)
        if match:
            text = match.group(1).strip()

    parsed = json.loads(text)
    distribution = {int(k): float(v) for k, v in parsed.items()}

    # Normalize to sum to 1
    total = sum(distribution.values())
    if total > 0:
        distribution = {k: v / total for k, v in distribution.items()}

    if save:
        _save_result(
            f"predict_{model}_{game.name.replace(' ', '_')}_{int(time.time())}.json",
            {
                "method": "predict_distribution",
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
    save: bool = True,
) -> dict[int, float]:
    """Call the model N times with a role-play prompt, build empirical distribution.

    Each call asks the model to play the game as a human participant.
    Responses are parsed to extract integer choices.
    """
    if prompt is None:
        prompt = (
            "You are answering questions as if you were a human. "
            "Do not break character.\n\n"
            f"{game.description}\n\n"
            "What amount of money would you request? "
            "Reply with just the number."
        )

    client = _get_client()
    raw_responses: list[str] = []
    parsed_actions: list[int | None] = []
    failures = 0

    for i in range(n):
        response = client.messages.create(
            model=model,
            max_tokens=256,
            temperature=temperature,
            messages=[{"role": "user", "content": prompt}],
        )
        raw = response.content[0].text
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
                "model": model,
                "game": game.name,
                "prompt": prompt,
                "n_requested": n,
                "n_valid": len(valid),
                "n_failures": failures,
                "temperature": temperature,
                "raw_responses": raw_responses,
                "parsed_actions": parsed_actions,
                "distribution": {str(k): v for k, v in distribution.items()},
            },
        )

    return distribution


if __name__ == "__main__":
    from src.games import ELEVEN_TWENTY_GAME

    logging.basicConfig(level=logging.INFO)

    game = ELEVEN_TWENTY_GAME

    # Test parsing
    assert _parse_action("17", game.action_space) == 17
    assert _parse_action("I would request 18 shekels.", game.action_space) == 18
    assert _parse_action("My choice is 20.", game.action_space) == 20
    assert _parse_action("banana", game.action_space) is None
    print("Parsing tests passed.")

    # Uncomment to run actual API calls:
    # dist = predict_distribution(game)
    # print(f"Direct prediction: {dist}")
    #
    # dist = sample_responses(game, n=5)
    # print(f"Sampled distribution (n=5): {dist}")
