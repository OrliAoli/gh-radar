<h1 align="center">OpenDesign：Claude Design 的开源替代方案</h1>

> ⚡ **[OpenDesign Cloud —— 官方模型服务。](https://open-design.ai/zh/pricing/)** 一次充值，就能在 OpenDesign 里同时用上 Agent 模型和图片模型：Agent 侧支持 GPT、Claude、DeepSeek；图片侧支持 GPT Image 2.0、Seedream 5.0 Pro、Nano Banana 2.0。
>
> 🚀 **[DeepSeek V4 Flash 和 V4 Pro 现已上线。](https://open-design.ai/zh/pricing/)** 把顶级智力用在原型、演示稿、设计系统和日常 Agent 任务上。OpenDesign 会员可直接在应用内无限量使用这两款模型，为期两周。
>
> 🧩 **[现已支持 DeepSeek Harness。](https://open-design.ai/zh/agents/deepseek-harness-design/)** 把 DeepSeek 官方的 `dsh` Agent 调度框架接进 OpenDesign 当原生运行时，支持结构化思考、工具调用、模型发现、中断取消和会话恢复。生成的文件会留在 OpenDesign 的工作流里，可直接实时预览和交付。

<p align="center">
  <img src="https://repo-assets.open-design.ai/resources/images/hero.png" alt="OpenDesign 主视觉横幅 —— 标题「Claude Design 的开源替代方案」叠加在古典柱廊与长袍人物的画面上，背景是数字代码，配有设计系统、插件、编程 Agent、媒体供应商四项数据卡片" width="100%" />
</p>

<p align="center">
  <a href="https://open-design.ai/?utm_source=github&utm_medium=referral&utm_content=readme_website">官网</a> ·
  <a href="https://open-design.ai/?utm_source=github&utm_medium=referral&utm_content=readme_download">下载</a> ·
  <a href="https://open-design.ai/cloud/?utm_source=github&utm_medium=referral&utm_content=readme_cloud">OpenDesign Cloud</a> ·
  <a href="https://discord.gg/mHAjSMV6gz">Discord</a> ·
  <a href="https://x.com/OpenDesignHQ">关注 @OpenDesignHQ</a>
</p>

<p align="center">
  <a href="https://github.com/nexu-io/open-design/releases"><img alt="版本" src="https://img.shields.io/github/v/release/nexu-io/open-design?style=flat&color=blueviolet&label=release&include_prereleases&display_name=tag" /></a>
  <a href="LICENSE"><img alt="许可证" src="https://img.shields.io/badge/license-Apache%202.0-blue.svg?style=flat" /></a>
  <a href="https://discord.gg/mHAjSMV6gz"><img alt="discord" src="https://img.shields.io/discord/1479002485040480266?style=flat&logo=discord&logoColor=white&label=discord&color=5865F2&cacheSeconds=3600" /></a>
  <a href="QUICKSTART.md"><img alt="快速上手" src="https://img.shields.io/badge/quickstart-3%20commands-green?style=flat" /></a>
</p>

<p align="center"><b>English</b> · <a href="docs/i18n/README.es.md">Español</a> · <a href="docs/i18n/README.pt-BR.md">Português</a> · <a href="docs/i18n/README.de.md">Deutsch</a> · <a href="docs/i18n/README.fr.md">Français</a> · <a href="docs/i18n/README.zh-CN.md">简体中文</a> · <a href="docs/i18n/README.zh-TW.md">繁體中文</a> · <a href="docs/i18n/README.ko.md">한국어</a> · <a href="docs/i18n/README.ja-JP.md">日本語</a> · <a href="docs/i18n/README.ar.md">العربية</a> · <a href="docs/i18n/README.ru.md">Русский</a> · <a href="docs/i18n/README.uk.md">Українська</a> · <a href="docs/i18n/README.tr.md">Türkçe</a> · <a href="docs/i18n/README.th.md">ภาษาไทย</a></p>

---

## OpenDesign 是什么

🎨 **Claude Design 的开源替代方案。**　🖥️ **面向 macOS 和 Windows 的本地优先原生桌面应用。**　⚡ **可组合的技能、品牌级的 `DESIGN.md` 设计系统、开箱即用的插件。**　🖼️ 能生成 **网页 · 桌面 · 移动端原型**、**实时看板 / 交互式产物**、**演示稿**、**图片**、**视频**，以及 **HyperFrames** 动态图形。🔒 沙箱 iframe 预览 · 导出 HTML / PDF / PPTX / MP4。　🤖 **可跑在 DeepSeek Harness（`dsh`）· Claude Code · OpenClaw · Codex · Cursor · OpenCode · Qwen · Copilot · Amp · Hermes · Kimi · Antigravity 等 26 个不同的本地命令行程序之上**，也可以通过 BYOK 接任意 OpenAI 兼容端点。

Anthropic 随 Claude Design 发布的那一套「Agent 原生」闭环——摸清需求、锁定方向、流式产出成品、自我批判、交付——原本是封闭的。OpenDesign 就是把它**拆成一套文件系统**：功能技能、渲染设计模板、设计系统、插件，全都是你笔记本上已有的那些编程 Agent 能读、能写、能改造的普通文件。你的命令行就是设计引擎，你的笔记本就是工作室，你团队的 `DESIGN.md` 就是品牌契约。

它也是**Agent 时代的 Figma 替代品**——不是在画布上推像素，而是直接交付用真 CSS、真字体、真组件写出来的单页成品，直接导出 HTML / PDF / PPTX / MP4——而且已经套好了你的设计系统，已经能在你天天用的那个 Agent 里跑起来。

---

## 产品导览

快速看一遍 OpenDesign 的核心工作流。从 **首页**写一份需求开始，到 **插件**页挑可复用的技能，再到把品牌参考变成一个 **设计系统**。然后进入某个项目的 **工作室**，在一个地方创建和打磨原型、演示稿、移动应用、图片、文档和 HyperFrames。

### 核心页面

<table>
<tr>
<td valign="top">
<img src="docs/screenshots/product-tour/home.png" alt="OpenDesign 首页，含产物类型、需求撰写框、模型选择器与示例" /><br/>
<sub><b>首页</b> —— 选一种产物类型、写下需求，开工前先定好设计系统、工作目录和模型。</sub>
</td>
</tr>
</table>

<table>
<tr>
<td width="50%" valign="top">
<img src="docs/screenshots/product-tour/plugins.png" alt="OpenDesign 插件页，展示官方技能目录" /><br/>
<sub><b>插件</b> —— 按分类浏览官方技能、搜索目录，点 <code>试一下</code> 直接启动工作流。</sub>
</td>
<td width="50%" valign="top">
<img src="docs/screenshots/product-tour/design-system.png" alt="OpenDesign 工作室里的 Shopify 设计系统预览" /><br/>
<sub><b>设计系统</b> —— 提炼并打磨一个品牌的视觉语言，预览结果，然后在同一个工作区里用它创作。</sub>
</td>
</tr>
</table>

### 工作室 —— 一个项目里做六种产物

在项目的工作室里，对话、生成的文件和实时预览是放在一起的，横跨六种产物类型：

<table>
<tr>
<td width="50%" valign="top">
<img src="docs/screenshots/product-tour/studio-prototype.png" alt="OpenDesign 工作室里的网页原型预览" /><br/>
<sub><b>原型</b> —— 生成或复刻网页体验，检查渲染出来的页面，就地跟 Agent 反复打磨。</sub>
</td>
<td width="50%" valign="top">
<img src="docs/screenshots/product-tour/studio-deck.png" alt="OpenDesign 工作室里的多页演示稿预览" /><br/>
<sub><b>演示稿</b> —— 做多页幻灯片，检查缩略图和演讲备注，好了就导出。</sub>
</td>
</tr>
<tr>
<td width="50%" valign="top">
<img src="docs/screenshots/product-tour/studio-mobile-app.png" alt="移动应用产物预览" /><br/>
<sub><b>移动应用</b> —— 在设备预览里生成和打磨移动端界面，旁边就是对话、输出文件和下一步操作。</sub>
</td>
<td width="50%" valign="top">
<img src="docs/screenshots/product-tour/studio-image.png" alt="生成的图片预览" /><br/>
<sub><b>图片</b> —— 根据项目对话生成视觉素材，全尺寸预览结果，然后下载或打开。</sub>
</td>
</tr>
<tr>
<td width="50%" valign="top">
<img src="docs/screenshots/product-tour/studio-document.png" alt="多页文档预览" /><br/>
<sub><b>文档</b> —— 做精美的多页指南和编辑类文档，检查渲染出来的版式，好了就导出或分享。</sub>
</td>
<td width="50%" valign="top">
<img src="docs/screenshots/product-tour/studio-hyperframe.png" alt="HyperFrame 动态图形预览" /><br/>
<sub><b>HyperFrame</b> —— 做代码驱动的动效图形，在工作室里预览动画，导出成片视频。</sub>
</td>
</tr>
</table>

---

## 平台兼容性

> OpenDesign 用两种方式接入主流编程 Agent：对「消费 OD」的 Agent 走 **技能、CLI、MCP**；对「由 OD 直接启动」的 Agent 走 **原生运行时适配器**。DeepSeek Harness 是通过官方 `dsh` CLI 接入的一等公民原生运行时，支持结构化流式输出、模型发现、中断取消和会话恢复。

| 编程 Agent / 平台 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | 状态 &nbsp;&nbsp; | 快速配置 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; |
|---|:---:|---|
| [Claude Code](https://docs.anthropic.com/en/docs/claude-code) | ✅ 支持 | `od mcp install claude` |
| [Claude Desktop](https://claude.ai/download) | ✅ 支持¹ | `od mcp install claude-desktop` |
| [Codex CLI](https://github.com/openai/codex) | ✅ 支持 | `od mcp install codex` |
| [DeepSeek Reasonix](https://github.com/esengine/DeepSeek-Reasonix) | ✅ 支持 | `od mcp install reasonix` |
| [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness) | ✅ 原生运行时 | `od agent setup deepseek-harness` |
| [Raven](https://github.com/EverMind-AI/Raven) | ✅ 支持 | `od mcp install raven` |
| [Cursor](https://www.cursor.com/cli) | ✅ 支持 | `od mcp install cursor` |
| [VS Code + GitHub Copilot](https://github.com/features/copilot) | ✅ 支持 | `od mcp install copilot` |
| [GitHub Copilot CLI](https://github.com/features/copilot/cli) | ✅ 支持 | `od mcp install copilot` |
| [OpenCode](https://opencode.ai/) | ✅ 支持 | `od mcp install opencode` |
| [OpenClaw](https://github.com/openclaw/openclaw) | ✅ 支持 | `od mcp install openclaw` |
| [Antigravity](https://antigravity.google) | ✅ 支持 | `od mcp install antigravity` |
| [Cline](https://github.com/cline/cline) | ✅ 支持 | `od mcp install cline` |
| [Trae](https://www.trae.ai/) | ✅ 支持 | `od mcp install trae` |
| [Kimi CLI](https://github.com/MoonshotAI/kimi-cli) | ✅ 支持 | `od mcp install kimi` |
| [Kiro](https://kiro.dev) | ✅ 支持 | `od mcp install kiro` |
| [Pi Agent](https://github.com/badlogic/pi-mono) | ✅ 支持 | `od mcp install pi` |
| [Mistral Vibe CLI](https://github.com/mistralai/mistral-vibe) | ✅ 支持 | `od mcp install vibe` |
| [Hermes Agent](https://github.com/nousresearch/hermes-agent) | ✅ 支持 | `od mcp install hermes` |

用 DeepSeek Harness 的话，先装官方的 `dsh` CLI，然后在 OpenDesign 里选它，或者跑 `od agent setup deepseek-harness` 来安装/修复 OD 的连接组件。MCP 集成方面：`od mcp install <agent> --print` 可以空跑预览 · `--uninstall` 卸载 · 完整列表见 `od mcp install --help`。

¹ Claude Desktop 的自动 MCP 配置目前只支持 macOS 和 Windows。

<p align="center">
  <img src="https://repo-assets.open-design.ai/resources/images/coding-agents.png" alt="OpenDesign 支持的 26 个编程 Agent CLI —— DeepSeek Harness · Claude Code · Codex · OpenCode · Hermes · Antigravity · Vela · Grok Build · Kimi · Cursor Agent · Qwen · Qoder · GitHub Copilot · Pi · Kiro · Kilo · Mistral Vibe · DeepSeek · Reasonix · Aider · Amp · CodeBuddy · Mimo · AtomCode · Devin · Trae" width="100%" />
</p>

**没装任何 CLI？** BYOK 代理（`POST /api/proxy/{anthropic,openai,azure,google,ollama,senseaudio}/stream`）给你同样的闭环（不起子进程）——填上 `baseUrl` + `apiKey` + `model` 就行，内置 OpenAI、Atlas Cloud、Anthropic、Azure OpenAI、Google Gemini、Ollama、LM Studio、vLLM 等预设，或任意 OpenAI 兼容端点。Atlas Cloud 用 `https://api.atlascloud.ai/v1`，配你自己的 Key 和 OpenAI 兼容的模型 ID，比如 `qwen/qwen3.5-flash`。按目标地址做的 SSRF 防护会在守护进程边界拦掉内网 IP / 链路本地地址 / CGNAT 地址。

运行时定义放在 [`apps/daemon/src/runtimes/defs/`](apps/daemon/src/runtimes/defs/)，注册和共享流处理在 [`apps/daemon/src/runtimes/`](apps/daemon/src/runtimes/)。适配器契约见 [`docs/agent-adapters.md`](docs/agent-adapters.md)。

---

## 演示

四大产品品类，全部由跑在你笔记本上的编程 Agent 渲染出来。点缩略图看真实案例。

### 1 · 原型 —— 网页 · 桌面 · 移动端

默认的输出形态。读取你的 `DESIGN.md`、在沙箱 iframe 里渲染的单页 HTML 产物。

<table>
<tr>
<td width="50%" valign="top">
<img src="docs/screenshots/skills/dating-web.png" alt="网页原型 dating-web" /><br/>
<sub><b>网页原型</b> —— 一份带滚动条、KPI 和图表的编辑风格看板。直接由 <code>design-templates/dating-web/</code> 渲染出来。</sub>
</td>
<td width="50%" valign="top">
<img src="docs/screenshots/skills/gamified-app.png" alt="游戏化应用" /><br/>
<sub><b>移动应用原型</b> —— 三屏的游戏化流程，带经验值进度条和任务详情。可以直接交给 Cursor / Codex / Claude Code 变成 React/Next/Vue。</sub>
</td>
</tr>
</table>

### 2 · 实时产物与看板

实时看板、决策室、KPI 墙——通过一个「微调面板」拉数据、可以就地编辑的单页产物。

<table>
<tr>
<td width="50%" valign="top">
<img src="docs/screenshots/skills/live-dashboard.png" alt="实时看板" /><br/>
<sub><b>实时看板</b> —— 一面可编辑的 KPI 墙，微调面板会把值得调的参数都摆出来。Agent 输出一份 manifest，iframe 不用重载就直接重渲染。</sub>
</td>
<td width="50%" valign="top">
<img src="docs/screenshots/skills/research-decision-room.png" alt="决策室" /><br/>
<sub><b>决策室</b> —— 给产品 / 研究 / 运营会议用的多来源简报产物。</sub>
</td>
</tr>
<tr>
<td width="50%" valign="top">
<img src="docs/screenshots/skills/github-dashboard.png" alt="GitHub 看板" /><br/>
<sub><b>GitHub 风格看板</b> —— 把仓库指标做成实时产物呈现。</sub>
</td>
<td width="50%" valign="top">
<img src="docs/screenshots/skills/flowai-live-dashboard-template.png" alt="Flow 实时看板" /><br/>
<sub><b>Flow 实时看板模板</b> —— 面向特定领域的 KPI 模板，通过当前生效的 <code>DESIGN.md</code> 套上品牌风格。</sub>
</td>
</tr>
</table>

### 3 · 演示稿 —— 杂志风、周报、融资路演

<table>
<tr>
<td width="50%" valign="top">
<img src="docs/screenshots/07-magazine-deck.png" alt="杂志风演示稿（guizang-ppt）" /><br/>
<sub><b>演示稿模式（guizang-ppt）</b> —— 杂志版式、WebGL 主视觉、P0/P1/P2 清单。原封不动打包自 <a href="https://github.com/op7418/guizang-ppt-skill"><code>op7418/guizang-ppt-skill</code></a>，保留其原始许可证。</sub>
</td>
<td width="50%" valign="top">
<img src="docs/screenshots/skills/deck-swiss-international.png" alt="瑞士风格演示稿" /><br/>
<sub><b>瑞士国际风格演示稿</b> —— 网格锚定，单色点缀。是 <code>design-templates/html-ppt-*/</code> 下 <b>15 套演示稿模板</b>和 <b>36 种主题</b>中的一种。</sub>
</td>
</tr>
</table>

每份演示稿都能导出成 **HTML**（单文件、资源内联）、**PDF**（浏览器打印，针对演示稿优化）、**PPTX**（Agent 驱动的技能）、**ZIP**（压缩包）或 **Markdown**。

### 4 · 图片 —— `gpt-image-2`、ImageRouter、自定义 API

<table>
<tr>
<td width="20%" valign="top"><img src="https://cms-assets.youmind.com/media/1776662673014_nf0taw_HGRMNDybsAAGG88.jpg" alt="插画风城市美食地图" /><br/><sub><b>插画风城市美食地图</b><br/>手绘编辑风旅行海报</sub></td>
<td width="20%" valign="top"><img src="https://cms-assets.youmind.com/media/1777453149026_gd2k50_HHCSvymboAAVscc.jpg" alt="电影感电梯场景" /><br/><sub><b>电影感电梯场景</b><br/>单帧编辑级静帧</sub></td>
<td width="20%" valign="top"><img src="https://cms-assets.youmind.com/media/1777453164993_mt5b69_HHDoWfeaUAEA6Vt.jpg" alt="赛博朋克动漫头像" /><br/><sub><b>赛博朋克头像</b><br/>个人头像 —— 霓虹面部文字</sub></td>
<td width="20%" valign="top"><img src="https://cms-assets.youmind.com/media/1776661968404_8a5flm_HGQc_KOaMAA2vt0.jpg" alt="3D 石阶演化图" /><br/><sub><b>3D 石阶</b><br/>凿石质感信息图</sub></td>
<td width="20%" valign="top"><img src="https://cms-assets.youmind.com/media/1777453184257_vb9hvl_HG9tAkOa4AAuRrn.jpg" alt="质感人像" /><br/><sub><b>质感人像</b><br/>编辑风棚拍</sub></td>
</tr>
</table>

**93 条拿来就能复现的提示词**放在 [`prompt-templates/`](prompt-templates/) —— 带预览缩略图、完整提示词正文、目标模型、宽高比和来源标注。点一下就把需求丢进撰写框。

### 5 · 视频与 HyperFrames —— Agent 原生的动态图形

**[HyperFrames][hyperframes]** 是 HeyGen 开源、Agent 原生的视频框架，在 OpenDesign 里被当作一等公民集成进来。Agent 写 HTML + CSS + GSAP，HyperFrames 用无头 Chrome + FFmpeg 把它渲染成确定性的 MP4。配上 **Seedance 2.0** 做电影感文生视频 / 图生视频，**Veo 3 / Sora 2 / Kling 2** 做路由模型变体，**Suno v5 / Lyria 2** 做音频层。

<table>
<tr>
<td width="25%" valign="top"><a href="prompt-templates/video/hyperframes-saas-product-promo-30s.json"><img src="https://static.heygen.ai/hyperframes-oss/docs/images/catalog/blocks/app-showcase.png" alt="SaaS 宣传片" /></a><br/><sub><b>30 秒 SaaS 产品宣传片</b> · 16:9 · UI 3D 揭示</sub></td>
<td width="25%" valign="top"><a href="prompt-templates/video/hyperframes-tiktok-karaoke-talking-head.json"><img src="https://static.heygen.ai/hyperframes-oss/docs/images/catalog/blocks/tiktok-follow.png" alt="TikTok 卡拉 OK" /></a><br/><sub><b>TikTok 卡拉 OK 口播</b> · 9:16 · 语音合成 + 逐字同步字幕</sub></td>
<td width="25%" valign="top"><a href="prompt-templates/video/hyperframes-brand-sizzle-reel.json"><img src="https://static.heygen.ai/hyperframes-oss/docs/images/catalog/blocks/logo-outro.png" alt="品牌高光合集" /></a><br/><sub><b>30 秒品牌高光合集</b> · 16:9 · 音频驱动的动态字体</sub></td>
<td width="25%" valign="top"><a href="prompt-templates/video/hyperframes-data-bar-chart-race.json"><img src="https://static.heygen.ai/hyperframes-oss/docs/images/catalog/blocks/data-chart.png" alt="柱状图竞赛" /></a><br/><sub><b>柱状图竞赛</b> · 16:9 · 纽约时报风格数据信息图</sub></td>
</tr>
<tr>
<td width="25%" valign="top"><a href="prompt-templates/video/hyperframes-flight-map-route.json"><img src="https://static.heygen.ai/hyperframes-oss/docs/images/catalog/blocks/nyc-paris-flight.png" alt="航线地图" /></a><br/><sub><b>航线地图</b> · 16:9 · 苹果风格航线揭示</sub></td>
<td width="25%" valign="top"><a href="prompt-templates/video/hyperframes-logo-outro-cinematic.json"><img src="https://static.heygen.ai/hyperframes-oss/docs/images/catalog/blocks/logo-outro.png" alt="Logo 收尾" /></a><br/><sub><b>4 秒电影感 Logo 收尾</b> · 16:9 · 逐块拼装 + 辉光</sub></td>
<td width="25%" valign="top"><a href="prompt-templates/video/hyperframes-money-counter-hype.json"><img src="https://static.heygen.ai/hyperframes-oss/docs/images/catalog/blocks/apple-money-count.png" alt="金额滚动" /></a><br/><sub><b>$0 → $10K 金额滚动</b> · 9:16 · 苹果风格高燃</sub></td>
<td width="25%" valign="top"><a href="prompt-templates/video/hyperframes-website-to-video-promo.json"><img src="https://static.heygen.ai/hyperframes-oss/docs/images/catalog/blocks/instagram-follow.png" alt="网页转视频" /></a><br/><sub><b>网页转视频</b> · 16:9 · 按三种视口抓取站点</sub></td>
</tr>
</table>

仓库自带 11 套 HyperFrames 模板 + 39 条 Seedance 提示词。目录缩略图版权归 HeyGen；框架本身是 Apache-2.0。OD 特有的渲染流程（合成缓存、沙箱执行绕过、把 MP4 当芯片用）详见 [`design-templates/hyperframes/`](design-templates/hyperframes/)。

[hyperframes]: https://github.com/heygen-com/hyperframes

---

## 为什么选 OpenDesign

> **2026 年 4 月，Anthropic 发布了 Claude Design —— 这是大模型第一次不再只写文字，而是直接交付设计成品。** 它火了。但它始终是闭源的、只收费、只能用云端，锁死在 Anthropic 的模型、Anthropic 的技能、Anthropic 的界面上。不能检出代码，不能自托管，不能部署到 Vercel，不能换成你自己的 Agent。

OpenDesign（简称 OD）就是那个开源替代品。同样的闭环，同样的「成品优先」心智模型，一点锁定都没有：

- 🤖 **Agent 原生、模型无感。** 我们不自带 Agent。你 `PATH` 里本来就有的 `claude` / `codex` / `cursor-agent` / `copilot` / `hermes` / `kimi` 就是设计引擎。点一下就能换。
- 🧠 **默认就是品牌级。** 每次渲染都把当前包的 `DESIGN.md` 当作核心品牌契约来读。仓库自带 151 个设计系统包；早期包可能只有 `DESIGN.md`，新一些的包还会带 `manifest.json`、`tokens.css`、组件、素材和来源证据。丢一个文件夹进去，选择器就能找到它。
- 🖥️ **本地优先，每一层都支持 BYOK。** 提供 macOS（Apple 芯片 + Intel）和 Windows（x64）的原生桌面应用。Linux 桌面用户目前可以[从源码运行](#-run-from-source)，最新正式版没有预编译的 Linux 包。产品分析和会话回放需要你同意才开；脱敏后的安全与稳定性遥测始终开启。在描述守护进程的数据路径之前，贡献者和运维人员**必须**先读 `AGENTS.md` 里的 **Daemon data directory contract**。本 README **不得**复述它。
- 🌍 **四个层面都可组合。** **插件**承载可运行的工作流 · 功能**技能**承载 Agent 行为 · **设计模板**承载渲染蓝图 · **设计系统**承载品牌。四者都用可移植、可版本化的目录，任何人都能编写和发布。
- 🔁 **刷新已有代码库。** 把一个 `git` 仓库 + `DESIGN.md` 交给 Agent，它就能按品牌规范重构你真实的组件。专门的插件能把 Figma / Pencil 的工作流迁移成 React / Next.js / Vue 代码。
- 🔒 **隐私是信念。** 一切都在你的数据所在的地方跑 —— 你的笔记本、你团队的服务器、你的 Vercel 项目。需要联网时，BYOK 代理有 SSRF 防护。

### 对比

| | Claude Design | Figma | Lovable / v0 / Bolt | **OpenDesign** |
|---|---|---|---|---|
| 开源 | ❌ | ❌ | ❌ | **✅ Apache-2.0** |
| 自托管 / 桌面端 | ❌ | ❌ | ❌ | **✅ macOS + Windows + Docker + Vercel 网页版** |
| Agent 原生（跑在你的 CLI 里） | 仅 Anthropic | ❌ | 仅云端 Agent | **✅ 25 个 CLI + BYOK** |
| 品牌级 `DESIGN.md` | 私有格式 | 主题 JSON | 有限的 token | **✅ 自带 151 套** |
| 技能 / 插件 / 模板 | 封闭 | 插件商店 | 封闭 | **✅ 100+ 功能技能 · 渲染模板 · 277 个插件** |
| HyperFrames（HTML→MP4） | ❌ | ❌ | ❌ | **✅ 一等公民** |
| 把已有仓库刷新成品牌规范 | ❌ | ❌ | ❌ | **✅ 通过 Agent + `DESIGN.md`** |
| 最低付费门槛 | Pro / Max / Team | Pro / Org | Pro / Team | **BYOK · 任意兼容端点** |

---

## 快速开始

### 🖥️ 下载桌面应用（推荐 —— 零配置）

用 OpenDesign 最快的方式。不用装 Node，不用装 pnpm，不用克隆仓库。

- **macOS**（Apple 芯片 · Intel x64）→ [**open-design.ai**](https://open-design.ai/?utm_source=github&utm_medium=referral&utm_content=readme_download_macos) 或 [GitHub Releases](https://github.com/nexu-io/open-design/releases)
- **Windows**（x64）→ [**open-design.ai**](https://open-design.ai/?utm_source=github&utm_medium=referral&utm_content=readme_download_windows) 或 [GitHub Releases](https://github.com/nexu-io/open-design/releases)
- **Linux** → 官方发布里目前没有预编译的 Linux 包。暂时请[从源码运行 OpenDesign](#-run-from-source)；Linux 发布工作跟踪在 [#4368](https://github.com/nexu-io/open-design/issues/4368)。

装完之后：应用会自动扫描你 `PATH` 里的每一个编程 Agent CLI，加载 100+ 功能技能、独立的渲染模板目录和 151 套设计系统，然后让你在入口界面里直接打字写需求。

### 🤖 装进你的编程 Agent（不开界面）

你完全可以不打开图形界面就用 OpenDesign —— 在 Claude Code、Codex、Cursor、Copilot、OpenClaw、Antigravity、Hermes、Kimi 等里面，把它当技能、插件或 MCP 服务来调。

如果你是通过 DMG 或 Homebrew cask 装的 macOS 桌面应用，你的 shell 可能仍然把 `od` 解析成苹果自带的 `/usr/bin/od`（八进制转储工具）。这种情况下，请打开桌面应用的 **设置 → MCP server**，复制针对你客户端的那段配置；它用的是绝对路径，不依赖裸 `od` 命令。

```bash
# 一行装进你正在用的那个 Agent：
od mcp install <agent>
# <agent> = claude | codex | reasonix | raven | cursor | copilot | openclaw
#         | antigravity | pi | vibe | hermes | cline | kimi | kiro
#         | trae | opencode

# 给 curl 安装方式用的托管等价命令：
curl -fsSL https://open-design.ai/install.sh | sh -s <agent>
```

`install.sh` 只是 `od mcp install` 的一层薄壳封装；它存在的意义是让托管 URL 返回 shell 而不是落地页的 HTML 兜底，并且当你的 shell 把 `od` 解析成非 OpenDesign 的二进制时能快速失败报错。

> **macOS / WSL2 用户：** `/usr/bin/od` 是系统的八进制转储命令，可能会盖掉 OpenDesign 的 `od` 命令。桌面应用用户请优先用 **设置 → MCP server** 里那段配置；WSL2 用户请先照 [`WSL2 配置指南`](docs/wsl-setup.md) 走一遍。

然后在 Agent 里面：

```
> 用 open-design，按 Linear 的设计系统生成一个落地页
```

在基于文件系统的本地 CLI 运行中，Agent 会把选中的功能技能或设计模板跟你的 `DESIGN.md` 组合起来，写出规范的项目文件，OpenDesign 再预览这些文件。走 BYOK / 纯 API、没有文件工具的运行，则直接返回一个完整的 `<artifact>` 块。

### 🐳 用 Docker 跑

```bash
git clone https://github.com/nexu-io/open-design.git
cd open-design/deploy
cp .env.example .env
echo "OD_API_TOKEN=$(openssl rand -hex 32)" >> .env
docker compose up -d
# 打开 http://127.0.0.1:7456
```

如果浏览器要你输账号密码，用户名填 `open-design`，密码填 `deploy/.env` 里那个 `OD_API_TOKEN` 的值。这样 Docker 桥接网络的流量也是带鉴权的，不需要用主机网络。API 客户端可以继续用 `Authorization: Bearer <OD_API_TOKEN>`。

### 🚀 部署到 Sealos

[![Deploy on Sealos](https://sealos.io/Deploy-on-Sealos.svg)](https://sealos.io/products/app-store/open-design/)

Sealos 应用商店模板跑的是已发布的 OpenDesign Docker 镜像，带持久化工作区存储和公共代理上的 Basic Auth。要做自定义公开或共享的 Docker 部署，请照 [`deploy/README.md`](deploy/README.md#local-compose) 里的反向代理和 `OPEN_DESIGN_ALLOWED_ORIGINS` 指引来。

### 🧑‍💻 从源码运行

```bash
git clone https://github.com/nexu-io/open-design.git
cd open-design
corepack enable && pnpm install
pnpm tools-dev run web
```

打开 `tools-dev` 打印出来的那个网址；除非你显式传了端口参数，开发端口是动态分配的。

需要 Node `~24`、pnpm `10.33.x`。WSL2 用户见 [`docs/wsl-setup.md`](docs/wsl-setup.md)；原生 Windows 用户见 [`docs/windows-troubleshooting.md`](docs/windows-troubleshooting.md)。完整的快速上手、环境变量和打包构建流程 → [`QUICKSTART.md`](QUICKSTART.md)。

### 一个完整工作流 —— 从需求到成品

`需求 → 插件 → 方向 → 设计系统 → 成品 → 交付 → 记忆`

1. **产品经理提交一份需求。** 插件选择器会给出落地页 · 融资路演 · 看板 · 社交帖 · PM 规格文档 · OKR 计分卡等选项。
2. **设计师（或 Agent）锁定方向。** 没有品牌？从 5 个精选方向里挑。有品牌？丢一张截图或一个网址进去 → Agent 会连 GitHub、导入 Figma，把品牌固化成一份可复用的 `DESIGN.md`。
3. **Agent 做出第一版交付物。** 插件 + 功能技能或设计模板 + `DESIGN.md` 三者绑定。基于文件系统的 CLI 运行会写出规范的项目文件，预览跟着这些文件走；走 BYOK / 纯 API、没有文件工具的运行则返回一个完整的 `<artifact>` 块。
4. **交给工程。** 成品是真 HTML/CSS —— 丢进 Cursor、Codex 或 Claude Code 就能当代码接着往下做。或者直接导出 PPTX / PDF / MP4 给市场部。
5. **OpenDesign 越用越聪明。** 你的截图、字体、调色板和确认过的成品会累积成下一次会话的默认值。返工更少，跑偏更少。

---

## 在你的编程 Agent 里用 OpenDesign

OpenDesign 提供一个 **stdio MCP 服务**和分 Agent 的 **安装脚本**。别的仓库里任何兼容 MCP 的 Agent 都能直接读你本地 OpenDesign 项目的文件 —— token CSS、JSX 组件、入口 HTML —— 当成可以按名字查询的结构化 API。Agent 看到的永远是活文件，不是过期的导出包。

```bash
# 一行安装（支持 16+ 个 CLI）：
od mcp install <agent>

# 然后 Agent 就能：
od project list --json
od files list <project-id> --json
od files read <project-id> <relative-path>
od plugin list --json
od skills list --json
```

**为什么用 MCP？** 每轮迭代都导出再重新挂一个 zip 包，会打断心流。MCP 把设计源文件直接暴露出来 —— Agent 看到的永远是活文件。

**对一个从零开始的 Agent，** 安装器会放置 `~/.config/<agent>/open-design.json`（或对应平台的等价路径），外加一段可复制粘贴的 MCP 配置。Cursor 拿到一个一键深链；Claude Code 拿到一行 `claude mcp add-json`；其他每个 Agent 都拿到符合它配置格式的 JSON。在 macOS 桌面安装上，请优先用设置里那段配置，而不是在终端里手敲裸 `od mcp install <agent>`，因为 `/usr/bin/od` 可能在 PATH 上抢先。完整的分 Agent 流程 → 桌面应用的 **设置 → MCP server**，或 [`docs/agent-adapters.md`](docs/agent-adapters.md)。

**安全模型。** 默认只读，守护进程只绑 `127.0.0.1`，代理边界上拦 SSRF。要暴露到局域网必须显式设 `OD_BIND_HOST` 加 `OD_ALLOWED_ORIGINS`。连接器凭据和实时产物预览路由无论如何都只留在本机回环上。

**内网自托管的模型端点。** 为防止 SSRF，守护进程默认会拦掉解析到私有/内网地址段的供应商 base URL（RFC1918、链路本地、CGNAT 和云元数据 IP），并提示 `Internal IPs blocked`。如果你跑的是内网自托管网关（比如在仅 VPN 可达的 `10.x` / `192.168.x` 地址上的 LiteLLM 或 Ollama），用 `OD_ALLOWED_INTERNAL_HOSTS=<host1>,<host2>,...` 把那个主机放行 —— 逗号或空格分隔的裸主机名或 IP 列表（`10.0.0.5`、`litellm.internal.corp`；也接受 `host:port` 或完整 URL，会化简成主机名；IPv6 必须加方括号，比如 `[fd00::1]`）。这份白名单是严格的显式选择加入（默认为空）、精确主机匹配（不做子域或子串匹配），并且**只**作用于你配置的供应商端点（连接测试、模型发现、BYOK 对话）。它**故意不**放松对上游响应里返回的下载 URL 的防护，那些仍然被拦。格式错误 —— 或者用了不支持的 CIDR 记法 —— 会被丢弃并给出警告，而不是被静默信任，这样一个拼写错误永远不会悄悄放宽（或没能放宽）防护。把某个主机名加进白名单，意味着信任它解析出来的任何地址（跟 `OD_ALLOWED_ORIGINS` 一样）；如果你希望重新校验 DNS 解析后的地址，那就把解析出来的 IP 加进白名单。

---

## 技能与设计模板

**100+ 个功能技能随仓库发布，放在 [`skills/`](skills/) 里**。每个都遵循 Agent Skills 的 [`SKILL.md`][skill] 约定，提供可复用的 Agent 行为、参考资料或工具函数。可渲染的起手式单独放在 [`design-templates/`](design-templates/)；它们也可能用 `SKILL.md`，但会进设计模板目录，而不是功能技能注册表。

设计模板目录由两种**模式**撑起来：`prototype`（网页/移动端/桌面端的单页产物）和 `deck`（横向滑动的演示稿）。其他模板覆盖 `image`、`video`、`audio` 和工具类场景。**`scenario`** 字段按受众给模板分组：`design` · `marketing` · `operation` · `engineering` · `product` · `finance` · `hr` · `sale` · `personal`。

| 设计模板 | 模式 | 场景 | 产出什么 |
|---|---|---|---|
| [`web-prototype`](design-templates/web-prototype/) | prototype | design | 默认落地页 / 主视觉 |
| [`saas-landing`](design-templates/saas-landing/) | prototype | marketing | 主视觉 / 功能 / 定价 / 行动号召 |
| [`dashboard`](design-templates/dashboard/) | prototype | operation | 后台 / 分析看板（带侧边栏） |
| [`mobile-app`](design-templates/mobile-app/) | prototype | design | iPhone 15 Pro / Pixel 框起来的应用 |
| [`mobile-onboarding`](design-templates/mobile-onboarding/) | prototype | design | 闪屏 · 价值主张 · 登录流程 |
| [`social-carousel`](design-templates/social-carousel/) | prototype | marketing | 3 张 1080×1080 的轮播图 |
| [`email-marketing`](design-templates/email-marketing/) | prototype | marketing | 有 table 兜底的品宣邮件 |
| [`magazine-poster`](design-templates/magazine-poster/) | prototype | marketing | 单页杂志版式 |
| [`motion-frames`](design-templates/motion-frames/) | prototype | marketing | 循环播放的 CSS 动态主视觉 |
| [`sprite-animation`](design-templates/sprite-animation/) | prototype | marketing | 8 比特像素动画解说 |
| [`pm-spec`](design-templates/pm-spec/) | prototype | product | PM 规格文档（带目录 + 决策记录） |
| [`team-okrs`](design-templates/team-okrs/) | prototype | product | OKR 计分卡 |
| [`eng-runbook`](design-templates/eng-runbook/) | prototype | engineering | 故障处理手册 |
| [`finance-report`](design-templates/finance-report/) | prototype | finance | 高管财务摘要 |
| [`hr-onboarding`](design-templates/hr-onboarding/) | prototype | hr | 岗位入职计划 |
| [`guizang-ppt`](design-templates/guizang-ppt/) | deck | marketing | 杂志风网页 PPT（演示稿默认） |
| [`html-ppt-*`](design-templates/) | deck | marketing | 15 套模板 × 36 种主题（母版在 [`design-templates/html-ppt/`](design-templates/html-ppt/)） |
| [`hyperframes`](design-templates/hyperframes/) | video | marketing | HTML → MP4 动态图形（HeyGen 开源框架） |
| [`critique`](design-templates/critique/) | utility | design | 五维自我批判评分表 |
| [`tweaks`](design-templates/tweaks/) | utility | design | AI 输出的微调面板 manifest |

完整协议和目录划分 → [`docs/skills-protocol.md`](docs/skills-protocol.md)。注册表端点：功能技能用 `GET /api/skills`，渲染模板用 `GET /api/design-templates`。

---

## 设计系统

**仓库自带 151 个以 `DESIGN.md` 为核心的品牌级设计系统包**。早期包可能只含这份 Markdown 契约；新一些的包还会带 `manifest.json`、编译好的 `tokens.css`、组件样例、素材和来源证据。目录里混有源自上游的系统和项目自有的补充；[`design-systems/README.md`](design-systems/README.md) 记录了包的结构和来源。换一套系统 → 下一次渲染就用新的 token。

<details>
<summary><b>完整目录（点击展开）</b></summary>

**AI 与大模型** — `claude` · `cohere` · `mistral-ai` · `minimax` · `together-ai` · `replicate` · `runwayml` · `elevenlabs` · `ollama` · `x-ai`

**开发者工具** — `cursor` · `vercel` · `linear-app` · `framer` · `expo` · `clickhouse` · `mongodb` · `supabase` · `hashicorp` · `posthog` · `sentry` · `warp` · `webflow` · `sanity` · `mintlify` · `lovable` · `composio` · `opencode-ai` · `voltagent`

**效率工具** — `notion` · `figma` · `miro` · `airtable` · `superhuman` · `intercom` · `zapier` · `cal` · `clay` · `raycast`

**金融科技** — `stripe` · `coinbase` · `binance` · `kraken` · `mastercard` · `revolut` · `wise`

**电商** — `shopify` · `airbnb` · `uber` · `nike` · `starbucks` · `pinterest`

**媒体** — `spotify` · `playstation` · `wired` · `theverge` · `meta`

**汽车** — `tesla` · `bmw` · `ferrari` · `lamborghini` · `bugatti` · `renault`

**其它** — `apple` · `ibm` · `nvidia` · `vodafone` · `resend` · `spacex`

**起手式** — `default`（中性现代）· `warm-editorial`

</details>

可以用 [`scripts/sync-design-systems.ts`](scripts/sync-design-systems.ts) 重新导入整个库。想加你自己的品牌 → 往 `design-systems/<brand>/` 里丢一份 `DESIGN.md`。完整指南 → [`design-systems/README.md`](design-systems/README.md)。

[acd2]: https://github.com/VoltAgent/awesome-design-md

---

## 插件

**277 个官方插件，外加 183 个可再加工的参考示例**，放在 [`plugins/_official/`](plugins/_official/)。每一项都是一个以 `open-design.json` 为锚点的可移植插件目录，再配上它那种类型所需的载荷：比如 Agent 工作流要 `SKILL.md`，媒体模板要 `template.json`，设计系统条目要 `DESIGN.md`。直接跳到某个分类：

| 分类 | 数量 | 内容 |
|---|---|---|
| [`scenarios/`](plugins/_official/scenarios/) | 13 | 完整设计场景 —— [`od-default`](plugins/_official/scenarios/od-default/)、[`od-design-refine`](plugins/_official/scenarios/od-design-refine/)、[`od-figma-migration`](plugins/_official/scenarios/od-figma-migration/)、[`od-code-migration`](plugins/_official/scenarios/od-code-migration/)、[`od-react-export`](plugins/_official/scenarios/od-react-export/)、[`od-nextjs-export`](plugins/_official/scenarios/od-nextjs-export/)、[`od-vue-export`](plugins/_official/scenarios/od-vue-export/)、[`od-media-generation`](plugins/_official/scenarios/od-media-generation/)、[`od-new-generation`](plugins/_official/scenarios/od-new-generation/)、[`od-tune-collab`](plugins/_official/scenarios/od-tune-collab/)、[`od-plugin-authoring`](plugins/_official/scenarios/od-plugin-authoring/)、[`od-share-to-community`](plugins/_official/scenarios/od-share-to-community/)、[`od-web-effect-extractor`](plugins/_official/scenarios/od-web-effect-extractor/) |
| [`image-templates/`](plugins/_official/image-templates/) | 45 | 一次成图的提示词 —— 编辑风、电影感、产品、人像 |
| [`video-templates/`](plugins/_official/video-templates/) | 63 | HyperFrames / Seedance / Veo 动态模板 |
| [`design-systems/`](plugins/_official/design-systems/) | 143 | 包装成插件的品牌 `DESIGN.md` |
| [`atoms/`](plugins/_official/atoms/) | 13 | 可复用的 UI 片段（按钮、主视觉、KPI 卡片） |
| [`examples/`](plugins/_official/examples/) | 183 | 可再加工的参考产出 |

另外 [`plugins/community/`](plugins/community/) 放社区插件，[`plugins/registry/`](plugins/registry/) 放发布流程。

### 插件能做什么

- 🤖 **在任何编程 Agent 里跑** —— [Claude Code](docs/agent-adapters.md)、Codex、Cursor、Copilot、[OpenClaw](https://github.com/openclaw/openclaw)、[Antigravity](https://antigravity.google)、Hermes、Kimi……都走 Agent 本来就认识的那套技能协议。
- 🔁 **迁移 Figma / Pencil 工作流** → 变成 React、Next.js 或 Vue 源码。见 [`od-figma-migration`](plugins/_official/scenarios/od-figma-migration/)。
- 🛠️ **把已有代码库刷新成品牌规范** —— 把插件指向一个 `git` 仓库 + `DESIGN.md`，就能拿到一个 PR。见 [`od-code-migration`](plugins/_official/scenarios/od-code-migration/)。
- 💾 **沉淀自定义工作流** —— 你团队可复用的模板就摆在自带模板旁边。

### 使用插件

插件在 **网页界面** 和 **`od` 命令行**上是完全对等的 —— 同一套 `/api/plugins` 端点，挑你顺手的那个用。

**在桌面 / 网页应用里：** 打开 **插件**页浏览市场，点 **安装**；在项目的工作室里，插件会显示成输入框上的小标签，点一下就应用（还会带上它声明的输入项）。

**在命令行上**（不开界面也能跑 —— 这是外部 Agent 走的路径）：

```bash
od plugin list                       # 列出已装插件（可用 --task-kind / --mode / --tag 过滤）
od plugin search "landing page"      # 按关键词搜
od plugin info od-default            # 查看某个插件的元数据、输入项和能力
od plugin install od-figma-migration # 从注册表安装；也可以接 ./本地文件夹 或 https://… 链接
od plugin apply od-default --input brief="给我们种子轮做一页路演"
od plugin upgrade od-default         # 升级
od plugin uninstall od-default       # 卸载
```

每条命令都支持 `--json`，所以你可以把它管道给 `jq` / `xargs` 接进自动化流程。

### 做一个插件

一个 OpenDesign 插件需要 `open-design.json`，外加它那种类型所需的载荷。工作流技能或场景还要带 `SKILL.md`；仅含 manifest 的模板和设计系统条目则用各自的载荷代替：

```
my-plugin/
├── open-design.json    ← 必填：市场元数据 + 输入项 + 流水线 + 能力
├── SKILL.md            ← Agent 技能 / 场景条目必填；其他插件类型省略
├── README.md           ← 可选：用法、安装、注册表链接
├── preview/            ← 可选：index.html / poster.png（视觉类插件强烈建议给）
└── examples/           ← 可选：具体用例
```

`open-design.json` 的核心字段：`specVersion`（当前 `1.0.0`）、`name`（稳定 ID）、`version`（语义化版本）、可选的 `compat.agentSkills[].path`（当条目暴露 Agent 技能时指向 `./SKILL.md`）、`od.kind`（`skill` / `scenario` / `atom` / `bundle`）、`od.taskKind`（`new-generation` / `figma-migration` / `code-migration` / `tune-collab`）、`od.mode`（输出形态，如 `prototype` / `deck` / `live-artifact` / `image` / `video` / `hyperframes` / `audio` / `design-system` / `scenario`）、`od.capabilities[]`（**声明最小集** —— 受限安装默认只给 `prompt:inject`）、`od.inputs[]`（应用时的参数）。

本地搭骨架 + 校验：

```bash
od plugin scaffold --id my-plugin --title "My Plugin"   # 生成骨架
od plugin validate ./my-plugin                          # 检查 manifest / 文件布局
pnpm guard && pnpm --filter @open-design/plugin-runtime typecheck
```

完整字段集和运行时契约 → [`plugins/spec/SPEC.md`](plugins/spec/SPEC.md)；用编程 Agent 开发插件 → [`plugins/spec/AGENT-DEVELOPMENT.md`](plugins/spec/AGENT-DEVELOPMENT.md)；可直接复制的最小模板 → [`plugins/spec/examples/`](plugins/spec/examples/)。

### 贡献插件

1. 把插件文件夹丢进 [`plugins/community/`](plugins/community/)（第三方插件），或者 —— 想让它随 OpenDesign 一起发布 —— 丢进 [`plugins/_official/`](plugins/_official/) 里对应的那一层。
2. 通过校验：`od plugin validate`、`pnpm guard`、`pnpm --filter @open-design/plugin-runtime typecheck`。
3. 用 [`plugins/spec/CONTRIBUTING.md`](plugins/spec/CONTRIBUTING.md) 里的模板填 PR（ID、版本、层、模式、能力、触发示例；视觉类插件附上截图 / 预览）。
4. 要发布到外部注册表（skills.sh / ClawHub / 独立 GitHub 仓库）→ [`plugins/spec/PUBLISHING-REGISTRIES.md`](plugins/spec/PUBLISHING-REGISTRIES.md)。

插件注册表端点：`GET /api/plugins`。目录总览 → [`plugins/README.md`](plugins/README.md)（[简体中文](plugins/README.zh-CN.md)）。

---

## 架构

```
┌────────────────── browser (Next.js 16) / Electron shell ──────────────┐
│  chat · file workspace · iframe preview · settings · import · MCP     │
└──────────────┬─────────────────────────────────────┬─────────────────┘
               │ /api/*                              │
               ▼                                     ▼
   ┌─────────────────────────────────┐   /api/proxy/{provider}/stream (SSE)
   │  local daemon (Express+SQLite)  │   ─→ any OpenAI-compatible BYOK,
   │                                  │       SSRF-guarded at the edge
   │  /api/skills    /api/design-templates    /api/plugins    │
   │  /api/design-systems            │
   │  /api/chat (SSE)   /api/proxy/* │
   │  /api/projects/:id/files/...    │
   │  /api/artifacts/{save,lint}     │
   │  /api/import/claude-design      │
   │  MCP stdio server                │
   └─────────┬───────────────────────┘
             │ spawn(cli, [...], { cwd: managed project cwd })
             ▼
   ┌──────────────────────────────────────────────────────────────────┐
   │  Local runtime definitions come from runtimes/registry.ts;                 │
   │  the base registry has 27 definitions (including byok-opencode),           │
   │  backed by 26 distinct local CLI executables because byok-opencode shares │
   │  the OpenCode executable. See docs/agent-adapters.md.                     │
   │  composes a functional skill or design template + DESIGN.md; writes files │
   └──────────────────────────────────────────────────────────────────┘
```

| 层 | 技术栈 |
|---|---|
| 前端 | Next.js 16 App Router + React 18 + TypeScript |
| 守护进程 | Node 24 · Express · SSE 流式输出 · `better-sqlite3` |
| 存储 | 在改动或记录守护进程存储路径之前，你**必须**先读 `AGENTS.md` 里的 **Daemon data directory contract**。本 README **不得**复述它。 |
| 预览 | 文件系统运行渲染规范的项目文件；BYOK / 纯 API 运行把一整个 `<artifact>` 块解析进沙箱 `srcdoc` iframe |
| 导出 | HTML（内联版）· PDF（浏览器打印）· PPTX（Agent 驱动）· ZIP · Markdown · MP4（HyperFrames） |
| 桌面端 | Electron 外壳 + 沙箱渲染进程 + 边车 IPC（STATUS · EVAL · SCREENSHOT · CONSOLE · CLICK · SHUTDOWN） |
| 生命周期 | 单一入口：`pnpm tools-dev`（start / stop / run / status / logs / inspect / check） |

完整架构 → [`docs/architecture.md`](docs/architecture.md)。技能协议 → [`docs/skills-protocol.md`](docs/skills-protocol.md)。Agent 适配器契约 → [`docs/agent-adapters.md`](docs/agent-adapters.md)。

---

## 路线图

- [x] 守护进程 + 跨 26 个不同编程 Agent CLI 可执行文件的 27 个运行时定义 + 技能/设计模板注册表 + 设计系统目录
- [x] 网页应用 + 对话 + 提问表单 + 五方向选择器 + 待办进度 + 沙箱预览
- [x] 100+ 功能技能 · 独立的渲染模板目录 · 151 个设计系统包 · 5 种视觉方向 · 5 种设备外框
- [x] SQLite 支撑的项目 · 会话 · 消息 · 标签页 · 模板
- [x] 多供应商 BYOK 代理（`/api/proxy/{anthropic,openai,azure,google,ollama,senseaudio}/stream`），带 OpenAI 兼容预设（含 Atlas Cloud）+ SSRF 防护
- [x] Claude Design ZIP 导入（`/api/import/claude-design`）
- [x] 边车协议 + Electron 桌面端 + IPC 自动化
- [x] 产物 lint 接口 + 五维自我批判的产出前关卡
- [x] **0.8.0** —— 插件市场基础设施（261 个官方插件、manifest 规范、分 Agent 安装脚本）
- [x] **0.9.0** —— OpenDesign Cloud（内置在应用里的官方模型服务：零配置，一键登录）
- [x] **0.10.0** —— 一体化设计工作区：整个手艺闭环在一个窗口里完成（参考资料 → 素材 → 交互式编辑 → 动效 → 交付）
- [x] **0.11.0** —— _The Bazaar_：公开地做出来 —— 一个人人可取用、可贡献的插件与设计系统社区市场
- [x] **0.12.0** —— _Brand-backed Design System_：把你已有的品牌变成一套可复用、可移植的 `DESIGN.md` 系统
- [x] **0.13.0** —— _Stay in Flow_：原生会话恢复、更快的模型选择，以及直接导出成带截图的 PPTX / PDF
- [x] 发布桌面版 —— macOS（Apple 芯片 + Intel）+ Windows（x64）
- [ ] 发布 Linux 桌面版（可选线）—— 跟踪在 [#4368](https://github.com/nexu-io/open-design/issues/4368)
- [ ] 批注模式的精准编辑 —— 部分落地；可靠的定向打补丁还在做
- [ ] AI 输出的微调面板交互 —— 尚未实现
- [ ] `npx od init` 用来搭一个带 `DESIGN.md` 的项目骨架
- [ ] 插件 SDK + `od plugin {add,list,remove,test,publish}` 命令行
- [ ] Figma / Pencil → React / Next / Vue 迁移插件（alpha）
- [ ] 刷新已有代码库的插件（指向一个 git 仓库 + `DESIGN.md`）

分阶段交付 → [`docs/roadmap.md`](docs/roadmap.md)。

---

## 社区

每个渠道背后都是真人。

- 💬 **Discord** —— 日常唠嗑、插件分享、提问 → [**discord.gg/mHAjSMV6gz**](https://discord.gg/mHAjSMV6gz)
- 🐦 **X / Twitter** —— 发布说明、里程碑、幕后花絮 → [**@OpenDesignHQ**](https://x.com/OpenDesignHQ)
- 🗣️ **GitHub Discussions** —— 深度问答、RFC、"晒作品" → [**Discussions**](https://github.com/nexu-io/open-design/discussions)
- 🐛 **GitHub Issues** —— 报 bug、提需求 → [**Issues**](https://github.com/nexu-io/open-design/issues)

[`good-first-issue`](https://github.com/nexu-io/open-design/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22) 和 [`help-wanted`](https://github.com/nexu-io/open-design/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22) 这两个标签是最容易上手的入口。

---

## 参与贡献

OpenDesign 能一直往前走，是因为贡献者 —— 设计师、工程师、提示词作者 —— 一直在出现。很多用得最多的技能、设计系统和插件，都是核心团队以外的人写的。

### 🎯 从哪里开始（收益最大，改动最小）

| 想做…… | 怎么做 | 放在哪 |
|---|---|---|
| 一个新的功能**技能** | 丢一个含 `SKILL.md` 的文件夹，可选带 `assets/` + `references/` | [`skills/`](skills/) · 规范见 [`docs/skills-protocol.md`](docs/skills-protocol.md) |
| 一个新的渲染**设计模板** | 加一个可渲染的 `SKILL.md` 包 | [`design-templates/`](design-templates/) |
| 一个新的**设计系统** | 丢一个以 `DESIGN.md` 为核心的包；需要时补上 `manifest.json`、`tokens.css`、组件、素材或来源证据 | [`design-systems/<brand>/`](design-systems/) |
| 一个新的**插件** | 在某个分类目录下丢 `open-design.json` + 该类型的载荷 | [`plugins/community/`](plugins/community/) · 规范见 [`plugins/spec/SPEC.md`](plugins/spec/SPEC.md) · Agent 开发指南见 [`plugins/spec/AGENT-DEVELOPMENT.md`](plugins/spec/AGENT-DEVELOPMENT.md) |
| 支持一个新的**编程 Agent CLI** | 一个运行时定义 + 一条注册表记录；只有新的传输格式才需要加解析器 | [`apps/daemon/src/runtimes/defs/`](apps/daemon/src/runtimes/defs/) |
| 修 bug 或打磨界面 | 翻 [`good-first-issue`](https://github.com/nexu-io/open-design/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22) 标签 | [Issues →](https://github.com/nexu-io/open-design/issues) |
| 翻译文档 | 更新 `README.<lang>.md` 文件 | [`TRANSLATIONS.md`](TRANSLATIONS.md) |

### 🤖 以 Agent 身份参与贡献

如果**正在读这段话的就是 Agent**，最快的路径是：

```bash
# 1. 本地起起来
git clone https://github.com/nexu-io/open-design.git
cd open-design && corepack enable && pnpm install
pnpm tools-dev run web

# 2. 找一个 good-first-issue 并认领
gh issue list --label "good first issue" --state open --limit 20
gh issue develop <number>   # 创建分支和 worktree

# 3. 做改动，跑检查
pnpm guard && pnpm typecheck
pnpm --filter @open-design/<package> test

# 4. 开 PR
gh pr create --fill
```

对 Agent 友好的完整贡献流程、代码风格和 PR 标准 → [`CONTRIBUTING.md`](CONTRIBUTING.md)（[Deutsch](docs/i18n/CONTRIBUTING.de.md) · [Français](docs/i18n/CONTRIBUTING.fr.md) · [简体中文](docs/i18n/CONTRIBUTING.zh-CN.md) · [日本語](docs/i18n/CONTRIBUTING.ja-JP.md) · [한국어](docs/i18n/CONTRIBUTING.ko.md) · [Português](docs/i18n/CONTRIBUTING.pt-BR.md) · [ภาษาไทย](docs/i18n/CONTRIBUTING.th.md)）。

### 🏅 OpenDesign Fellow 计划

我们正在全球招募 **OpenDesign Fellows** —— Fellow 会跟核心团队一起塑造产品、在所在地区官方代表 OpenDesign、在本地把社区做起来，背后有资金支持（$1,000 / 月）、免费的大模型额度，以及一条直通评审的通道。详情 → [`MAINTAINERS.md`](MAINTAINERS.md) 和 [Discord](https://discord.gg/mHAjSMV6gz) 上的公告。

---

## 维护者

他们扛下了不少活儿 —— 日常维护、评审和社区支持。

<table>
  <tr>
    <td align="center" valign="top" width="200">
      <a href="https://github.com/Nagendhra-web">
        <img src="https://github.com/Nagendhra-web.png" width="96" alt="@Nagendhra-web" /><br/>
        <sub><b>@Nagendhra-web</b></sub>
      </a><br/>
      <sub>维护者</sub>
    </td>
    <td align="center" valign="top" width="200">
      <a href="https://github.com/Sid-Qin">
        <img src="https://github.com/Sid-Qin.png" width="96" alt="@Sid-Qin" /><br/>
        <sub><b>@Sid-Qin</b></sub>
      </a><br/>
      <sub>维护者</sub>
    </td>
    <td align="center" valign="top" width="200">
      <a href="https://github.com/YOMXXX">
        <img src="https://github.com/YOMXXX.png" width="96" alt="@YOMXXX" /><br/>
        <sub><b>@YOMXXX</b></sub>
      </a><br/>
      <sub>维护者</sub>
    </td>
  </tr>
</table>

维护者规则、晋升标准和退出机制 → [`MAINTAINERS.md`](MAINTAINERS.md)（另有 [Deutsch](docs/i18n/MAINTAINERS.de.md) · [Français](docs/i18n/MAINTAINERS.fr.md) · [简体中文](docs/i18n/MAINTAINERS.zh-CN.md) · [日本語](docs/i18n/MAINTAINERS.ja-JP.md) · [한국어](docs/i18n/MAINTAINERS.ko.md) · [Português](docs/i18n/MAINTAINERS.pt-BR.md) · [ภาษาไทย](docs/i18n/MAINTAINERS.th.md)）。

## 贡献者

感谢每一位参与过的人 —— 代码、文档、反馈、一个犀利的 issue、一个新技能、一套新设计系统。

<a href="https://github.com/nexu-io/open-design/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=nexu-io/open-design&max=500&columns=20&anon=1&cache_bust=2026-08-04" alt="OpenDesign 贡献者们" />
</a>

---

## 仓库活跃度

<picture>
  <img alt="OpenDesign —— 仓库指标" src="https://repo-assets.open-design.ai/resources/images/github-metrics.svg" />
</picture>

上面这个 SVG 由 [`.github/workflows/metrics.yml`](.github/workflows/metrics.yml) 每天用 [`lowlighter/metrics`](https://github.com/lowlighter/metrics) 重新生成。

---

## 给我们点个星

<p align="center">
  <a href="https://github.com/nexu-io/open-design"><img src="https://repo-assets.open-design.ai/resources/images/star-us.png" alt="在 GitHub 上给 OpenDesign 点星 —— github.com/nexu-io/open-design" width="100%" /></a>
</p>

如果这东西替你省下了三十分钟，就给它一颗 ★。星星付不了房租 —— 但它们会告诉下一个设计师、下一个 Agent、下一个贡献者：这个实验值得他们花时间。一次点击，三秒钟，一个真实的信号。

<a href="https://star-history.dera.page/#nexu-io/open-design&Date">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://star-history.dera.page/svg?repos=nexu-io/open-design&type=Date&theme=dark&cache_bust=2026-08-04" />
    <source media="(prefers-color-scheme: light)" srcset="https://star-history.dera.page/svg?repos=nexu-io/open-design&type=Date&cache_bust=2026-08-04" />
    <img alt="OpenDesign 星标历史" src="https://star-history.dera.page/svg?repos=nexu-io/open-design&type=Date&cache_bust=2026-08-04" />
  </picture>
</a>

---

## 参考与渊源

| 项目 | 角色 |
|---|---|
| Claude Design | 本仓库是其开源替代品的那个闭源产品。 |
| [`alchaincyf/huashu-design`](https://github.com/alchaincyf/huashu-design) | 设计哲学的指南针 —— 初级设计师工作流、品牌素材协议、反 AI 垃圾内容清单、五维批判。 |
| [`op7418/guizang-ppt-skill`](https://github.com/op7418/guizang-ppt-skill) | 杂志风网页 PPT 技能，原封不动打包在 [`design-templates/guizang-ppt/`](design-templates/guizang-ppt/) 下。演示稿模式的默认选择。 |
| [`lewislulu/html-ppt-skill`](https://github.com/lewislulu/html-ppt-skill) | HTML PPT Studio 家族 —— 15 套演示稿模板、36 种主题、31 种页面版式、动画运行时、磁吸卡片演讲模式。 |
| [`OpenCoworkAI/open-codesign`](https://github.com/OpenCoworkAI/open-codesign) | 第一个开源的 Claude Design 替代品；我们借鉴了它的交互模式（流式产物闭环、沙箱 iframe、实时 Agent 面板）。 |
| [`multica-ai/multica`](https://github.com/multica-ai/multica) | 守护进程 + 适配器架构 —— 扫描 PATH 发现 Agent，本地守护进程是唯一有特权的进程。 |
| [`VoltAgent/awesome-design-md`](https://github.com/VoltAgent/awesome-design-md) | 最初的 9 段式 `DESIGN.md` 结构和 70 套源自上游的系统的历史来源；现在这些包可能已经在那套基线之上做了扩展。 |
| [`bergside/awesome-design-skills`](https://github.com/bergside/awesome-design-skills) | `design-systems/` 下新增的 57 个设计技能的来源。 |
| [`heygen-com/hyperframes`](https://github.com/heygen-com/hyperframes) | HTML→MP4 动态图形框架，在 OpenDesign 里集成为一等公民 `hyperframes-html`。 |
| [Claude Code skills][skill] | 我们原样采用的 `SKILL.md` 约定。 |

详细的来源说明 → [`docs/references.md`](docs/references.md)。

[skill]: https://docs.anthropic.com/en/docs/claude-code/skills

## 许可证

Apache-2.0。自带独立 `LICENSE` 文件的打包技能和模板保留各自的许可证，包括 `design-templates/guizang-ppt/`（MIT，[@op7418](https://github.com/op7418)）、`design-templates/html-ppt/`（MIT，[@lewislulu](https://github.com/lewislulu)）和 `skills/web-clone/`（MIT，[@Jane-xiaoer](https://github.com/Jane-xiaoer)）。
