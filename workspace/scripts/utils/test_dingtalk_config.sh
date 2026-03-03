#!/bin/bash
# 钉钉通知配置测试脚本

echo "钉钉通知配置测试"
echo "================="
echo "测试时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# 检查环境变量
echo "1. 检查环境变量配置:"
echo "----------------------------------------"

DINGTALK_WEBHOOK=${DINGTALK_WEBHOOK_URL:-""}
DINGTALK_SECRET=${DINGTALK_SECRET:-""}

if [ -n "$DINGTALK_WEBHOOK" ]; then
    echo "✅ DINGTALK_WEBHOOK_URL: 已设置"
    # 隐藏敏感信息，只显示部分
    echo "   值: ${DINGTALK_WEBHOOK:0:50}..."
else
    echo "❌ DINGTALK_WEBHOOK_URL: 未设置"
    echo "   请执行: export DINGTALK_WEBHOOK_URL='你的Webhook URL'"
fi

if [ -n "$DINGTALK_SECRET" ]; then
    echo "✅ DINGTALK_SECRET: 已设置"
    echo "   值: ${DINGTALK_SECRET:0:10}..."
else
    echo "⚠️  DINGTALK_SECRET: 未设置（可选）"
fi

echo ""
echo "2. 测试钉钉通知模块:"
echo "----------------------------------------"

# 测试钉钉通知模块
python3 << 'EOF'
import os
from dingtalk_notifier import DingTalkNotifier

webhook_url = os.environ.get("DINGTALK_WEBHOOK_URL")
secret = os.environ.get("DINGTALK_SECRET")

print("钉钉通知模块测试:")
print(f"  Webhook URL: {'✅ 已配置' if webhook_url else '❌ 未配置'}")
print(f"  Secret: {'✅ 已配置' if secret else '⚠️  未配置（可选）'}")

if webhook_url:
    print("\n正在测试钉钉通知发送...")
    notifier = DingTalkNotifier(webhook_url, secret)
    
    if notifier.enabled:
        print("✅ 钉钉通知器初始化成功")
        
        # 发送测试消息
        import datetime
        test_title = "监控卫士钉钉通知测试"
        test_message = f"这是增强版智能超时监控卫士的钉钉通知功能测试\n测试时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n如果收到此消息，说明钉钉通知配置成功！"
        
        print("发送测试消息...")
        success = notifier.send_simple_message(test_title, test_message)
        
        if success:
            print("🎉 钉钉测试通知发送成功！请检查钉钉群消息")
        else:
            print("❌ 钉钉测试通知发送失败，请检查配置和网络")
    else:
        print("❌ 钉钉通知器初始化失败")
else:
    print("\n⚠️  未配置Webhook URL，跳过实际发送测试")
    print("   请先设置环境变量: export DINGTALK_WEBHOOK_URL='你的Webhook URL'")
EOF

echo ""
echo "3. 测试集成版监控卫士:"
echo "----------------------------------------"

# 检查集成版代码
if [ -f "enhanced_guardian_with_dingtalk.py" ]; then
    echo "✅ 集成版监控卫士代码存在"
    
    # 测试集成版
    python3 << 'EOF'
import os
from enhanced_guardian_with_dingtalk import EnhancedGuardianWithDingTalk

print("集成版监控卫士测试:")
guardian = EnhancedGuardianWithDingTalk()

# 检查配置
config = guardian.config
print(f"  通知渠道: {config['notification_channels']}")
print(f"  钉钉配置: {'✅ 已启用' if guardian.dingtalk_notifier.enabled else '❌ 未启用'}")

if guardian.dingtalk_notifier.enabled:
    print("✅ 钉钉通知功能已集成到监控卫士")
    
    # 显示仪表板
    print("\n监控卫士仪表板:")
    print(guardian.get_dashboard())
else:
    print("⚠️  钉钉通知功能未启用，请配置Webhook URL")
EOF
else
    echo "❌ 集成版监控卫士代码不存在"
fi

echo ""
echo "4. 配置建议:"
echo "----------------------------------------"

cat << 'EOF'
📋 完整配置步骤:

1. 创建钉钉机器人:
   - 打开钉钉群 → 群设置 → 智能群助手
   - 添加机器人 → 自定义机器人
   - 设置名称和安全设置（推荐加签）
   - 复制Webhook URL和Secret

2. 配置环境变量:
   export DINGTALK_WEBHOOK_URL="你的Webhook URL"
   export DINGTALK_SECRET="你的加签密钥"
   
   # 永久保存
   echo 'export DINGTALK_WEBHOOK_URL="你的URL"' >> ~/.bashrc
   echo 'export DINGTALK_SECRET="你的密钥"' >> ~/.bashrc
   source ~/.bashrc

3. 更新监控配置:
   - 编辑 timeout_guardian_optimized_config.json
   - 添加钉钉配置:
     {
       "notification_channels": ["log", "dingtalk"],
       "dingtalk_config": {
         "webhook_url": "你的URL",
         "secret": "你的密钥",
         "mention_users": ["手机号"]
       }
     }

4. 启动监控:
   python3 enhanced_guardian_with_dingtalk.py --config timeout_guardian_optimized_config.json

5. 验证功能:
   - 创建测试任务并等待超时
   - 检查钉钉群是否收到通知
   - 查看日志确认发送状态
EOF

echo ""
echo "5. 快速测试命令:"
echo "----------------------------------------"
echo "🔧 手动发送测试消息:"
echo "  python3 -c \""
echo "  from dingtalk_notifier import DingTalkNotifier"
echo "  notifier = DingTalkNotifier('你的URL', '你的密钥')"
echo "  notifier.send_simple_message('测试', '测试消息')\""
echo ""
echo "🚀 启动集成版监控:"
echo "  python3 enhanced_guardian_with_dingtalk.py --test"
echo ""
echo "📊 查看当前状态:"
echo "  python3 enhanced_guardian_with_dingtalk.py --dashboard"
echo ""
echo "📝 查看详细指南:"
echo "  阅读: 钉钉通知配置指南.md"

echo ""
echo "测试完成!"
echo "如果遇到问题，请检查:"
echo "1. 钉钉机器人是否正常"
echo "2. Webhook URL是否正确"
echo "3. 网络连接是否正常"
echo "4. 查看日志文件: enhanced_timeout_guardian.log"