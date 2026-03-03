#!/bin/bash
# 工作空间自动整理脚本

echo "🧹 工作空间整理脚本 v1.0"
echo "=========================="
echo "运行时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

WORKSPACE_DIR="/home/admin/openclaw/workspace"
cd "$WORKSPACE_DIR"

# 1. 清理临时文件（超过7天）
echo "1. 清理临时文件..."
find temp/ -type f -mtime +7 -delete 2>/dev/null
echo "   ✅ 清理完成"

# 2. 归档旧日志（超过30天）
echo "2. 归档旧日志..."
find logs/ -type f -mtime +30 -exec mv {} archive/ \; 2>/dev/null
echo "   ✅ 归档完成"

# 3. 检查目录结构
echo "3. 检查目录结构..."
missing_dirs=0
for dir in configs scripts/monitor scripts/system scripts/utils docs logs temp archive projects; do
    if [ ! -d "$dir" ]; then
        echo "   ⚠️  缺失目录: $dir"
        missing_dirs=$((missing_dirs + 1))
    fi
done

if [ $missing_dirs -eq 0 ]; then
    echo "   ✅ 目录结构完整"
else
    echo "   ⚠️  发现 $missing_dirs 个缺失目录"
fi

# 4. 检查根目录文件
echo "4. 检查根目录..."
root_files=$(find . -maxdepth 1 -type f ! -name ".*" ! -name "DIRECTORY_STRUCTURE.md" ! -name "organize_workspace.sh" | wc -l)
if [ $root_files -eq 0 ]; then
    echo "   ✅ 根目录干净"
else
    echo "   ⚠️  根目录有 $root_files 个文件需要处理:"
    find . -maxdepth 1 -type f ! -name ".*" ! -name "DIRECTORY_STRUCTURE.md" ! -name "organize_workspace.sh" -printf "   - %f\n"
fi

# 5. 生成报告
echo ""
echo "📊 整理报告:"
echo "============"
echo "目录结构:"
for dir in configs scripts/monitor scripts/system scripts/utils docs logs temp archive projects; do
    if [ -d "$dir" ]; then
        count=$(find "$dir" -type f | wc -l)
        size=$(du -sh "$dir" 2>/dev/null | cut -f1)
        echo "  $dir/: $count 个文件 ($size)"
    fi
done

echo ""
echo "总文件数: $(find . -type f ! -path "./.git/*" ! -path "./lifeos/.git/*" | wc -l)"
echo "总大小: $(du -sh . 2>/dev/null | cut -f1)"

echo ""
echo "🎯 建议:"
if [ $root_files -gt 0 ]; then
    echo "1. 处理根目录的 $root_files 个文件"
fi
if [ $missing_dirs -gt 0 ]; then
    echo "2. 创建缺失的 $missing_dirs 个目录"
fi
echo "3. 定期运行本脚本保持整洁"

echo ""
echo "✅ 整理完成!"
