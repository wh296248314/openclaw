# 配置文件说明

## 根目录配置文件
这些是OpenClaw Agent的核心配置文件，必须保持在根目录：

- `AGENTS.md` - Agent工作空间说明
- `SOUL.md` - Agent人格定义
- `USER.md` - 用户信息
- `TOOLS.md` - 工具配置
- `IDENTITY.md` - Agent身份
- `HEARTBEAT.md` - 心跳任务
- `DIRECTORY_STRUCTURE.md` - 目录结构说明

## 配置目录 (`configs/`)
分类存放的配置文件：

### `configs/openclaw/`
- OpenClaw系统配置（暂无）

### `configs/monitor/`
- `guardian_config.json` - 监控卫士配置
- `timeout_guardian_history.json` - 超时监控历史
- `timeout_guardian_optimized_config.json` - 优化配置
- `timeout_monitor_state.json` - 监控状态

### `configs/system/`
- `obsidian-sync-state.json` - Obsidian同步状态

## 数据目录 (`data/`)
- `data/guardian_tasks.json` - 监控卫士任务数据
- `data/monitor/simple_tasks.json` - 简单监控任务数据
- `data/system/` - 系统数据（空）

## 使用说明
1. 核心配置文件不要移动位置
2. 项目特定配置放在对应项目目录
3. 系统级配置放在configs目录相应子目录