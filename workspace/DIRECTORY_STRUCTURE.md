# 工作空间目录结构说明

## 🎯 设计原则
1. **分类清晰**：按功能分类，不混放
2. **查找方便**：知道找什么就知道去哪找
3. **维护简单**：定期整理，保持整洁
4. **安全可控**：重要文件有备份，临时文件可清理

## 📁 目录结构（优化后）

### 根目录核心文件
- `AGENTS.md` - Agent工作空间说明
- `SOUL.md` - Agent人格定义
- `USER.md` - 用户信息
- `TOOLS.md` - 工具配置
- `IDENTITY.md` - Agent身份
- `HEARTBEAT.md` - 心跳任务
- `CONFIG_README.md` - 配置文件说明
- `DIRECTORY_STRUCTURE.md` - 目录结构说明

### configs/ - 配置文件
```
configs/
├── openclaw/     # OpenClaw系统配置
├── monitor/      # 监控配置
│   ├── guardian_config.json
│   ├── timeout_guardian_history.json
│   ├── timeout_guardian_optimized_config.json
│   └── timeout_monitor_state.json
└── system/       # 系统配置
    └── obsidian-sync-state.json
```

### data/ - 数据文件
```
data/
├── guardian_tasks.json      # 监控卫士任务数据
├── monitor/                 # 监控数据
│   └── simple_tasks.json
└── system/                  # 系统数据
```

### docs/ - 文档
```
docs/
├── README.md               # 文档索引
├── guides/                 # 使用指南
│   ├── 钉钉通知配置指南.md
│   └── 虎码输入法相关指南.md
├── references/             # 参考文档
│   ├── 智能超时监控卫士相关文档.md
│   └── SCRM相关分析报告.md
├── plans/                  # 计划文档
│   └── 实施计划相关文档.md
└── 其他文档.md
```

### scripts/ - 脚本文件
```
scripts/
├── monitor/                # 监控相关脚本
│   ├── guardian_enhanced.py
│   ├── guardian_final_fixed.py
│   └── timeout_guardian.py
├── system/                 # 系统工具脚本
├── utils/                  # 通用工具脚本
└── projects/               # 项目脚本
```

### projects/ - 项目文件
```
projects/
├── guardian/              # 监控卫士项目
├── obsidian/              # Obsidian项目
└── clash-party/           # Clash Party项目
```

### logs/ - 日志文件
```
logs/
├── monitor/               # 监控日志
│   ├── guardian_enhanced.log
│   └── guardian_final.log
└── system/                # 系统日志
```

### memory/ - 记忆文件（特殊目录）
- 每日工作记录 (`YYYY-MM-DD.md`)
- 长期记忆维护文件

### lifeos/ - Obsidian笔记系统（特殊目录）
- 个人知识管理系统
- 保持原有结构

### archive/ - 归档文件
- 旧版本备份
- 历史文件归档
- 不再活跃的文件

### temp/ - 临时文件
- 临时测试文件
- 待处理文件
- 短期存储文件

## 🔄 文件命名规范
### 脚本文件
- `monitor_`开头：监控相关
- `sys_`开头：系统工具
- `util_`开头：通用工具
- `test_`开头：测试文件（放temp/）

### 配置文件
- 使用有意义的名称
- 避免通用名如`config.json`
- 包含应用名和用途

### 文档文件
- 中文描述性名称
- 包含日期和版本
- 使用Markdown格式

## 🧹 维护规则
### 每日维护
1. 清理`temp/`目录中的旧文件
2. 移动新文件到正确目录
3. 检查`logs/`目录大小

### 每周维护
1. 归档`logs/`中的旧日志
2. 整理`docs/`中的文档
3. 检查文件分类是否正确

### 每月维护
1. 全面检查目录结构
2. 清理`archive/`中的过期文件
3. 更新本说明文档

## 🚀 快速查找指南
| 要找什么 | 去哪个目录 |
|----------|------------|
| 配置文件 | `configs/` |
| 监控脚本 | `scripts/monitor/` |
| 系统工具 | `scripts/system/` |
| 通用工具 | `scripts/utils/` |
| 文档资料 | `docs/` |
| 运行日志 | `logs/` |
| 临时文件 | `temp/` |
| 历史备份 | `archive/` |
| 每日记录 | `memory/` |
| 笔记系统 | `lifeos/` |

## ⚠️ 注意事项
1. **不要直接在根目录创建文件**
2. **新文件先放`temp/`，再分类移动**
3. **大文件不要放Git仓库**
4. **定期运行整理脚本**

## 🔧 整理工具
- `organize_workspace.sh` - 自动整理脚本
- `cleanup_temp_files.sh` - 清理临时文件
- `check_directory_structure.sh` - 检查目录结构

---
*保持整洁，提高效率。*
*最后更新：2026-03-04 工作空间优化完成*
