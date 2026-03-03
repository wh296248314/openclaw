        lines.append("=" * 60)
        lines.append("增强版监控卫士（钉钉通知版） - 实时仪表板")
        lines.append("=" * 60)
        
        lines.append(f"\n📊 活跃任务: {len(self.active_tasks)} 个")
        if self.active_tasks:
            for task_id, task in self.active_tasks.items():
                elapsed = (datetime.now() - task["start_time"]).total_seconds()
                priority = task["priority"]
                icon = "🔴" if priority == "critical" else "🟠" if priority == "high" else "🟡" if priority == "medium" else "🟢"
                lines.append(f"{icon} {task['task_name']} - {elapsed:.1f}s")
        
        lines.append(f"\n📈 历史任务: {len(self.task_history)} 个")
        if self.task_history:
            completed = sum(1 for t in self.task_history if t.get("status") == "completed")
            total = len(self.task_history)
            rate = (completed / total * 100) if total > 0 else 0
            lines.append(f"  完成率: {rate:.1f}% ({completed}/{total})")
        
        # 钉钉通知状态
        dingtalk_status = "✅ 已启用" if self.dingtalk_notifier.enabled else "⚠️  未配置"
        lines.append(f"\n📱 钉钉通知: {dingtalk_status}")
        
        lines.append("\n" + "=" * 60)
        return "\n".join(lines)


def test_dingtalk_integration():
    """测试钉钉通知集成"""
    print("🎯 测试钉钉通知集成功能")
    print("=" * 50)
    
    # 创建实例
    guardian = EnhancedGuardianWithDingTalk()
    
    # 检查钉钉配置
    webhook_url = guardian.config["dingtalk_config"]["webhook_url"]
    
    if webhook_url:
        print(f"✅ 找到钉钉Webhook配置")
        print(f"   通知渠道: {guardian.config['notification_channels']}")
    else:
        print("⚠️  未配置钉钉Webhook URL")
        print("   请设置环境变量:")
        print("   export DINGTALK_WEBHOOK_URL='你的Webhook URL'")
        print("   export DINGTALK_SECRET='你的加签密钥'（可选）")
    
    # 启动监控
    guardian.start()
    
    # 创建测试任务
    print("\n📝 创建测试任务:")
    test_tasks = [
        ("test_dingtalk_critical", "钉钉通知测试-关键任务", "critical", 25),
        ("test_dingtalk_high", "钉钉通知测试-重要任务", "high", 45)
    ]
    
    for task_id, name, priority, est in test_tasks:
        guardian.start_task(task_id, name, priority, est)
        icon = "🔴" if priority == "critical" else "🟠"
        print(f"{icon} {name} (优先级: {priority}, 预估: {est}秒)")
    
    print("\n🔄 监控中... 等待超时触发钉钉通知")
    print("按 Ctrl+C 停止测试")
    
    try:
        # 等待足够时间让任务超时
        for i in range(4):
            time.sleep(15)
            print(f"\n⏰ 第{i+1}次检查 ({datetime.now().strftime('%H:%M:%S')})")
            print(guardian.get_dashboard())
            
            # 模拟任务完成
            if i == 2:
                guardian.complete_task("test_dingtalk_critical", "测试完成")
                print("✅ 关键任务完成")
            elif i == 3:
                guardian.complete_task("test_dingtalk_high", "测试完成")
                print("✅ 重要任务完成")
                
    except KeyboardInterrupt:
        print("\n\n🛑 用户中断测试...")
    finally:
        guardian.stop()
        print("\n✅ 钉钉通知集成测试完成")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true", help="测试钉钉通知集成")
    parser.add_argument("--dashboard", action="store_true", help="显示仪表板")
    parser.add_argument("--config", help="配置文件路径")
    
    args = parser.parse_args()
    
    if args.test:
        test_dingtalk_integration()
    elif args.dashboard:
        guardian = EnhancedGuardianWithDingTalk(args.config)
        print(guardian.get_dashboard())
    else:
        print("增强版监控卫士（钉钉通知版）")
        print("使用说明:")
        print("  python3 enhanced_guardian_with_dingtalk.py --test    # 测试钉钉通知")
        print("  python3 enhanced_guardian_with_dingtalk.py --dashboard  # 显示仪表板")
        print("")
        print("环境变量配置:")
        print("  export DINGTALK_WEBHOOK_URL='你的钉钉机器人Webhook URL'")
        print("  export DINGTALK_SECRET='你的加签密钥'（可选）")
        print("")
        print("钉钉机器人创建步骤:")
        print("  1. 打开钉钉群 → 群设置 → 智能群助手")
        print("  2. 添加机器人 → 自定义机器人")
        print("  3. 设置机器人名称和安全设置")
        print("  4. 复制Webhook URL和加签密钥")