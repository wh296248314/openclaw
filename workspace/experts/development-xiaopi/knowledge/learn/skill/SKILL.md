---
name: learning-agent
description: 定期学习技能，发现并推荐有用的agent技能。用于持续学习和技能更新。
metadata:
  {
    "openclaw": {
      "requires": { "bins": ["clawhub"] },
      "install": [
        {
          "id": "node",
          "kind": "node",
          "package": "clawhub",
          "bins": ["clawhub"],
          "label": "Install ClawHub CLI"
        }
      ]
    }
  }
---

# 学习工作流

这个技能负责定期搜索和发现有用的agent技能，并生成推荐报告。

## 功能

1. **技能发现** - 搜索ClawHub发现相关技能
2. **技能评估** - 评估技能的实用性
3. **推荐生成** - 生成技能推荐报告

## 使用方式

### 发现技能
```
发现 AI_Agents 领域的新技能
```

### 扫描所有关注领域
```
扫描所有关注领域
```

### 生成周报
```
生成本周学习报告
```
