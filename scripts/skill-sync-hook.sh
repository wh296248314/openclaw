#!/bin/bash
# 技能安装后自动同步钩子
# 放在 ~/.npm-global/lib/node_modules/openclaw/scripts/post-install-skill.js 中调用

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
"$SCRIPT_DIR/sync-skills-to-agents.sh"
