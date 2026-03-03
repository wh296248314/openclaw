#!/bin/bash
# 测试过滤逻辑

SOURCE_FILE="/home/admin/openclaw/workspace/memory/2026-03-02.md"

# 使用修改后的过滤逻辑
FILTERED_CONTENT=$(awk '
BEGIN { in_section=0; print_header=1 }
/^# / { if (print_header) print $0; print_header=0; next }
/^## ✅ |^## 🔄 |^## 📋 |^## 📊 / { 
    in_section=1; 
    print $0; 
    next 
}
/^## / && !/^## ✅ |^## 🔄 |^## 📋 |^## 📊 / { 
    in_section=0; 
    next 
}
in_section { print $0 }
' "$SOURCE_FILE")

echo "=== 过滤后的内容 ==="
echo "$FILTERED_CONTENT"
echo "=== 结束 ==="