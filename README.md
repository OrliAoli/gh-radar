# 每日 GitHub 雷达（P1）

AI / Agent 领域的个人雷达。GitHub Actions 每天抓一次快照，每 3 天聚合出一期 20 条榜单，
前端是纯静态页面，和数据**同源部署**到国内 CDN（不走 jsDelivr）。

---

## 一、目录结构

```
gh-radar/
├── .github/workflows/
│   ├── daily.yml          每天 UTC 00:30 抓取存快照（不发布）
│   ├── smoke-test.yml     手动触发，验证 Actions 机房能否抓到 trending
│   └── publish.yml        每 3 天聚合发布
├── config/
│   ├── rules.txt          关键词规则（你唯一需要手改的文件）
│   ├── thresholds.json    所有可调数字
│   └── allocation.json    20 条名额怎么分
├── scripts/
│   ├── fetch.py           抓取：trending HTML + Search API
│   ├── filter.py          过滤与打分：解析 rules.txt，判定类别
│   ├── build.py           聚合：多日合并、双车道计分、配额、输出
│   └── radar.py           统一入口（--fetch-only / --fetch-and-deploy）
├── data/
│   ├── latest.json        前端读取的唯一入口
│   ├── state.json         记录 first_seen / periods_on_board
│   └── daily/             每日快照 YYYY-MM-DD.json
├── feed.xml               RSS 输出
└── web/                   前端（index.html / style.css / js/*.js）
```

---

## 二、⚠️ 改 rules.txt 必须 commit + push 才生效

**这是最容易踩的坑。** GitHub Actions 是从 git 仓库里读文件的，不是读你电脑上的文件。
你在本机改完 `config/rules.txt`，**不 push 的话，下次定时抓取用的还是旧规则。**

正确流程（三条命令）：

```bash
cd /Users/orli/CodeBuddy/20260911100549/gh-radar

git add config/rules.txt
git commit -m "调整关键词规则"
git push origin main
```

push 之后，**下一次**定时抓取才会用上新规则。
想立刻生效，就去 GitHub 仓库的 Actions 页面手动点一次「每日抓取快照 → Run workflow」。

---

## 三、两条常用命令（给定时任务用）

```bash
# 每天跑：只抓取存快照，不生成页面
python3 /Users/orli/CodeBuddy/20260911100549/gh-radar/scripts/radar.py --fetch-only

# 每 3 天跑：抓取 + 聚合 + 生成页面 + 部署
python3 /Users/orli/CodeBuddy/20260911100549/gh-radar/scripts/radar.py --fetch-and-deploy
```

单跑某一步也可以：

```bash
python3 scripts/fetch.py            # 只抓取
python3 scripts/build.py --days 3   # 只聚合
python3 scripts/filter.py           # 检查规则解析是否正常
```

---

## 四、rules.txt 语法

```
[GLOBAL_FILTER]   全局排除，命中即丢弃（整榜生效，行首不加 !）
[WEAK]            降权区，命中不排除，得分 ×0.5
[QUALITY_GATE]    质量门槛，命中后必须 总星>50000 或 本期爆发指数进前 3，否则丢弃
[组名]            兴趣组，命中决定 category
```

组内规则行：

| 写法 | 含义 | 作用域 |
|:---|:---|:---|
| `关键词` | 普通词，命中即算，同组多个之间是 OR | 组内 |
| `/正则/` | 正则匹配，忽略大小写 | 组内 |
| `+关键词` | 必须词，所有 `+` 都要命中（AND） | 组内 |
| `!关键词` | 过滤词，命中即排除 | **仅当前组** |
| `@数字` | 该组最多取多少条 | 组内 |
| `# 注释` | 注释行 | — |

**注意**：`[GLOBAL_FILTER]` 是全局的，`!` 只在组内生效，这两层不能混。
要全局排除必须写进 `[GLOBAL_FILTER]`。

---

## 五、三个必须知道的坑

1. **`ai` 这个词要写成词边界**：`/llm|大模型|人工智能|ai/` 里的 `ai` 是子串匹配，
   `chain`、`train`、`main`、`email` 都会命中。建议改成 `/\bai\b|llm|大模型|人工智能/`。
2. **GitHub Search API 每条查询最多 5 个 OR 运算符**，`fetch.py` 已自动分片，
   你加关键词时不用担心这个限制。
3. **`stars_today` 为 `null` 是合法状态**，不是错误。
   搜索 API 天生没有"今日新增"字段，只有爬 trending 页面才有。前端遇到 `null` 显示「—」。
