#!/usr/bin/env python3
"""
Claude Code Stop Hook - Auto Documentation Update

Blocks Claude from stopping until project documentation is updated.
Triggers in 'acceptEdits' or 'bypassPermissions' modes.

Files updated:
- _docs/HANDOFF_YYYYMMDD.md (session completion notes)
- CLAUDE.md (claude memory)
- README.md (project readme)
- DEVELOPER_GUIDE.md (developer documentation)
"""

import json
import sys
import os
from datetime import datetime


def main():
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)

    permission_mode = input_data.get("permission_mode", "")
    stop_hook_active = input_data.get("stop_hook_active", False)

    # Prevent infinite loop
    if stop_hook_active:
        sys.exit(0)

    # Only trigger in acceptEdits/bypassPermissions modes
    # Remove this check to trigger in all modes
    if permission_mode not in ["acceptEdits", "bypassPermissions"]:
        sys.exit(0)

    # Check marker file (indicates docs were updated this session)
    marker_file = "/tmp/.claude_docs_updated"
    if os.path.exists(marker_file):
        os.remove(marker_file)
        sys.exit(0)

    current_date = datetime.now().strftime("%Y%m%d")

    output = {
        "decision": "block",
        "reason": f"""Before stopping, update the following documentation files:

1. **HANDOFF_{current_date}.md** - Create handoff document:
   - Summary of work completed this session
   - Key decisions made and rationale
   - Current state of implementation
   - Known issues or blockers
   - Next steps and priorities
   - Any context the next session needs

2. **CLAUDE.md** - Update Claude memory:
   - Add new learnings about this codebase
   - Update current project state
   - Note any new patterns or conventions discovered
   - Update list of key files if changed

3. **README.md** - Update if needed:
   - Project description
   - Installation instructions
   - Usage examples
   - Current features

4. **DEVELOPER_GUIDE.md** - Update if needed:
   - Architecture overview
   - Key abstractions and patterns
   - How to extend/modify the system
   - Prompting guidelines for agents

After updating, create marker file: touch /tmp/.claude_docs_updated
Then you can stop."""
    }

    print(json.dumps(output))
    sys.exit(0)


if __name__ == "__main__":
    main()
