#!/bin/bash

# Obsidian Git 自动提交脚本
# 每天三次自动提交：中午12点、晚上7点、晚上11点

# 设置工作目录（Obsidian库位置）
OBSIDIAN_DIR="$HOME/Documents/LifeOS"
LOG_FILE="$HOME/openclaw/workspace/commit-log.md"

# 检查Obsidian目录是否存在
if [ ! -d "$OBSIDIAN_DIR" ]; then
    echo "错误：Obsidian目录不存在: $OBSIDIAN_DIR"
    exit 1
fi

# 进入Obsidian目录
cd "$OBSIDIAN_DIR" || exit 1

# 获取当前时间
CURRENT_TIME=$(date '+%Y-%m-%d %H:%M:%S')
COMMIT_TIME=$(date '+%H:%M')

# 根据时间确定提交类型
if [ "$COMMIT_TIME" = "12:00" ]; then
    COMMIT_TYPE="中午提交"
    COMMIT_MSG="🕛 中午自动提交 - $CURRENT_TIME"
elif [ "$COMMIT_TIME" = "19:00" ]; then
    COMMIT_TYPE="晚上提交"
    COMMIT_MSG="🌙 晚上自动提交 - $CURRENT_TIME"
elif [ "$COMMIT_TIME" = "23:00" ]; then
    COMMIT_TYPE="睡前提交"
    COMMIT_MSG="🌜 睡前自动提交 - $CURRENT_TIME"
else
    COMMIT_TYPE="手动提交"
    COMMIT_MSG="🤖 自动提交 - $CURRENT_TIME"
fi

# 执行Git操作
echo "开始 $COMMIT_TYPE..."
echo "时间: $CURRENT_TIME"
echo "目录: $OBSIDIAN_DIR"

# 添加所有更改
git add .

# 检查是否有更改需要提交
if git diff --cached --quiet; then
    echo "没有更改需要提交"
    STATUS="无更改"
else
    # 提交更改
    git commit -m "$COMMIT_MSG"
    
    # 推送到远程仓库
    git push origin main
    
    echo "提交完成: $COMMIT_MSG"
    STATUS="已提交"
fi

# 记录到日志文件
echo "## $CURRENT_TIME" >> "$LOG_FILE"
echo "- **类型**: $COMMIT_TYPE" >> "$LOG_FILE"
echo "- **状态**: $STATUS" >> "$LOG_FILE"
echo "- **消息**: $COMMIT_MSG" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

echo "$COMMIT_TYPE 完成 - $STATUS"