#!/usr/bin/env python3
import os
import docx

def analyze_document(file_path):
    """分析回流数据问题文档"""
    doc = docx.Document(file_path)
    
    analysis = {
        "title": "回流数据问题梳理分析",
        "sections": [],
        "processes": [],
        "problems": [],
        "solutions": [],
        "key_points": []
    }
    
    # 提取所有内容
    content = []
    for para in doc.paragraphs:
        if para.text.strip():
            content.append(para.text.strip())
    
    # 分析文档结构
    current_section = ""
    for line in content:
        if line.startswith("一、"):
            current_section = "使用场景"
            analysis["sections"].append({"title": line, "type": "section"})
        elif line.startswith("二、"):
            current_section = "问题分析"
            analysis["sections"].append({"title": line, "type": "section"})
        elif line.startswith("三、"):
            current_section = "解决方案"
            analysis["sections"].append({"title": line, "type": "section"})
        elif line.startswith("1、") or line.startswith("2、"):
            if current_section == "使用场景":
                analysis["processes"].append(line)
            elif current_section == "问题分析":
                analysis["problems"].append(line)
            elif current_section == "解决方案":
                analysis["solutions"].append(line)
        elif "流程" in line:
            analysis["key_points"].append(line)
        elif "BUG" in line or "问题" in line:
            analysis["key_points"].append(line)
        elif "方案" in line:
            analysis["key_points"].append(line)
    
    return analysis

def generate_flowchart_markdown(analysis):
    """生成流程图Markdown"""
    flowchart = """# 回流数据问题梳理 - 流程图分析

## 📊 文档概要
**文档标题**: 副本关于回流数据问题梳理.docx
**核心问题**: SCRM系统中回流（存量）资源处理流程的数据混淆和统计失真问题

## 🔄 系统使用场景

### 1. 新增资源处理流程
```mermaid
flowchart TD
    A[创建活动] --> B[新增资源导入TMK公海]
    B --> C[电话外呼触达]
    C --> D{意向判断}
    D -->|预约成功| E[自动流转回SCRM系统]
    D -->|未成功| F[继续外呼或放弃]
    E --> G[分配给销售/校区跟进]
    G --> H[后续转化]
```

### 2. 回流（存量）资源处理流程
```mermaid
flowchart TD
    A[历史未转化资源] --> B[创建/修改活动名称]
    B --> C[投入TMK团队清洗激活]
    C --> D[电话外呼触达]
    D --> E{意向判断}
    E -->|预约成功| F[流转回SCRM系统]
    E -->|未成功| G[继续清洗或放弃]
    F --> H[分配给销售跟进]
    H --> I[后续转化]
```

## ⚠️ 回流资源存在的BUG

### 问题流程图
```mermaid
flowchart TD
    A[修改活动名称] --> B[系统更新所有历史数据]
    B --> C[包含：<br>1. 尚未回流的历史资源<br>2. 已在读学员<br>3. 真正需回流资源]
    C --> D[数据混淆]
    C --> E[看板统计失真]
    
    D --> F[已转化/无需跟进资源<br>归类在当前活动]
    E --> G[未跟进资源提醒<br>计入所有历史数据]
    
    F --> H[干扰运营判断]
    G --> H
    H --> I[影响管理效率与数据准确性]
```

## 🎯 核心诉求与解决方案

### 方案一：剔除干扰项
```mermaid
flowchart TD
    A[BI未跟进资源提醒] --> B{数据筛选}
    B -->|排除| C[已在读学员数据]
    B -->|仅统计| D[真正需要外呼触达的资源]
    D --> E[准确统计]
    E --> F[提升管理效率]
```

### 方案二：规范更名操作
```mermaid
flowchart TD
    A[需要更改活动名称] --> B{操作对象选择}
    B -->|仅对| C[已回流的数据]
    B -->|避免波及| D[未回流数据<br>在读学员数据]
    C --> E[从源头减少统计干扰]
    D --> F[保持数据纯净]
```

## 📋 关键问题总结

### 数据混淆问题
1. **现象**: 修改活动名称时，系统更新所有历史数据
2. **影响**: 已转化/无需跟进资源被错误归类
3. **后果**: 数据准确性下降，运营判断受干扰

### 统计失真问题
1. **现象**: 未跟进资源提醒计入所有历史数据
2. **影响**: 包含已在读学员等不应统计的数据
3. **后果**: 管理效率降低，数据看板失真

## 💡 建议实施步骤

```mermaid
flowchart LR
    A[问题识别] --> B[方案评估]
    B --> C[技术实施]
    C --> D[测试验证]
    D --> E[上线部署]
    E --> F[监控优化]
    
    subgraph 方案一
        C1[修改BI统计逻辑]
        C1 --> D1[排除在读学员]
    end
    
    subgraph 方案二
        C2[优化活动更名功能]
        C2 --> D2[限制更名范围]
    end
    
    B --> 方案一
    B --> 方案二
```

---
*分析完成时间: 2026-02-28*
*文档来源: 副本关于回流数据问题梳理.docx*
"""
    
    return flowchart

def main():
    file_path = "/home/admin/Downloads/副本关于回流数据问题梳理.docx"
    
    if not os.path.exists(file_path):
        print("❌ 文件不存在:", file_path)
        return
    
    print("📊 分析文档内容...")
    analysis = analyze_document(file_path)
    
    print("\n✅ 分析完成！")
    print(f"📑 文档标题: {analysis['title']}")
    print(f"📋 章节数量: {len(analysis['sections'])}")
    print(f"🔄 流程描述: {len(analysis['processes'])} 个")
    print(f"⚠️ 问题点: {len(analysis['problems'])} 个")
    print(f"🎯 解决方案: {len(analysis['solutions'])} 个")
    
    # 生成流程图Markdown
    flowchart_md = generate_flowchart_markdown(analysis)
    
    # 保存到文件
    output_path = "/home/admin/openclaw/workspace/回流数据问题梳理-流程图.md"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(flowchart_md)
    
    print(f"\n📁 流程图已保存到: {output_path}")
    
    # 预览部分内容
    print("\n📝 流程图预览（前20行）:")
    print("="*60)
    lines = flowchart_md.split("\n")
    for i in range(min(30, len(lines))):
        print(lines[i])
    print("="*60)

if __name__ == "__main__":
    main()