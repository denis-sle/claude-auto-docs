#!/bin/bash
# Install claude-auto-docs hook into current project

set -e

echo "Installing Claude Auto-Docs Hook..."

# Create directories
mkdir -p .claude/hooks

# Copy hook script
cp "$(dirname "$0")/.claude/hooks/update-docs-hook.py" .claude/hooks/
chmod +x .claude/hooks/update-docs-hook.py

echo "✓ Hook script installed to .claude/hooks/"

# Check if settings file exists
if [ -f ".claude/settings.local.json" ]; then
    echo ""
    echo "⚠ .claude/settings.local.json exists"
    echo "  Add this to your hooks configuration:"
    echo ""
    cat << 'EOF'
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
EOF
elif [ -f ".claude/settings.json" ]; then
    echo ""
    echo "⚠ .claude/settings.json exists"
    echo "  Merge the hooks configuration from .claude/settings.json.example"
else
    cp "$(dirname "$0")/.claude/settings.json.example" .claude/settings.json
    echo "✓ Settings file created at .claude/settings.json"
fi

echo ""
echo "✓ Installation complete!"
echo ""
echo "Next steps:"
echo "  1. Restart Claude Code"
echo "  2. Verify with /hooks command"
echo "  3. (Optional) Copy templates/ to your project"
