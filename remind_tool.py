#!/usr/bin/env python3
"""
Parse REMINDERS.md for checklist reminders, print context for hooks, or
fire macOS notifications (notify mode).
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path

ACTIVE = re.compile(
    r"^\s*-\s*\[\s*\]\s*(?P<when>\d{4}-\d{2}-\d{2}(?:T\d{2}:\d{2})?)\s+(?P<msg>.+?)\s*$"
)


def project_root() -> Path:
    env = os.environ.get("CLAUDE_PROJECT_DIR")
    if env:
        return Path(env).expanduser().resolve()
    return Path.cwd().resolve()


def reminders_path(root: Path) -> Path:
    return root / "REMINDERS.md"


def parse_active_lines(text: str) -> list[tuple[str, str]]:
    """Return (when_str, message) for each unchecked reminder line."""
    rows: list[tuple[str, str]] = []
    for line in text.splitlines():
        m = ACTIVE.match(line)
        if m:
            rows.append((m.group("when"), m.group("msg").strip()))
    return rows


def is_due(when_s: str, now: datetime) -> bool:
    try:
        if "T" in when_s:
            dt = datetime.fromisoformat(when_s)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=now.tzinfo)
            return now >= dt
        d = date.fromisoformat(when_s)
        return now.date() >= d
    except ValueError:
        return False


def apple_quote(s: str) -> str:
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def cmd_context(root: Path) -> int:
    path = reminders_path(root)
    if not path.is_file():
        return 0
    now = datetime.now().astimezone()
    due_msgs: list[str] = []
    for when_s, msg in parse_active_lines(path.read_text(encoding="utf-8")):
        if is_due(when_s, now):
            due_msgs.append(f"- {when_s} — {msg}")
    if not due_msgs:
        return 0
    print("### Due reminders (from REMINDERS.md)\n")
    print("The user asked to be reminded; acknowledge these proactively.\n")
    for line in due_msgs:
        print(line)
    print(
        "\nSuggest marking finished items as `- [x] ...` in REMINDERS.md "
        "or removing them so they stop surfacing."
    )
    return 0


def cmd_notify(root: Path) -> int:
    path = reminders_path(root)
    if not path.is_file():
        return 0
    now = datetime.now().astimezone()
    due_msgs = [msg for when_s, msg in parse_active_lines(path.read_text(encoding="utf-8")) if is_due(when_s, now)]
    if not due_msgs:
        return 0
    if sys.platform != "darwin":
        print("notify mode is only implemented for macOS (osascript).", file=sys.stderr)
        for m in due_msgs:
            print(m)
        return 0
    for msg in due_msgs:
        body = apple_quote(msg[:200])
        script = f"display notification {body} with title {apple_quote('Reminder')}"
        subprocess.run(["osascript", "-e", script], check=False)
    return 0


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: remind_tool.py context|notify", file=sys.stderr)
        return 2
    mode = sys.argv[1]
    root = project_root()
    if mode == "context":
        return cmd_context(root)
    if mode == "notify":
        return cmd_notify(root)
    print("unknown mode; use context or notify", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
