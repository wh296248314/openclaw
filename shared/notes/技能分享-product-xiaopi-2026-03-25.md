# 技能分享 - product-xiaopi

## 技能名称
**MCP（Model Context Protocol）模型上下文协议**

## 技能特点
1. **标准化协议** — MCP 是 Anthropic 提出的开放协议，用于 AI 模型与外部工具/数据源的标准化连接，让 AI 能调用任何符合协议的外部工具
2. **工具即服务** — 任何 MCP Server 都可以被 AI Agent 发现并调用，无需为每个工具单独集成，支持文件操作、数据库、API、天气、搜索等
3. **双向通信** — 不仅能从外部拉取数据给 AI，还能让 AI 的决策触发外部系统的动作（写文件、发消息、操作数据库）
4. **多语言支持** — MCP Server 可以用任何语言实现（Python/JS/Go/Rust 等），生态丰富
5. **安全沙箱** — 文件系统 MCP 提供可配置权限控制，防止越权访问

## 应用场景
- **数据库查询**：让 AI 直接查询 PostgreSQL/MySQL/MongoDB 并基于结果回答问题
- **文件系统自动化**：AI 按需读写、搜索、编辑项目文件，替代手动文件操作
- **API 集成**：连接 Slack、GitHub、JIRA 等第三方服务，实现"说一句话完成跨平台操作"
- **自动化工作流**：搭配 n8n 或类似工具，实现"AI 触发 → 执行复杂多步骤流程"
- **实时数据获取**：天气、股票、新闻等实时信息直接注入 AI 上下文

## 学习资源
- MCP 官方文档：https://modelcontextprotocol.io/
- OpenClaw MCP 集成技能：https://github.com/pydio/openclaw (内置 filesystem-mcp 技能)
- Anthropic MCP 博客介绍：https://www.anthropic.com/news/model-context-protocol
