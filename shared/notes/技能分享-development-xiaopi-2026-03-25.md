# 技能分享 - development-xiaopi

## 技能名称
MCP (Model Context Protocol) — 模型上下文协议

## 技能特点

1. **开放标准，厂商无关**
   MCP 是由 Anthropic 提出的开放协议，任何 AI 厂商都可以实现，不绑定特定模型供应商。

2. **双向工具调用与数据访问**
   AI 模型不仅可以调用工具（tools），还可以从外部数据源读取上下文（resources），同时通过 prompts 模板实现复杂工作流。

3. **标准化握手与发现机制**
   客户端通过标准化的 `initialize` 握手获取服务端能力清单（capabilities），包括支持哪些工具、资源和 prompts，无需硬编码适配。

4. **安全沙箱隔离**
   MCP 原生支持权限 scope（如只读 vs 读写），避免 AI 随意执行高危操作。

5. **生态快速扩张**
   已有 20+ 主流供应商（GitHub、Slack、Google、Azure 等）提供官方 MCP Server，覆盖代码、数据库、通讯、云服务等场景。

## 应用场景

- **代码助手**：通过 MCP 访问 GitHub Repo、GitLab Issues，实现"读代码+提PR+更新状态"一条龙自动化。
- **数据分析**：AI 直接查询 PostgreSQL、MySQL，返回结构化结果再进行 LLM 分析。
- **客服/办公自动化**：MCP Server 对接 Slack/飞书，AI 自动完成消息收发、任务创建。
- **个人助手**：本地文件、浏览器书签、日历均可通过 MCP 暴露给 AI，成为真正的"第二大脑"。
- **OpenClaw 扩展**：OpenClaw 的 `mcporter` 技能正是 MCP 集成的一种实现方式，可灵活接入任意支持 MCP 的外部服务。

## 学习资源

- 官方规范：https://modelcontextprotocol.io
- Anthropic 博客介绍：https://www.anthropic.com/news/model-context-protocol
- GitHub 官方 SDK（Python/TypeScript）：https://github.com/modelcontextprotocol
- MCP Server 精选列表：https://github.com/modelcontextprotocol/servers
