# Claude Code Auto-Documentation Hook

Stop hook that forces Claude to update documentation (HANDOFF, CLAUDE.md, README, DEVELOPER_GUIDE) before ending each session. Never lose context between sessions — every handoff is automatically documented.

## Problem

When working with Claude Code on long sessions, important context gets lost:
- What was done this session?
- What decisions were made and why?
- What should the next session focus on?

Manually updating docs is easy to forget.

## Solution

A **Stop hook** that blocks Claude from finishing until documentation is updated:

```
Claude finishes work
        ↓
   Stop hook runs
        ↓
   Docs updated?  ──Yes──→  Allow stop
        ↓ No
   BLOCK stop
   "Update these files before stopping"
        ↓
   Claude updates docs
        ↓
   Allow stop
```

## Files Updated

| File | Purpose |
|------|---------|
| `HANDOFF_YYYYMMDD.md` | Session summary, decisions, next steps |
| `CLAUDE.md` | Claude's memory about this project |
| `README.md` | Project description, installation, usage |
| `DEVELOPER_GUIDE.md` | Architecture, patterns, prompting guidelines |

## Installation

### 1. Copy hook to your project

```bash
mkdir -p .claude/hooks
curl -o .claude/hooks/update-docs-hook.py https://raw.githubusercontent.com/YOUR_USERNAME/claude-auto-docs/main/.claude/hooks/update-docs-hook.py
chmod +x .claude/hooks/update-docs-hook.py
```

### 2. Add hook to settings

Edit `.claude/settings.local.json` (personal) or `.claude/settings.json` (team):

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$CLAUDE_PROJECT_DIR/.claude/hooks/update-docs-hook.py\"",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

**Using venv?** Replace `python3` with your path:
```json
"command": "\"$CLAUDE_PROJECT_DIR/venv/bin/python\" \"$CLAUDE_PROJECT_DIR/.claude/hooks/update-docs-hook.py\""
```

### 3. Restart Claude Code

Verify with `/hooks` command.

## Configuration

### Trigger modes

By default, hook triggers only in `acceptEdits` and `bypassPermissions` modes.

To trigger in **all modes**, edit the hook and remove lines 27-29:
```python
# if permission_mode not in ["acceptEdits", "bypassPermissions"]:
#     sys.exit(0)
```

### Customize files to update

Edit the `reason` string in `update-docs-hook.py` (around line 47).

**To add a file:**
```python
5. **NEW_FILE.md** - Update if needed:
   - What to include
   - Another point
```

**To remove a file:**
Simply delete that numbered section from the `reason` string.

**Example — only HANDOFF and CLAUDE.md:**
```python
"reason": f"""Before stopping, update:

1. **HANDOFF_{current_date}.md** - Session summary, decisions, next steps

2. **CLAUDE.md** - Update project memory and current state

After updating, create marker: touch /tmp/.claude_docs_updated"""
```

## How It Prevents Infinite Loops

1. `stop_hook_active` flag — if Claude is already continuing from a stop hook, allow stop
2. Marker file `/tmp/.claude_docs_updated` — created after docs update, cleaned on next stop

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Hook not triggering | Check `/hooks`, ensure script is executable |
| Infinite loop | Remove marker: `rm /tmp/.claude_docs_updated` |
| Python not found | Update path in settings.json |

## License

MIT
