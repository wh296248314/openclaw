#!/bin/bash
# 检查各小皮变更，记录到待汇报队列
# 由cron每小时执行

QUEUE_FILE="/tmp/expert-changes-queue.txt"
LAST_STATE="/tmp/expert-last-state.txt"
CURRENT_STATE="/tmp/expert-current-state.txt"

# 生成当前状态
echo "=== $(date '+%Y-%m-%d %H:%M') ===" > "$CURRENT_STATE"
for dir in /home/pixiu/.openclaw/workspace/experts/*/; do
  name=$(basename "$dir")
  echo -e "\n【$name】" >> "$CURRENT_STATE"
  find "$dir" -mindepth 2 -maxdepth 2 -type d ! -path "*/memory/*" ! -path "*/skills/*" ! -path "*/self-improving/*" 2>/dev/null | sed "s|$dir||" >> "$CURRENT_STATE"
done

# 比较差异
if [ -f "$LAST_STATE" ]; then
  DIFF=$(diff "$LAST_STATE" "$CURRENT_STATE" 2>/dev/null)
  
  if [ -n "$DIFF" ]; then
    TIMESTAMP=$(date '+%Y-%m-%d %H:%M')
    
    # 记录到待汇报队列
    {
      echo "## $TIMESTAMP"
      echo "$DIFF"
      echo "---END---"
    } >> "$QUEUE_FILE"
    
    # 同时记录到变更日志
    {
      echo "## $TIMESTAMP"
      echo "\`\`\`"
      echo "$DIFF"
      echo "\`\`\`"
    } >> "/home/pixiu/.openclaw/workspace/shared/logs/变更日志.md"
  fi
fi

# 更新状态
cp "$CURRENT_STATE" "$LAST_STATE"
