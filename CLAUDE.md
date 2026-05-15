# Work tracking

- Canonical task list: `WORK_BACKLOG.md` (sections: Inbox, Next, In progress, Done). Use **task list** lines: `- [ ]` for open items, `- [x]` when done, so Markdown / todo extensions stay in sync.
- When the user mentions new work, follow-ups, or "I should…", add a bullet to **Inbox** unless they say not to. Keep titles short and actionable.
- Move items between sections only when they clearly change status. Do not invent tasks.
- For a focused triage or weekly review, use the `/work-backlog` skill.
- For a larger capture or re-org, delegate to the **work-tracker** subagent (or start a dedicated session: `claude --agent work-tracker` from this directory).

## Reminders (time-based nudges)

- Store dated nudges in `REMINDERS.md` (see file for format). Use the **`/reminders`** skill or ask **work-tracker** to add or complete lines.
- **When you open Claude Code** in this repo, a **SessionStart** hook (`.claude/settings.json`) runs `.claude/hooks/reminder-context.sh` and injects **due** reminders into the session so Claude can surface them even if you do not remember to ask.
- **When Claude Code is closed**, the model cannot notify you. Schedule macOS notifications, for example daily at 9:00:

```cron
0 9 * * * cd /Users/ari.rajaramicloud.com/Desktop/Claude && /usr/bin/python3 scripts/remind_tool.py notify
```

  Use `crontab -e` to add that line (adjust the path if you move the folder). `notify` uses `osascript` and only fires for due unchecked lines.

Project definitions: `.claude/agents/work-tracker.md`, `.claude/skills/work-backlog/SKILL.md`, `.claude/skills/reminders/SKILL.md`.
