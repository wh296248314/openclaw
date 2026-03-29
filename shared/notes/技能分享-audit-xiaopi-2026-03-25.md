# 技能分享 - audit-xiaopi

## 技能名称
MCP (Model Context Protocol) - 模型上下文协议

## 技能特点
1. **标准化协议**：MCP 是 Anthropic 提出的开放标准协议，用于连接 AI 模型与外部数据源和工具
2. **双向通信**：支持服务器向 AI 推送数据，也支持 AI 主动调用工具，实现了真正的交互式通信
3. **开箱即用**：已有众多开源 MCP 服务器（Filesystem、GitHub、Slack、PostgreSQL 等），可快速集成
4. **安全隔离**：每个 MCP 服务器运行在独立进程中，权限边界清晰，避免模型直接访问敏感系统
5. **多路复用**：单一 MCP 客户端可同时连接多个服务器，支持复杂的工具和数据组合

## 应用场景
1. **AI 代码助手**：让 AI 直接读写本地文件、运行 Shell 命令、操作 Git 仓库
2. **数据分析**：AI 连接数据库执行查询，返回结构化数据进行分析
3. **自动化工作流**：连接 Slack/邮件等通讯工具，实现 AI 驱动的通知和审批流程
4. **知识库问答**：对接向量数据库或 Wikipedia，让 AI 基于最新知识回答问题
5. **跨平台集成**：统一接口连接各种 SaaS 服务（GitHub、Notion、Figma 等）

## 学习资源
- 官方文档：https://modelcontextprotocol.io/
- MCP GitHub：https://github.com/modelcontextprotocol
- Claude MCP 集成指南：https://docs.anthropic.com/en/docs/claude-code/mcp
