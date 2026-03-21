#!/bin/bash
# 档案馆定期查验脚本
# 用法: check_archives.sh
# 建议: 每天定时执行

ARCHIVES_DIR="$HOME/.openclaw/workspace/archives"
TODAY=$(date +%Y%m%d)
YESTERDAY=$(date -d "yesterday" +%Y%m%d)

echo "📋 档案馆查验报告 - $(date +'%Y-%m-%d %H:%M')"
echo "========================================"

# 1. 今日新增文件
echo ""
echo "📅 今日新增文件 (${TODAY}):"
TODAY_FILES=$(find "$ARCHIVES_DIR" -type f -name "*${TODAY}*" 2>/dev/null | wc -l)
if [ "$TODAY_FILES" -gt 0 ]; then
    find "$ARCHIVES_DIR" -type f -name "*${TODAY}*" 2>/dev/null | while read f; do
        echo "  ✅ $(basename "$f")"
    done
else
    echo "  ⚪ 无新增文件"
fi

# 2. 按类型统计
echo ""
echo "📊 按类型统计:"
for type_dir in "$ARCHIVES_DIR"/按类型/*/; do
    if [ -d "$type_dir" ]; then
        count=$(find "$type_dir" -type f 2>/dev/null | wc -l)
        name=$(basename "$type_dir")
        echo "  📁 $name: $count 个"
    fi
done

# 3. 按部门统计
echo ""
echo "🏢 按部门统计:"
for dept_dir in "$ARCHIVES_DIR"/按部门/*/; do
    if [ -d "$dept_dir" ]; then
        count=$(find "$dept_dir" -type f 2>/dev/null | wc -l)
        name=$(basename "$dept_dir")
        echo "  👤 $name: $count 个"
    fi
done

# 4. 检查未归档的任务
echo ""
echo "⚠️ 待检查任务:"
# 查找没有对应产出物的JJC任务
echo "  (暂无对应旨意产出物的任务检查)"

# 5. 总体统计
echo ""
echo "📈 总体统计:"
TOTAL_FILES=$(find "$ARCHIVES_DIR" -type f 2>/dev/null | wc -l)
TOTAL_SIZE=$(du -sh "$ARCHIVES_DIR" 2>/dev/null | cut -f1)
echo "  📦 总文件数: $TOTAL_FILES"
echo "  💾 总大小: $TOTAL_SIZE"

# 6. 生成报告
REPORT_FILE="$ARCHIVES_DIR/查验报告-${TODAY}.md"
cat > "$REPORT_FILE" << EOF
# 档案馆查验报告

**日期:** $(date +'%Y-%m-%d %H:%M')

## 统计摘要

| 项目 | 数量 |
|------|------|
| 总文件数 | $TOTAL_FILES |
| 总大小 | $TOTAL_SIZE |
| 今日新增 | $TODAY_FILES |

## 今日新增

$(if [ "$TODAY_FILES" -gt 0 ]; then
    find "$ARCHIVES_DIR" -type f -name "*${TODAY}*" 2>/dev/null | while read f; do
        echo "- $(basename "$f")"
    done
else
    echo "- 无新增文件"
fi)

## 问题记录

(如有异常请记录在此)

EOF

echo ""
echo "📝 报告已生成: $REPORT_FILE"
