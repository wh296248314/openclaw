#!/bin/bash
# 工作空间快速查找脚本

if [ $# -eq 0 ]; then
    echo "🔍 工作空间快速查找工具"
    echo "用法: $0 <搜索词>"
    echo ""
    echo "示例:"
    echo "  $0 guardian      # 查找监控相关文件"
    echo "  $0 .py          # 查找Python文件"
    echo "  $0 config       # 查找配置文件"
    exit 1
fi

SEARCH_TERM="$1"
echo "搜索: '$SEARCH_TERM'"
echo "=========================="

# 按目录分类搜索
echo "📁 configs/:"
find configs/ -type f -iname "*$SEARCH_TERM*" 2>/dev/null | head -5

echo ""
echo "📁 scripts/monitor/:"
find scripts/monitor/ -type f -iname "*$SEARCH_TERM*" 2>/dev/null | head -5

echo ""
echo "📁 scripts/system/:"
find scripts/system/ -type f -iname "*$SEARCH_TERM*" 2>/dev/null | head -5

echo ""
echo "📁 scripts/utils/:"
find scripts/utils/ -type f -iname "*$SEARCH_TERM*" 2>/dev/null | head -5

echo ""
echo "📁 docs/:"
find docs/ -type f -iname "*$SEARCH_TERM*" 2>/dev/null | head -5

echo ""
echo "📁 logs/:"
find logs/ -type f -iname "*$SEARCH_TERM*" 2>/dev/null | head -5

echo ""
echo "📊 统计:"
total=$(find . -type f -iname "*$SEARCH_TERM*" ! -path "./.git/*" ! -path "./lifeos/.git/*" 2>/dev/null | wc -l)
echo "找到 $total 个匹配文件"
