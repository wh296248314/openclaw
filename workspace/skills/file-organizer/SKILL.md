---
name: file-organizer
version: 2.0.0
description: 整理和管理workspace目录，清理杂乱的测试数据、临时文件，按类型/日期分类归档。支持飞书文档整理、团队协作整理、MEMORY管理。
---

# File Organizer v2.0

小皮团队专用文件整理技能，支持workspace、飞书文档、团队协作整理。

## 功能概览

| 功能 | 说明 |
|------|------|
| 目录整理 | workspace文件整理、清理、归档 |
| 飞书文档 | 云盘、文档、知识库整理 |
| 团队协作 | experts/各小皮目录规范化 |
| MEMORY管理 | 每日memory记录检查和清理 |
| 脚本工具 | 自动化清理归档脚本 |

---

## 一、目录整理

### 标准目录结构

```
workspace/
├── AGENTS.md, SOUL.md, USER.md, TOOLS.md, MEMORY.md
├── HEARTBEAT.md, BOOTSTRAP.md
├── experts/              # 专家小皮目录
│   ├── product-xiaopi/
│   ├── design-xiaopi/
│   ├── development-xiaopi/
│   ├── testing-xiaopi/
│   ├── deployment-xiaopi/
│   └── audit-xiaopi/
├── skills/              # 技能目录
├── shared/              # 共享资源
│   ├── notes/           # 团队规范文档
│   ├── templates/       # 模板
│   ├── assets/          # 静态资源
│   └── data/            # 数据文件
├── knowledge/           # 知识库
└── memory/              # 日常记忆
```

### 识别杂乱文件

- **测试文件**: `test_*.py`, `*_test.py`, `__pycache__/`, `node_modules/`
- **临时文件**: `*.log`, `*.swp`, `*~`, `.DS_Store`, `*.tmp`
- **备份文件**: `*.bak`, `*.backup`, `*_old*`
- **空目录**: 检查 `shared/data/` 等空目录

### 常用命令

| 操作 | 命令 |
|------|------|
| 查看目录树 | `find /home/pixiu/.openclaw/workspace/ -maxdepth 2 -type d` |
| 查找大文件 | `find /home/pixiu/.openclaw/workspace/ -type f -size +5M` |
| 查找旧文件 | `find /home/pixiu/.openclaw/workspace/ -type f -mtime +30` |
| 统计文件数 | `find /home/pixiu/.openclaw/workspace/ -type f \| wc -l` |

---

## 二、飞书文档整理

### 整理内容

- 知识库文档归档
- 旧版本文档清理
- 无效链接检查
- 文档分类（需求/设计/开发/测试/部署）

### 整理规则

```
需求文档 → shared/notes/产品-xxx.md
设计文档 → shared/notes/设计-xxx.md
开发文档 → shared/notes/研发-xxx.md
测试文档 → shared/notes/测试-xxx.md
部署文档 → shared/notes/部署-xxx.md
```

---

## 三、团队协作整理

### experts/ 目录规范

每个小皮目录应包含：
```
{xiaopi}/
├── AGENTS.md      # 必须：角色定义
├── SOUL.md        # 必须：核心职责
├── USER.md        # 必须：用户信息
├── MEMORY.md      # 必须：日常记录
├── HEARTBEAT.md   # 推荐：心跳任务
└── workspace/     # 可选：工作文件
```

### 文件命名规范

- 使用中划线：`团队协作方案.md`
- 格式：`[类型]-[话题]-[名称].md`
- 避免：空格、特殊字符、中文拼音混合

---

## 四、MEMORY管理

### 每日必做

1. **开始工作**：读取 `memory/YYYY-MM-DD.md` 和昨日memory
2. **工作中**：重要事项即时记录
3. **结束工作**：更新当日memory

### MEMORY检查清单

- [ ] 今日任务完成情况
- [ ] 遇到的问题和解决方案
- [ ] 明日待办
- [ ] 学到的新技能/经验

### 过期文件清理

- `memory/` 下超过7天的日志可归档
- `MEMORY.md` 只保留精华，定期精简

---

## 五、自动化脚本

### scripts/cleanup_temp.sh

清理临时文件：
```bash
#!/bin/bash
# 清理临时文件
find /home/pixiu/.openclaw/workspace/ -type d -name "__pycache__" -exec rm -rf {} +
find /home/pixiu/.openclaw/workspace/ -type f -name "*.log" -delete
find /home/pixiu/.openclaw/workspace/ -type f -name ".DS_Store" -delete
echo "临时文件已清理"
```

### scripts/archive_old.sh

归档旧文件：
```bash
#!/bin/bash
# 归档30天前的文件
mkdir -p /home/pixiu/.openclaw/workspace/shared/archive
find /home/pixiu/.openclaw/workspace/ -type f -mtime +30 -exec mv {} /home/pixiu/.openclaw/workspace/shared/archive/ \;
echo "旧文件已归档"
```

### scripts/check_memory.sh

检查memory记录：
```bash
#!/bin/bash
# 检查各小皮memory记录情况
for dir in /home/pixiu/.openclaw/workspace/experts/*/; do
    name=$(basename $dir)
    mem_file="$dir/MEMORY.md"
    if [ -f "$mem_file" ]; then
        echo "✅ $name 有memory记录"
    else
        echo "❌ $name 缺少memory记录"
    fi
done
```

### scripts/check_empty_dirs.sh

检查空目录：
```bash
#!/bin/bash
# 查找并报告空目录
find /home/pixiu/.openclaw/workspace/ -type d -empty
```

---

## 六、文档分类模板

### 按类型分类

| 类型 | 扩展名 |
|------|--------|
| 图片 | .jpg, .jpeg, .png, .gif, .webp, .svg |
| 文档 | .md, .doc, .docx, .pdf, .txt, .xlsx |
| 代码 | .js, .ts, .py, .java, .go, .html, .css |
| 视频 | .mp4, .avi, .mov |
| 音频 | .mp3, .wav, .flac |
| 压缩 | .zip, .rar, .7z, .tar.gz |

---

## 七、执行流程

1. **扫描** - 查看目录结构 `find -maxdepth 2 -type d`
2. **分析** - 识别需要整理的文件类型
3. **备份** - 重要文件先备份
4. **清理** - 删除测试/临时文件
5. **归档** - 移动旧文件到archive
6. **报告** - 汇总整理结果

> ⚠️ **重要**：删除文件前先确认，使用 `trash` 而非 `rm` 以便恢复

---

## 触发场景

- 用户说"整理文件"、"清理目录"、"归档文件"
- 每日工作结束前的自动整理
- 团队汇报前的文档整理
- 审核小皮要求的定期检查

---

*v2.0 - 整合中英文版，增加飞书文档、团队协作、MEMORY管理功能*
