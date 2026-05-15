# Reminders

Time-based nudges live here. The **work-tracker** agent and **`/reminders`** skill can add, edit, or mark items done.

## Format

Each active reminder is one line:

```text
- [ ] YYYY-MM-DD Short reminder text
```

Optional time (local timezone, 24h):

```text
- [ ] YYYY-MM-DDTHH:MM Standup prep
```

Mark **done** (stops session injection and daily notify):

```text
- [x] 2026-05-01 Old reminder
```

**Date only** (`YYYY-MM-DD`): treated as “due that calendar day onward” until checked off.  
**With `T…`**: due at or after that exact local time.

## Active

- [ ] 2099-01-01 Example: delete this line after you add a real reminder

## How you get reminded

1. **Claude Code**: a **SessionStart** hook injects due items into context whenever you start or resume a session in this project (see `.claude/settings.json`).
2. **Outside Claude**: run `python3 scripts/remind_tool.py notify` on a schedule (see `CLAUDE.md` for macOS `cron` / `launchd`).

