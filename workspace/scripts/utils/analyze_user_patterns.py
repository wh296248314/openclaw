#!/usr/bin/env python3
import os
import re
from datetime import datetime

def analyze_files():
    patterns = {
        "称呼": [],
        "沟通风格": [],
        "任务偏好": [],
        "技术偏好": [],
        "反馈模式": []
    }
    
    # 检查现有配置文件
    config_files = ["SOUL.md", "USER.md", "MEMORY.md", "TOOLS.md"]
    
    for file in config_files:
        if os.path.exists(file):
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            if file == "USER.md":
                # 提取用户信息
                name_match = re.search(r"Name:\s*(.+)", content)
                if name_match:
                    patterns["称呼"].append(f"英文名: {name_match.group(1)}")
                
                call_match = re.search(r"What to call them:\s*(.+)", content)
                if call_match:
                    patterns["称呼"].append(f"称呼: {call_match.group(1)}")
            
            elif file == "SOUL.md":
                # 提取行为准则
                if "务实温和" in content:
                    patterns["沟通风格"].append("务实温和，克制但有温度")
                if "有自己的立场" in content:
                    patterns["沟通风格"].append("有自己的立场，敢下结论")
                if "禁止废话" in content:
                    patterns["沟通风格"].append("禁止废话，不客套")
                if "中文互联网口语" in content:
                    patterns["沟通风格"].append("允许自然的中文互联网口语")
    
    # 从今日工作记录中提取
    today_file = "memory/2026-03-03.md"
    if os.path.exists(today_file):
        with open(today_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 提取任务类型偏好
        if "SCRM" in content:
            patterns["任务偏好"].append("SCRM系统相关工作")
        if "监控卫士" in content:
            patterns["任务偏好"].append("系统监控和自动化")
        if "clash-party" in content:
            patterns["技术偏好"].append("代理工具配置")
        if "虎码输入法" in content:
            patterns["技术偏好"].append("中文输入法配置")
    
    return patterns

if __name__ == "__main__":
    patterns = analyze_files()
    
    print("🎯 用户模式分析结果:")
    print("=" * 50)
    
    for category, items in patterns.items():
        if items:
            print(f"\n{category}:")
            for item in set(items):  # 去重
                print(f"  • {item}")
    
    print("\n" + "=" * 50)
    print(f"分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

