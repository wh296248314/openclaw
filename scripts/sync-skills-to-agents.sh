#!/bin/bash
# 同步主skills目录到所有小皮agent
# 用法: sync-skills-to-agents.sh

MAIN_SKILLS="$HOME/.openclaw/workspace/skills"
EXPERTS_DIR="$HOME/.openclaw/workspace/experts"
LOG_FILE="$HOME/.openclaw/logs/skill-sync.log"

mkdir -p "$(dirname "$LOG_FILE")"

echo "=== $(date) ===" >> "$LOG_FILE"

# 遍历所有expert workspace目录
for workspace_dir in "$EXPERTS_DIR"/*/; do
    expert_name=$(basename "$workspace_dir")
    
    # 创建skills目录
    mkdir -p "$workspace_dir/skills"
    
    # 同步（排除隐藏文件和node_modules）
    rsync -av --exclude='.*' --exclude='node_modules' \
        "$MAIN_SKILLS/" "$workspace_dir/skills/" \
        >> "$LOG_FILE" 2>&1
    
    echo "  $expert_name: ✅" >> "$LOG_FILE"
done

echo "同步完成" >> "$LOG_FILE"
