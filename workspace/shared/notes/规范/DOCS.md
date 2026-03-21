# 文档管理规范

## 目录结构

```
deployment-xiaopi/
├── 身份文件（根目录）
│   ├── SOUL.md          # 专家灵魂定义
│   ├── IDENTITY.md      # 身份标识
│   ├── USER.md          # 用户信息
│   ├── MEMORY.md        # 长期记忆
│   ├── TOOLS.md         # 工具配置
│   └── AGENTS.md        # 工作规范
│
├── memory/              # 每日工作日志
│   ├── 2026-03-15.md   # 当天日志
│   └── ...
│
├── learning/           # 学习体系
│   ├── domains.md      # 学习领域
│   ├── workflow.md     # 工作流
│   ├── discovered.md   # 发现记录
│   ├── skill-inventory.md  # 技能库存
│   └── learning-cron.sh   # 定时脚本
│
└── skills/             # 已安装技能
    ├── monitoring/
    └── kubernetes-devops/
```

## 日常整理要求

### 每天必做
1. 记录当日工作到 `memory/YYYY-MM-DD.md`
2. 更新 `learning/skill-inventory.md`（如有安装新技能）
3. 检查 `learning/discovered.md`（如有新发现）

### 定期整理
- 每周六：检查learning目录，生成汇总
- 每月末：清理过期日志，整理归档

## 文档命名规范
- 日期格式：`YYYY-MM-DD.md`
- 技能文档：与技能名一致
- 学习文档：用英文或拼音避免乱码
