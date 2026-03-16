# 文档管理规范

## 原则

1. **固定位置**：所有文档放在 `/home/pixiu/.openclaw/workspace/experts/product-xiaopi/` 目录下
2. **分类清晰**：按类型分目录（memory/, skills/, configs/等）
3. **每日整理**：每天工作结束前整理当天创建的文档
4. **命名规范**：使用有意义的文件名，格式 `YYYY-MM-DD-描述.md`

## 目录结构

```
product-xiaopi/
├── AGENTS.md           #  workspace配置
├── SOUL.md             #  身份定义
├── USER.md             #  用户信息
├── TOOLS.md            #  工具配置
├── IDENTITY.md         #  身份标识
├── MEMORY.md           #  长期记忆
├── HEARTBEAT.md        #  心跳配置
├── BOOTSTRAP.md        #  启动配置（如果有）
├── skill-discovery-config.md  # 技能发现配置
├── memory/             #  每日工作日志
│   ├── 2026-03-12.md
│   ├── 2026-03-13.md
│   └── ...
└── skills/             #  安装的技能（如果需要）
```

## 每日整理检查清单

- [ ] 当天创建的文档是否放在正确位置？
- [ ] 文档命名是否规范？
- [ ] 需要更新的记忆是否已同步到MEMORY.md？
- [ ] 临时文件是否清理？

## 更新日志

- 2026-03-15: 创建文档管理规范
