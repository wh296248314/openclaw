#!/usr/bin/env python3
"""
技能库状态检查脚本
检查所有已安装技能的状态和依赖
"""

import os
import sys
import json
import subprocess
from pathlib import Path

def check_python_skill(skill_path):
    """检查Python技能"""
    results = {
        "status": "unknown",
        "python_available": False,
        "dependencies": [],
        "issues": []
    }
    
    # 检查Python3是否可用
    try:
        subprocess.run(["python3", "--version"], capture_output=True, check=True)
        results["python_available"] = True
    except:
        results["issues"].append("Python3不可用")
        results["status"] = "error"
        return results
    
    # 检查requirements.txt
    req_file = os.path.join(skill_path, "requirements.txt")
    if os.path.exists(req_file):
        results["dependencies"].append("requirements.txt存在")
        # 可以在这里添加依赖检查逻辑
    
    # 检查Python脚本
    py_files = list(Path(skill_path).glob("*.py"))
    if py_files:
        results["dependencies"].append(f"找到{len(py_files)}个Python文件")
    
    if not results["issues"]:
        results["status"] = "ok"
    
    return results

def check_skill(skill_name, skill_path):
    """检查单个技能"""
    print(f"\n🔍 检查技能: {skill_name}")
    print(f"   路径: {skill_path}")
    
    # 检查SKILL.md文件
    skill_md = os.path.join(skill_path, "SKILL.md")
    if os.path.exists(skill_md):
        print("   ✅ SKILL.md存在")
        
        # 读取技能描述
        with open(skill_md, 'r', encoding='utf-8') as f:
            content = f.read(500)
            if "description:" in content:
                # 提取描述
                lines = content.split('\n')
                for line in lines:
                    if line.startswith("description:"):
                        desc = line.replace("description:", "").strip()
                        print(f"   描述: {desc}")
                        break
    else:
        print("   ❌ SKILL.md缺失")
    
    # 检查配置文件
    config_files = list(Path(skill_path).glob("*.json")) + list(Path(skill_path).glob("*.yaml")) + list(Path(skill_path).glob("*.yml"))
    if config_files:
        print(f"   找到{len(config_files)}个配置文件")
    
    # 检查Python技能
    py_check = check_python_skill(skill_path)
    if py_check["status"] == "ok":
        print("   ✅ Python环境正常")
    elif py_check["issues"]:
        print(f"   ⚠️ Python问题: {', '.join(py_check['issues'])}")
    
    # 检查脚本文件
    script_files = list(Path(skill_path).glob("*.sh")) + list(Path(skill_path).glob("*.py"))
    if script_files:
        print(f"   找到{len(script_files)}个脚本文件")
    
    return True

def main():
    """主函数"""
    print("=" * 60)
    print("技能库状态检查")
    print("=" * 60)
    
    # 检查自定义技能
    custom_skills_dir = Path.home() / ".openclaw" / "skills"
    if custom_skills_dir.exists():
        print(f"\n📁 自定义技能目录: {custom_skills_dir}")
        
        skill_dirs = [d for d in custom_skills_dir.iterdir() if d.is_dir()]
        print(f"找到 {len(skill_dirs)} 个自定义技能")
        
        for skill_dir in skill_dirs:
            check_skill(skill_dir.name, str(skill_dir))
    
    # 检查Feishu技能
    feishu_skills_dir = Path.home() / ".openclaw" / "extensions" / "feishu" / "skills"
    if feishu_skills_dir.exists():
        print(f"\n📁 Feishu技能目录: {feishu_skills_dir}")
        
        skill_dirs = [d for d in feishu_skills_dir.iterdir() if d.is_dir()]
        print(f"找到 {len(skill_dirs)} 个Feishu技能")
        
        for skill_dir in skill_dirs:
            check_skill(f"feishu-{skill_dir.name}", str(skill_dir))
    
    # 检查系统技能
    system_skills_dir = Path("/home/admin/.npm-global/lib/node_modules/openclaw/skills")
    if system_skills_dir.exists():
        print(f"\n📁 系统技能目录: {system_skills_dir}")
        
        skill_dirs = [d for d in system_skills_dir.iterdir() if d.is_dir()]
        print(f"找到 {len(skill_dirs)} 个系统技能")
        
        # 只检查几个关键系统技能
        key_skills = ["clawhub", "healthcheck", "skill-creator", "tmux", "weather"]
        for skill_name in key_skills:
            skill_dir = system_skills_dir / skill_name
            if skill_dir.exists():
                check_skill(skill_name, str(skill_dir))
    
    print("\n" + "=" * 60)
    print("检查完成")
    print("=" * 60)

if __name__ == "__main__":
    main()