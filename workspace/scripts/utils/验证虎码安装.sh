#!/bin/bash
echo "虎码输入法安装验证"
echo "===================="

echo "1. 文件检查:"
if [ -f /usr/share/ibus-table/tables/tiger.db ]; then
    echo "   ✅ tiger.db 已安装"
    ls -lh /usr/share/ibus-table/tables/tiger.db
else
    echo "   ❌ tiger.db 未找到"
fi

echo ""
echo "2. ibus服务检查:"
if pgrep ibus-daemon > /dev/null; then
    echo "   ✅ ibus-daemon 正在运行"
    ps aux | grep ibus-daemon | grep -v grep
else
    echo "   ❌ ibus-daemon 未运行"
fi

echo ""
echo "3. 输入法框架检查:"
im-config -m | grep ibus && echo "   ✅ ibus 是当前输入法框架" || echo "   ⚠️  ibus 不是当前框架"

echo ""
echo "4. 使用说明:"
echo "   📝 文件已安装完成！"
echo "   🔧 接下来需要:"
echo "       1. 重新登录系统或重启"
echo "       2. 打开系统设置 → 区域与语言 → 输入源"
echo "       3. 点击'+'添加输入源"
echo "       4. 选择'中文' → 查找'虎码'或'Tiger'"
echo "       5. 使用 Super+Space 切换输入法"
echo ""
echo "5. 快速测试:"
echo "   重启ibus: pkill ibus-daemon && ibus-daemon -drx &"
echo "   打开设置: ibus-setup"
