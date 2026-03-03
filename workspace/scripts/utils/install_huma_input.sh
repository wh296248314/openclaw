#!/bin/bash
# 尝试安装虎码输入法的脚本

echo "尝试安装虎码输入法..."

# 方法1: 检查是否有现成的ibus-table包
echo "方法1: 搜索ibus-table相关包"
apt-cache search huma 2>/dev/null || echo "未找到huma相关包"

# 方法2: 检查是否有fcitx版本
echo -e "\n方法2: 搜索fcitx相关包"
apt-cache search fcitx.*huma 2>/dev/null || echo "未找到fcitx-huma相关包"

# 方法3: 尝试从GitHub查找
echo -e "\n方法3: 检查GitHub上的虎码输入法项目"
# 虎码输入法可能是一个开源项目，需要从源码编译

# 方法4: 检查是否有第三方PPA
echo -e "\n方法4: 检查PPA源"
grep -r "huma" /etc/apt/sources.list* 2>/dev/null || echo "未找到huma相关PPA"

# 方法5: 检查当前用户是否有自定义输入法配置
echo -e "\n方法5: 检查用户输入法配置"
if [ -d ~/.config/ibus/tables ]; then
    echo "ibus tables目录存在，检查内容:"
    ls -la ~/.config/ibus/tables/
else
    echo "ibus tables目录不存在"
fi

# 方法6: 尝试安装ibus-table-all查看所有可用表格
echo -e "\n方法6: 安装ibus-table-all查看所有表格"
sudo apt install -y ibus-table-all 2>/dev/null | tail -20

echo -e "\n当前可用的中文输入法表格:"
apt list ibus-table-* 2>/dev/null | grep -v "Listing" | head -30

echo -e "\n建议:"
echo "1. 虎码输入法可能需要从源码编译安装"
echo "2. 可以尝试安装其他中文输入法如:"
echo "   sudo apt install ibus-pinyin ibus-libpinyin"
echo "3. 或者安装fcitx输入法框架:"
echo "   sudo apt install fcitx fcitx-pinyin fcitx-table"
echo "4. 设置默认输入法:"
echo "   im-config -n ibus  # 设置ibus为默认"
echo "   im-config -n fcitx # 设置fcitx为默认"