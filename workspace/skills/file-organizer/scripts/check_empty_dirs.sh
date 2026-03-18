#!/bin/bash
# 查找空目录
# 用法: bash scripts/check_empty_dirs.sh

WORKSPACE="/home/pixiu/.openclaw/workspace"

echo "🔍 查找空目录..."
echo ""

empty_dirs=$(find $WORKSPACE -type d -empty)

if [ -z "$empty_dirs" ]; then
    echo "✅ 没有空目录"
else
    echo "⚠️  以下目录为空："
    echo "$empty_dirs"
    echo ""
    echo "可以删除这些空目录以保持目录整洁"
fi
