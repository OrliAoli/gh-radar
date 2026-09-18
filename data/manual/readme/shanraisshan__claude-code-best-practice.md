> 徽章、图片链接、人名和 X 用户名保持原样未翻（人名和账号名翻了就找不到了）。

# claude-code-best-practice

从「氛围编程」到「Agent 工程」——练到位，Claude 才好用

![updated with Claude Code](https://img.shields.io/badge/updated_with_Claude_Code-Sep%2018%2C%202026%209%3A46%20AM%20PKT-white?style=flat&labelColor=555) <a href="https://github.com/shanraisshan/claude-code-best-practice/stargazers"><img src="https://img.shields.io/github/stars/shanraisshan/claude-code-best-practice?style=flat&label=%E2%98%85&labelColor=555&color=white" alt="GitHub Stars"></a><br>

[![Best Practice](!/tags/best-practice.svg)](best-practice/) [![Implemented](!/tags/implemented.svg)](implementation/) [![Orchestration Workflow](!/tags/orchestration-workflow.svg)](orchestration-workflow/orchestration-workflow.md) [![Claude](!/tags/claude.svg)](https://code.claude.com/docs) [![Boris](!/tags/boris-cherny.svg)](#-tips-and-tricks) [![Community](!/tags/community.svg)](#-subscribe) ![点下面这些徽章可以看原始出处](!/tags/click-badges.svg)<br>
<img src="!/tags/a.svg" height="14"> = 子 Agent　·　<img src="!/tags/c.svg" height="14"> = 命令　·　<img src="!/tags/s.svg" height="14"> = 技能

<p align="center">
  <img src="!/claude-jumping.svg" alt="Claude Code 吉祥物在跳" width="120" height="100"><br>
  <a href="https://github.com/trending"><img src="!/root/github-trending-day.svg" alt="GitHub 今日趋势榜第 1 名"></a>
</p>

<p align="center">
  <img src="!/root/supported-label.svg" alt="由以下方支持：" height="34">&nbsp;&nbsp;<a href="https://disrupt.com/?utm_source=github&utm_campaign=shayan_claude_code_best_practice"><img src="!/root/supported-disrupt.svg" alt="Disrupt.com —— 重新想象风险投资" height="34"></a>&nbsp;&nbsp;<a href="https://claudekit.cc/?utm_source=github&utm_medium=sponsorship&utm_campaign=shayan_claude_code_best_practice"><img src="!/root/supported-claudekit.svg" alt="ClaudeKit —— 生产可用的技能与工作流" height="34"></a>
</p>

<p align="center">
  <img src="!/root/boris-slider.gif" alt="Boris Cherny 谈 Claude Code" width="600"><br>
  Boris Cherny 在 X 上的发言（<a href="https://x.com/bcherny/status/2007179832300581177">推文 1</a> · <a href="https://x.com/bcherny/status/2017742741636321619">推文 2</a> · <a href="https://x.com/bcherny/status/2021699851499798911">推文 3</a>）
</p>

> [!TIP]
> 先去看 [**怎么用**](#how-to-use) 那一节，才能把这个仓库的价值吃透。

## 🧠 核心概念

| 功能 | 文件位置 | 说明 |
|---------|----------|-------------|
| <img src="!/tags/a.svg" height="14"> [**子 Agent（Subagents）**](https://code.claude.com/docs/en/sub-agents) | `.claude/agents/<名字>.md` | [![最佳实践](!/tags/best-practice.svg)](best-practice/claude-subagents.md) [![已实现](!/tags/implemented.svg)](implementation/claude-subagents-implementation.md) |
| <img src="!/tags/c.svg" height="14"> [**命令（Commands）**](https://code.claude.com/docs/en/commands) | `.claude/commands/<名字>.md` | [![最佳实践](!/tags/best-practice.svg)](best-practice/claude-commands.md) [![已实现](!/tags/implemented.svg)](implementation/claude-commands-implementation.md) |
| <img src="!/tags/s.svg" height="14"> [**技能（Skills）**](https://code.claude.com/docs/en/skills) | `.claude/skills/<名字>/SKILL.md` | [![最佳实践](!/tags/best-practice.svg)](best-practice/claude-skills.md) [![已实现](!/tags/implemented.svg)](implementation/claude-skills-implementation.md) [官方技能库](https://github.com/anthropics/skills/tree/main/skills) · [大仓用的技能](reports/claude-skills-for-larger-mono-repos.md) |
| [**工作流（Workflows）**](https://code.claude.com/docs/en/common-workflows) | [`.claude/commands/weather-orchestrator.md`](.claude/commands/weather-orchestrator.md) | [![编排工作流](!/tags/orchestration-workflow.svg)](orchestration-workflow/orchestration-workflow.md) |
| [**钩子（Hooks）**](https://code.claude.com/docs/en/hooks) | `.claude/hooks/` | [![最佳实践](!/tags/best-practice.svg)](https://github.com/shanraisshan/claude-code-hooks) [![已实现](!/tags/implemented.svg)](https://github.com/shanraisshan/claude-code-hooks) [指南](https://code.claude.com/docs/en/hooks-guide) |
| [**MCP 服务（MCP Servers）**](https://code.claude.com/docs/en/mcp) | `.claude/settings.json`、`.mcp.json` | [![最佳实践](!/tags/best-practice.svg)](best-practice/claude-mcp.md) [![已实现](!/tags/implemented.svg)](.mcp.json) |
| [**插件（Plugins）**](https://code.claude.com/docs/en/plugins) | 可分发包 | [插件市场](https://code.claude.com/docs/en/discover-plugins) · [自建市场](https://code.claude.com/docs/en/plugin-marketplaces) |
| [**设置（Settings）**](https://code.claude.com/docs/en/settings) | `.claude/settings.json` | [![最佳实践](!/tags/best-practice.svg)](best-practice/claude-settings.md) [![已实现](!/tags/implemented.svg)](.claude/settings.json) [权限](https://code.claude.com/docs/en/permissions) · [模型配置](https://code.claude.com/docs/en/model-config) · [输出风格](https://code.claude.com/docs/en/output-styles) · [沙箱](https://code.claude.com/docs/en/sandboxing) · [快捷键](https://code.claude.com/docs/en/keybindings) · [自动模式配置](https://code.claude.com/docs/en/auto-mode-config) |
| [**状态栏（Status Line）**](https://code.claude.com/docs/en/statusline) | `.claude/settings.json` | [![最佳实践](!/tags/best-practice.svg)](https://github.com/shanraisshan/claude-code-status-line) [![已实现](!/tags/implemented.svg)](.claude/settings.json) |
| [**记忆（Memory）**](https://code.claude.com/docs/en/memory) | `CLAUDE.md`、`.claude/rules/`、`~/.claude/rules/`、`~/.claude/projects/<项目>/memory/` | [![最佳实践](!/tags/best-practice.svg)](best-practice/claude-memory.md) [![已实现](!/tags/implemented.svg)](CLAUDE.md) [自动记忆](https://code.claude.com/docs/en/memory) · [自动记忆深度解析](reports/claude-agent-memory.md) · [规则](https://code.claude.com/docs/en/memory#organize-rules-with-claude/rules/) |
| [**检查点（Checkpointing）**](https://code.claude.com/docs/en/checkpointing) | 自动（跟踪文件改动） |  |
| [**会话（Sessions）**](https://code.claude.com/docs/en/sessions) | `--resume`、`--continue`、`/resume`、`/branch` |  |
| [**上下文窗口（Context Window）**](https://code.claude.com/docs/en/context-window) | `/compact`、`/clear`、`/context` |  |
| [**命令行启动参数（CLI Startup Flags）**](https://code.claude.com/docs/en/cli-reference) | `claude [参数]` | [![最佳实践](!/tags/best-practice.svg)](best-practice/claude-cli-startup-flags.md) [交互模式](https://code.claude.com/docs/en/interactive-mode) · [环境变量](https://code.claude.com/docs/en/env-vars) |
| **AI 术语** | | [![最佳实践](!/tags/best-practice.svg)](https://github.com/shanraisshan/claude-code-codex-cursor-gemini/blob/main/reports/ai-terms.md) |
| [**最佳实践（Best Practices）**](https://code.claude.com/docs/en/best-practices) | | [提示词工程](https://github.com/anthropics/prompt-eng-interactive-tutorial) · [扩展 Claude Code](https://code.claude.com/docs/en/features-overview) |
| [**提示词库（Prompt Library）**](https://code.claude.com/docs/en/prompt-library) | |  |

### 🔥 热门新功能

| 功能 | 位置 | 说明 |
|---------|----------|-------------|
| [**Ultrareview**](https://code.claude.com/docs/en/ultrareview) ![beta](!/tags/beta.svg) | `/code-review ultra`、`claude ultrareview [目标]` | [任务跟踪](https://code.claude.com/docs/en/ultrareview#track-a-running-review) |
| [**开发容器（Devcontainers）**](https://code.claude.com/docs/en/devcontainer) | `.devcontainer/` |  |
| [**频道（Channels）**](https://code.claude.com/docs/en/channels) ![beta](!/tags/beta.svg) | `--channels`，基于插件 | [参考文档](https://code.claude.com/docs/en/channels-reference) |
| [**去闪烁模式（No Flicker Mode）**](https://code.claude.com/docs/en/fullscreen) ![beta](!/tags/beta.svg) | `/tui fullscreen`、`CLAUDE_CODE_NO_FLICKER=1` | [![最佳实践](!/tags/best-practice.svg)](https://x.com/bcherny/status/2039421575422980329) |
| [**自动模式（Auto Mode）**](https://code.claude.com/docs/en/permission-modes#eliminate-prompts-with-auto-mode) | `--permission-mode auto`、`Shift+Tab` | [![最佳实践](!/tags/best-practice.svg)](https://x.com/claudeai/status/2036503582166393240) [博客](https://claude.com/blog/auto-mode) |
| [**增强包（Power-ups）**](best-practice/claude-power-ups.md) | `/powerup` | [![最佳实践](!/tags/best-practice.svg)](best-practice/claude-power-ups.md) |
| [**快速模式（Fast Mode）**](https://code.claude.com/docs/en/fast-mode) ![beta](!/tags/beta.svg) | `/fast`、`"fastMode": true` |  |
| [**顾问（Advisor）**](https://code.claude.com/docs/en/advisor) ![beta](!/tags/beta.svg) | `/advisor`、`advisorModel`、`--advisor` | [博客](https://claude.com/blog/the-advisor-strategy) |
| [**电脑操作（Computer Use）**](https://code.claude.com/docs/en/computer-use) ![beta](!/tags/beta.svg) | `computer-use` 这个 MCP 服务 | [桌面版](https://code.claude.com/docs/en/desktop#let-claude-use-your-computer) |
| [**Agent SDK**](https://code.claude.com/docs/en/agent-sdk/overview) | `npm` / `pip` 包 | [快速上手](https://code.claude.com/docs/en/agent-sdk/quickstart) · [示例](https://github.com/anthropics/claude-agent-sdk-demos) |
| [**Ralph Wiggum 循环**](https://github.com/anthropics/claude-code/tree/main/plugins/ralph-wiggum) | 插件 | [![最佳实践](!/tags/best-practice.svg)](https://github.com/ghuntley/how-to-ralph-wiggum) [![已实现](!/tags/implemented.svg)](https://github.com/shanraisshan/ralph-wiggum-self-evolving-loop) |
| [**Chrome 集成**](https://code.claude.com/docs/en/chrome) | `--chrome`、浏览器扩展 | [![最佳实践](!/tags/best-practice.svg)](reports/claude-in-chrome-v-chrome-devtools-mcp.md) |
| [**Claude Code 网页版**](https://code.claude.com/docs/en/claude-code-on-the-web) ![beta](!/tags/beta.svg) | `claude.ai/code` | [例行任务](https://code.claude.com/docs/en/routines) |
| [**产物（Artifacts）**](https://code.claude.com/docs/en/artifacts) | `/share`、`Artifact` 工具 |  |
| [**Slack 集成**](https://code.claude.com/docs/en/slack) | 在 Slack 里 `@Claude` |  |
| [**代码评审（Code Review）**](https://code.claude.com/docs/en/code-review) ![beta](!/tags/beta.svg) | GitHub App（托管式） | [![最佳实践](!/tags/best-practice.svg)](https://x.com/claudeai/status/2031088171262554195) [博客](https://claude.com/blog/code-review) [本地 /code-review](https://code.claude.com/docs/en/commands) |
| [**GitHub Actions**](https://code.claude.com/docs/en/github-actions) | `.github/workflows/` | [GitLab CI/CD](https://code.claude.com/docs/en/gitlab-ci-cd) |
| [**远程控制（Remote Control）**](https://code.claude.com/docs/en/remote-control) | `/remote-control`、`/rc` | [![最佳实践](!/tags/best-practice.svg)](https://x.com/noahzweben/status/2032533699116355819) [无头模式](https://code.claude.com/docs/en/headless) |
| [**深链（Deep Links）**](https://code.claude.com/docs/en/deep-links) | `claude-cli://open?repo=…&q=…` |  |
| [**动态工作流（Dynamic Workflows）**](https://code.claude.com/docs/en/workflows) | `/workflows`、`ultracode` 关键词、`/effort ultracode`、`.claude/workflows/` | [深度研究](https://code.claude.com/docs/en/workflows#run-a-bundled-workflow) |
| [**Agent 团队（Agent Teams）**](https://code.claude.com/docs/en/agent-teams) ![beta](!/tags/beta.svg) | 内置（靠环境变量开关） | [![最佳实践](!/tags/best-practice.svg)](https://x.com/bcherny/status/2019472394696683904) [![已实现](!/tags/implemented.svg)](implementation/claude-agent-teams-implementation.md) |
| [**Agent 视图（Agent View）**](https://code.claude.com/docs/en/agent-view) ![beta](!/tags/beta.svg) | `claude agents`、`--bg`、`/bg` |  |
| [**跨会话通信（Cross-Session Messaging）**](https://code.claude.com/docs/en/cross-session-messaging) | `SendMessage`、`ListAgents`、`/list-agents` |  |
| [**定时任务（Scheduled Tasks）**](https://code.claude.com/docs/en/scheduled-tasks) | `/loop`、`/schedule`、cron 工具 | [![最佳实践](!/tags/best-practice.svg)](https://x.com/bcherny/status/2030193932404150413) [![已实现](!/tags/implemented.svg)](implementation/claude-scheduled-tasks-implementation.md) [桌面版定时任务](https://code.claude.com/docs/en/desktop-scheduled-tasks) · [发布公告](https://x.com/noahzweben/status/2036129220959805859) |
| [**例行任务（Routines）**](https://code.claude.com/docs/en/routines) ![beta](!/tags/beta.svg) | `claude.ai/code/routines`、`/schedule` | [桌面版任务](https://code.claude.com/docs/en/desktop-scheduled-tasks) |
| [**任务（Tasks）**](reports/claude-global-vs-project-settings.md#tasks-system) | `/tasks`、`~/.claude/tasks/` | [![最佳实践](!/tags/best-practice.svg)](reports/claude-global-vs-project-settings.md) [Ultrareview 跟踪](https://code.claude.com/docs/en/ultrareview#track-a-running-review) |
| [**目标（Goal）**](https://code.claude.com/docs/en/goal) | `/goal <条件>`、`/goal clear` | [![已实现](!/tags/implemented.svg)](implementation/claude-goal-implementation.md) |
| [**语音输入（Voice Dictation）**](https://code.claude.com/docs/en/voice-dictation) | `/voice` | [![最佳实践](!/tags/best-practice.svg)](https://x.com/trq212/status/2028628570692890800) |
| [**内置技能（Bundled Skills）**](https://code.claude.com/docs/en/skills#bundled-skills) | `/code-review`、`/batch` | [![最佳实践](!/tags/best-practice.svg)](https://x.com/bcherny/status/2027534984534544489) |
| [**Git 工作树（Git Worktrees）**](https://code.claude.com/docs/en/worktrees) | `--worktree`/`-w`、`.worktreeinclude`、`EnterWorktree`/`ExitWorktree`、`isolation: "worktree"`、`WorktreeCreate`/`WorktreeRemove` 钩子 | [![最佳实践](!/tags/best-practice.svg)](https://x.com/bcherny/status/2025007393290272904) |

<p align="center">
  <img src="!/claude-jumping.svg" alt="章节分隔" width="60" height="50">
</p>

<a id="orchestration-workflow"></a>

## <a href="orchestration-workflow/orchestration-workflow.md"><img src="!/tags/orchestration-workflow-hd.svg" alt="编排工作流"></a>

<img src="!/tags/c.svg" height="14"> **命令** → <img src="!/tags/a.svg" height="14"> **Agent** → <img src="!/tags/s.svg" height="14"> **技能** 这套模式的实现细节，见 [orchestration-workflow](orchestration-workflow/orchestration-workflow.md)。

<p align="center">
  <img src="orchestration-workflow/orchestration-workflow.svg" alt="命令-技能-Agent 架构流程" width="100%">
</p>

<p align="center">
  <img src="orchestration-workflow/orchestration-workflow.gif" alt="编排工作流演示" width="600">
</p>

![怎么用](!/tags/how-to-use.svg)

```bash
claude
/weather-orchestrator
```

<p align="center">
  <img src="!/claude-jumping.svg" alt="章节分隔" width="60" height="50">
</p>

## ⚙️ 开发工作流

所有主流工作流最后都收敛到同一套架构模式：**调研 → 计划 → 执行 → 评审 → 上线**

| 名称 | ★ | 工作流 | <img src="!/tags/a.svg" height="14"> | <img src="!/tags/c.svg" height="14"> | <img src="!/tags/s.svg" height="14"> |
|------|---|----------|---|---|---|
| [Superpowers](https://github.com/obra/superpowers) | 288k | 头脑风暴 → 用 git worktrees → 写计划 → 子 Agent 驱动开发 → 测试驱动开发 → 请求代码评审 → 收尾开发分支 | 0 | 0 | 14 |
| [Matt Pocock Skills](https://github.com/mattpocock/skills) | 265k | 拷问文档 → 转成规格 → 转成工单 → 实现 → TDD → 代码评审 → 改进代码库架构 | 0 | 0 | 37 |
| [Everything Claude Code](https://github.com/affaan-m/ECC) | 260k | 计划 → TDD 工作流 → 实现 → 代码评审 → 修构建 → 安全扫描 → 端到端测试 → 测试覆盖率 → 保存会话 | 68 | 94 | 286 |
| [Spec Kit](https://github.com/github/spec-kit) | 138k | 宪章 → 明确需求 → 计划 → 拆任务 → 实现 → 收敛 | 0 | 10 | 0 |
| [gstack](https://github.com/garrytan/gstack) | 133k | 办公时间 → CEO 评审 → 工程评审 → 设计评审 → 设计撒网 → 设计 HTML → 评审 → QA → 上线 → 复盘 | 0 | 0 | 53 |
| [agent-skills](https://github.com/addyosmani/agent-skills) | 89k | 规格 → 计划 → 构建 → 测试 → 评审 → 上线 | 3 | 7 | 21 |
| [OpenSpec](https://github.com/Fission-AI/OpenSpec) | 69k | 上手 → 探索 → 提议 → 快进 → 应用 → 验证 → 同步 → 归档 | 0 | 12 | 7 |
| [Get Shit Done](https://github.com/gsd-build/get-shit-done) | 64.6k | 新项目 → 探索 → 规格阶段 → 计划阶段 → 执行阶段 → 评审 → 验证阶段 → 上线 | 33 | 85 | 0 |
| [BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD) | 53k | 锻造想法 → 产品简报 → PRD → 规格 → 构建 → 代码评审 → 走查 → 复盘 | 0 | 0 | 35 |
| [oh-my-claudecode](https://github.com/Yeachan-Heo/oh-my-claudecode) | 39.2k | 深度访谈 → ralplan → 团队计划 → 团队 PRD → 团队执行 → 团队验证 → 团队修复 | 19 | 0 | 39 |
| [Compound Engineering](https://github.com/EveryInc/compound-engineering-plugin) | 25.1k | 头脑风暴 → 计划 → 干活 → 简化代码 → 代码评审 → 沉淀 | 0 | 1 | 36 |
| [HumanLayer](https://github.com/humanlayer/humanlayer) | 11.6k | 调研代码库 → 创建计划 → 校验计划 → 实现计划 → 迭代计划 → 提交 → 写 PR 描述 → 本地评审 | 6 | 27 | 0 |

> *注：黄色标签表示「子循环」——在某个父步骤内部反复执行的步骤（比如每个任务跑一遍、每个 story 跑一遍，或者一直跑到验证条件通过为止）。*

### 其他

- [RPI](development-workflows/rpi/rpi-workflow.md) [![已实现](!/tags/implemented.svg)](development-workflows/rpi/rpi-workflow.md)
- [Ralph Wiggum 循环](https://www.youtube.com/watch?v=eAtvoGlpeRU) [![已实现](!/tags/implemented.svg)](https://github.com/shanraisshan/ralph-wiggum-self-evolving-loop)
- [Andrej Karpathy（OpenAI 创始成员）的工作流](https://x.com/karpathy/status/2015883857489522876)
- [Peter Steinberger（OpenClaw 作者）的工作流](https://youtu.be/8lF7HmQ_RgY?t=2582)
- Boris Cherny（Claude Code 作者）的工作流 —— [13 条](tips/claude-boris-13-tips-03-jan-26.md) · [10 条](tips/claude-boris-10-tips-01-feb-26.md) · [12 条](tips/claude-boris-12-tips-12-feb-26.md) · [2 条](tips/claude-boris-2-tips-25-mar-26.md) · [15 条](tips/claude-boris-15-tips-30-mar-26.md) · [6 条](tips/claude-boris-6-tips-16-apr-26.md) [![Boris](!/tags/boris-cherny.svg)](https://x.com/bcherny)
- Thariq（Anthropic）的工作流 —— [技能篇](tips/claude-thariq-tips-17-mar-26.md) · [会话管理篇](tips/claude-thariq-tips-16-apr-26.md) [![Thariq](!/tags/thariq.svg)](https://x.com/trq212)

<p align="center">
  <img src="!/claude-jumping.svg" alt="章节分隔" width="60" height="50">
</p>

## 🔀 跨模型工作流

把 Claude Code 跟别的模型一起用 —— Codex、Gemini、GPT、Kimi、DeepSeek、本地模型 —— 有三种接法：

- **插件** —— 另一个模型的命令行跑在 Claude Code 里面（斜杠命令如 `/codex:review`）
- **MCP** —— Claude Code 通过模型上下文协议把另一个模型当工具调用
- **路由** —— 把 Claude Code 的 API 端点换成另一个供应商

方法论见：[跨模型（Claude Code + Codex）工作流](development-workflows/cross-model-workflow/cross-model-workflow.md) [![已实现](!/tags/implemented.svg)](development-workflows/cross-model-workflow/cross-model-workflow.md) —— 手动开两个终端：在 Claude 里做计划，在 Codex 里做 QA 评审。

| 名称 | ★ | 类型 | 对接到 | 干什么 |
|------|---|------|------------|--------------|
| [musistudio/claude-code-router](https://github.com/musistudio/claude-code-router) | 34k | 路由 | OpenRouter、DeepSeek、Ollama、Gemini、Kimi、Qwen、Groq 等 | 把 Claude Code 的 API 转接到任意兼容供应商，还能按任务选模型 |
| [router-for-me/CLIProxyAPI](https://github.com/router-for-me/CLIProxyAPI) | 32k | 路由 | Gemini CLI、Codex、Claude Code、Antigravity | 把各个 CLI 包装成 OpenAI/Gemini/Claude/Codex 兼容的 API 服务 |
| [openai/codex-plugin-cc](https://github.com/openai/codex-plugin-cc) | 18k | 插件 | Codex / GPT-5 | OpenAI 官方插件：在 Claude Code 里用 `/codex:review`、`/codex:adversarial-review`、`/codex:rescue` |
| [BeehiveInnovations/pal-mcp-server](https://github.com/BeehiveInnovations/pal-mcp-server) | 12k | MCP | Gemini、OpenAI、Azure、Grok、Ollama、OpenRouter（50+ 模型） | 多模型 MCP 服务（前身叫 `zen-mcp-server`）——把别的模型当成 Claude 的工具来调 |

<p align="center">
  <img src="!/claude-jumping.svg" alt="章节分隔" width="60" height="50">
</p>

## 🧰 技能合集

下面这些仓库主要是精心整理的 `SKILL.md` 文件库（跟上面完整的流程方法论不同）。按星数从高到低排。

| 名称 | ★ | <img src="!/tags/s.svg" height="14"> |
|------|---|---|
| [mattpocock/skills](https://github.com/mattpocock/skills) | 264k | 37 |
| [anthropics/skills](https://github.com/anthropics/skills) | 177k | 19 |
| [Egonex-AI/Understand-Anything](https://github.com/Egonex-AI/Understand-Anything) | 67k | 8 |
| [scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills) | 45k | 166 |
| [wshobson/agents](https://github.com/wshobson/agents) | 40k | 171 |
| [awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills) | 34k | 1,497+（清单） |
| [impeccable](https://github.com/pbakaus/impeccable) | 27k | 1（附带 7 个设计领域参考） |
| [agent-skills](https://github.com/addyosmani/agent-skills) | 27k | 21 |
| [claude-skills](https://github.com/alirezarezvani/claude-skills) | 15k | 246（跨 9 个领域） |
| [shanraisshan/draw-json-architecture-skill](https://github.com/shanraisshan/draw-json-architecture-skill) | 3 | 1 |

<p align="center">
  <img src="!/claude-jumping.svg" alt="章节分隔" width="60" height="50">
</p>

## 🤖 Agent 合集

下面这些仓库主要是精心整理的子 Agent 定义库（`.claude/agents/*.md`）。按星数从高到低排。

| 名称 | ★ | <img src="!/tags/a.svg" height="14"> |
|------|---|---|
| [msitarzewski/agency-agents](https://github.com/msitarzewski/agency-agents) | 153k | 279 |
| [VoltAgent/awesome-claude-code-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents) | 25k | 158 |

<p align="center">
  <img src="!/claude-jumping.svg" alt="章节分隔" width="60" height="50">
</p>

## 💡 技巧与窍门（83 条）

🚫👶 = 不用盯着它干活

[提示词](#tips-prompting) · [计划](#tips-planning) · [上下文](#tips-context) · [会话](#tips-session) · [CLAUDE.md + .claude/rules](#tips-claudemd) · [Agent](#tips-agents) · [命令](#tips-commands) · [技能](#tips-skills) · [钩子](#tips-hooks) · [工作流](#tips-workflows) · [进阶](#tips-workflows-advanced) · [Git / PR](#tips-git-pr) · [调试](#tips-debugging) · [小工具](#tips-utilities) · [日常](#tips-daily)

![社区](!/tags/community.svg)

<a id="tips-prompting"></a>■ **提示词（3 条）**

| 技巧 | 出处 |
|-----|--------|
| 给 Claude 出难题 —— 「就这些改动拷问我，我没通过你的测试之前不许提 PR」，或者「证明给我看这真的能跑」，然后让 Claude 去 diff 主分支和你的分支 🚫👶 | [![Boris](!/tags/boris-cherny.svg)](https://x.com/bcherny/status/2017742752566632544) |
| 改得不满意时说 —— 「现在你知道了全部情况，把这套推翻，重新实现那个优雅的解法」🚫👶 | [![Boris](!/tags/boris-cherny.svg)](https://x.com/bcherny/status/2017742752566632544) |
| 大部分 bug Claude 自己就能修 —— 把报错粘进去说「修一下」，别管它怎么修 🚫👶 | [![Boris](!/tags/boris-cherny.svg)](https://x.com/bcherny/status/2017742750473720121) |

<a id="tips-planning"></a>■ **计划 / 规格（7 条）**

| 技巧 | 出处 |
|-----|--------|
| 永远先开 [计划模式](https://code.claude.com/docs/en/common-workflows) | [![Boris](!/tags/boris-cherny.svg)](https://x.com/bcherny/status/2007179845336527000) |
| 先写一份极简的规格或提示词，让 Claude 用 [AskUserQuestion](https://code.claude.com/docs/en/cli-reference) 工具来采访你，然后**另开一个会话**去执行这份规格 | [![Thariq](!/tags/thariq.svg)](https://x.com/trq212/status/2005315275026260309) |
| 一定要做「分阶段 + 带关卡」的计划，每个阶段都配多组测试（单元、自动化、集成） | [![Dex](!/tags/community-dex.svg)](videos/claude-dex-mlops-community-24-mar-26.md) [![视频](!/tags/video.svg)](https://youtu.be/YwZR6tc7qYg?t=1032) |
| 把 PRD 拆成贯穿所有层的「纵向切片」（曳光弹）——数据库 + 服务 + UI 一起做。AI 默认会按横向分层（先数据库阶段，再 API 阶段，再前端阶段），那样端到端的反馈要拖到最后一阶段才拿得到。出自《程序员修炼之道》 🚫👶 | [![Matt](!/tags/community-matt.svg)](videos/claude-matt-pocock-24-apr-26.md) [![视频](!/tags/video.svg)](https://youtu.be/-QFHIoCo-Ko) |
| 再开一个 Claude，让它以资深工程师的身份评审你的计划；或者用[跨模型](#-cross-model-workflows)来做评审 | [![Boris](!/tags/boris-cherny.svg)](https://x.com/bcherny/status/2017742745365057733) |
| 写详细的规格、把歧义降到最低再交出去 —— 你说得越具体，产出越好 | [![Boris](!/tags/boris-cherny.svg)](https://x.com/bcherny/status/2017742752566632544) |
| 做原型 > 写 PRD —— 直接做 20~30 个版本，而不是写规格。现在造东西的成本很低，多打几枪 | [![Boris](!/tags/boris-cherny.svg)](https://youtu.be/julbw1JuAz0?t=3630) [![视频](!/tags/video.svg)](https://youtu.be/julbw1JuAz0?t=3630) |

<a id="tips-context"></a>■ **上下文（5 条）**

| 技巧 | 出处 |
|-----|--------|
| 在 100 万上下文的模型上，用到 **约 30~40 万 token** 时就开始「上下文腐化」了——对智力敏感的任务，别让会话飘过这个量 | [![Thariq](!/tags/thariq.svg)](tips/claude-thariq-tips-16-apr-26.md) |
| 用到 **约 40% 上下文**时就进入「变笨区」——「你会撞上一个结果开始变差的临界点」。新手：「尽量控制在 40% 以下，到 60% 就该收尾了」。老手：「狠一点，压在 30% 以下」——只有在简单任务上才顶到 60%。切换任务时用手动 [/compact](https://code.claude.com/docs/en/interactive-mode) 或 [/clear](https://code.claude.com/docs/en/cli-reference) 重置 | [![Dex](!/tags/community-dex.svg)](videos/claude-dex-mlops-community-24-mar-26.md) [![视频](!/tags/video.svg)](https://youtu.be/YwZR6tc7qYg?t=1541) |
| 「回退」优于「纠正」——连按两次 Esc 或用 [/rewind](https://code.claude.com/docs/en/checkpointing) 退到失败那次尝试之前，带着学到的东西重新提示，而不是让失败的尝试和纠正留在上下文里污染它 🚫👶 | [![Thariq](!/tags/thariq.svg)](tips/claude-thariq-tips-16-apr-26.md) |
| 带提示词的 [/compact](https://code.claude.com/docs/en/interactive-mode)（比如 `/compact 只保留 auth 重构，把调试测试那部分丢掉`）比让自动压缩触发要好——因为自动压缩发生时模型正处于最不聪明的时刻 | [![Thariq](!/tags/thariq.svg)](tips/claude-thariq-tips-16-apr-26.md) |
| 用子 Agent 来管理上下文——先问自己「我还会需要这份工具输出，还是只要结论？」——20 次文件读取 + 12 次 grep + 3 次走弯路都留在子进程里，只有最终报告回来 🚫👶 | [![Thariq](!/tags/thariq.svg)](tips/claude-thariq-tips-16-apr-26.md) |

<a id="tips-session"></a>■ **会话管理（6 条）**

| 技巧 | 出处 |
|-----|--------|
| 每一轮都是一次分叉点——Claude 结束一轮后，根据你要带走多少上下文，在「继续、/rewind、/clear、/compact、开子 Agent」之间选一个 | [![Thariq](!/tags/thariq.svg)](tips/claude-thariq-tips-16-apr-26.md) |
| 新任务 = 新会话——相关的任务（比如给刚写完的东西补文档）可以复用上下文提效，但真正的新任务值得开一个干净的会话 | [![Thariq](!/tags/thariq.svg)](tips/claude-thariq-tips-16-apr-26.md) |
| 回退前先说「从这里开始总结一下」，让 Claude 写一份交接说明——就像未来那个 Claude 给上一版的自己留张纸条 | [![Thariq](!/tags/thariq.svg)](tips/claude-thariq-tips-16-apr-26.md) |
| /compact 和 /clear 的区别——compact 有损但保势头（任务中途、细节模糊点没关系）；/clear 再补一段说明更费事，但你能精确控制带走什么（下一步很关键时用） | [![Thariq](!/tags/thariq.svg)](tips/claude-thariq-tips-16-apr-26.md) |
| 长会话用「回顾」——让 Claude 简短总结一下做了什么、下一步是什么，隔几分钟或几小时回来时特别有用。可以在 /config 里用 recaps 关掉 | [![Boris](!/tags/boris-cherny.svg)](tips/claude-boris-6-tips-16-apr-26.md) |
| 用 [/rename](https://code.claude.com/docs/en/cli-reference) 给重要会话起名字（比如 `[TODO - 重构任务]`），之后用 [/resume](https://code.claude.com/docs/en/cli-reference) 找回来——同时跑多个 Claude 时给每个实例都打个标签 | [![Cat](!/tags/cat-wu.svg)](https://every.to/podcast/how-to-use-claude-code-like-the-people-who-built-it) |

<a id="tips-claudemd"></a>■ **CLAUDE.md + .claude/rules（8 条）**

| 技巧 | 出处 |
|-----|--------|
| [CLAUDE.md](https://code.claude.com/docs/en/memory) 每个文件最好控制在 [200 行以内](https://code.claude.com/docs/en/memory#write-effective-instructions)。humanlayer 那边压到了 [60 行](https://www.humanlayer.dev/blog/writing-a-good-claude-md)（[但也不是 100% 保证生效](https://www.reddit.com/r/ClaudeCode/comments/1qn9pb9/claudemd_says_must_use_agent_claude_ignores_it_80/)） | [![Boris](!/tags/boris-cherny.svg)](https://x.com/bcherny/status/2007179840848597422) [![Dex](!/tags/community-dex.svg)](https://www.humanlayer.dev/blog/writing-a-good-claude-md) |
| `.claude/rules/*.md` 会像 CLAUDE.md 一样自动加载进每个会话——加上 `paths:` 的 YAML 头，就能只在 Claude 碰到匹配该通配符的文件时才懒加载 | [![Claude](!/tags/claude.svg)](https://code.claude.com/docs/en/memory#organize-rules-with-claude/rules/) |
| 把领域专用的 CLAUDE.md 规则用 [\<important if="..."\> 标签](https://www.hlyr.dev/blog/stop-claude-from-ignoring-your-claude-md) 包起来，防止文件变长后 Claude 无视它们 | [![Dex](!/tags/community-dex.svg)](https://www.hlyr.dev/blog/stop-claude-from-ignoring-your-claude-md) |
| 大仓（monorepo）用[多份 CLAUDE.md](best-practice/claude-memory.md)——祖先目录和子目录会叠加加载 | [![Boris](!/tags/boris-cherny.svg)](https://x.com/bcherny/status/2016339448863355206) |
| 用 [.claude/rules/](https://code.claude.com/docs/en/memory#organize-rules-with-claude/rules/) 把长指令拆开 | [![Claude](!/tags/claude.svg)](https://code.claude.com/docs/en/memory#organize-rules-with-claude/rules/) |
| 任何开发者都应该能启动 Claude、说一句「跑测试」，然后一次就跑通——如果跑不通，说明你的 CLAUDE.md 缺了搭建、构建、测试的关键命令 | [![Dex](!/tags/community-dex.svg)](https://x.com/dexhorthy/status/2034713765401551053) |
| 保持代码库干净、把迁移做完——迁移到一半的框架会让模型困惑，可能挑错模式 | [![Boris](!/tags/boris-cherny.svg)](https://youtu.be/julbw1JuAz0?t=1112) [![视频](!/tags/video.svg)](https://youtu.be/julbw1JuAz0?t=1112) |
| 把强制行为（署名、权限、模型）放进 [settings.json](best-practice/claude-settings.md)——别在 CLAUDE.md 里写「绝对不要加 Co-Authored-By」，因为 `attribution.commit: ""` 是确定性的配置 | [![davila7](!/tags/community-davila7.svg)](https://x.com/dani_avila7/status/2036182734310195550) |

<a id="tips-agents"></a><img src="!/tags/a.svg" height="14"> **Agent（4 条）**

| 技巧 | 出处 |
|-----|--------|
| 按功能建专门的[子 Agent](https://code.claude.com/docs/en/sub-agents)（带额外上下文）+ [技能](https://code.claude.com/docs/en/skills)（渐进式展开），而不是笼统地建「测试」「后端工程师」这种 | [![Boris](!/tags/boris-cherny.svg)](https://x.com/bcherny/status/2007179850139000872) |
| 说一句「用子 Agent」就能往一个问题上堆更多算力——把任务分出去，让主上下文保持干净专注 🚫👶 | [![Boris](!/tags/boris-cherny.svg)](https://x.com/bcherny/status/2017742755737555434) |
| 用 [tmux 跑 Agent 团队](https://code.claude.com/docs/en/agent-teams) + [git worktrees](https://x.com/bcherny/status/2025007393290272904) 做并行开发 | [![Boris](!/tags/boris-cherny.svg)](https://x.com/bcherny/status/2025007393290272904) |
| 用[推理时算力](https://code.claude.com/docs/en/sub-agents)——分开的上下文窗口能让结果更好；一个 Agent 造出来的 bug，另一个（同一个模型）能找出来 | [![Boris](!/tags/boris-cherny.svg)](https://x.com/bcherny/status/2031151689219321886) |

<a id="tips-commands"></a><img src="!/tags/c.svg" height="14"> **命令（3 条）**

| 技巧 | 出处 |
|-----|--------|
| 日常工作流用[命令](https://code.claude.com/docs/en/skills)，别用[子 Agent](https://code.claude.com/docs/en/sub-agents) | [![Boris](!/tags/boris-cherny.svg)](https://x.com/bcherny/status/2007179847949500714) |
| 所有一天要跑很多遍的「内循环」工作流，都做成[斜杠命令](https://code.claude.com/docs/en/skills)——省掉重复的提示词。命令存在 `.claude/commands/` 里，会进 git | [![Boris](!/tags/boris-cherny.svg)](https://x.com/bcherny/status/2007179847949500714) |
| 一天之内做过不止一次的事，就把它做成[技能](https://code.claude.com/docs/en/skills)或[命令](https://code.claude.com/docs/en/skills)——比如写个 /techdebt、上下文导出、或数据分析命令 | [![Boris](!/tags/boris-cherny.svg)](https://x.com/bcherny/status/2017742748984742078) |

<a id="tips-skills"></a><img src="!/tags/s.svg" height="14"> **技能（9 条）**

| 技巧 | 出处 |
|-----|--------|
| 用 [context: fork](https://code.claude.com/docs/en/skills) 让技能在独立的子 Agent 里跑——主上下文只看得到最终结果，看不到中间的 tool 调用。`agent` 字段可以指定子 Agent 类型 | [![Lydia](!/tags/lydia.svg)](https://x.com/lydiahallie/status/2033603164398883042) |
| 大仓用[子目录里放技能](reports/claude-skills-for-larger-mono-repos.md) | [![Claude](!/tags/claude.svg)](https://code.claude.com/docs/en/skills) |
| 技能是**文件夹**不是文件——用 `references/`、`scripts/`、`examples/` 这些子目录做[渐进式展开](https://code.claude.com/docs/en/skills) | [![Thariq](!/tags/thariq.svg)](https://x.com/trq212/status/2033949937936085378) |
| 每个技能里建一个「坑（Gotchas）」小节——信息密度最高的部分，把 Claude 踩过的坑一条条加进去 | [![Thariq](!/tags/thariq.svg)](https://x.com/trq212/status/2033949937936085378) |
| 技能的 `description` 字段是**触发器**不是摘要——写给模型看（「我什么时候该启动？」） | [![Thariq](!/tags/thariq.svg)](https://x.com/trq212/status/2033949937936085378) |
| 别在技能里写显而易见的东西——只写能把 Claude 推出默认行为的那部分 🚫👶 | [![Thariq](!/tags/thariq.svg)](https://x.com/trq212/status/2033949937936085378) |
| 别在技能里给 Claude 铺死轨道——给目标和约束，别给死板的一二三步 🚫👶 | [![Thariq](!/tags/thariq.svg)](https://x.com/trq212/status/2033949937936085378) |
| 在技能里放脚本和库，让 Claude 去组合，而不是每次重新拼一遍样板代码 | [![Thariq](!/tags/thariq.svg)](https://x.com/trq212/status/2033949937936085378) |
| 在 `SKILL.md` 里嵌 `!命令`，把动态的 shell 输出注入提示词——Claude 启动时自动跑，模型只看得到结果 | [![Lydia](!/tags/lydia.svg)](https://x.com/lydiahallie/status/2034337963820327017) |

<a id="tips-hooks"></a>■ **钩子（5 条）**

| 技巧 | 出处 |
|-----|--------|
| 在技能里用[按需钩子](https://code.claude.com/docs/en/skills)——比如 /careful 拦住破坏性命令，/freeze 拦住指定目录外的改动 | [![Thariq](!/tags/thariq.svg)](https://x.com/trq212/status/2033949937936085378) |
| 用 PreToolUse 钩子[统计技能使用情况](https://code.claude.com/docs/en/skills)，找出哪些最常用、哪些触发不足 | [![Thariq](!/tags/thariq.svg)](https://x.com/trq212/status/2033949937936085378) |
| 用 [PostToolUse 钩子](https://code.claude.com/docs/en/hooks)自动格式化代码——Claude 生成的代码格式已经不错，钩子补上最后 10%，避免 CI 挂掉 | [![Boris](!/tags/boris-cherny.svg)](https://x.com/bcherny/status/2007179852047335529) |
| 用钩子把[权限请求](https://code.claude.com/docs/en/hooks)转给 Opus 处理——让它扫一遍有没有攻击，安全的就自动放行 🚫👶 | [![Boris](!/tags/boris-cherny.svg)](https://x.com/bcherny/status/2017742755737555434) |
| 用 [Stop 钩子](https://code.claude.com/docs/en/hooks)在一轮结束时推 Claude 一把，让它继续干或者校验一下自己的活 | [![Boris](!/tags/boris-cherny.svg)](https://x.com/bcherny/status/2021701059253874861) |

<a id="tips-workflows"></a>■ **工作流（5 条）**

| 技巧 | 出处 |
|-----|--------|
| 用 [/model](https://code.claude.com/docs/en/model-config) 选模型和推理强度，[/context](https://code.claude.com/docs/en/interactive-mode) 看上下文用了多少，[/usage](https://code.claude.com/docs/en/costs) 查套餐额度，[/extra-usage](https://code.claude.com/docs/en/interactive-mode) 配超额计费，[/config](https://code.claude.com/docs/en/settings) 改设置——**计划模式用 Opus、写代码用 Sonnet**，两头好处都拿到 | [![Cat](!/tags/cat-wu.svg)](https://x.com/_catwu/status/1955694117264261609) |
| 在 [/config](https://code.claude.com/docs/en/settings) 里把[思考模式](https://code.claude.com/docs/en/model-config)打开（能看到推理过程）、把[输出风格](https://code.claude.com/docs/en/output-styles)设成「解释型」（输出更详细，带 ★ 要点框），能更好地理解 Claude 为什么这么决定 | [![Boris](!/tags/boris-cherny.svg)](https://x.com/bcherny/status/2007179838864666847) |
| 在提示词里用 `ultrathink` 关键词触发[高强度推理](https://docs.anthropic.com/en/docs/build-with-claude/extended-thinking#tips-and-best-practices) | [![Claude](!/tags/claude.svg)](https://docs.anthropic.com/en/docs/build-with-claude/extended-thinking#tips-and-best-practices) |
| `/focus` 模式会隐藏所有中间过程、只显示最终结果——相信模型会跑对命令，你只看结果就行（用 /focus 切换） | [![Boris](!/tags/boris-cherny.svg)](tips/claude-boris-6-tips-16-apr-26.md) |
| 用 Opus 4.7 的自适应思考来调节力度——`low` 更快更省 token，`max` 最聪明（档位：low · medium · high · xhigh · max） | [![Boris](!/tags/boris-cherny.svg)](tips/claude-boris-6-tips-16-apr-26.md) |

<a id="tips-workflows-advanced"></a>■ **工作流进阶（9 条）**

| 技巧 | 出处 |
|-----|--------|
| 多画 ASCII 架构图来理解你的系统 | [![Boris](!/tags/boris-cherny.svg)](https://x.com/bcherny/status/2017742759218794768) |
| 用 [/loop](https://code.claude.com/docs/en/scheduled-tasks) 做本地周期性巡检（最长 7 天）· 用 [/schedule](https://code.claude.com/docs/en/routines) 做云端周期任务，即使你关机了也会跑 | [![Boris](!/tags/boris-cherny.svg)](https://x.com/bcherny/status/2038454341884154269) |
| 用 [Ralph Wiggum 插件](https://github.com/shanraisshan/ralph-wiggum-self-evolving-loop)跑长时间自主任务 | [![Boris](!/tags/boris-cherny.svg)](https://x.com/bcherny/status/2007179858435281082) |
| 用[/permissions](https://code.claude.com/docs/en/permissions) 的通配符语法（`Bash(npm run *)`、`Edit(/docs/**)`），别用 `dangerously-skip-permissions` | [![Boris](!/tags/boris-cherny.svg)](https://x.com/bcherny/status/2007179854077407667) |
| 用 [/sandbox](https://code.claude.com/docs/en/sandboxing) 做文件和网络隔离，减少权限弹窗——内部实测减少 84% | [![Boris](!/tags/boris-cherny.svg)](https://x.com/bcherny/status/2021700506465579443) [![Cat](!/tags/cat-wu.svg)](https://creatoreconomy.so/p/inside-claude-code-how-an-ai-native-actually-works-cat-wu) |
| 值得投入做[产品验证](https://code.claude.com/docs/en/skills)类技能（比如 signup-flow-driver、checkout-verifier）——花一周打磨都值 | [![Thariq](!/tags/thariq.svg)](https://x.com/trq212/status/2033949937936085378) |
| 用[自动模式](https://code.claude.com/docs/en/permission-modes#eliminate-prompts-with-auto-mode)，别用 `dangerously-skip-permissions`——自动模式有个模型分类器判断每条命令安不安全，安全的自动放行，有风险的暂停来问你。`Shift+Tab` 在 Ask → Plan → Auto 之间切换 🚫👶 | [![Boris](!/tags/boris-cherny.svg)](tips/claude-boris-6-tips-16-apr-26.md) |
| 用 /less-permission-prompts 技能扫描会话历史，找出反复弹窗但其实安全的 bash/MCP 命令，给你一份推荐白名单直接粘进[设置](best-practice/claude-settings.md) | [![Boris](!/tags/boris-cherny.svg)](tips/claude-boris-6-tips-16-apr-26.md) |
| 做一个 /go 技能，让它（1）用 bash/浏览器/电脑操作端到端测试（2）跑 /simplify（3）提个 PR——这样你回来的时候就能确定代码是能跑的 🚫👶 | [![Boris](!/tags/boris-cherny.svg)](tips/claude-boris-6-tips-16-apr-26.md) |

<a id="tips-git-pr"></a>■ **Git / PR（5 条）**

| 技巧 | 出处 |
|-----|--------|
| PR 要小而聚焦——[中位数 118 行](tips/claude-boris-2-tips-25-mar-26.md)（141 个 PR、一天改了 4.5 万行），一个 PR 只做一个功能，好评审也好回滚 | [![Boris](!/tags/boris-cherny.svg)](https://x.com/bcherny/status/2038552880018538749) |
| PR 一律用 [squash merge](tips/claude-boris-2-tips-25-mar-26.md)——历史干净、一个功能一个提交，`git revert` 和 `git bisect` 都好用 | [![Boris](!/tags/boris-cherny.svg)](https://x.com/bcherny/status/2038552880018538749) |
| 勤提交——尽量每小时至少一次，任务一完成就提交 | ![Shayan](!/tags/community-shayan.svg) |
| 在同事的 PR 上 @claude，让它根据反复出现的评审意见自动生成 lint 规则——把自己从代码评审里摘出来 🚫👶 | [![Boris](!/tags/boris-cherny.svg)](https://youtu.be/julbw1JuAz0?t=2715) [![视频](!/tags/video.svg)](https://youtu.be/julbw1JuAz0?t=2715) |
| 用 [/code-review](https://code.claude.com/docs/en/code-review) 做多 Agent 的 PR 分析——在合并前抓出 bug、安全漏洞和回归 | [![Boris](!/tags/boris-cherny.svg)](https://x.com/bcherny/status/2031089411820228645) |

<a id="tips-debugging"></a>■ **调试（6 条）**

| 技巧 | 出处 |
|-----|--------|
| 养成习惯：卡在任何问题上就截图丢给 Claude | ![Shayan](!/tags/community-shayan.svg) |
| 用 MCP（[Chrome 里的 Claude](https://code.claude.com/docs/en/chrome)、[Playwright](https://github.com/microsoft/playwright-mcp)、[Chrome DevTools](https://developer.chrome.com/blog/chrome-devtools-mcp)）让 Claude 自己去看控制台日志 | [![Claude](!/tags/claude.svg)](https://code.claude.com/docs/en/chrome) |
| 想看日志，就让 Claude 把终端命令当**后台任务**跑，方便调试 | ![Shayan](!/tags/community-shayan.svg) |
| 用 [/doctor](https://code.claude.com/docs/en/cli-reference) 诊断安装、鉴权和配置问题 | ![Shayan](!/tags/community-shayan.svg) |
| 用[跨模型](#-cross-model-workflows)做 QA——比如让 [Codex](https://github.com/shanraisshan/codex-cli-best-practice) 评审计划和实现 | ![Shayan](!/tags/community-shayan.svg) |
| 「Agent 式搜索」（glob + grep）比 RAG 好用——Claude Code 试过向量数据库又放弃了，因为代码会漂移失同步、权限也复杂 | [![Boris](!/tags/boris-cherny.svg)](https://youtu.be/julbw1JuAz0?t=3095) [![视频](!/tags/video.svg)](https://youtu.be/julbw1JuAz0?t=3095) |

<a id="tips-utilities"></a>■ **小工具（5 条）**

| 技巧 | 出处 |
|-----|--------|
| 用 [iTerm](https://iterm2.com/)/[Ghostty](https://ghostty.org/)/[tmux](https://github.com/tmux/tmux) 这类终端，而不是 IDE（[VS Code](https://code.visualstudio.com/)/[Cursor](https://www.cursor.com/)） | [![Boris](!/tags/boris-cherny.svg)](https://x.com/bcherny/status/2017742753971769626) |
| 用 [/voice](https://code.claude.com/docs/en/voice-dictation) 或 [Wispr Flow](https://wisprflow.ai) 语音输入（效率 10 倍） | [![Boris](!/tags/boris-cherny.svg)](https://x.com/bcherny/status/2038454362226467112) |
| 用 [claude-code-hooks](https://github.com/shanraisshan/claude-code-hooks) 接收 Claude 的反馈提示 | ![Shayan](!/tags/community-shayan.svg) |
| 用[状态栏](https://github.com/shanraisshan/claude-code-status-line)感知上下文占用，并快速压缩 | [![Boris](!/tags/boris-cherny.svg)](https://x.com/bcherny/status/2021700784019452195) ![Shayan](!/tags/community-shayan.svg) |
| 探索 [settings.json](best-practice/claude-settings.md) 里的功能，比如[计划目录](best-practice/claude-settings.md#plans-directory)、[转圈动词](best-practice/claude-settings.md#display--ux)，做出自己的风格 | [![Boris](!/tags/boris-cherny.svg)](https://x.com/bcherny/status/2021701145023197516) |

<a id="tips-daily"></a>■ **日常（2 条）**

| 技巧 | 出处 |
|-----|--------|
| 每天[更新](https://code.claude.com/docs/en/setup) Claude Code | ![Shayan](!/tags/community-shayan.svg) |
| 每天开工前先读一遍[更新日志](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md) | ![Shayan](!/tags/community-shayan.svg) |

![Boris Cherny 及团队](!/tags/claude.svg)

| 文章 / 推文 | 出处 |
|-----------------|--------|
| [把 Opus 4.7 用好的 6 条技巧（Boris）｜26 年 4 月 16 日](tips/claude-boris-6-tips-16-apr-26.md) | [推文](https://x.com/bcherny) |
| [会话管理与 100 万上下文（Thariq）｜26 年 4 月 16 日](tips/claude-thariq-tips-16-apr-26.md) | [推文](https://x.com/trq212) |
| [Claude Code 里 15 个被埋没的隐藏功能（Boris）｜26 年 3 月 30 日](tips/claude-boris-15-tips-30-mar-26.md) | [推文](https://x.com/bcherny/status/2038454336355999749) |
| [Squash 合并与 PR 体积分布（Boris）｜26 年 3 月 25 日](tips/claude-boris-2-tips-25-mar-26.md) | [推文](https://x.com/bcherny/status/2038552880018538749) |
| [造 Claude Code 的经验教训：我们怎么用技能（Thariq）｜26 年 3 月 17 日](tips/claude-thariq-tips-17-mar-26.md) | [文章](https://x.com/trq212/status/2033949937936085378) |
| [代码评审与推理时算力（Boris）｜26 年 3 月 10 日](tips/claude-boris-2-tips-10-mar-26.md) | [推文](https://x.com/bcherny/status/2031089411820228645) |
| /loop —— 最长 3 天的周期性任务（Boris）｜2026 年 3 月 7 日 | [推文](https://x.com/bcherny/status/2030193932404150413) |
| 用 AskUserQuestion + ASCII 图（Thariq）｜2026 年 2 月 28 日 | [推文](https://x.com/trq212/status/2027543858289250472) |
| 像 Agent 一样看世界——造 Claude Code 的经验教训（Thariq）｜2026 年 2 月 28 日 | [文章](https://x.com/trq212/status/2027463795355095314) |
| Git Worktrees —— Boris 的 5 种用法｜2026 年 2 月 21 日 | [推文](https://x.com/bcherny/status/2025007393290272904) |
| 造 Claude Code 的经验教训：提示词缓存就是一切（Thariq）｜2026 年 2 月 20 日 | [文章](https://x.com/trq212/status/2024574133011673516) |
| [大家定制自己 Claude 的 12 种方式（Boris）｜26 年 2 月 12 日](tips/claude-boris-12-tips-12-feb-26.md) | [推文](https://x.com/bcherny/status/2021699851499798911) |
| [来自团队的 10 条 Claude Code 使用建议（Boris）｜26 年 2 月 1 日](tips/claude-boris-10-tips-01-feb-26.md) | [推文](https://x.com/bcherny/status/2017742741636321619) |
| [我怎么用 Claude Code —— 我那套朴素配置里的 13 条经验（Boris）｜26 年 1 月 3 日](tips/claude-boris-13-tips-03-jan-26.md) | [推文](https://x.com/bcherny/status/2007179832300581177) |
| 让 Claude 用 AskUserQuestion 工具采访你（Thariq）｜25 年 12 月 28 日 | [推文](https://x.com/trq212/status/2005315275026260309) |
| 永远开计划模式、给 Claude 一个验证手段、用 /code-review（Boris）｜25 年 12 月 27 日 | [推文](https://x.com/bcherny/status/2004711722926616680) |

#### 从 Claude Code 命令行程序里扒出来的技巧

[转圈动词与技巧（从 v2.1.121 程序文件里提取）](reports/claude-spinner-verbs-and-tips.md)

<p align="center">
  <img src="!/claude-jumping.svg" alt="章节分隔" width="60" height="50">
</p>

## 🎬 视频 / 播客

| 视频 / 播客 | 出处 | 链接 |
|-----------------|--------|--------|
| 从氛围编程到 Agent 工程（Andrej）｜2026 年 5 月 2 日｜AI Engineer | [![Karpathy](!/tags/community-karpathy.svg)](https://x.com/karpathy) | [YouTube](https://www.youtube.com/watch?v=96jN2OCOfLs) |
| 全流程演示：AI 写代码的工作流（Matt）｜2026 年 4 月 24 日｜Matt Pocock | [![Matt](!/tags/community-matt.svg)](https://x.com/mattpocockuk) | [YouTube](https://youtu.be/-QFHIoCo-Ko) |
| 我们在「调研-计划-实现」上搞错的一切（Dex）｜2026 年 3 月 24 日｜MLOps Community | [![Dex](!/tags/community-dex.svg)](https://x.com/daborhyde) | [YouTube](https://youtu.be/YwZR6tc7qYg) |
| 跟 Boris Cherny 一起造 Claude Code（Boris）｜2026 年 3 月 4 日｜The Pragmatic Engineer | [![Boris](!/tags/boris-cherny.svg)](https://x.com/bcherny) | [YouTube](https://youtu.be/julbw1JuAz0) |
| Claude Code 负责人：写代码这件事被解决之后（Boris）｜2026 年 2 月 19 日｜Lenny's Podcast | [![Boris](!/tags/boris-cherny.svg)](https://x.com/bcherny) | [YouTube](https://youtu.be/We7BZVKbCVw) |
| 跟创造者 Boris Cherny 一起走进 Claude Code（Boris）｜2026 年 2 月 17 日｜Y Combinator | [![Boris](!/tags/boris-cherny.svg)](https://x.com/bcherny) | [YouTube](https://youtu.be/PQU9o_5rHC4) |
| Boris Cherny（Claude Code 创造者）谈什么成就了他的职业（Boris）｜2025 年 12 月 15 日｜Ryan Peterman | [![Boris](!/tags/boris-cherny.svg)](https://x.com/bcherny) | [YouTube](https://youtu.be/AmdLVWMdjOk) |
| 造它的工程师讲 Claude Code 的秘密（Cat）｜2025 年 10 月 29 日｜Every | [![Boris](!/tags/boris-cherny.svg)](https://x.com/bcherny) | [YouTube](https://youtu.be/IDSAMqip6ms) |

<p align="center">
  <img src="!/claude-jumping.svg" alt="章节分隔" width="60" height="50">
</p>

## 🔔 关注渠道

| 平台 | 账号 | 徽章 |
|--------|------|-------|
| ![Reddit](https://img.shields.io/badge/-FF4500?style=flat&logo=reddit&logoColor=white) | [r/ClaudeAI](https://www.reddit.com/r/ClaudeAI/)、[r/ClaudeCode](https://www.reddit.com/r/ClaudeCode/)、[r/Anthropic](https://www.reddit.com/r/Anthropic/) | ![Boris + 团队](!/tags/claude.svg) |
| ![X](https://img.shields.io/badge/-000?style=flat&logo=x&logoColor=white) | [Claude](https://x.com/claudeai)、[Claude Devs](https://x.com/ClaudeDevs)、[Anthropic](https://x.com/AnthropicAI)、Boris、Thariq、Cat、Lydia、Noah、Anthony、Alex、Kenneth | ![Boris + 团队](!/tags/claude.svg) |
| ![X](https://img.shields.io/badge/-000?style=flat&logo=x&logoColor=white) | 社区作者与项目作者（Jesse Kriss / Superpowers、Affaan Mustafa / ECC、Garry Tan / gstack、Dex Horthy / HumanLayer、Kieran Klaassen / Compound Eng、Tabish Gilani / OpenSpec、Brian McAdams / BMAD、Lex Christopherson / GSD、Matt Pocock / Skills、Dani Avila / CC Templates、Dan Shipper / Every、Andrej Karpathy / AutoResearch、Peter Steinberger / OpenClaw、Sigrid Jin / claw-code、Yeachan Heo / oh-my-claudecode） | ![社区](!/tags/community.svg) |
| ![YouTube](https://img.shields.io/badge/-F00?style=flat&logo=youtube&logoColor=white) | [Anthropic](https://www.youtube.com/@anthropic-ai) | ![Boris + 团队](!/tags/claude.svg) |
| ![YouTube](https://img.shields.io/badge/-F00?style=flat&logo=youtube&logoColor=white) | [Lenny's Podcast](https://www.youtube.com/@LennysPodcast)、[Y Combinator](https://www.youtube.com/@ycombinator)、[The Pragmatic Engineer](https://www.youtube.com/@pragmaticengineer)、[Ryan Peterman](https://www.youtube.com/@ryanlpeterman)、[Every](https://www.youtube.com/@every_media)、[MLOps Community](https://www.youtube.com/@MLOps) | ![社区](!/tags/community.svg) |

<p align="center">
  <img src="!/claude-jumping.svg" alt="章节分隔" width="60" height="50">
</p>

## ☠️ 被它取代的创业公司 / 生意

| Claude 的功能 | 取代了谁 |
|-|-|
| [**代码评审**](https://code.claude.com/docs/en/code-review) | [Greptile](https://greptile.com)、[CodeRabbit](https://coderabbit.ai)、[Devin Review](https://devin.ai)、[OpenDiff](https://opendiff.com)、[Cursor BugBot](https://bugbot.dev) |
| [**语音输入**](https://code.claude.com/docs/en/voice-dictation) | [Wispr Flow](https://wisprflow.ai)、[SuperWhisper](https://superwhisper.com/) |
| [**远程控制**](https://code.claude.com/docs/en/remote-control) | [OpenClaw](https://openclaw.ai/) |
| [**Chrome 里的 Claude**](https://code.claude.com/docs/en/chrome) | [Playwright MCP](https://github.com/microsoft/playwright-mcp)、[Chrome DevTools MCP](https://developer.chrome.com/blog/chrome-devtools-mcp) |
| [**电脑操作**](https://docs.anthropic.com/en/docs/agents-and-tools/computer-use) | [OpenAI CUA](https://openai.com/index/computer-using-agent/) |
| [**Cowork**](https://claude.com/blog/cowork-research-preview) | [ChatGPT Agent](https://openai.com/chatgpt/agent/)、[Perplexity Computer](https://www.perplexity.ai/computer/)、[Manus](https://manus.im) |
| [**任务（Tasks）**](https://x.com/trq212/status/2014480496013803643) | [Beads](https://github.com/steveyegge/beads) |
| [**计划模式**](https://code.claude.com/docs/en/common-workflows) | [Agent OS](https://github.com/buildermethods/agent-os) |
| [**设计**](https://claude.com/design) | [Figma](https://figma.com)、[Framer](https://framer.com)、[Sketch](https://sketch.com)、[v0](https://v0.dev) |
| [**Agent SDK**](https://code.claude.com/docs/en/agent-sdk/overview) | [LangChain](https://langchain.com)、[LangGraph](https://www.langchain.com/langgraph)、[CrewAI](https://www.crewai.com)、[AutoGen](https://github.com/microsoft/autogen)、[OpenAI Assistants API](https://platform.openai.com/docs/assistants/overview) |
| [**技能 / 插件**](https://code.claude.com/docs/en/plugins) | 那些 YC 的「AI 套壳」创业公司（[reddit 讨论](https://reddit.com/r/ClaudeAI/comments/1r6bh4d/claude_code_skills_are_basically_yc_ai_startup/)） |

<p align="center">
  <img src="!/claude-jumping.svg" alt="章节分隔" width="60" height="50">
</p>

<a id="billion-dollar-questions"></a>
![值十亿美元的问题](!/tags/billion-dollar-questions.svg)

*如果你有答案，欢迎发给我：shanraisshan@gmail.com*

**记忆与指令（4 问）**

1. `CLAUDE.md` 里到底该放什么——又该把什么留在外面？
2. 如果已经有 `CLAUDE.md` 了，还有必要单独搞一份 `constitution.md` 或 `rules.md` 吗？
3. `CLAUDE.md` 该多久更新一次？怎么判断它已经过时了？
4. 为什么 Claude 还是会无视 `CLAUDE.md` 里的指令——哪怕你全大写写了 MUST？（[reddit 讨论](https://reddit.com/r/ClaudeCode/comments/1qn9pb9/claudemd_says_must_use_agent_claude_ignores_it_80/)）

**Agent、技能与工作流（6 问）**

1. 什么时候该用命令、什么时候用 Agent、什么时候用技能——什么时候原生 Claude Code 其实就够好了？
2. 模型在进步，你的 Agent、命令、工作流该多久更新一次？
3. 该建一个通才子 Agent，还是按功能/角色建专才？给子 Agent 一个详细人设能不能提升质量？一份「完美的研究/视觉人设提示词」长什么样？
4. 该依赖 Claude Code 内置的计划模式，还是自己做一个能强制团队流程的计划命令/Agent？
5. 如果你有一套个人技能（比如带你自己代码风格的 /implement），怎么把社区技能（比如 /simplify）接进来又不打架——两者冲突时谁说了算？
6. 我们现在到那一步了吗？能不能把一个现存代码库转成规格文档、把代码删了，然后只靠规格让 AI 重新生成出一模一样的代码？

**规格与文档（3 问）**

1. 代码库里每个功能都该配一份 markdown 规格文档吗？
2. 规格要多久更新一次，才不会在新功能上线后过时？
3. 实现新功能时，怎么应对它对其它功能规格文档的连锁影响？

### 🤔 [代码还重要吗？](https://github.com/shanraisshan/agentic-engineering)

<p align="center">
  <img src="!/claude-jumping.svg" alt="章节分隔" width="60" height="50">
</p>

## 专题报告

<p align="center">
  <a href="reports/claude-agent-sdk-vs-cli-system-prompts.md"><img src="https://img.shields.io/badge/Agent_SDK_vs_CLI-555?style=for-the-badge" alt="Agent SDK 与 CLI 对比"></a>
  <a href="reports/claude-in-chrome-v-chrome-devtools-mcp.md"><img src="https://img.shields.io/badge/Browser_Automation_MCP-555?style=for-the-badge" alt="浏览器自动化 MCP"></a>
  <a href="reports/claude-global-vs-project-settings.md"><img src="https://img.shields.io/badge/Global_vs_Project_Settings-555?style=for-the-badge" alt="全局设置与项目设置"></a>
  <a href="reports/claude-skills-for-larger-mono-repos.md"><img src="https://img.shields.io/badge/Skills_in_Monorepos-555?style=for-the-badge" alt="大仓里的技能"></a>
  <br>
  <a href="reports/claude-agent-memory.md"><img src="https://img.shields.io/badge/Agent_Memory-555?style=for-the-badge" alt="Agent 记忆"></a>
  <a href="reports/claude-advanced-tool-use.md"><img src="https://img.shields.io/badge/Advanced_Tool_Use-555?style=for-the-badge" alt="高级工具用法"></a>
  <a href="reports/claude-usage-and-rate-limits.md"><img src="https://img.shields.io/badge/Usage_&_Rate_Limits-555?style=for-the-badge" alt="用量与速率限制"></a>
  <a href="reports/claude-agent-command-skill.md"><img src="https://img.shields.io/badge/Agents_vs_Commands_vs_Skills-555?style=for-the-badge" alt="Agent 与命令与技能"></a>
  <br>
  <a href="reports/llm-day-to-day-degradation.md"><img src="https://img.shields.io/badge/LLM_Degradation-555?style=for-the-badge" alt="大模型退化"></a>
  <a href="reports/why-harness-is-important.md"><img src="https://img.shields.io/badge/Why_Harness_is_Important-555?style=for-the-badge" alt="为什么调度框架重要"></a>
  <a href="reports/claude-spinner-verbs-and-tips.md"><img src="https://img.shields.io/badge/Spinner_Verbs_&_Tips-555?style=for-the-badge" alt="转圈动词与技巧"></a>
</p>

<p align="center">
  <img src="!/claude-jumping.svg" alt="章节分隔" width="60" height="50">
</p>

<a id="how-to-use"></a>

## <img src="!/tags/how-to-use-hd.svg" alt="怎么用">

按下面这几步走，才能把这个仓库的价值榨干：

1. **把这个仓库当成一门课来读，而不是当成一套工作流或技能。** 它首先是参考资料，动手是后面的事。
2. **别把 Claude 当聊天机器人用。** 先把基本单元学明白——Agent、命令、技能、钩子——再把它们拼成你自己的工作流。
3. **跑一遍 [`/weather-orchestrator`](orchestration-workflow/orchestration-workflow.md)**，看完整的「命令 → Agent → 技能」流程。把它当成任何开发工作流（从计划到上线）的模板。
4. **干活时留意那些自定义的钩子提示音。** 它们的实现放在专门的 [Claude Code Hooks 仓库](https://github.com/shanraisshan/claude-code-hooks)里；其他模式比如 [Agent 团队](implementation/claude-agent-teams-implementation.md)就放在本仓库的 `implementation/` 目录下。
5. **从 [🔥 热门](#-hot) 那张子表里学进阶主题和它们的实现** —— 比如 [Ralph Wiggum 自我进化循环](https://github.com/shanraisshan/ralph-wiggum-self-evolving-loop) 就是一个完整可跑的仓库，你可以克隆下来看这套模式从头到尾长什么样。
6. **在你自己的项目里把 Claude 指向[技巧与窍门](#-tips-and-tricks-83)那一节**，让它给你提修改建议——尤其是怎么重构你的 `CLAUDE.md`。每条技巧都有 Claude 官方团队或社区的出处。
7. **订阅[关注渠道](#-subscribe)里列的 Reddit 和 YouTube 频道**，跟上社区节奏。

**🎬 视频**

<a href="https://www.youtube.com/watch?v=AkAhkalkRY4"><img src="!/thumbnail/video-1.png" alt="在 YouTube 观看" width="240"></a>
<a href="https://youtu.be/lPjhM6BBK0Q"><img src="!/thumbnail/video-2.png" alt="在 YouTube 观看" width="240"></a>

**📊 演讲**

<a href="https://github.com/shanraisshan/claude-code-best-practice/tree/main/presentation/2026-04-25-gdg-kolachi-cli-claude-code-gemini"><img src="!/thumbnail/presentation-1.png" alt="Claude Code 与 Gemini CLI —— GDG Kolachi" width="240"></a>

<p align="center">
  <img src="!/claude-jumping.svg" alt="章节分隔" width="60" height="50">
</p>

<p align="center">
  <a href="https://github.com/trending?since=monthly"><img src="!/root/github-trending.png" alt="GitHub 趋势榜" width="1200"></a><br>
  ✨2026 年 3 月登上 GitHub 趋势榜✨
</p>

## 星标历史

[![星标历史图](https://api.star-history.com/svg?repos=shanraisshan/claude-code-best-practice&type=Date&v=2)](https://star-history.com/#shanraisshan/claude-code-best-practice&Date)

<a href="https://github.com/shanraisshan/claude-code-best-practice/stargazers"><img src="https://img.shields.io/github/stars/shanraisshan/claude-code-best-practice?style=flat&label=%E2%98%85&labelColor=555&color=white" alt="GitHub 星标数" align="center"></a> 颗星，还在涨

## 作者的其它仓库

<table>
<tr>
<td align="center" width="140">
  <a href="https://github.com/shanraisshan/claude-code-hooks"><img src="!/claude-speaking.svg" alt="Claude Code Hooks" width="64" height="64"></a><br>
  <a href="https://github.com/shanraisshan/claude-code-hooks"><strong>Claude Code<br>Hooks</strong></a>
</td>
<td align="center" width="140">
  <a href="https://github.com/shanraisshan/codex-cli-best-practice"><img src="!/codex-jumping.svg" alt="Codex CLI 最佳实践" width="64" height="64"></a><br>
  <a href="https://github.com/shanraisshan/codex-cli-best-practice"><strong>Codex CLI<br>最佳实践</strong></a>
</td>
<td align="center" width="140">
  <a href="https://github.com/shanraisshan/codex-cli-hooks"><img src="!/codex-speaking.svg" alt="Codex CLI Hooks" width="64" height="64"></a><br>
  <a href="https://github.com/shanraisshan/codex-cli-hooks"><strong>Codex CLI<br>Hooks</strong></a>
</td>
<td align="center" width="140">
  <a href="https://github.com/shanraisshan/gemini-cli-best-practice"><img src="!/gemini-jumping.svg" alt="Gemini CLI 最佳实践" width="64" height="64"></a><br>
  <a href="https://github.com/shanraisshan/gemini-cli-best-practice"><strong>Gemini CLI<br>最佳实践</strong></a>
</td>
<td align="center" width="140">
  <a href="https://github.com/shanraisshan/gemini-cli-hooks"><img src="!/gemini-speaking.svg" alt="Gemini CLI Hooks" width="64" height="64"></a><br>
  <a href="https://github.com/shanraisshan/gemini-cli-hooks"><strong>Gemini CLI<br>Hooks</strong></a>
</td>
</tr>
</table>

## 作者自述

![作者自述](!/tags/developed-by.svg)

> | # | 工作流 | 说明 |
> |---|----------|-------------|
> | 1 | /workflows:development-workflows | 并行调研 10 个工作流仓库，更新「开发工作流」表格和跨工作流分析报告 |
> | 2 | /workflows:skill-collections | 并行调研 5 个技能合集仓库，更新「技能合集」表格 |
> | 3 | /workflows:agent-collections | 并行调研各个 Agent 合集仓库，更新「Agent 合集」表格 |
> | 4 | /workflows:best-practice:workflow-concepts | 用 Claude Code 最新的功能和概念更新 README 的「核心概念」一节 |
> | 5 | /workflows:best-practice:workflow-claude-settings | 跟踪 Claude Code 设置报告的变动，找出需要更新的地方 |
> | 6 | /workflows:best-practice:workflow-claude-subagents | 跟踪 Claude Code 子 Agent 报告的变动，找出需要更新的地方 |
> | 7 | /workflows:best-practice:workflow-claude-commands | 跟踪 Claude Code 命令报告的变动，找出需要更新的地方 |
> | 8 | /workflows:best-practice:workflow-claude-skills | 跟踪 Claude Code 技能报告的变动，找出需要更新的地方 |

## 其它

[![Claude for OSS](!/tags/claude-for-oss.svg)](https://claude.com/contact-sales/claude-for-oss)
[![Claude 社区大使](!/tags/claude-community-ambassador.svg)](https://claude.com/community/ambassadors)
[![Claude 认证架构师](!/tags/claude-certified-architect.svg)](https://anthropic.skilljar.com/claude-certified-architect-foundations-access-request)
[![Anthropic 学院](!/tags/anthropic-academy.svg)](https://anthropic.skilljar.com/)
[![加入 Claude 巴基斯坦 WhatsApp 社区](!/tags/whatsapp-claude-pakistan.svg)](https://chat.whatsapp.com/BDUV2stIS0c7X5uY7RY6nS)

<p align="center">
  <img src="!/claude-jumping.svg" alt="章节分隔" width="60" height="50">
</p>

## <img src="!/tags/sponsor-heart.svg" width="22" height="22" align="center"> 赞助我的工作

如果你觉得我做的东西有用，请我喝一杯奶茶 🍵 吧：

<a href="https://buy.polar.sh/polar_cl_R6wjUESl8RiJD0iVaTyStBUV6WNuYvDmLJ0si1XXj4C"><img src="!/tags/polar.svg" alt="Polar" width="40" height="40" align="center"></a> <a href="https://buy.polar.sh/polar_cl_R6wjUESl8RiJD0iVaTyStBUV6WNuYvDmLJ0si1XXj4C"><strong>Polar</strong></a>

**想让你的品牌出现在页头？** 页头位置对外开放 —— 发邮件给 [shanraisshan@gmail.com](mailto:shanraisshan@gmail.com)。
