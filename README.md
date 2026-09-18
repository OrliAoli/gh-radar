# 每日 GitHub 雷达

AI / Agent 领域的个人雷达。抓取跑在 GitHub 的服务器上，每 3 天出一期 20 条榜单，
前端是纯静态页面，和数据**同源部署**（不走 jsDelivr，国内直连打开）。

仓库：https://github.com/OrliAoli/gh-radar

---

## 一、我每天要做什么？

**什么都不用做。** 两个定时任务在 GitHub 上自动跑：

| 任务 | 时间 | 干什么 |
|:---|:---|:---|
| 每日抓取快照 | 每天北京时间 08:30 | 抓数据、存快照、自动提交。**不出页面** |
| 每 3 天聚合发布 | 每 3 天北京时间 08:40 | 抓取 + 聚合 + 打包 + 提交，出榜单 |

打开固定网址就能看最新一期。

**唯一需要你动手的时候**：想改关键词规则（见第三节）。

---

## 二、两条命令（给本地定时任务用）

```bash
# 每天跑：只抓取存快照，不生成页面
python3 /Users/orli/CodeBuddy/20260911100549/gh-radar/scripts/radar.py --fetch-only

# 每 3 天跑：抓取 + 聚合 + 生成页面 + 打包（加 --site-name 才会真的部署）
python3 /Users/orli/CodeBuddy/20260911100549/gh-radar/scripts/radar.py --fetch-and-deploy
```

> ⚠️ **你的 Mac 直连 `github.com` 主站不稳**（实测收到 32KB 就卡死，20 秒超时）。
> 所以抓取**必须留在 GitHub Actions 上**，这一点没有退路。
> 如果一定要在 Mac 本地跑，先确保代理开着（你的 Frost Proxy，端口 10809）：
> ```bash
> HTTPS_PROXY=http://127.0.0.1:10809 HTTP_PROXY=http://127.0.0.1:10809 \
>   python3 scripts/radar.py --fetch-only
> ```

单独跑某一步：

```bash
python3 scripts/fetch.py            # 只抓取
python3 scripts/build.py --days 3   # 只聚合
python3 scripts/filter.py           # 检查规则解析是否正常
python3 scripts/summarize.py        # 生成中文简介（没配 Key 会自动跳过）
python3 scripts/deploy.py           # 打包成 dist/
```

---

## 三、怎么改关键词规则

### 结论先说：改完必须 commit + push，否则不生效

GitHub Actions 是从**仓库**里读文件的，不是读你电脑上的文件。
你在本机改完不 push，下次定时抓取用的还是旧规则。

### 三步操作

**第 1 步**：改 `config/rules.txt`（唯一需要手改的文件）。语法见第四节。

**第 2 步**：在终端里跑这三条：

```bash
cd /Users/orli/CodeBuddy/20260911100549/gh-radar
git add config/rules.txt
git commit -m "调整关键词规则"
git push origin main
```

> 如果 push 报 `could not read Username`，先跑一次 `/Users/orli/homebrew/bin/gh auth setup-git`。
> 如果 push 卡住不动，是网络问题，前面加代理：
> `HTTPS_PROXY=http://127.0.0.1:10809 HTTP_PROXY=http://127.0.0.1:10809 git push origin main`

**第 3 步**：想立刻生效，去 GitHub 仓库的 **Actions** 页面，
点「每 3 天聚合发布」→ 右边 **Run workflow** → 绿色按钮。等一两分钟刷新页面。

---

## 四、rules.txt 语法

### 四个特殊区块

```
[GLOBAL_FILTER]   全局排除，命中即丢弃（整榜生效，行首不加 !）
[WEAK]            降权区，命中不排除，得分 ×0.5
[QUALITY_GATE]    质量门槛，命中后必须 总星>50000 或 本期爆发指数进前 3，否则丢弃
[组名]            兴趣组，命中决定条目归到哪个类别
```

### 组内规则行

| 写法 | 含义 | 作用域 |
|:---|:---|:---|
| `关键词` | 普通词，命中即算，同组多个之间是 OR | 组内 |
| `/正则/` | 正则匹配，忽略大小写 | 组内 |
| `+关键词` | 必须词，所有 `+` 都要命中（AND） | 组内 |
| `!关键词` | 过滤词，命中即排除 | **仅当前组** |
| `@数字` | 该组最多取多少条 | 组内 |
| `# 注释` | 注释行 | — |

**注意**：`[GLOBAL_FILTER]` 是全局的，`!` 只在组内生效，这两层不能混。

### ⚠️ 短英文词一定要加词边界

`ai`、`go`、`ui` 这类两个字母的词，直接写会**子串误命中**：
`ai` 会匹配上 `chain`、`train`、`main`、`email`、`detail`。

**错误写法**：`/llm|大模型|ai/`　→ 物流系统 `fleetbase` 靠 "supply **chai**n" 混进来过
**正确写法**：`/\bai\b|llm|大模型/`

---

## 五、目录结构

```
gh-radar/
├── .github/workflows/
│   ├── daily.yml          每天 UTC 00:30 抓取存快照（不发布）
│   ├── publish.yml        每 3 天 UTC 00:40 聚合 + 打包 + 提交
│   └── smoke-test.yml     手动触发，验证 Actions 机房能否抓到 trending
├── config/
│   ├── rules.txt          关键词规则（唯一需要手改的文件）
│   └── thresholds.json    所有可调数字（配额、门槛、权重）
├── scripts/
│   ├── fetch.py           抓取：trending HTML + Search API 双源
│   ├── filter.py          过滤与打分：解析 rules.txt，判定类别
│   ├── build.py           聚合：多日合并、双车道计分、配额分配、输出
│   ├── summarize.py       中文简介生成（OpenAI 兼容接口，Key 留空则跳过）
│   ├── deploy.py          打包 dist/（可选部署到 EdgeOne Pages）
│   └── radar.py           统一入口
├── data/
│   ├── latest.json        前端读取的唯一入口
│   ├── state.json         记录 first_seen / periods_on_board
│   └── daily/             每日快照 YYYY-MM-DD.json
├── web/                   前端源码
│   ├── index.html
│   ├── style.css
│   └── js/{config,api,store,filters,cards,shelf,obsidian,app}.js
├── dist/                  打包产物（部署用的就是它）
└── feed.xml               RSS 输出
```

---

## 六、数据怎么流过来的

```
GitHub Actions 服务器（境外，直连 github.com）
   │
   ├─ 每天 08:30  抓 trending + Search API → data/daily/YYYY-MM-DD.json（不发布）
   │
   └─ 每 3 天 08:40
        ├─ 抓最新一天
        ├─ 合并最近 3 天，同一仓库取【峰值】stars_today（不是平均值）
        ├─ 按 rules.txt 过滤 + 打分 + 分 20 个名额
        ├─ 生成 data/latest.json 和 dist/
        └─ 提交回仓库 → EdgeOne Pages 自动发布
```

### 双车道计分（关键设计）

| 车道 | 是什么 | 怎么排 | 填哪些名额 |
|:---|:---|:---|:---|
| **车道 A** | 有今日新增星数的（来自 trending） | 爆发指数 | `burst` |
| **车道 B** | 没有今日新增的（来自搜索池） | 命中强度 ×（星数 + 新鲜度） | `ai_skill` / `growth` |

**为什么分两条车道**：搜索 API 天生不提供"今日新增"字段。
如果所有条目按同一个分数排，搜索池的条目永远是 0 分、永远垫底，`ai_skill` 那一类就全空了。

### 名额分配（`config/thresholds.json`）

先按 `category_min` 分保底 → 剩余名额按分数给未达 `category_quota` 上限的类别 → 任何类别不超上限。

| 类别 | 保底 | 上限 |
|:---|---:|---:|
| `ai_skill` | 8 | 12 |
| `burst` | 4 | 6 |
| `growth` | 4 | 6 |
| `classic` | 1 | 3 |

总量硬卡 **20 条**。

---

## 七、三条铁律

1. **`stars_today` 拿不到就写 `null`，绝不填 0。** 填 0 会让新项目被排序算法误判成"没涨"。
   前端遇到 `null` 显示 `—`，不伪装成有效数字。
2. **`stars_today` 为 `null` 是合法状态**，不是错误数据。搜索池天生没有这个字段，
   聚合阶段绝不当无效条目丢掉。
3. **绝不编造项目名、星数、描述。** 中文简介没配 Key 就留空，前端显示「简介待生成」，
   绝不用模板硬凑。部分类目失败就标记"本期缺失"，绝不用其他类目数据填补。

---

## 八、本地预览

```bash
cd /Users/orli/CodeBuddy/20260911100549/gh-radar
python3 scripts/deploy.py                        # 打包到 dist/
python3 -m http.server 8899 --directory dist     # 起本地服务
# 浏览器打开 http://127.0.0.1:8899/
```

---

## 九、中文简介怎么开

现在 `title_cn` / `reason_cn` 是空的，页面显示「简介待生成」。这是**预期行为**。

要开启，在 GitHub 仓库的 **Settings → Secrets and variables → Actions → New repository secret**
里加三个（后两个可省）：

| 名称 | 说明 |
|:---|:---|
| `LLM_API_KEY` | 大模型 API Key（OpenAI 兼容接口都行） |
| `LLM_BASE_URL` | 可选，默认 `https://api.openai.com/v1` |
| `LLM_MODEL` | 可选，默认 `gpt-4o-mini` |

没配 Key 时 `summarize.py` 会直接跳过，字段保持为空 —— 宁可为空，也不用模板硬凑。

---

## 十、已知限制

- **首次发现日期 / 持续期数目前不准确**：需要累积多期数据才有意义，
  现在只有 1 天快照，所以 `first_seen` 全是同一天、`periods_on_board` 全是 1。
- **「调教雷达」写的是偏好，不能直接改仓库文件**：静态网页无法写本地/仓库文件。
  它会把你的偏好存下来，并生成一段可复制的规则片段，需要你手动粘进 `config/rules.txt` 再 push。
- **中文简介默认关闭**：需要自己配 LLM Key。
- **Mac 本地跑必须挂代理**：直连 `github.com` 主站不稳。
