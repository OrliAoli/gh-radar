> **本篇为「框架式翻译」。**
> 原文是一份「1000+ 技能」的清单仓库，正文主体是 184 条一行式链接（每条 = 技能名 + 一句话介绍）。
> 因此本篇翻译：**开头介绍、快速上手、「什么是 Claude Skills」、「上手使用」、「创建技能」、「贡献指南」、「资源」全部翻译 · 技能分类的章节标题全部翻译 · 184 条技能清单保留英文原文**（点「对照原文」可看完整清单，链接本身才是主体）。

<h1 align="center">Awesome Claude Skills</h1>

<p align="center">
<a href="https://dashboard.composio.dev/login?utm_source=Github&utm_medium=Youtube&utm_campaign=2025-11&utm_content=AwesomeSkills">
  <img width="1280" height="640" alt="Composio 横幅" src="https://github.com/user-attachments/assets/e91255af-e4ba-4d71-b1a8-bd081e8a234a">
</a>

</p>

<p align="center">
  <a href="https://awesome.re">
    <img src="https://awesome.re/badge.svg" alt="Awesome" />
  </a>
  <a href="https://makeapullrequest.com">
    <img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square" alt="欢迎提 PR" />
  </a>
  <a href="https://www.apache.org/licenses/LICENSE-2.0">
    <img src="https://img.shields.io/badge/License-Apache_2.0-blue.svg?style=flat-square" alt="许可证：Apache-2.0" />
  </a>
</p>
<div>
<p align="center">
  <a href="https://twitter.com/composio">
    <img src="https://img.shields.io/badge/Follow on X-000000?style=for-the-badge&logo=x&logoColor=white" alt="在 X 上关注" />
  </a>
  <a href="https://www.linkedin.com/company/composiohq/">
    <img src="https://img.shields.io/badge/Follow on LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="在 LinkedIn 上关注" />
  </a>
  <a href="https://discord.com/invite/composio">
    <img src="https://img.shields.io/badge/Join our Discord-5865F2?style=for-the-badge&logo=discord&logoColor=white" alt="加入 Discord" />
  </a>
  </p>
</div>

一份全面、精选的清单，收录了 **1000+ 个可直接投入生产、且实用的 Claude 技能与插件**。它们不只提升 Claude.ai 和 Claude Code 的效率，也覆盖 Codex、Cursor、Gemini CLI、Antigravity 等各类编程 Agent。

## 让你的技能真正能动手做事

技能告诉你的 Agent **该怎么做**。而一个 MCP 网关，给它安全访问所需工具的权限。

Composio 的 [MCP 网关](https://composio.dev/mcp-gateway)提供单一 MCP 端点，接入 1000+ 个集成，内置鉴权、基于团队的访问控制、审计日志和面向生产的可靠性。

---

## 快速上手：把 Claude 接到 1000+ 个应用上

**connect-apps** 插件让 Claude 能真正动手做事 —— 发邮件、创建 issue、往 Slack 发帖。它在底层用 Composio 处理鉴权并连接 1000+ 个应用。

### 1. 安装插件

```bash
claude --plugin-dir ./connect-apps-plugin
```

### 2. 运行安装

```
/connect-apps:setup
```

提示时粘贴你的 API Key。（可以在 [dashboard.composio.dev](https://dashboard.composio.dev/login?utm_source=Github&utm_content=AwesomeSkills) 免费领一个。）

### 3. 重启并试一试

```bash
exit
claude
```

> **想要「不只生成文字」的技能？** Claude 可以发邮件、创建 issue、往 Slack 发帖，在 1000+ 个应用上执行动作。[看看怎么做到的 →](./connect/)

如果你收到了那封邮件，说明 Claude 已经连上 1000+ 个应用了。

**[查看所有支持的应用 →](https://composio.dev/toolkits)**

---

## 目录

- [什么是 Claude Skills？](#什么是-claude-skills)
- [技能清单](#技能清单)
  - [文档处理](#文档处理)
  - [开发与代码工具](#开发与代码工具)
  - [数据与分析](#数据与分析)
  - [商业与营销](#商业与营销)
  - [沟通与写作](#沟通与写作)
  - [创意与媒体](#创意与媒体)
  - [效率与整理](#效率与整理)
  - [协作与项目管理](#协作与项目管理)
  - [安全与系统](#安全与系统)
  - [通过 Composio 做应用自动化](#通过-composio-做应用自动化)
- [上手使用](#上手使用)
- [创建技能](#创建技能)
- [参与贡献](#参与贡献)
- [资源](#资源)
- [许可证](#许可证)

## 什么是 Claude Skills？

Claude Skills 是可复用的指令包，用来教 AI Agent 处理某一类特定任务。每个技能就是一个文件夹，里面有一个 `SKILL.md`，带 YAML 前言（name、description）和 Markdown 格式的指令，还可以附带脚本、参考资料和素材。Anthropic 在 2025 年 10 月提出了这个格式，并在 2025 年 12 月把它作为[开放标准](https://github.com/anthropics/skills)发布；现在 Claude Code、Claude.ai、Claude API、OpenAI Codex、Cursor、Gemini CLI、Antigravity 和 Windsurf 都支持它。

技能是**渐进式加载**的。会话开始时，Agent 只看到每个技能的名字和描述 —— 大概每个技能 100 个 token。只有当 Agent 判断这个技能跟当前任务相关时，才会加载 `SKILL.md` 的完整正文（通常不到 5,000 token）。`scripts/` 和 `references/` 里的辅助文件按需加载。正是这一点，让单个 Agent 能挂载上百个技能而不撑爆上下文窗口。

技能既不是 MCP 服务，也不是工具。MCP 定义的是 Agent 怎么连到外部系统 —— 鉴权、传输、工具发现。工具是 Agent 调用的一个个具体函数。技能定义的是**工作流** —— 连上之后该做什么、按什么顺序做、有什么护栏。在生产环境里这三层是一起跑的：**MCP 管接入，工具管动作，技能管行为。**

## 技能清单

> 以下 10 个分类共 184 条技能，每条都是「技能名 + 一句话介绍 + GitHub 链接」。**保留英文原文**（技能名是英文，介绍翻了对查找没帮助），点本页「对照原文」可看完整清单。

### 文档处理
Word / PDF / PPTX / Excel 的创建与编辑，以及 EPUB 转换、法律文书等专门场景。

### 开发与代码工具
写代码、调试、重构、前端构建等开发全流程技能。

### 数据与分析
数据处理、统计、可视化、报表相关技能。

### 商业与营销
营销文案、增长分析、商业计划等场景技能。

### 沟通与写作
写作、改写、邮件、报告等文字质量相关技能。

### 创意与媒体
图像、音频、视频等创意内容生成技能。

### 效率与整理
笔记、日程、任务管理、信息整理类技能。

### 协作与项目管理
项目跟踪、会议纪要、团队协作类技能。

### 安全与系统
安全审计、系统运维、合规检查类技能。

### 辅助技术
无障碍、特殊场景支持类技能。

### 通过 Composio 做应用自动化
通过 Composio 的 MCP 网关，让 Claude 在 1000+ 个第三方应用上执行真实动作（发邮件、建 issue、发帖等）。

## 上手使用

### 在 Claude.ai 里用技能

1. 点聊天界面里的技能图标（🧩）。
2. 从市场里添加技能，或上传自定义技能。
3. Claude 会根据你的任务自动激活相关技能。

### 在 Claude Code 里用技能

1. 把技能放进 `~/.config/claude-code/skills/`：
   ```bash
   mkdir -p ~/.config/claude-code/skills/
   cp -r skill-name ~/.config/claude-code/skills/
   ```

2. 检查技能元数据：
   ```bash
   head ~/.config/claude-code/skills/skill-name/SKILL.md
   ```

3. 启动 Claude Code：
   ```bash
   claude
   ```

4. 技能会自动加载，并在相关时被激活。

### 通过 API 使用技能

用 Claude Skills API 以编程方式加载和管理技能：

```python
import anthropic

client = anthropic.Anthropic(api_key="your-api-key")

response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    skills=["skill-id-here"],
    messages=[{"role": "user", "content": "Your prompt"}]
)
```

细节见 [Skills API 文档](https://docs.claude.com/en/api/skills-guide)。

## 创建技能

### 技能的结构

每个技能是一个文件夹，里面有一个带 YAML 前言的 `SKILL.md`：

```
skill-name/
├── SKILL.md          # 必填：技能指令与元数据
├── scripts/          # 可选：辅助脚本
├── templates/        # 可选：文档模板
└── resources/        # 可选：参考文件
```

### 技能基础模板

```markdown
---
name: my-skill-name
description: A clear description of what this skill does and when to use it.
---

# My Skill Name

Detailed description of the skill's purpose and capabilities.

## When to Use This Skill

- Use case 1
- Use case 2
- Use case 3

## Instructions

[Detailed instructions for Claude on how to execute this skill]

## Examples

[Real-world examples showing the skill in action]
```

### 技能最佳实践

- 聚焦在具体、可重复的任务上
- 给出清晰的示例和边界情况
- 指令是写给 **Claude** 看的，不是给终端用户看的
- 在 Claude.ai、Claude Code 和 API 上都测一遍
- 写清前置条件和依赖
- 包含出错处理的指引

## 参与贡献

我们欢迎贡献！请先读一遍我们的[贡献指南](CONTRIBUTING.md)，了解：

- 怎么提交新技能
- 技能质量的标准
- PR 的流程
- 行为准则

### 快速贡献步骤

1. 确保你的技能基于一个真实用例
2. 检查现有技能里有没有重复
3. 遵循技能结构模板
4. 在多个平台上测试你的技能
5. 带着清晰的文档提交 PR

## 资源

### 官方文档

- [Claude Skills 总览](https://www.anthropic.com/news/skills) —— 官方发布公告与功能说明
- [技能用户指南](https://support.claude.com/en/articles/12512180-using-skills-in-claude) —— 怎么在 Claude 里用技能
- [创建自定义技能](https://support.claude.com/en/articles/12512198-creating-custom-skills) —— 技能开发指南
- [Skills API 文档](https://docs.claude.com/en/api/skills-guide) —— API 集成指南
- [Agent Skills 博客](https://anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) —— 工程深度解析

### 社区资源

- [Anthropic 技能仓库](https://github.com/anthropics/skills) —— 官方示例技能
- [Claude 社区](https://community.anthropic.com) —— 跟其他用户讨论技能
- [技能市场](https://claude.ai/marketplace) —— 发现和分享技能

### 灵感与用例

- [Lenny's Newsletter](https://www.lennysnewsletter.com/p/everyone-should-be-using-claude-code) —— 人们用 Claude Code 的 50 种方式
- [Notion Skills](https://www.notion.so/notiondevs/Notion-Skills-for-Claude-28da4445d27180c7af1df7d8615723d0) —— Notion 集成技能
- [Top Claude Skills](https://composio.dev/content/top-claude-skills)

## 加入社区

- [加入我们的 Discord](https://discord.com/invite/composio) —— 跟其他在做 Claude Skills 的开发者聊天
- [关注 Twitter/X](https://x.com/composio) —— 第一时间了解新技能和新功能
- 有问题？写信到 [support@composio.dev](mailto:support@composio.dev)

---

<p align="center">
  <b>加入 20,000+ 位正在打造「能交付」的 Agent 的开发者</b>
</p>

<p align="center">
  <a href="https://platform.composio.dev/?utm_source=Github&utm_content=AwesomeSkills">
    <img src="https://img.shields.io/badge/Get_Started_Free-4F46E5?style=for-the-badge" alt="免费开始"/>
  </a>
</p>

## 许可证

本仓库以 Apache License 2.0 授权。

各个技能可能有不同的许可证 —— 请查看每个技能文件夹里的具体授权信息。

---

**说明**：Claude Skills 可跨 Claude.ai、Claude Code 和 Claude API 使用。一旦你创建了一个技能，它就可以在所有平台上通用，让你在各处使用 Claude 时的工作流保持一致。
