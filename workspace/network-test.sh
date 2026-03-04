#!/bin/bash
echo "🔍 网络连接诊断测试 - $(date)"
echo "=========================================="

# 测试1: 基本网络连接
echo "1. 测试基本网络连接..."
ping -c 2 8.8.8.8 > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "   ✅ 基本网络连接正常"
else
    echo "   ❌ 基本网络连接失败"
fi

# 测试2: DNS解析
echo "2. 测试DNS解析..."
nslookup github.com > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "   ✅ DNS解析正常"
else
    echo "   ❌ DNS解析失败"
fi

# 测试3: GitHub API访问
echo "3. 测试GitHub API访问..."
curl -s --connect-timeout 5 https://api.github.com/zen > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "   ✅ GitHub API访问正常"
else
    echo "   ❌ GitHub API访问失败"
fi

# 测试4: Git远程连接测试
echo "4. 测试Git远程连接..."
cd /home/admin/openclaw/workspace
timeout 5 git ls-remote --heads origin > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "   ✅ Git远程连接正常"
else
    echo "   ❌ Git远程连接失败"
fi

# 测试5: 检查待推送提交
echo "5. 检查待推送提交..."
PENDING_COMMITS=$(git log --oneline origin/main..HEAD | wc -l)
echo "   待推送提交: $PENDING_COMMITS 个"

# 测试6: 检查lifeos仓库状态
echo "6. 检查lifeos仓库状态..."
cd /home/admin/openclaw/workspace/lifeos
LIFEOS_STATUS=$(git status --porcelain)
if [ -z "$LIFEOS_STATUS" ]; then
    echo "   ✅ Lifeos仓库干净"
else
    echo "   ⚠️  Lifeos仓库有未提交更改"
fi

LIFEOS_SYNC=$(git log --oneline origin/main..HEAD | wc -l)
if [ $LIFEOS_SYNC -eq 0 ]; then
    echo "   ✅ Lifeos仓库已同步"
else
    echo "   ⚠️  Lifeos仓库有 $LIFEOS_SYNC 个提交待推送"
fi

echo "=========================================="
echo "🔍 网络诊断完成 - $(date)"