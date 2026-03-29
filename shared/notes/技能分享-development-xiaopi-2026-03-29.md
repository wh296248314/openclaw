# 技能分享 - development-xiaopi

## 技能名称
MCP (Model Context Protocol) — 模型上下文协议

## 技能特点

1. **标准化工具调用接口**：MCP 为 AI 助手提供了一种统一的方式来发现和调用外部工具和服务，无需为每个数据源单独定制集成。AI 可以像使用本地工具一样无缝调用远程 API、数据库、文件系统等资源。

2. **双向通信架构**：采用客户端-服务器模式，支持从简单的请求-响应到流式响应和长时间运行的任务。MCP 服务器可以托管在本地（stdio 模式）或远程（HTTP/SSE 模式），灵活适配不同部署场景。

3. **安全沙箱机制**：通过明确的权限范围（scopes）控制工具访问能力，每个工具调用前都需要明确的授权，防止 AI 越权操作。工具定义包含输入输出 schema，实现类型安全的交互。

4. **多工具聚合能力**：一个 MCP 客户端可以同时连接多个 MCP 服务器，AI 可以在一次对话中综合调用来自不同来源的工具（如同时查询数据库 + 调用 GitHub API + 搜索网络）。

5. **热插拔扩展**：无需修改 AI 模型的提示词，通过配置文件即可动态加载新的工具和能力，支持工具的版本管理和按需启用/禁用。

## 应用场景

- **数据库操作**：让 AI 直接读写 PostgreSQL、MySQL、MongoDB 等数据库，执行 SQL 查询、聚合分析、生成报表
- **API 集成**：连接 Slack、GitHub、Jira、Figma 等第三方服务，实现自动化工作流（如自动创建 Issue、自动发送通知）
- **文件系统增强**：在安全管控下提供特定目录的读写能力，适用于代码生成后自动写入、配置文件管理等场景
- **企业内部知识库**：连接向量数据库或文档服务，让 AI 基于真实业务数据回答问题
- **多工具编排**：在一个复杂任务中协调多个工具，如"查库存 → 计算补货量 → 生成采购单 → 发消息通知负责人"

## 学习资源

- 官方文档：https://modelcontextprotocol.io/
- MCP SDK（TypeScript）：https://github.com/modelcontextprotocol/typescript-sdk
- MCP Python SDK：https://github.com/modelcontextprotocol/python-sdk
- OpenClaw MCP 集成技能：https://docs.openclaw.com/plugins/mcp
