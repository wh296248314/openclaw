#!/bin/bash

# 智能超时监控卫士启动脚本
# 作者: 皮休 (Pixiu)
# 创建时间: 2026-03-03

echo "🛡️  启动智能超时监控卫士..."
echo "========================================"

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到Python3，请先安装Python3"
    exit 1
fi

# 检查Python版本
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "✅ Python版本: $PYTHON_VERSION"

# 检查依赖
echo "🔍 检查依赖..."
if ! python3 -c "import threading" 2>/dev/null; then
    echo "❌ 错误: Python threading模块不可用"
    exit 1
fi

# 创建必要的目录
mkdir -p logs
mkdir -p data

# 设置文件权限
chmod +x timeout_guardian.py
chmod +x guardian_cli.py

# 显示配置信息
echo ""
echo "📋 配置信息:"
echo "   超时阈值: 60秒"
echo "   最大提醒次数: 3次"
echo "   检查间隔: 30秒"
echo "   日志目录: ./logs"
echo "   数据目录: ./data"
echo ""

# 显示使用说明
echo "📖 使用说明:"
echo "   1. 启动监控: ./guardian_cli.py start"
echo "   2. 查看统计: ./guardian_cli.py stats"
echo "   3. 创建任务: ./guardian_cli.py task"
echo "   4. 查看帮助: ./guardian_cli.py help"
echo ""

# 询问是否立即启动
read -p "是否立即启动监控卫士? (y/n): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🚀 启动监控卫士..."
    python3 guardian_cli.py start
else
    echo "✅ 准备就绪！你可以随时使用上述命令启动。"
    echo ""
    echo "💡 提示:"
    echo "   • 首次运行会创建一个演示任务"
    echo "   • 监控数据会自动保存到 timeout_guardian_history.json"
    echo "   • 按 Ctrl+C 可以安全退出"
fi

echo ""
echo "========================================"
echo "🛡️  智能超时监控卫士已准备就绪！"