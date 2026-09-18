> **本篇为「框架式翻译」。**
> 原文共 2.3 万英文词，其中绝大部分是几百条一行式的链接清单（每条 = 项目名 + 一句话介绍）。
> 逐字翻译这些清单的阅读价值很低——链接本身才是主体。
> 因此本篇翻译：**标题与说明全翻 · 目录全翻 · 「从这里开始」和「Anthropic 官方」两节全翻 · 其余章节保留中文标题与范围说明，正文清单保留英文原文**（点「对照原文」可看完整清单）。

![Awesome Claude Code](assets/awesome-claude-code-banner.png)

<!-- Awesome Claude Code -->

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

_一份精心挑选的资源合集，献给最棒的 Agent —— [Claude Code](https://code.claude.com/docs/)，来自 [Anthropic PBC](https://github.com/anthropics/claude-code) 那支势不可挡的团队，是编程搭档里当之无愧的冠军。这里陈列着顶级的技能、多面手的 Agent、亮眼的状态栏、一流的开发者工具，对了，还有插件。新手和老手都适合，重点放在代码质量、安全性和原创性上。_

<br>

你现在看到的这一版列表，是带着一个明确目的发布的：**突出上一版里_没有_出现过的资源**，尤其是从推荐名单里做出的精选。不过这只是暂时的 —— 未来几周还会持续补充新资源，「历史」资源也会被迁移到新格式。所以，如果你之前上过榜而现在看不到自己的项目，原因就在这里 —— 那些仍在维护、依然优秀的历史资源很快会被加回来 —— 而在此期间，它们也被完整保留在 [README_ALTERNATIVES](README_ALTERNATIVES/) 目录里（只是不再更新）。

<br>

## Claude Code 行情条 —— GitHub 上各类 Claude Code 项目一览

<div align="center">

<picture>
  <img src="assets/repo-ticker.svg" alt="精选 Claude Code 项目" width="100%">
</picture>

</div>

## 最近新增

<div align="center">

<picture>
  <source media="(prefers-color-scheme: light)" srcset="assets/recently-added-light.svg">
  <img src="assets/recently-added.svg" alt="最近新增的资源" width="100%">
</picture>

</div>

# 目录

- [从这里开始](#从这里开始)
- [Anthropic 官方](#anthropic-官方)
- [文档、知识与学习](#文档知识与学习)
  - [Obsidian](#obsidian)
- [开源软件](#开源软件)
- [科研与学术探究](#科研与学术探究)
- [供应商、运行时与集成基础设施](#供应商运行时与集成基础设施)
- [远程控制、通知与语音输入输出](#远程控制通知与语音输入输出)
- [第三方客户端](#第三方客户端)
- [状态栏](#状态栏)
- [设计与 UI/UX](#设计与-uiux)
- [写作与文字质量](#写作与文字质量)
- [创意媒体](#创意媒体)
- [基础设施与 DevOps](#基础设施与-devops)
- [安全](#安全)
- [Agent 编排](#agent-编排)
  - [Ralph Wiggum](#ralph-wiggum)
  - [动态工作流](#动态工作流)
- [技能](#技能)
- [记忆与上下文持久化](#记忆与上下文持久化)
- [可观测性与监控](#可观测性与监控)
  - [会话监控器](#会话监控器)
  - [用量与成本](#用量与成本)
  - [可观测性](#可观测性)
- [配置](#配置)
- [测试](#测试)
- [代码检查](#代码检查)
- [多用途工具](#多用途工具)

---

## 从这里开始

- [A Field Guide to Claude Fable 5](https://claude.com/blog/a-field-guide-to-claude-fable-finding-your-unknowns)　作者 [Thariq Shihipar，Anthropic](https://github.com/ThariqS) —— 关于怎么跟 Claude Fable（以及跟 AI 本身）一起工作、一起思考，写得非常扎实、有洞见。文笔很好。有一点点拉姆斯菲尔德式认识论的味道，但总体是篇佳作。

- [andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills)　作者 [multica-ai](https://github.com/multica-ai) —— 一份直接可用的 `CLAUDE.md`，把「用大模型辅助写代码」的四条行为准则蒸馏进 Claude Code —— 低摩擦、见效快。灵感来自 Karpathy，源自 Andrej Karpathy 公开的关于大模型写代码的那些坑的笔记，由 multica-ai 编写。

- [Beyond the Prompt: Claude Code](https://arps18.github.io/posts/claude-code-mastery)　作者 [Arpan Patel](https://arps18.github.io/) —— 你要的这里都有。异常清晰、信息密度极高，是「Claude Code 的精华版」，新手、进阶用户、甚至你家宠物都看得懂。

- [Claude Code Guide](https://github.com/zebbern/claude-code-guide)　作者 [zebbern](https://github.com/zebbern) —— 一份最新的 Claude Code 单页速查手册：安装、环境变量、斜杠命令、MCP、钩子、子 Agent，跟官方更新日志保持同步。

- [Claude Code Hooks: Complete Guide](https://hidekazu-konishi.com/entry/claude_code_hooks_complete_guide.html)　作者 [Hidekazu Konishi](https://hidekazu-konishi.com) —— 逐个走一遍每种钩子事件：什么时候触发、两个返回通道、常见反模式，以及可以直接抄的 `settings.json` 示例。

- [Claude Code: Everything You Need to Know](https://github.com/wesammustafa/Claude-Code-Everything-You-Need-to-Know)　作者 [wesammustafa](https://github.com/wesammustafa) —— 一份「先建心智模型」的概念型入门读物，讲清 Claude Code 是什么、它的 Agent 循环怎么运作，然后层层铺开搭建、提示词工程工作流、技能、钩子、MCP、子 Agent 和 Agent 团队，还按经验水平给新手分了路径。

- [claude-howto](https://github.com/luongnv89/claude-howto)　作者 [luongnv89](https://github.com/luongnv89) —— 结构化的、分章节的 Claude Code 上手指南，带一份自测小测验和十个模块的渐进学习路径 —— 斜杠命令、记忆、技能、子 Agent、MCP、钩子、插件、检查点 —— 配有可视化图表和可复制粘贴的模板。

- [explore-claude-code](https://github.com/LukeRenton/explore-claude-code)　作者 [Luke Renton](https://github.com/LukeRenton) —— 一个可点击浏览的、带注解的 Claude Code 项目实例：每个文件和文件夹 —— `CLAUDE.md`、`settings.json`、规则、命令、技能、Agent、钩子、插件、`.mcp.json` —— 都是真实存在且被解释过的概念，用「实地认路」而不是长篇文字来教你这个工具的表面结构。

- [Learn Claude Code](https://github.com/shareAI-lab/learn-claude-code)　作者 [shareAI-lab](https://github.com/shareAI-lab) —— 一份非常有意思的分析，讲 Claude Code 这类编程 Agent 是怎么设计出来的。它尝试把一个 Agent 拆成最基本的零件，然后用最少的代码重新搭出来。很好的学习资料。最终产物是一个几百行 Python 写成的、带技能、子 Agent 和待办清单的简易 Agent。

- [Writing a Good CLAUDE.md](https://www.humanlayer.dev/blog/writing-a-good-claude-md)　作者 [HumanLayer](https://www.humanlayer.dev) —— 一篇讲 `CLAUDE.md` 手艺的文章：指令预算的权衡、渐进式展开，以及一条检验标准 —— 去掉某一行，Claude 会不会因此出错。

## Anthropic 官方

- [Agent Skills](https://github.com/anthropics/skills)　作者 [Anthropic](https://github.com/anthropics) —— Anthropic 官方的 Agent 技能仓库 —— `SKILL.md` 格式、一份技能模板和示例技能，跟 Claude Code 原生加载的是同一套格式。

- [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)　作者 [Anthropic](https://www.anthropic.com) —— Anthropic 关于 Agent 模式的基础分类法 —— 提示链、路由、编排者-工作者、评估者-优化者 —— 以及各自该在什么场景下用。

- [Claude Code Best Practices](https://code.claude.com/docs/en/best-practices)　作者 [Anthropic](https://code.claude.com/docs) —— Anthropic 官方的 Claude Code 高效使用指南：Agent 循环的心智模型、`CLAUDE.md` 用法和工作流模式。

- [Claude Code Cheatsheet](https://support.claude.com/en/articles/14553413-claude-code-cheatsheet)　作者 [Anthropic](https://support.claude.com) —— Anthropic 官方的 Claude Code 速查表 —— 核心词汇（会话、上下文窗口、`CLAUDE.md`）、内置斜杠命令和键盘快捷键的速查。

- [Claude Code GitHub Action](https://github.com/anthropics/claude-code-action)　作者 [Anthropic](https://github.com/anthropics) —— 官方的 GitHub Action，用来在 CI 里跑 Claude Code：在 issue 和 PR 里 @claude，就能把改代码、评审、修 bug 这些活派给它。

- [Claude Code Security Review](https://github.com/anthropics/claude-code-security-review)　作者 [Anthropic](https://github.com/anthropics) —— 官方的 AI 安全评审 GitHub Action，用 Claude 分析 PR 的 diff，找出漏洞。

- [Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)　作者 [Anthropic](https://www.anthropic.com) —— Anthropic 关于怎么经营上下文窗口的指南 —— 压缩、即时检索、记笔记 —— 这是长时间跑 Agent 能有效的底层基本功。

- [How Claude Code Works](https://code.claude.com/docs/en/how-claude-code-works)　作者 [Anthropic](https://code.claude.com/docs) —— 官方的概念讲解：Claude Code 的 Agent 循环、工具和上下文窗口，以及技能、钩子、子 Agent 是怎么一层层叠上去的。

- [How We Built Our Multi-Agent Research System](https://www.anthropic.com/engineering/multi-agent-research-system)　作者 [Anthropic](https://www.anthropic.com) —— 一份实操经验谈，讲编排者与子 Agent 的协同、提示设计和效果评估，能直接对应到 Claude Code 的子 Agent 和 Agent 团队上。

- [Official Plugin Directory](https://github.com/anthropics/claude-plugins-official)　作者 [Anthropic](https://github.com/anthropics) —— Anthropic 官方精选的高质量 Claude Code 插件目录，可以在 Claude Code 里直接安装。

- [Steering Claude Code: Skills, Hooks, Rules, Subagents and More](https://claude.com/blog/steering-claude-code-skills-hooks-rules-subagents-and-more)　作者 [Anthropic](https://claude.com/blog) —— 一套选择扩展机制的框架，围绕「确定性控制 vs 概率性控制」和「上下文隔离」这两个维度来组织。

---

## 其余章节（标题与范围说明）

以下各章收录的都是具体项目链接。**章节名已翻译，每条项目的英文介绍保留原文**（项目名、链接、作者名一律不动），想看完整清单请点本页面上的「对照原文」开关。

### [文档、知识与学习](#文档知识与学习)
教程、指南、速查表、知识库这类用来「学明白」的资源。含 [Obsidian](#obsidian) 子章节（把 Claude Code 接进 Obsidian 笔记库的方案）。

### [开源软件](#开源软件)
围绕 Claude Code 生态的开源项目与工具。

### [科研与学术探究](#科研与学术探究)
用 Claude Code 做文献检索、实验分析、学术写作这类科研向的资源。

### [供应商、运行时与集成基础设施](#供应商运行时与集成基础设施)
模型供应商接入、运行时环境、以及把 Claude Code 接到别的系统上的基础设施。

### [远程控制、通知与语音输入输出](#远程控制通知与语音输入输出)
远程操控、消息推送、以及语音输入 / 语音播报相关的工具。

### [第三方客户端](#第三方客户端)
非官方的 Claude Code 客户端与替代界面。

### [状态栏](#状态栏)
定制 Claude Code 底部状态栏的方案（显示上下文占用、当前模型、花费等）。

### [设计与 UI/UX](#设计与-uiux)
让 Claude Code 参与界面设计、产出 UI 稿的资源。

### [写作与文字质量](#写作与文字质量)
提升 Claude 写作质量的提示词、规则与工具。

### [创意媒体](#创意媒体)
图像、视频、音频等创意内容生成相关的资源。

### [基础设施与 DevOps](#基础设施与-devops)
部署、容器、CI/CD、运维相关的工具与配置。

### [安全](#安全)
权限控制、沙箱、漏洞扫描、提示词注入防护等安全相关资源。

### [Agent 编排](#agent-编排)
多 Agent 协同编排的方案，含两个子章节：
- [Ralph Wiggum](#ralph-wiggum) —— 自主循环迭代的 Agent 模式
- [动态工作流](#动态工作流) —— 可编排的动态工作流

### [技能](#技能)
各类 `SKILL.md` 技能包与技能合集。

### [记忆与上下文持久化](#记忆与上下文持久化)
跨会话记忆、上下文压缩与持久化方案。

### [可观测性与监控](#可观测性与监控)
三个子章节：
- [会话监控器](#会话监控器) —— 实时监控会话状态
- [用量与成本](#用量与成本) —— token 消耗与费用统计
- [可观测性](#可观测性) —— 日志、追踪与指标

### [配置](#配置)
`settings.json` 等配置文件的最佳实践与示例。

### [测试](#测试)
自动化测试、测试生成相关资源。

### [代码检查](#代码检查)
Lint、格式化、静态检查相关资源。

### [多用途工具](#多用途工具)
横跨多个场景的综合性工具。
