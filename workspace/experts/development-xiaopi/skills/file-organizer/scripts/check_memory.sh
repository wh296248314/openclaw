#!/bin/bash
# 检查各小皮memory记录情况
# 用法: bash scripts/check_memory.sh

WORKSPACE="/home/pixiu/.openclaw/workspace"
EXPERTS="$WORKSPACE/experts"

echo "📋 检查各小皮memory记录..."
echo ""

total=0
has_mem=0
no_mem=0

for dir in "$EXPERTS"/*/; do
    if [ -d "$dir" ]; then
        name=$(basename "$dir")
        mem_file="$dir/MEMORY.md"
        
        if [ -f "$mem_file" ]; then
            # 检查最后修改时间
            last_mod=$(stat -c %y "$mem_file" 2>/dev/null | cut -d' ' -f1)
            echo "✅ $name - 有memory (最后更新: $last_mod)"
            ((has_mem++))
        else
            echo "❌ $name - 缺少MEMORY.md"
            ((no_mem++))
        fi
        ((total++))
    fi
done

echo ""
echo "📊 统计：$total 个小皮，$has_mem 有记录，$no_mem 缺失"

if [ $no_mem -gt 0 ]; then
    echo "⚠️  提醒：缺失memory的小皮需要补交！"
fi
