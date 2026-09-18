<p align="center">
  <a href="https://graphify.com"><img src="https://raw.githubusercontent.com/Graphify-Labs/graphify/v8/docs/graphify-logo.png" width="480" height="252" alt="Graphify"/></a>
</p>

<p align="center">
  <a href="https://trendshift.io/repositories/25296?utm_source=repository-badge&amp;utm_medium=badge&amp;utm_campaign=badge-repository-25296" target="_blank" rel="noopener noreferrer"><img src="https://trendshift.io/api/badge/repositories/25296" alt="Graphify-Labs%2Fgraphify | Trendshift" width="250" height="55"/></a>
</p>

<div align="center">
<details><summary><b>用其它语言阅读本文</b></summary>

🇺🇸 <a href="README.md">English</a> | 🇨🇳 <a href="docs/translations/README.zh-CN.md">简体中文</a> | 🇯🇵 <a href="docs/translations/README.ja-JP.md">日本語</a> | 🇰🇷 <a href="docs/translations/README.ko-KR.md">한국어</a> | 🇩🇪 <a href="docs/translations/README.de-DE.md">Deutsch</a> | 🇫🇷 <a href="docs/translations/README.fr-FR.md">Français</a> | 🇪🇸 <a href="docs/translations/README.es-ES.md">Español</a> | 🇮🇳 <a href="docs/translations/README.hi-IN.md">हिन्दी</a> | 🇧🇷 <a href="docs/translations/README.pt-BR.md">Português</a> | 🇷🇺 <a href="docs/translations/README.ru-RU.md">Русский</a> | 🇸🇦 <a href="docs/translations/README.ar-SA.md">العربية</a> | 🇮🇷 <a href="docs/translations/README.fa-IR.md">فارسی</a> | 🇮🇹 <a href="docs/translations/README.it-IT.md">Italiano</a> | 🇵🇱 <a href="docs/translations/README.pl-PL.md">Polski</a> | 🇳🇱 <a href="docs/translations/README.nl-NL.md">Nederlands</a> | 🇹🇷 <a href="docs/translations/README.tr-TR.md">Türkçe</a> | 🇺🇦 <a href="docs/translations/README.uk-UA.md">Українська</a> | 🇻🇳 <a href="docs/translations/README.vi-VN.md">Tiếng Việt</a> | 🇮🇩 <a href="docs/translations/README.id-ID.md">Bahasa Indonesia</a> | 🇸🇪 <a href="docs/translations/README.sv-SE.md">Svenska</a> | 🇬🇷 <a href="docs/translations/README.el-GR.md">Ελληνικά</a> | 🇷🇴 <a href="docs/translations/README.ro-RO.md">Română</a> | 🇨🇿 <a href="docs/translations/README.cs-CZ.md">Čeština</a> | 🇫🇮 <a href="docs/translations/README.fi-FI.md">Suomi</a> | 🇩🇰 <a href="docs/translations/README.da-DK.md">Dansk</a> | 🇳🇴 <a href="docs/translations/README.no-NO.md">Norsk</a> | 🇭🇺 <a href="docs/translations/README.hu-HU.md">Magyar</a> | 🇹🇭 <a href="docs/translations/README.th-TH.md">ภาษาไทย</a> | 🇺🇿 <a href="docs/translations/README.uz-UZ.md">Oʻzbekcha</a> | 🇹🇼 <a href="docs/translations/README.zh-TW.md">繁體中文</a> | 🇵🇭 <a href="docs/translations/README.fil-PH.md">Filipino</a> | 🇮🇱 <a href="docs/translations/README.he-IL.md">עברית</a>

</details>
</div>

<p align="center">
  <a href="https://pypi.org/project/graphifyy/"><img src="https://img.shields.io/pypi/v/graphifyy" alt="PyPI"/></a>
  <a href="https://pepy.tech/project/graphifyy"><img src="https://img.shields.io/pepy/dt/graphifyy?color=blue&label=downloads" alt="下载量"/></a>
  <a href="https://discord.gg/2DDrEgvZb4"><img src="https://img.shields.io/badge/Discord-Join-5865F2?style=flat&logo=discord&logoColor=white" alt="Discord"/></a>
  <a href="https://www.youtube.com/@graphifylabs"><img src="https://img.shields.io/badge/YouTube-Graphify%20Labs-FF0000?style=flat&logo=youtube&logoColor=white" alt="YouTube"/></a>
  <a href="https://www.linkedin.com/company/graphify-labs"><img src="https://img.shields.io/badge/LinkedIn-Graphify%20Labs-0077B5?logo=linkedin" alt="LinkedIn"/></a>
  <a href="https://www.ycombinator.com/companies/graphify-labs"><img src="https://img.shields.io/badge/Y%20Combinator-S26-F0652F?style=flat&logo=ycombinator&logoColor=white" alt="YC S26"/></a>
</p>

<p align="center">
  <b>graphify 平台在公开 v1 发布之前已开放抢先体验：<a href="https://app.graphify.com/login">app.graphify.com</a></b>
</p>

在你的 AI 编程助手里敲一句 `/graphify`，它就会把你的整个项目（代码、文档、PDF、图片、视频）映射成一张**知识图谱**，让你**用提问代替在文件里 grep**。

- **代码建图免费，且完全本地。** 代码用 tree-sitter 的 AST（抽象语法树）来解析：确定性结果、不调大模型、一个字节都不离开你的机器。（文档、PDF、图片和视频会用到你助手的模型，或者你配的 API Key，做一遍语义提取。）
- **每一条连线都有解释。** 每条关系都带 `EXTRACTED`（源码里明写的）或 `INFERRED`（由 graphify 推理出来的）标签，所以你能分清哪些是原文读到的、哪些是推断出来的。
- **它不是向量索引。** 没有嵌入，没有向量库：这是一张你可以真正遍历的图。提一个问题、追两个东西之间的路径，或者解释某一个概念。

> 想要它一直开着、在后台持续更新你的代码、文档和会议记录，而不是只有你喊它时才动一下？这就是我们在 **[graphify.com](https://graphify.com)** 正在做的东西，抢先体验现已开放：**[app.graphify.com](https://app.graphify.com/login)**。

<p align="center">
  <img src="https://raw.githubusercontent.com/Graphify-Labs/graphify/v8/docs/graph-hero.png" alt="graphify 的交互式 graph.html：把 FastAPI 代码库画成一张力导向知识图谱，带检测出的社群图例" width="900">
</p>
<p align="center">
  <em>由 graphify 映射出来的 FastAPI 代码库。每个节点是一个概念，颜色是检测出的社群，整张图在 graph.html 里可以点。</em>
</p>

**开始用**（30 秒）：

```bash
uv tool install graphifyy      # 装命令行工具（或者：pipx install graphifyy）
graphify install               # 把技能注册到你的 AI 助手里
```

然后在你的 AI 助手里：

```
/graphify .
```

就这样。你会拿到**三个文件**：

```
graphify-out/
├── graph.html       用浏览器打开 —— 点节点、筛选、搜索
├── GRAPH_REPORT.md  精华摘要：关键概念、出人意料的联系、建议追问的问题
└── graph.json       完整图谱 —— 随时可以查询，不用再翻一遍你的文件
```

**支持** Claude Code、Cursor、Codex、Gemini CLI、GitHub Copilot 以及另外 15+ 个平台 —— [挑你的平台](#install)。

---

## 看它实际跑起来

<p align="center">
  <img src="https://raw.githubusercontent.com/Graphify-Labs/graphify/v8/docs/demo-path.svg" alt="graphify 路径查询：终端问 FastAPI 到 ModelField 之间的最短路径，答案在知识图谱上一跳一跳地亮起来" width="900">
</p>

图建好之后，你就查它，而不是读文件。下面是真实输出，graphify 跑在前面那张图所示的 FastAPI 代码库上：

```text
$ graphify explain "APIRouter"
Node: APIRouter
  Source:    routing.py L2210
  Community: 2
  Degree:    47

Connections (47):
  --> RequestValidationError [uses] [INFERRED]
  --> Dependant [uses] [INFERRED]
  --> .get() [method] [EXTRACTED]
  <-- __init__.py [imports] [EXTRACTED]
  ...

$ graphify path "FastAPI" "ModelField"
Shortest path (3 hops):
  FastAPI --uses--> DefaultPlaceholder <--references-- get_request_handler() --references--> ModelField
```

每条边都带一个**置信标签**（`EXTRACTED` = 源码里明写的，`INFERRED` = 推理出来的），所以你能分清哪些是直接读到的、哪些是推断的。`graphify query "<问题>"` 会用大白话问题返回一个范围化的子图，`graphify path A B` 则追踪任意两个东西是怎么连起来的。

---

## 它能做什么

开箱即得的能力：

| 能力 | 你能得到什么 |
|---|---|
| **枢纽节点（God nodes）** | 连接最多的那些概念，让你看清一切都流经哪里 |
| **社群（Communities）** | 把图切成子系统（Leiden 算法），标签不靠大模型生成 |
| **跨文件关联** | 通过 tree-sitter 的 AST，在约 40 种语言上解析出 `calls` / `imports` / `inherits` / `mixes_in` |
| **查询、路径、解释** | 提问题、追两个东西之间的路径、解释一个概念，全部对着 `graph.json` 做 |
| **设计意图 + 文档引用** | `# NOTE:` / `# WHY:` 这类注释和 ADR/RFC 引用会被抽成一等节点，并连到它们所解释的代码上 |
| **不止代码** | 文档、PDF、图片、视频/音频全都映射进同一张图 |
| **本地优先** | 代码用 tree-sitter 在本地解析（不调大模型，数据不出你的机器）；只有对文档/媒体做语义提取时才调后端，而且只在你配了后端的情况下 |

---

## 基准测试

| 基准 | 指标 | graphify | 同场对比 |
|---|---|---|---|
| LOCOMO (n=300) | recall@10 | **0.497** | mem0 0.048，supermemory 0.149 |
| LOCOMO (n=300) | 问答准确率 | 45.3% | supermemory 49.7%，mem0 27.3% |
| LongMemEval-S (n=50) | 问答准确率 | **76%** | 与稠密 RAG 打平 |
| 建图 | 大模型额度消耗 | **0** | 大多数系统是按 token 计费 |

所有系统跑在同一套测试架上、用同一个模型和同样的预算，由一位裁判打分，并用第二位裁判做盲校验（一致率 90.6%，Cohen's kappa 0.81）。完整的分系统表格、代码智能那一项的结果，以及复现命令：**[BENCHMARKS.md](./BENCHMARKS.md)**。

---

## 前置条件

| 要求 | 最低版本 | 怎么查 | 怎么装 |
|---|---|---|---|
| Python | 3.10+ | `python --version` | [python.org](https://www.python.org/downloads/) |
| uv *（推荐）* | 任意 | `uv --version` | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| pipx *（备选）* | 任意 | `pipx --version` | `pip install pipx` |

**macOS 快速安装（Homebrew）：**
```bash
brew install python@3.12 uv
```

**Windows 快速安装：**
```powershell
winget install astral-sh.uv
```

**Ubuntu/Debian：**
```bash
sudo apt install python3.12 python3-pip pipx
# 或者装 uv：
curl -LsSf https://astral.sh/uv/install.sh | sh
```

---

## 安装

> **官方包：** PyPI 上的包名是 `graphifyy`（两个 y）。PyPI 上其它 `graphify*` 包都跟本项目无关。命令行命令仍然叫 `graphify`。

**第一步 —— 装包：**

```bash
# 推荐（独立环境；如果装完找不到 'graphify'，跑：uv tool update-shell）：
uv tool install graphifyy

# 备选：
pipx install graphifyy
pip install graphifyy  # 可能需要配 PATH —— 见下面说明
```

**第二步 —— 把技能注册到你的 AI 助手：**

```bash
graphify install
```

就这样。打开你的 AI 助手，输入 `/graphify .`

想把助手技能装进当前仓库而不是你的用户配置目录，加 `--project`：

```bash
graphify install --project
graphify install --project --platform codex
```

项目级安装会写在当前目录下，比如 `.claude/skills/graphify/SKILL.md` 或 `.agents/skills/graphify/SKILL.md`（外加一个技能按需加载的 `references/` 附带目录），并会为可提交的文件打印一条 `git add` 提示。支持项目级安装的各平台命令用同样的参数，比如 `graphify claude install --project` 或 `graphify codex install --project`。

> **PowerShell 说明：** 用 `graphify .` 而不是 `/graphify .` —— 在 PowerShell 里前置的斜杠是路径分隔符。

> **`graphify: command not found`（找不到命令）？** `uv tool install` / `pipx install` 把 `graphify` 命令放在它们的工具 bin 目录（`~/.local/bin`）。如果刚装完你的 shell 找不到它 —— 在全新的 macOS + zsh 环境上很常见 —— 说明那个目录还没进 `PATH`：跑 `uv tool update-shell`（或 `pipx ensurepath`），然后开一个新终端。用裸 `pip` 的话，把 `~/.local/bin`（Linux）或 `~/Library/Python/3.x/bin`（Mac）加进 PATH，或者跑 `python -m graphify`。

> **用 `uvx` / `uv tool run` 跑而不安装？** 要写包名，不是命令名：`uvx --from graphifyy graphify install`。直接 `uvx graphify …` 会失败（`No solution found … no versions of graphify`），因为 `uv tool run` 把第一个词当成*包名*，而包名是 `graphifyy` —— `graphify` 命令只是在它里面。

> **尽量避免在 Mac/Windows 上用 `pip install`。** 技能会在运行时从 `graphify-out/.graphify_python` 解析 Python 解释器；如果它指向的环境跟 `pip` 装包的那个环境不是同一个，你会得到 `ModuleNotFoundError: No module named 'graphify'`。`uv tool install` 和 `pipx install` 会把包隔离在自己的环境里，彻底避开这个问题。

> **Git 钩子与 uv tool / pipx：** `graphify hook install` 会在安装时把当前的解释器路径直接写进钩子脚本，所以即使在 `~/.local/bin` 不在 PATH 上的图形化 git 客户端和 CI 运行器里，提交后钩子也能正常触发。如果你重装或升级了 graphify，重新跑一次 `graphify hook install` 来刷新写入的路径。

> **严格模式（Claude Code）：** `graphify install --project --strict` 会让助手真正去用这张图。默认安装是*劝导*它在读文件之前先跑 `graphify query`；严格模式会*拦掉*会话中第一次裸读源码的操作，把它重定向到图上，然后退回劝导模式（所以每次会话最多触发一次，不会卡住）。运行时可以用 `GRAPHIFY_HOOK_STRICT=1`/`0` 切换；默认安装行为不变（软劝导）。

<details>
<summary><b>挑你的平台</b>（20+ 个助手，点击展开）</summary>

| 平台 | 安装命令 |
|----------|----------------|
| Claude Code (Linux/Mac) | `graphify install` |
| Claude Code (Windows) | `graphify install`（自动识别）或 `graphify install --platform windows` |
| CodeBuddy | `graphify install --platform codebuddy` |
| Codex | `graphify install --platform codex` |
| OpenCode | `graphify install --platform opencode` |
| Kilo Code | `graphify install --platform kilo` |
| GitHub Copilot CLI | `graphify install --platform copilot` |
| VS Code Copilot Chat | `graphify vscode install` |
| Aider | `graphify install --platform aider` |
| OpenClaw | `graphify install --platform claw` |
| Factory Droid | `graphify install --platform droid` |
| Trae | `graphify install --platform trae` |
| Trae CN | `graphify install --platform trae-cn` |
| Gemini CLI | `graphify install --platform gemini` |
| Hermes | `graphify install --platform hermes` |
| Kimi Code | `graphify install --platform kimi` |
| Amp | `graphify amp install` |
| Agent Skills（跨框架） | `graphify install --platform agents`（别名 `--platform skills`） |
| Kiro IDE/CLI | `graphify kiro install` |
| Pi 编程 Agent | `graphify install --platform pi` |
| Cursor | `graphify cursor install` |
| Devin CLI | `graphify devin install` |
| Google Antigravity | `graphify antigravity install` |

Codex 用户还需要在 `~/.codex/config.toml` 的 `[features]` 下加 `multi_agent = true`，才能做并行提取。CodeBuddy 用的是跟 Claude Code 一样的 Agent 工具和 PreToolUse 钩子机制。Factory Droid 用 `Task` 工具做并行子 Agent 派发。OpenClaw 和 Aider 走串行提取（这两个平台上的并行 Agent 支持还比较早期）。Trae 用 Agent 工具做并行子 Agent 派发，并且**不支持** `PreToolUse` 钩子，所以 `AGENTS.md` 是它那个平台上「始终生效」的机制。

`--platform agents`（别名 `--platform skills`）面向通用的跨框架 [Agent-Skills](https://github.com/anthropics/skills) 位置：全局安装写到规范里的用户级 `~/.agents/skills/`（会被 `npx skills` 和符合规范的框架读取），项目级（`--project`）安装写到 `./.agents/skills/`。裸跑 `graphify install` 按设计仍是单平台（Claude Code）—— 当你想让任何读 `.agents/skills` 的框架都能发现这个技能时，用指定的 `agents` 平台。

> Codex 用的是 `$graphify` 而不是 `/graphify`。

</details>

<details>
<summary><b>可选扩展</b>（只装你需要的）</summary>

| 扩展 | 加了什么 | 安装 |
|---|---|---|
| `pdf` | PDF 提取 | `uv tool install "graphifyy[pdf]"` |
| `office` | 支持 `.docx` 和 `.xlsx` | `uv tool install "graphifyy[office]"` |
| `google` | Google Sheets 渲染 | `uv tool install "graphifyy[google]"` |
| `video` | 视频/音频转写（faster-whisper + yt-dlp） | `uv tool install "graphifyy[video]"` |
| `mcp` | MCP stdio 服务 | `uv tool install "graphifyy[mcp]"` |
| `neo4j` | 支持推送到 Neo4j | `uv tool install "graphifyy[neo4j]"` |
| `falkordb` | 支持推送到 FalkorDB | `uv tool install "graphifyy[falkordb]"` |
| `svg` | 导出 SVG 图 | `uv tool install "graphifyy[svg]"` |
| `leiden` | Leiden 社群检测（Python < 3.13 用 graspologic；3.13+ 用原生后端） | `uv tool install "graphifyy[leiden]"` |
| `ollama` | Ollama 本地推理 | `uv tool install "graphifyy[ollama]"` |
| `openai` | OpenAI / OpenAI 兼容 API | `uv tool install "graphifyy[openai]"` |
| `gemini` | Google Gemini API | `uv tool install "graphifyy[gemini]"` |
| `anthropic` | Anthropic Claude API（`--backend claude`，用 `ANTHROPIC_API_KEY`） | `uv tool install "graphifyy[anthropic]"` |
| `bedrock` | AWS Bedrock（用 IAM，不需要 API Key） | `uv tool install "graphifyy[bedrock]"` |
| `azure` | Azure OpenAI Service（`--backend azure`，用 `AZURE_OPENAI_API_KEY` + `AZURE_OPENAI_ENDPOINT`） | `uv tool install "graphifyy[openai]"` |
| `sql` | SQL 表结构提取 | `uv tool install "graphifyy[sql]"` |
| `postgres` | 在线 PostgreSQL 内省（`--postgres DSN`） | `uv tool install "graphifyy[postgres]"` |
| `dm` | BYOND DreamMaker `.dm`/`.dme` AST 提取（如果没有匹配你平台的 wheel，可能需要 C 编译器 + `python3-dev`） | `uv tool install "graphifyy[dm]"` |
| `terraform` | Terraform / HCL `.tf`/`.tfvars`/`.hcl` AST 提取 | `uv tool install "graphifyy[terraform]"` |
| `pascal` | Pascal / Delphi `.pas`/`.dpr`/`.dpk`/`.inc` AST 提取（`calls`/`inherits` 边更准；没装时退回正则提取器） | `uv tool install "graphifyy[pascal]"` |
| `ocaml` | OCaml `.ml`/`.mli` AST 提取 | `uv tool install "graphifyy[ocaml]"` |
| `commonlisp` | Common Lisp `.lisp`/`.cl`/`.lsp`/`.asd` AST 提取 | `uv tool install "graphifyy[commonlisp]"` |
| `robot` | Robot Framework `.robot`/`.resource` 提取（套件、测试用例、关键字、关键字调用和 resource/library 导入边） | `uv tool install "graphifyy[robot]"` |
| `chinese` | 中文查询分词（jieba） | `uv tool install "graphifyy[chinese]"` |
| `all` | 以上全部 | `uv tool install "graphifyy[all]"` |

</details>

---

## 让你的助手一直用这张图

建好图之后，在项目里跑一次这个：

| 平台 | 命令 |
|----------|---------|
| Claude Code | `graphify claude install` |
| CodeBuddy | `graphify codebuddy install` |
| Codex | `graphify codex install` |
| OpenCode | `graphify opencode install` |
| Kilo Code | `graphify kilo install` |
| GitHub Copilot CLI | `graphify copilot install` |
| VS Code Copilot Chat | `graphify vscode install` |
| Aider | `graphify aider install` |
| OpenClaw | `graphify claw install` |
| Factory Droid | `graphify droid install` |
| Trae | `graphify trae install` |
| Trae CN | `graphify trae-cn install` |
| Cursor | `graphify cursor install` |
| Gemini CLI | `graphify gemini install` |
| Hermes | `graphify hermes install` |
| Kimi Code | `graphify install --platform kimi` |
| Amp | `graphify amp install` |
| Agent Skills（跨框架） | `graphify agents install`（别名 `graphify skills install`） |
| Kiro IDE/CLI | `graphify kiro install` |
| Pi 编程 Agent | `graphify pi install` |
| Devin CLI | `graphify devin install` |
| Google Antigravity | `graphify antigravity install` |

这会写一个很小的配置文件，告诉你的助手：遇到代码库相关问题先去查知识图谱，优先用 `graphify query "<问题>"` 这种范围化查询，而不是去读完整的报告或者 grep 原始文件。

- **钩子型平台**（Claude Code、Gemini CLI）：钩子会在搜索类工具调用之前自动触发（在 Claude Code 上，还包括在用 Read/Glob 工具逐个读源码文件之前），把你的助手往「走图」这条路上推。
- **指令文件型平台**（Codex、OpenCode、Cursor 等）：靠常驻的指令文件（`AGENTS.md`、`.cursor/rules/` 等）提供同样的「先查询」引导。

`GRAPH_REPORT.md` 仍然保留，供大范围架构review使用。

**CodeBuddy** 做跟 Claude Code 一样的两件事：写一个 `CODEBUDDY.md` 片段，让 CodeBuddy 在回答架构问题之前先读 `graphify-out/GRAPH_REPORT.md`；并安装 `PreToolUse` 钩子（`.codebuddy/settings.json`），在 Bash 搜索命令和文件读取之前触发，把它推向 `graphify query`。

**Codex** 写到 `AGENTS.md` —— 在这个平台上，真正承载「始终生效的图引导」的就是它。`graphify codex install` 也会在 `.codex/hooks.json` 里注册一个 `PreToolUse` 钩子（`graphify hook-check`），但那条记录是**故意留空操作**的：Codex Desktop 会拒绝 `PreToolUse` 上的 `hookSpecificOutput.additionalContext`，所以在那儿输出引导会直接把 Bash 工具调用搞坏。跟 Claude Code（钩子 `graphify hook-guard` 负责劝导）不同，在 Codex 上钩子会触发但故意什么都不做，`AGENTS.md` 才是始终生效的机制。

**Kilo Code** 把 Graphify 技能装到 `~/.config/kilo/skills/graphify/SKILL.md`，并把一个原生 `/graphify` 命令装到 `~/.config/kilo/command/graphify.md`。`graphify kilo install` 还会写 `AGENTS.md` 外加一个原生 `tool.execute.before` 插件（`.kilo/plugins/graphify.js` 加 `.kilo/kilo.json` 或 `.kilo/kilo.jsonc` 注册），这样 Kilo 就通过原生 `.kilo` 配置获得了同样的「始终提醒用图」行为。

**Cursor** 写 `.cursor/rules/graphify.mdc`，带 `alwaysApply: true`，所以 Cursor 会在每次对话里自动带上它，不需要钩子。

想一次性从所有平台移除 graphify：`graphify uninstall`（加 `--purge` 会连 `graphify-out/` 一起删掉）。也可以用分平台的命令（比如 `graphify claude uninstall`）。

---

## 报告里有什么

- **枢纽节点** —— 你项目里连接最多的那些概念。一切都流经它们。
- **出人意料的联系** —— 那些分居不同文件或模块、但竟然有关联的东西。按「有多意外」排序。
- **「为什么」** —— 行内注释（`# NOTE:`、`# WHY:`、`# HACK:`）、文档字符串，以及文档里的设计意图，会被抽成独立节点，并连到它们所解释的代码上。
- **建议追问的问题** —— 4~5 个「这张图特别适合回答」的问题。
- **置信标签** —— 每一条推断出来的关系都会标上 `EXTRACTED`、`INFERRED` 或 `AMBIGUOUS`。你永远分得清哪些是查到的、哪些是猜的。

---

## 它处理哪些文件

| 类型 | 扩展名 |
|------|-----------|
| 代码（37 种 tree-sitter 语法） | `.py .ts .mts .cts .js .jsx .tsx .mjs .go .rs .java .c .cpp .cc .cxx .h .hpp .cu .cuh .metal .rb .cs .kt .kts .scala .php .swift .lua .luau .toc .zig .ps1 .psm1 .psd1 .ex .exs .m .mm .ml .mli .jl .vue .svelte .astro .groovy .gradle .dart .v .sv .svh .sql .f .f90 .f95 .f03 .f08 .pas .pp .dpr .dpk .lpr .inc .dfm .lfm .lpk .sh .bash .json .dm .dme .dmi .dmm .dmf .sln .slnx .csproj .fsproj .vbproj .xaml .razor .cshtml`（`.dm`/`.dme` 需要 `uv tool install graphifyy[dm]`，`.ml`/`.mli` 需要 `uv tool install graphifyy[ocaml]`；`.mts`/`.cts` 复用 TypeScript 语法，`.cc`/`.cxx`、CUDA 的 `.cu`/`.cuh` 和 Metal 的 `.metal` 复用 C++ 语法） |
| Salesforce Apex | `.cls .trigger`（基于正则；类、接口、枚举、方法、触发器、SOQL/DML 边） |
| Terraform / HCL | `.tf .tfvars .hcl`（需要 `uv tool install graphifyy[terraform]`） |
| OCaml | `.ml .mli`（需要 `uv tool install graphifyy[ocaml]`） |
| Common Lisp | `.lisp .cl .lsp .asd`（需要 `uv tool install graphifyy[commonlisp]`） |
| Robot Framework | `.robot .resource`（通过官方 `robot.api` 解析器，需要 `uv tool install graphifyy[robot]`；套件、测试用例、用户关键字、关键字调用和 Resource/Library/Variables 导入边） |
| MCP 配置 | `.mcp.json` `mcp.json` `mcp_servers.json` `claude_desktop_config.json` —— 抽出服务节点、包引用、所需环境变量 |
| 包清单 | `apm.yml` `pyproject.toml` `go.mod` `pom.xml` —— 每个包（按名字）生成一个规范节点外加 `depends_on` 边，所以被多个清单引用的包只形成单一枢纽 |
| 文档 | `.md .mdx .qmd .html .txt .rst .yaml .yml`（markdown 的 `[文字](./other.md)` 链接和 `[[双链]]` 会变成文档之间的 `references` 边） |
| Office | `.docx .xlsx`（需要 `uv tool install graphifyy[office]`） |
| Google Workspace | `.gdoc .gsheet .gslides`（需主动开启；需要 `gws` 鉴权和 `--google-workspace`；Sheets 需要 `uv tool install graphifyy[google]`） |
| PDF | `.pdf` |
| 图片 | `.png .jpg .webp .gif` |
| 视频 / 音频 | `.mp4 .mov .mp3 .wav` 等（需要 `uv tool install graphifyy[video]`） |
| YouTube / 网址 | 任意视频链接（需要 `uv tool install graphifyy[video]`） |

带字面量本地 `source`（`./...` 或 `../...`）的 Terraform 模块调用，会通过一条 `EXTRACTED` 的 `module_source` 边连到一个目录模块节点上。每个目录节点包含它扫描到的 `.tf` 文件，所以嵌套调用会暴露出「环境 → 应用 → 基座 → 资源」这样的路径。扫描公共的仓库根目录，可以把调用方和实现方都纳进来。路径相对调用模块解析，被排除的或根目录之外的文件不会被隐式加载。

远端 source 和 source 表达式不会被解析；`.tfvars`、通用 `.hcl` 和 `.tf.json` 文件不定义模块来源目标。`module.app.output` 这样的引用仍然指向模块调用，而不是它实现里的输出。这张图表示的是源码配置，不是求值后的 Terraform 实例。增量式的 Terraform 改动会对已扫描的 `.tf` 语料做调和，未改动的文件复用缓存的语法树。升级已有的图之后，跑一次 `graphify update .` 来重新生成 Terraform 的 ID 和拓扑。

代码是**在本地提取、不调任何 API** 的（通过 tree-sitter 的 AST）。其它一切都走你 AI 助手的模型 API。

Google Drive 桌面版里的 `.gdoc`、`.gsheet`、`.gslides` 文件只是快捷方式指针，不是文档内容。想在无界面提取里纳入原生 Google Docs、Sheets 和 Slides，先安装并鉴权 [`gws` CLI](https://github.com/googleworkspace/cli)，然后跑：

```bash
uv tool install "graphifyy[google]"  # Google Sheets 表格渲染需要
gws auth login -s drive
graphify extract ./docs --google-workspace
```

你也可以设 `GRAPHIFY_GOOGLE_WORKSPACE=1`。Graphify 会把快捷方式导出成 `graphify-out/converted/` 里的 Markdown 附带文件，然后再提取这些文件。

---

## 常用命令

```bash
/graphify .                        # 为当前文件夹建图
/graphify ./docs --update          # 只重新提取改动过的文件
/graphify . --cluster-only         # 不重新提取，只重跑聚类
/graphify . --cluster-only --resolution 1.5      # 更细粒度的社群
/graphify . --cluster-only --exclude-hubs 99     # 从枢纽节点排名里压掉工具型超级枢纽
/graphify . --no-viz               # 跳过 HTML，只要报告 + JSON
/graphify . --wiki                 # 从图生成一份 markdown wiki
graphify export callflow-html      # Mermaid 架构/调用流 HTML（装了钩子的话每次 git 提交自动重新生成）

/graphify query "what connects auth to the database?"
/graphify path "UserService" "DatabasePool"
/graphify explain "RateLimiter"

/graphify add https://arxiv.org/abs/1706.03762   # 抓一篇论文加进来
/graphify add <youtube-url>                       # 转写一个视频加进来

graphify hook install              # 提交和切换分支时自动重建（git pull 之后跑 `graphify update .` —— 见下面「推荐工作流」）
graphify merge-graphs a.json b.json              # 合并两张图

graphify prs                       # PR 面板：CI 状态、评审状态、worktree 映射
graphify prs 42                    # 深挖 PR #42，带图上的影响面
graphify prs --triage              # 用 AI 给你的评审队列排序（用你配的任意后端）
graphify prs --conflicts           # 共享同一社群的 PR —— 合并顺序风险
```

完整命令见下面的[完整命令参考](#完整命令参考)。

---

## 忽略文件

在项目根目录建一个 `.graphifyignore` —— 语法跟 `.gitignore` 一样，包括 `!` 取反。

**`.gitignore` 会被自动遵守。** graphify 会读取每个目录里的 `.gitignore`。如果同时存在 `.graphifyignore`，两者会**合并** —— `.graphifyignore` 的规则最后求值，所以在冲突时它说了算（包括 `!` 取反）。加 `.graphifyignore` 只会排除得更多；它永远不会把 `.gitignore` 已经排除掉的文件重新纳入。子目录作用域跟 git 一样 —— 一个忽略文件只影响它自己那棵子树。

当 git 忽略掉的生成代码或转译代码需要进图时，给 `graphify extract` 传 `--no-gitignore`。这会关掉 `.gitignore` 和 `.git/info/exclude`；`.graphifyignore` 仍然生效。

```
# .graphifyignore
node_modules/
dist/
*.generated.py

# 只索引 src/，其它都忽略
*
!src/
!src/**
```

---

## 团队配置

`graphify-out/` 是**打算提交进 git 的**，这样团队里每个人一开始就有一张地图。

**建议加进 `.gitignore` 的：**
```
graphify-out/cost.json        # 仅本地
# graphify-out/cache/         # 可选：提交能提速，跳过则仓库更小
```

> `manifest.json` 现在是可移植的 —— 键存成相对路径，加载时重新锚定，所以提交它是安全的，并且能避免首次检出时全量重建。

### 推荐工作流

每次克隆只要配一次。之后，你三个日常的 git 命令就能自己让图保持最新，还有一个用来跟团队同步：

| 你做 | graphify 做 |
|---|---|
| `graphify hook install`（克隆之后跑一次） | 装上下面这些钩子，外加一个合并驱动，让 `graph.json` 永远不出现冲突标记 |
| `git commit` | 自动重建 —— 只走 AST，不花 API 的钱 |
| `git checkout` / `git switch`（切分支） | 自动重建（只对单个文件 `git checkout -- <路径>` 的不会） |
| `git pull` / `git merge` | 紧接着跑 `graphify update .` |
| `git push` | 什么都不用做 |

提交和切分支的重建在后台跑并立即返回，所以在大型仓库上，图可能会比提交晚几秒 —— 第 5 步覆盖了那种「它还没追上你就先查了」的少见情况。

**一步步来：**
1. 克隆仓库，跑一次 `graphify hook install`。
2. 正常提交、切分支 —— 图自己会保持最新。
3. 每次 `git pull`（或 merge）之后，跑 `graphify update .`，让图跟你刚拉下来的内容同步。在大型或活跃的仓库上，用一个 pull 别名把它自动化：
   ```bash
   git config --global alias.gpull '!git pull && graphify update .'
   ```
4. 当文档或论文有变动时，跑 `/graphify --update` 也刷新那些节点（代码和文档各自独立更新）。
5. 如果某次查询看起来漏掉了你刚加的东西，先跑 `graphify update .`，再问一遍。

---

## 直接用这张图

```bash
# 从终端查询
graphify query "show the auth flow"
graphify query "what connects DigestAuth to Response?" --graph graphify-out/graph.json

# 把图暴露成 MCP 服务（供反复的工具调用访问）
python -m graphify.serve graphify-out/graph.json
python -m graphify.serve --graph graphify-out/graph.json  # 也接受 --graph 参数

# 注册到 Kimi Code：
kimi mcp add --transport stdio graphify -- python -m graphify.serve graphify-out/graph.json

# 或者用 HTTP 提供服务，让整个团队指向同一个 URL（本地不用装 graphify）：
python -m graphify.serve graphify-out/graph.json --transport http --port 8080
python -m graphify.serve graphify-out/graph.json --transport http --host 0.0.0.0 --api-key "$SECRET"
```

MCP 服务给你的助手提供结构化访问：`query_graph`、`get_node`、`get_neighbors`、`shortest_path`、`list_prs`、`get_pr_impact`、`triage_prs`。

### 共享 HTTP 服务

`--transport stdio`（默认）会给每个开发者起一个本地服务。`--transport http` 则通过 MCP Streamable HTTP 传输提供同样的工具，所以一个共享进程就能为整个团队服务 —— 客户端把 IDE 的 MCP 配置指向 `http://<host>:8080/mcp`，而不用在本地跑 graphify。

| 参数 | 默认值 | 用途 |
|---|---|---|
| `--transport {stdio,http}` | `stdio` | 用哪种传输 |
| `--host` | `127.0.0.1` | HTTP 绑定地址（用 `0.0.0.0` 可暴露到本机之外） |
| `--port` | `8080` | HTTP 绑定端口 |
| `--api-key` | 环境变量 `GRAPHIFY_API_KEY` | 要求 `Authorization: Bearer <key>`（或 `X-API-Key`） |
| `--path` | `/mcp` | HTTP 挂载路径 |
| `--json-response` | 关 | 返回纯 JSON 而不是 SSE 流 |
| `--stateless` | 关 | 不保留每会话状态（用于负载均衡 / CI 部署） |
| `--session-timeout` | `3600` | 空闲的有状态会话在 N 秒后被回收（`0` 表示不回收） |

默认的 `127.0.0.1` 绑定只监听回环。要在共享主机上暴露时，请**同时**设置 `--host 0.0.0.0` 和 `--api-key`。在容器里跑：

```bash
docker build -t graphify .
docker run -p 8080:8080 -v "$(pwd)/graphify-out:/data" graphify \
  /data/graph.json --transport http --host 0.0.0.0 --api-key "$SECRET"
```

> **WSL / Linux 说明：** Ubuntu 自带的是 `python3`，不是 `python`。用 venv 避免冲突：
> ```bash
> python3 -m venv .venv && .venv/bin/pip install "graphifyy[mcp]"
> ```

---

## 环境变量

这些只在**无界面 / CI 提取**（`graphify extract`）时才需要。当你在 IDE 里通过 `/graphify` 技能运行时，模型 API 由你的 IDE 会话提供 —— 不需要额外的 Key。

| 变量 | 用途 | 何时需要 |
|---|---|---|
| `ANTHROPIC_API_KEY` | Claude（Anthropic）后端 | `--backend claude` |
| `ANTHROPIC_BASE_URL` | Anthropic 兼容端点 URL（LiteLLM 代理、网关等） | `--backend claude`（默认：`https://api.anthropic.com`） |
| `ANTHROPIC_MODEL` | Claude 后端的模型名 —— 用自定义端点时，填你服务器暴露的模型名/别名 | `--backend claude`（默认：`claude-sonnet-4-6`） |
| `GEMINI_API_KEY` 或 `GOOGLE_API_KEY` | Google Gemini 后端 | `--backend gemini` |
| `OPENAI_API_KEY` | OpenAI 或 OpenAI 兼容 API | `--backend openai`（本地服务器接受任意非空值） |
| `OPENAI_BASE_URL` | OpenAI 兼容服务器 URL（llama.cpp、vLLM、LM Studio 等） | `--backend openai`（默认：`https://api.openai.com/v1`） |
| `OPENAI_MODEL` | OpenAI 后端的模型名 —— 自建服务器时填它暴露的模型名/别名（查它的 `/v1/models` 端点），比如 llama.cpp 用 `LFM2.5-8B-A1B-UD-Q4_K_XL` | `--backend openai`（默认：`gpt-4.1-mini`） |
| `DEEPSEEK_API_KEY` | DeepSeek 后端 | `--backend deepseek` |
| `MOONSHOT_API_KEY` | Kimi Code 后端 | `--backend kimi` |
| `OLLAMA_BASE_URL` | Ollama 本地推理 URL | `--backend ollama`（默认：`http://localhost:11434`） |
| `OLLAMA_MODEL` | Ollama 模型名 | `--backend ollama`（默认：自动检测） |
| `GRAPHIFY_OLLAMA_NUM_CTX` | 覆盖 Ollama 的 KV 缓存窗口大小 | 可选 —— 默认自动调整 |
| `GRAPHIFY_OLLAMA_KEEP_ALIVE` | Ollama 模型保持加载的分钟数 | 可选 —— 设 `0` 表示每块处理完就卸载 |
| `AZURE_OPENAI_API_KEY` | Azure OpenAI Service 后端 | `--backend azure` |
| `AZURE_OPENAI_ENDPOINT` | Azure 资源端点 URL | `--backend azure`（和 API Key 一起必填） |
| `AZURE_OPENAI_API_VERSION` | Azure API 版本覆盖 | 可选 —— 默认 `2024-12-01-preview` |
| `AZURE_OPENAI_DEPLOYMENT` 或 `GRAPHIFY_AZURE_MODEL` | Azure 部署名 | 可选 —— 默认 `gpt-4o` |
| `AWS_*` / `~/.aws/credentials` | AWS Bedrock —— 标准凭证链 | `--backend bedrock`（不需要 API Key，用 IAM） |
| `GRAPHIFY_MAX_WORKERS` | AST 并行线程数 | 可选 —— 也可以用 `--max-workers` 参数 |
| `GRAPHIFY_MAX_OUTPUT_TOKENS` | 提高输出上限，应对密集语料 | 可选 —— 比如大文件用 `32768` |
| `GRAPHIFY_API_TIMEOUT` | HTTP、claude-cli、Anthropic SDK 和 Bedrock 后端的单次调用超时秒数（默认：600） | 可选 —— 也可以用 `--api-timeout` 参数 |
| `GRAPHIFY_MAX_RETRIES` | 被限流（429）时重试多少次才放弃（默认：6；遵守 `Retry-After`） | 可选 —— 严格的组织级限额下调高（比如 kimi）；`0` 关闭 |
| `GRAPHIFY_MAX_RETRY_DEPTH` | 一个被截断的块最多可以二分重提取多少层（默认 3，即一个块最多 8 次子调用） | 可选 —— 调低可以压住最坏情况下的开销；`0` 关闭所有重试（不二分、不重试空响应），一个块正好只花一次调用 |
| `GRAPHIFY_FORCE` | 即使节点变少也强制重建 | 可选 —— 也可以用 `--force` 参数 |
| `GRAPHIFY_GOOGLE_WORKSPACE` | 自动开启 Google Workspace 导出 | 可选 —— 设为 `1` |
| `GRAPHIFY_TRIAGE_BACKEND` | `graphify prs --triage` 用的后端 | 可选 —— 从可用的 Key 自动检测 |
| `GRAPHIFY_TRIAGE_MODEL` | 分诊用的模型覆盖 | 可选 —— 比如 `claude-opus-4-7` |
| `GRAPHIFY_QUERY_LOG_ENABLE` | 设为 `1` 打开本地查询日志 `~/.cache/graphify-queries.log`（记录每次 query/path/explain 的问题 + 语料路径）。默认关闭 —— 你不主动开启就什么都不写（#1797） | 可选 |
| `GRAPHIFY_QUERY_LOG` | 开启查询日志并写到这个路径而不是默认位置 | 可选 —— 不设这个或 `_ENABLE` 就不开 |
| `GRAPHIFY_QUERY_LOG_DISABLE` | 设为 `1` 强制关掉查询日志（优先级高于开启变量） | 可选 |
| `GRAPHIFY_QUERY_LOG_RESPONSES` | 日志开启时，连完整的子图响应也记下来（默认关） | 可选 |
| `GRAPHIFY_MAX_GRAPH_BYTES` | 覆盖 `graph.json` 的 512 MiB 大小上限 —— 比如 `700MB`、`2GB`，或纯字节数 | 可选 —— 超大语料有用 |
| `GRAPHIFY_MAX_CONTEXTS` | 单个多项目 MCP 服务保留的「非默认项目图」数量上限 | 可选 —— 默认 `8`；非法值按 `8` 处理，小于 `1` 的按 `1` 处理 |
| `GRAPHIFY_LLM_TEMPERATURE` | 覆盖语义提取的 LLM 温度 —— 比如 `0.7`，或 `none` 表示不传 | 可选 —— 对 o1/o3/o4/gpt-5 推理模型自动省略 |

---

## 隐私

- **代码文件** —— 通过 tree-sitter 在本地处理。一个字节都不离开你的机器。纯代码语料不需要任何 API Key —— `graphify extract` 可以完全离线跑。在混合仓库上，加 `--code-only` 就只索引代码，跳过那些本来需要大模型的文档/PDF/图片。
- **视频 / 音频** —— 用 faster-whisper 在本地转写。一个字节都不离开你的机器。
- **文档、PDF、图片** —— 会发给你的 AI 助手做语义提取（通过 `/graphify` 技能，用的是你 IDE 会话里跑的那个模型）。无界面的 `graphify extract` 需要 `GEMINI_API_KEY` / `GOOGLE_API_KEY`（Gemini）、`MOONSHOT_API_KEY`（Kimi）、`ANTHROPIC_API_KEY`（Claude）、`OPENAI_API_KEY`（OpenAI）、`DEEPSEEK_API_KEY`（DeepSeek）、一个运行中的 Ollama 实例（`OLLAMA_BASE_URL`）、通过标准凭证链的 AWS 凭证（Bedrock —— 不需要 API Key，用 IAM），或者 `claude` 命令行程序（Claude Code —— 不需要 API Key，用你的 Claude 订阅）。`--dedup-llm` 参数用的是同一个 Key。
- **数据驻留** —— `graphify extract` 会根据你设了哪个 API Key 自动检测用哪个供应商（优先级：Gemini → Kimi → Claude → OpenAI → DeepSeek → Azure → Bedrock → Ollama）。对有数据驻留要求的代码，用 `--backend ollama`（完全本地）或显式传 `--backend` 参数。Kimi（`MOONSHOT_API_KEY`）会路由到 Moonshot AI 位于中国的服务器。
- **没有遥测**，没有用量追踪，没有数据分析。
- **查询日志** —— 每次 `graphify query`、`graphify path`、`graphify explain` 和 MCP 的 `query_graph` 调用都会以 JSON Lines 格式记到 `~/.cache/graphify-queries.log`（时间戳、问题、语料、返回的节点数、耗时）。完整子图响应**默认不存**。设 `GRAPHIFY_QUERY_LOG_DISABLE=1` 可以退出，或者设 `GRAPHIFY_QUERY_LOG=/dev/null` 让它静默而不关闭代码路径。

---

## 故障排查

**装完之后 `graphify: command not found`**
命令行工具装好了，但它的 bin 目录不在你 shell 的 `PATH` 上。按你的安装方式挑对应的修法：
- **uv**（`uv tool install graphifyy`）：命令落在 uv 的工具 bin 目录（`~/.local/bin`），全新的 macOS/zsh 环境常常没把它放进 `PATH`。跑 `uv tool update-shell`，然后开一个新终端。（用 `uv tool dir --bin` 找那个目录。）
- **pipx**（`pipx install graphifyy`）：跑 `pipx ensurepath`，然后开一个新终端。
- **pip**（`pip install graphifyy`）：pip 把脚本装到一个可能不在 `PATH` 上的用户 bin 目录 —— 把 `~/Library/Python/3.x/bin`（macOS）或 `~/.local/bin`（Linux）加进 `~/.zshrc`/`~/.bashrc` 的 `PATH`，或者直接跑 `python -m graphify`。

**`uvx graphify …` 或 `uv tool run graphify …` 解析不了 `graphify`**
PyPI 上的包名是 `graphifyy`；`graphify` 只是它提供的命令。`uv tool run` 把第一个词当成*包名*，所以它去找一个叫 `graphify` 的包，然后报 `No solution found … no versions of graphify`。显式写包名：`uvx --from graphifyy graphify install`（等同于 `uv tool run --from graphifyy graphify install`）。或者先用 `uv tool install graphifyy` 装一次，然后直接调 `graphify`。

**`uv run --with graphifyy python -m graphify` 悄悄跑了一个旧版本**
`uv run` 用的是你的*系统* Python，所以如果那儿也住着一个旧的 `graphifyy`（比如以前 `pip install graphifyy` 装的），Python 会先在 `sys.path` 上找到那份，而 `--with graphifyy` 覆盖不了它。它跑起来不报错，但你得到的是*旧*版本的行为 —— 比如 `OPENAI_BASE_URL` 这样的环境变量覆盖被静默忽略，于是请求打到了默认端点，然后报一个看起来像是 Key 不对的 401。特征是一行 `warning: skill is from graphify <新版本>, package is <旧版本>` —— 这说明加载的是另一份安装，不只是技能过期了。查一下到底加载了哪份：
```bash
python -c "import graphify; print(graphify.__file__)"
```
然后直接跑装好的命令（它用的是 uv 管理的那份），或者清掉系统里那份残留：
```bash
uvx --from graphifyy graphify extract . --backend openai   # 显式指定包名
pip uninstall graphifyy                                    # 或者删掉旧的系统安装
```

**`python -m graphify` 能用但 `graphify` 命令不行**
你 shell 的 `PATH` 不包含命令被装进去的那个 bin 目录。优先用 `uv tool install` / `pipx install` 而不是裸 `pip`，然后跑 `uv tool update-shell` / `pipx ensurepath` 并开一个新终端（见上面的安装说明）。

**PowerShell 里 `/graphify .` 报 "path not recognized"**
PowerShell 把开头的 `/` 当路径分隔符。在 Windows 上用 `graphify .`（不带斜杠）。

**`--update` 或重建之后图的节点变少了**
如果有一次重构删掉了文件，旧的节点会残留。传 `--force`（或设 `GRAPHIFY_FORCE=1`），即使重建后节点更少也覆盖。

**`extract` 退出时报 "extraction was incomplete ... refusing to overwrite"**
当某次提取崩了、或者遍历没能完整读完语料时，这次结果会比完整结果小，所以 `graphify extract` 拒绝用这个部分结果覆盖掉更大的已有图（这是为了保护你的 `graph.json`）。修掉底层的失败再重跑，或者传 `--allow-partial` 强行覆盖。

**图里同一个实体出现重复节点（幽灵重复）**
幽灵重复（同一个符号出现两次 —— 一次来自带源码位置的 AST 提取，一次来自不带位置的语义提取）现在会在建图时自动合并。如果你在 v0.8.33 之前建的图上看到这个，跑一次全量重提取来清理：
```bash
graphify extract . --force
```

**Ollama 显存不够 / 超出上下文窗口**
KV 缓存窗口是自动调整的，但对你的 GPU 来说可能还是太大。调小它：
```bash
GRAPHIFY_OLLAMA_NUM_CTX=8192 graphify extract ./docs --backend ollama --token-budget 4000
```

**`LLM returned invalid JSON` / `Unterminated string` 警告**
模型的 JSON 响应撞上了输出 token 上限，在字符串中间被截断了。graphify 会自动恢复（它把这个块劈成两半分别重提取，而超大的单个文档会先在标题/段落边界切片，保证整个文件仍被覆盖），所以这些警告很吵但不会丢数据。想减少这种折腾，要么提高输出上限，要么压小每块的输出：
```bash
GRAPHIFY_MAX_OUTPUT_TOKENS=16384 graphify extract . --mode deep   # 提上限
graphify extract . --mode deep --token-budget 4000                # 更小的输入块 → 更小的输出
```
用 OpenRouter 这类云端网关时，优先用 `--backend openai`（设 `OPENAI_BASE_URL`）而不是 Ollama 的兼容层 —— 那条 OpenAI 兼容路径更干净。如果模型自己有输出上限，压低 `--token-budget` 是最可靠的杠杆。

**图的 HTML 太大，浏览器打不开（>5000 个节点）**
跳过生成 HTML，直接用 JSON：
```bash
graphify cluster-only ./my-project --no-viz
graphify query "..."
```

**两个开发者同时提交后，`graph.json` 里出现冲突标记**
跑 `graphify hook install` —— 它会设置一个 git 合并驱动，自动对 `graph.json` 做并集合并，所以冲突永远不会发生。

**图没反映队友最近的改动**
在 `git pull` 或任何 merge 之后立刻跑 `graphify update .` —— 见[推荐工作流](#推荐工作流)。提交和切分支通过装好的钩子会自动更新图；只有跟 pull 同步这一步需要你自己跑。用 pull 别名把它折进去，怎么都是一条命令：
```bash
git config --global alias.gpull '!git pull && graphify update .'
```
用 `graphify hook status` 确认钩子是否生效；升级/重装解释器之后重新跑 `graphify hook install` 来刷新它们。

**提取文档或 PDF 时返回空的节点/边**
文档、PDF 和图片需要一次大模型调用 —— 纯代码语料不需要 Key。检查你的 API Key 是否设了、后端是否正确：
```bash
ANTHROPIC_API_KEY=sk-... graphify extract ./docs --backend claude
```

**IDE 里提示技能版本不匹配**
你装的 graphify 版本跟技能文件版本不一致。升级：
```bash
uv tool upgrade graphifyy
graphify install  # 覆盖技能文件
```

**Claude Code 的提示词缓存在每次 `graphify extract` 之后失效**
Graphify 会把输出文件（`graph.json`、`graphify-out/`）写进工作区。如果这些路径没被忽略，每次写入都会让 Claude Code 的提示词缓存失效，导致下一轮按「缓存写入」的价格重新全量上传。把它们加进 `.claudeignore`：
```text
# .claudeignore
graph.json
graphify-out/
```

---

## 完整命令参考

```
/graphify                          # 在当前目录跑
/graphify ./raw                    # 在指定文件夹跑
/graphify ./raw --mode deep        # 更激进的关系提取
graphify extract ./raw --code-only # 只索引代码 —— 本地 AST，不需要 API Key（跳过文档/PDF/图片）；这是 extract 的参数，不是技能的参数
/graphify ./raw --update           # 只重新提取改动过的文件
/graphify ./raw --directed         # 保留边的方向
/graphify ./raw --cluster-only     # 在已有图上重跑聚类
/graphify ./raw --no-viz           # 跳过 HTML 可视化
/graphify ./raw --obsidian         # 生成 Obsidian 知识库
/graphify ./raw --obsidian --obsidian-dir ~/vault  # 写进已有的知识库（绝不覆盖你自己的笔记或 .obsidian 配置）
/graphify ./raw --wiki             # 生成可被 Agent 抓取的 markdown wiki
/graphify ./raw --svg              # 导出 graph.svg
/graphify ./raw --graphml          # 导出给 Gephi / yEd 用
/graphify ./raw --neo4j            # 生成给 Neo4j 用的 cypher.txt
/graphify ./raw --neo4j-push bolt://localhost:7687
/graphify ./raw --falkordb         # 生成给 FalkorDB 用的 cypher.txt
/graphify ./raw --falkordb-push falkordb://localhost:6379
/graphify ./raw --watch            # 文件变动时自动同步
/graphify ./raw --mcp              # 启动 MCP stdio 服务

/graphify add https://arxiv.org/abs/1706.03762
/graphify add <video-url>
/graphify add https://... --author "Name" --contributor "Name"

/graphify query "what connects attention to the optimizer?"
/graphify query "..." --dfs --budget 1500
/graphify path "DigestAuth" "Response"
/graphify explain "SwinTransformer"

graphify save-result --question "Q" --answer "A" --nodes Foo Bar --outcome useful   # 记录一次问答的结果（工作记忆；outcome ∈ useful|dead_end|corrected）
graphify reflect                   # 把 graphify-out/memory/ 里的结果汇总成 reflections/LESSONS.md
graphify reflect --if-stale        # 当 LESSONS.md 已经比所有输入都新时，什么都不做（每会话跑一次的开销极低）
graphify reflect --out docs/LESSONS.md    # 把经验文档写到别处
graphify reflect --graph graphify-out/graph.json  # 按社群给经验分组 + 写工作记忆覆盖层 (.graphify_learning.json)
                                   # 覆盖层给节点打上 preferred/tentative/contested 标签（按近因加权，带来源）；
                                   # graphify explain / query 随后会显示一条 "Lesson:" 提示，当源码已变动时会标 "code changed — re-verify"

graphify uninstall                 # 一次性从所有平台移除
graphify uninstall --purge         # 连 graphify-out/ 一起删
graphify uninstall --project --platform codex  # 只移除项目级安装的文件

graphify hook install              # 提交后 + 检出后钩子
graphify hook uninstall
graphify hook status

# 始终生效的助手指令 —— 分平台
graphify claude install            # CLAUDE.md + PreToolUse 钩子（Claude Code）
graphify claude uninstall
graphify codebuddy install         # CODEBUDDY.md + PreToolUse 钩子（CodeBuddy）
graphify codebuddy uninstall
graphify codex install             # AGENTS.md + .codex/hooks.json 里的 PreToolUse 钩子（Codex）
graphify opencode install          # AGENTS.md + tool.execute.before 插件（OpenCode）
graphify kilo install              # 原生 Kilo 技能 + /graphify 命令 + AGENTS.md + .kilo 插件
graphify kilo uninstall
graphify cursor install            # .cursor/rules/graphify.mdc（Cursor）
graphify cursor uninstall
graphify gemini install            # GEMINI.md + BeforeTool 钩子（Gemini CLI）
graphify gemini uninstall
graphify copilot install           # 技能文件（GitHub Copilot CLI）
graphify copilot uninstall
graphify aider install             # AGENTS.md（Aider）
graphify aider uninstall
graphify claw install              # AGENTS.md（OpenClaw）
graphify claw uninstall
graphify droid install             # AGENTS.md（Factory Droid）
graphify droid uninstall
graphify trae install              # AGENTS.md（Trae）
graphify trae uninstall
graphify trae-cn install           # AGENTS.md（Trae CN）
graphify trae-cn uninstall
graphify hermes install             # AGENTS.md + ~/.hermes/skills/（Hermes）
graphify hermes uninstall
graphify amp install               # 技能文件（Amp）
graphify amp uninstall
graphify agents install            # ~/.agents/skills/ + AGENTS.md（跨框架；别名：graphify skills）
graphify agents uninstall
graphify kiro install               # .kiro/skills/ + .kiro/steering/graphify.md（Kiro IDE/CLI）
graphify kiro uninstall
graphify pi install                # 技能文件（Pi 编程 Agent）
graphify pi uninstall
graphify devin install             # 技能文件 + .windsurf/rules/graphify.md（Devin CLI）
graphify devin uninstall
graphify antigravity install       # .agents/rules + .agents/workflows（Google Antigravity）
graphify antigravity uninstall

graphify extract ./docs                        # 给 CI 用的无界面大模型提取（不需要 IDE）
graphify extract ./docs --backend gemini       # 显式指定后端：gemini, kimi, claude, openai, deepseek, ollama, bedrock, 或 claude-cli
graphify extract ./docs --backend gemini --model gemini-3.1-pro-preview
graphify extract ./docs --backend ollama       # 本地 Ollama（设 OLLAMA_BASE_URL / OLLAMA_MODEL）—— 回环地址不需要 API Key
OPENAI_BASE_URL=http://localhost:8080/v1 OPENAI_MODEL=my-model graphify extract ./docs --backend openai   # 任意 OpenAI 兼容服务器（llama.cpp, vLLM, LM Studio）
ANTHROPIC_BASE_URL=http://localhost:4000 ANTHROPIC_MODEL=my-model graphify extract ./docs --backend claude   # 任意 Anthropic 兼容端点（LiteLLM 代理、网关）
GRAPHIFY_OLLAMA_NUM_CTX=32768 graphify extract ./docs --backend ollama   # 覆盖 KV 缓存窗口（默认自动调整）
GRAPHIFY_OLLAMA_KEEP_ALIVE=0 graphify extract ./docs --backend ollama    # 每块处理完卸载模型（小显存 GPU 省显存）
graphify extract ./docs --backend bedrock      # 通过 IAM 用 AWS Bedrock —— 不需要 API Key，用 AWS 凭证链
graphify extract ./docs --backend claude-cli   # 走 Claude Code CLI —— 不需要 API Key，用你的 Claude 订阅
graphify extract ./docs --backend azure        # Azure OpenAI（设 AZURE_OPENAI_API_KEY + AZURE_OPENAI_ENDPOINT）
graphify extract ./docs --max-workers 16       # AST 并行度（也可用 GRAPHIFY_MAX_WORKERS）
graphify extract --postgres "postgresql://user:pass@host/db"   # 直接内省在线 PostgreSQL 表结构
graphify extract ./my-workspace --cargo        # 直接内省 Rust Cargo 工作区依赖
graphify extract ./docs --token-budget 30000   # 给本地/小模型用更小的语义块
graphify extract ./docs --max-concurrency 2    # 更少的大模型并行调用（本地推理时有用）
graphify extract ./docs --api-timeout 900      # 给慢的本地模型更长的 HTTP 超时（默认 600s）
graphify extract ./docs --google-workspace     # 提取前先用 gws 导出 .gdoc/.gsheet/.gslides
graphify extract ./src --no-gitignore          # 纳入被 git 忽略的源码；仍然遵守 .graphifyignore
graphify extract ./docs --mode deep           # 通过扩展系统提示词做更丰富的语义提取
graphify extract ./docs --no-cluster           # 只做原始提取，跳过聚类
graphify extract ./docs --timing               # 把各阶段耗时打到 stderr（cluster-only 上也可用）
graphify extract ./docs --force                # 即使新图节点更少也覆盖 graph.json（重构后或清理幽灵重复时用）
graphify extract ./docs --dedup-llm            # 对歧义实体对用大模型做仲裁（用同一个 API Key）
graphify extract ./src --no-dedup              # 跳过实体去重；在增量合并时这还会启用「缩水保护」，拒绝丢掉未改动文件的节点
graphify extract ./docs --global --as myrepo   # 提取并注册进跨项目的全局图
GRAPHIFY_MAX_OUTPUT_TOKENS=32768 graphify extract ./docs --backend claude  # 给密集语料提高输出上限

graphify export callflow-html                       # graphify-out/<项目名>-callflow.html
graphify export callflow-html --max-sections 8      # 限制生成的架构章节数
graphify export callflow-html --output docs/arch.html
graphify export callflow-html ./some-repo/graphify-out

graphify global add graphify-out/graph.json --as myrepo   # 把一个项目图注册进 ~/.graphify/global-graph.json
graphify global remove myrepo                         # 从全局图里移除一个项目
graphify global list                                  # 显示所有已注册仓库 + 节点/边数量
graphify global path                                  # 打印全局图文件路径

graphify prs                              # PR 面板：CI、评审、worktree、图影响面
graphify prs 42                           # 深挖 PR #42
graphify prs --triage                     # AI 分诊排序（从环境变量自动检测后端）
graphify prs --worktrees                  # worktree → 分支 → PR 映射
graphify prs --conflicts                  # 共享同一社群的 PR（合并顺序风险）
graphify prs --base main                  # 只筛目标为特定基分支的 PR
graphify prs --repo owner/repo            # 对另一个 GitHub 仓库跑
GRAPHIFY_TRIAGE_BACKEND=kimi graphify prs --triage   # 为分诊指定后端

graphify clone https://github.com/karpathy/nanoGPT
graphify merge-graphs a.json b.json --out merged.json
graphify --version                                    # 打印已安装版本
graphify watch ./src
graphify check-update ./src
graphify update ./src
graphify update ./src --no-cluster  # 跳过重新聚类，只写原始 AST 图
graphify update ./src --force       # 即使节点更少也覆盖
graphify cluster-only ./my-project
graphify cluster-only ./my-project --graph path/to/graph.json  # 自定义图位置
graphify cluster-only ./my-project --max-concurrency 16 --batch-size 200  # 并行社群命名（大图）
graphify cluster-only ./my-project --resolution 1.5            # 更多、更小的社群
graphify cluster-only ./my-project --exclude-hubs 99           # 把 p99 度数的节点排除在分区之外
graphify cluster-only ./my-project --no-label                  # 保留 "Community N" 占位名
graphify cluster-only ./my-project --backend=gemini            # 社群命名用的后端
graphify cluster-only ./my-project --backend=gemini --model gemini-2.5-pro  # 指定模型
graphify label ./my-project                                    # 用已配后端（重新）命名社群
graphify label ./my-project --backend=openai --model gpt-4o   # 强制指定后端和模型
```

> **社群命名：** 在 Agent 里（Claude Code、Gemini CLI）时，社群由 Agent 自己命名。当你裸跑命令行时，`cluster-only` 会用已配的后端（内置的或自定义 OpenAI 兼容供应商）自动命名 —— 传 `--no-label` 保留 `Community N`，或者跑 `graphify label` 按需（重新）生成名字。

---

## 了解更多

- [工作原理](docs/how-it-works.md) —— 提取流水线、社群检测、置信度打分、基准测试
- [ARCHITECTURE.md](ARCHITECTURE.md) —— 模块拆解、怎么加一门语言
- [可选集成](docs/docker-mcp-sqlite.md) —— Docker MCP Toolkit + SQLite
- [The Memory Layer](https://safishamsi.gumroad.com/l/qetvlo) —— 讲 graphify 背后那套想法的书，从头到尾讲架构

---

## graphify Enterprise

[**graphify Enterprise**](https://graphify.com) 是建在 graphify 之上的「始终在线」层 —— 它把同一套图方法用在你整个工作上下文上：会议、文件、文档、代码，并在后台持续更新。

为那些工作内容散落在上百次对话和文档里、永远无法完整重建的人与团队而做。

**[在 graphify.com 加入等候名单](https://graphify.com)。** 免费试用即将推出。

---

<details>
<summary>参与贡献</summary>

### 开发环境

项目用 [uv](https://docs.astral.sh/uv/) 做开发流程。装一次，然后：

```bash
git clone https://github.com/safishamsi/graphify.git
cd graphify
git checkout v8                        # 活跃开发分支

# 创建项目 venv 并安装 graphify + 全部扩展 + dev 组（pytest）。
# uv 默认会装 dev 依赖组；传 --no-dev 可跳过。
uv sync --all-extras
```

验证可编辑安装：
```bash
uv run graphify --version
uv run python -c "import graphify; print(graphify.__file__)"
```

### 跑测试

```bash
uv run pytest tests/ -q                # 跑全套
uv run pytest tests/test_extract.py -q # 单个模块
uv run pytest tests/ -q -k "python"    # 按名字过滤
```

### CI 对齐检查

权威的 CI 命令放在 [`.github/workflows/`](.github/workflows/)。做本地 CI 风格验证时，用 Python 3.10、3.12、3.13 或 3.14，然后跑：

```bash
uv sync --all-extras --frozen
uv run --frozen pytest tests/ -q --tb=short
uv run --frozen python -m tools.skillgen --check
uv run --frozen python -m tools.skillgen --audit-coverage
uv run --frozen python -m tools.skillgen --schema-singleton
uv run --frozen python -m tools.skillgen --monolith-roundtrip
uv run --frozen python -m tools.skillgen --always-on-roundtrip
uv run --frozen graphify --help
uv run --frozen graphify install
```

Ruff 作为额外的本地检查挺有用（`uv run --frozen ruff check .`），但目前不是阻塞性的 CI 任务。Pyright 同样只是本地/建议性检查，除非以后加进 CI。Bandit 和 pip-audit 这两个 CI 步骤目前用了 `continue-on-error`，所以它们的发现是建议性而非阻塞性的。

> macOS 说明：测试集同时包含 `sample.f90` 和 `sample.F90` 两个样例文件。它们在大小写不敏感的 HFS+ / APFS 文件系统上会冲突。如果你需要同时测两种 Fortran 变体，请在 Linux 或 Docker 容器里跑。

> Windows 说明：原生 Windows 测试集会检验符号链接、长路径、POSIX 权限、路径分隔符和 UTF-8 文件系统行为。请开启 Windows 开发者模式以允许非特权创建符号链接，或者从提权的 shell 里跑测试。依赖长路径测试之前，先开启 Windows 的 `LongPathsEnabled` 策略。改完这两项设置后重启受影响的 shell 或应用。要跟阻塞性的 GitHub Actions 测试矩阵完全一致，请在 WSL 或 Linux 里跑；CI 目前跑在 Ubuntu 上，Python 版本为 3.10、3.12、3.13 和 3.14。Pyright 作为本地建议性检查可用，但目前不是阻塞性的 CI 任务。

### Git 工作流

- 活跃开发在 `v8` 分支上进行。
- 提交风格：`fix: <描述>` / `feat: <描述>` / `docs: <描述>`
- 开 PR 之前，跑 `uv run pytest tests/ -q` 并确认通过。
- 任何新的语言提取器，都要往 `tests/fixtures/` 加一个样例文件，并往 `tests/test_languages.py` 加测试。

### 可以贡献什么

**实操案例**是最有用的贡献。在一个真实语料上跑 `/graphify`，把输出存到 `worked/{slug}/`，诚实写一份 `review.md` 说明这张图哪些做对了、哪些做错了，然后开 PR。

**提取 bug** —— 开一个 issue，附上输入文件、缓存条目（`graphify-out/cache/`），以及漏掉或搞错了什么。

模块职责和怎么加一门语言，见 [ARCHITECTURE.md](ARCHITECTURE.md)。

</details>

---

## 社区与链接

<p align="center">
  <a href="https://graphify.com"><img src="https://img.shields.io/badge/Website-graphify.com-4c1?style=flat&logo=googlechrome&logoColor=white" alt="官网"/></a>
  <a href="https://discord.gg/2DDrEgvZb4"><img src="https://img.shields.io/badge/Discord-Join-5865F2?style=flat&logo=discord&logoColor=white" alt="Discord"/></a>
  <a href="https://x.com/graphify"><img src="https://img.shields.io/badge/X-graphify-000000?logo=x&logoColor=white" alt="X"/></a>
  <a href="https://www.youtube.com/@graphifylabs"><img src="https://img.shields.io/badge/YouTube-Graphify%20Labs-FF0000?style=flat&logo=youtube&logoColor=white" alt="YouTube"/></a>
  <a href="https://github.com/sponsors/safishamsi"><img src="https://img.shields.io/badge/sponsor-safishamsi-ea4aaa?logo=github-sponsors" alt="赞助"/></a>
  <a href="https://safishamsi.gumroad.com/l/qetvlo"><img src="https://img.shields.io/badge/Book-The%20Memory%20Layer-2ea44f?style=flat&logo=gitbook&logoColor=white" alt="The Memory Layer"/></a>
</p>
