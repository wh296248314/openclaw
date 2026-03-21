#!/bin/bash
# 档案馆产出物提交流序
# 用法: submit_archive.sh <文件路径> <类型> <部门> [Tags...]
# 示例: submit_archive.sh PRD.md PRD 产品小皮 重要 技术

set -e

ARCHIVES_DIR="$HOME/.openclaw/workspace/archives"
DATE=$(date +%Y%m%d)

# 参数检查
if [ $# -lt 3 ]; then
    echo "用法: $0 <文件路径> <类型> <部门> [Tags...]"
    echo "示例: $0 PRD.md PRD 产品小皮 重要 技术"
    exit 1
fi

FILE_PATH="$1"
FILE_TYPE="$2"
DEPT="$3"
shift 3
TAGS="$@"

# 检查文件是否存在
if [ ! -f "$FILE_PATH" ]; then
    echo "❌ 文件不存在: $FILE_PATH"
    exit 1
fi

# 获取文件名
FILENAME=$(basename "$FILE_PATH")

# 生成标准命名
# {类型}-{部门}-{日期}-{原文件名}
NEW_NAME="${FILE_TYPE}-${DEPT}-${DATE}-${FILENAME}"

# 按类型放到对应目录
case "$FILE_TYPE" in
    PRD|PRD文档) TARGET_DIR="$ARCHIVES_DIR/按类型/PRD文档" ;;
    竞品分析) TARGET_DIR="$ARCHIVES_DIR/按类型/竞品分析" ;;
    设计|设计稿) TARGET_DIR="$ARCHIVES_DIR/按类型/设计稿" ;;
    代码) TARGET_DIR="$ARCHIVES_DIR/按类型/代码" ;;
    测试|测试报告) TARGET_DIR="$ARCHIVES_DIR/按类型/测试报告" ;;
    配置|配置文件) TARGET_DIR="$ARCHIVES_DIR/按类型/配置文件" ;;
    PPT) TARGET_DIR="$ARCHIVES_DIR/按类型/PPT" ;;
    技术|技术方案) TARGET_DIR="$ARCHIVES_DIR/按类型/技术方案" ;;
    *) TARGET_DIR="$ARCHIVES_DIR/按类型/其他" ;;
esac

mkdir -p "$TARGET_DIR"

# 复制文件
cp "$FILE_PATH" "$TARGET_DIR/$NEW_NAME"
echo "✅ 已提交到: $TARGET_DIR/$NEW_NAME"

# 按部门同步
DEPT_DIR="$ARCHIVES_DIR/按部门/"
case "$DEPT" in
    *产品*) mkdir -p "${DEPT_DIR}产品部" && cp "$FILE_PATH" "${DEPT_DIR}产品部/$NEW_NAME" ;;
    *设计*) mkdir -p "${DEPT_DIR}设计部" && cp "$FILE_PATH" "${DEPT_DIR}设计部/$NEW_NAME" ;;
    *研发*) mkdir -p "${DEPT_DIR}研发部" && cp "$FILE_PATH" "${DEPT_DIR}研发部/$NEW_NAME" ;;
    *测试*) mkdir -p "${DEPT_DIR}测试部" && cp "$FILE_PATH" "${DEPT_DIR}测试部/$NEW_NAME" ;;
    *部署*) mkdir -p "${DEPT_DIR}部署部" && cp "$FILE_PATH" "${DEPT_DIR}部署部/$NEW_NAME" ;;
    *审核*) mkdir -p "${DEPT_DIR}门下省" && cp "$FILE_PATH" "${DEPT_DIR}门下省/$NEW_NAME" ;;
    *管家*) mkdir -p "${DEPT_DIR}尚书省" && cp "$FILE_PATH" "${DEPT_DIR}尚书省/$NEW_NAME" ;;
    *) mkdir -p "${DEPT_DIR}其他" && cp "$FILE_PATH" "${DEPT_DIR}其他/$NEW_NAME" ;;
esac

# 按Tag同步
if [ -n "$TAGS" ]; then
    for tag in $TAGS; do
        TAG_DIR="$ARCHIVES_DIR/按Tag/$tag"
        mkdir -p "$TAG_DIR"
        cp "$FILE_PATH" "$TAG_DIR/$NEW_NAME"
        echo "  📌 已同步到: $TAG_DIR/$NEW_NAME"
    done
fi

# 按时间同步
TIME_DIR="$ARCHIVES_DIR/按时间/${DATE:0:4}年/${DATE:4:2}月"
mkdir -p "$TIME_DIR"
cp "$FILE_PATH" "$TIME_DIR/$NEW_NAME"
echo "  📅 已同步到: $TIME_DIR/$NEW_NAME"

# 更新Git
cd "$ARCHIVES_DIR"
if git rev-parse --git-dir > /dev/null 2>&1; then
    git add .
    git commit -m "docs: 归档 $NEW_NAME - $(date +'%Y-%m-%d %H:%M')"
    echo "✅ 已提交到Git"
fi

echo ""
echo "📋 提交完成！"
echo "   文件名: $NEW_NAME"
echo "   类型: $FILE_TYPE"
echo "   部门: $DEPT"
echo "   标签: ${TAGS:-无}"
