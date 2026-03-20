#!/usr/bin/env python3
"""Extract a readable summary from Claude Code JSONL session logs.

Parses the structured JSONL format written by Claude Code sessions and
prints a human-readable summary showing user messages, assistant responses,
thinking blocks, and tool calls.

Usage:
    python3 scripts/extract_session.py results/sessions/abc123.jsonl
    python3 scripts/extract_session.py session1.jsonl session2.jsonl
"""

import argparse
import json
import sys
import textwrap


def truncate(text: str, limit: int) -> str:
    """Truncate text to *limit* chars, adding '[...]' if needed."""
    text = text.strip()
    if len(text) <= limit:
        return text
    return text[:limit].rstrip() + " [...]"


def format_tool_input(input_data: dict) -> str:
    """Format a tool call's input dict as a brief key=value summary."""
    parts = []
    for key, val in input_data.items():
        val_str = str(val)
        if len(val_str) > 80:
            val_str = val_str[:77] + "..."
        parts.append(f"{key}={val_str}")
    return ", ".join(parts)


def extract_content_text(content) -> str:
    """Extract plain text from a tool_result content field.

    Handles both plain strings and structured [{type: "text", text: ...}] lists.
    """
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        texts = []
        for item in content:
            if isinstance(item, dict) and item.get("type") == "text":
                texts.append(item.get("text", ""))
            elif isinstance(item, str):
                texts.append(item)
        return "\n".join(texts)
    return str(content)


def process_session(path: str) -> None:
    """Read a JSONL session file and print a readable summary."""
    with open(path) as f:
        lines = f.readlines()

    entries = []
    for line_no, line in enumerate(lines, 1):
        line = line.strip()
        if not line:
            continue
        try:
            entries.append(json.loads(line))
        except json.JSONDecodeError:
            print(f"  [warning: skipped malformed JSON on line {line_no}]")

    # Print session header
    session_id = None
    for entry in entries:
        if "sessionId" in entry:
            session_id = entry["sessionId"]
            break
    print(f"Session: {session_id or 'unknown'}")
    print("=" * 70)

    msg_count = 0
    for entry in entries:
        entry_type = entry.get("type")

        # --- Queue operations (initial prompt) ---
        if entry_type == "queue-operation" and entry.get("operation") == "enqueue":
            content = entry.get("content", "")
            if content:
                print(f"\n>>> QUEUED TASK")
                print(f"    {content}")
            continue

        # --- User messages ---
        if entry_type == "user":
            msg = entry.get("message", {})
            content = msg.get("content")
            if content is None:
                continue

            if isinstance(content, str):
                msg_count += 1
                print(f"\n--- USER [{msg_count}] ---")
                print(textwrap.indent(content.strip(), "    "))
                continue

            # Structured content (tool results)
            if isinstance(content, list):
                for item in content:
                    if isinstance(item, dict) and item.get("type") == "tool_result":
                        tool_id = item.get("tool_use_id", "?")
                        result_text = extract_content_text(item.get("content", ""))
                        # Strip line-number prefixes from Read tool results
                        clean_lines = []
                        for rline in result_text.split("\n"):
                            stripped = rline
                            if "\u2192" in rline:
                                stripped = rline.split("\u2192", 1)[-1]
                            clean_lines.append(stripped)
                        result_text = "\n".join(clean_lines)
                        print(f"\n    TOOL RESULT (for {tool_id[:12]}...):")
                        print(textwrap.indent(truncate(result_text, 200), "        "))
                continue

        # --- Assistant messages ---
        if entry_type == "assistant":
            msg = entry.get("message", {})
            content_blocks = msg.get("content", [])
            model = msg.get("model", "")

            for block in content_blocks:
                if not isinstance(block, dict):
                    continue
                block_type = block.get("type")

                if block_type == "thinking":
                    thinking = block.get("thinking", "")
                    if thinking:
                        print(f"\n    THINKING ({model}):")
                        print(textwrap.indent(truncate(thinking, 500), "        "))

                elif block_type == "text":
                    text = block.get("text", "").strip()
                    if text:
                        print(f"\n    RESPONSE ({model}):")
                        print(textwrap.indent(text, "        "))

                elif block_type == "tool_use":
                    name = block.get("name", "?")
                    inp = block.get("input", {})
                    print(f"\n    TOOL CALL: {name}({format_tool_input(inp)})")

            continue

        # Skip other entry types: file-history-snapshot, dequeue, last-prompt, etc.


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extract readable summaries from Claude Code JSONL session logs."
    )
    parser.add_argument(
        "sessions",
        nargs="+",
        help="One or more .jsonl session files to process",
    )
    args = parser.parse_args()

    for i, path in enumerate(args.sessions):
        if i > 0:
            print("\n" + "=" * 70 + "\n")
        process_session(path)


if __name__ == "__main__":
    main()
