# 技能分享 - deployment-xiaopi

## 技能名称
n8n 工作流自动化平台

## 技能特点
1. **开源可自托管**：支持 Docker、Kubernetes 一键部署，数据完全自主可控，适合企业级 AI 工作流
2. **可视化 + 代码双模式**：通过图形化界面快速构建工作流，同时也支持编写 JavaScript/TypeScript 自定义逻辑
3. **丰富的集成节点**：内置 400+ 节点，支持 PostgreSQL、Redis、HTTP、Webhook、Slack、飞书、钉钉、GitHub 等主流服务
4. **AI Agent 原生支持**：内置 LLM Chain、Tools Agent、Chunking 等 AI 相关节点，可直接连接 OpenAI、Claude 等大模型
5. **错误处理与重试机制**：内置 Retry 策略、Error Trigger、Error Workflow，确保自动化流程的健壮性
6. **可版本化管理**：支持 Git 存储工作流 JSON，天然适配 CI/CD 流程

## 应用场景
- **AI Agent 工具链编排**：将大模型与外部工具（搜索、数据库、API）串联成完整 Agent 流水线
- **跨系统数据同步**：定时从数据库拉取数据，经 LLM 处理后写入另一个系统
- **飞书/钉钉 Bot 自动化**：接收消息 → 触发工作流 → 调用 AI 分析 → 自动回复
- **定时任务与监控**：Cron 式触发 + 条件分支，实现复杂的定时业务流程
- **RAG 数据管道**：文档上传 → Chunking → 向量化 → 存入向量数据库，全自动完成
- **CI/CD 流程的一部分**：工作流 JSON 化后通过 Git 管理，提交代码即触发部署

## 学习资源
- 官方文档：https://docs.n8n.io
- GitHub：https://github.com/n8n-io/n8n
- n8n 中文社区：https://github.com/nicehorse06/n8n-cn
- 官方模板库：https://n8n.io/workflows
- 部署指南（Docker/K8s）：https://docs.n8n.io/hosting/installation/
