# 技能分享 - testing-xiaopi

## 技能名称
Agentic Coding（代理化编程）

## 技能特点
1. **验收合约驱动**：通过"验收合同"（Acceptance Contracts）定义任务完成标准，AI 在提交前必须通过所有验收条件，而非仅追求代码能跑。
2. **Micro Diffs（微差分）**：将大任务拆解为极小的代码变更，每次只做一个有意义的改动，便于人工 review 和回滚，降低 AI 生成代码的试错成本。
3. **红绿循环（Red-Green Loop）**：遵循 TDD 思想——先写失败测试（Red），再写最小实现（Green），最后重构（Refactor）。AI 编程也遵循此节奏，确保每一步都有可验证的输出。
4. **确定性交接点（Deterministic Handoff）**：任务在明确定义的检查点交接，每个阶段的结果以结构化文件形式固化，下一阶段 AI 从文件读取上下文，而非依赖记忆或对话历史。
5. **人工审查嵌入**：在关键节点（代码生成后、上线前）自动暂停，等待人工确认，而非全程 autonomous 跑到底。

## 应用场景
- 复杂功能开发（多步骤、需要多次迭代的 feature）
- AI Coding 工具集成（Cursor、Claude Code、Copilot 等）
- 高可靠性要求的代码提交（Code Review 前置检查）
- 团队协作场景（多人使用 AI 辅助开发时的质量门禁）

## 学习资源
- Anthropic: "Agentic Coding Practices" — https://docs.anthropic.com/
- Martin Fowler: "Micro Commit" 理念 — https://martinfowler.com/articles/micro-commit.html
- Red-Green-Refactor (Cucumber/Beck TDD) — https://martinfowler.com/bliki/TestDrivenDevelopment.html
