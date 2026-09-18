#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
每日抓取脚本 —— 只负责"拿数据"，不做过滤、不做聚合、不发布。

两个数据源，各司其职：
  1) github.com/trending（爬 HTML）
     唯一官方提供 "X stars today" 的源。没有它就没有爆发指数。
  2) GitHub Search API
     补充候选池。trending 每个语言只有 25 条、类目粗糙，覆盖不了兴趣组。

三条铁律：
  · 拿不到 stars_today 就写 None，绝不填 0（0 会让新项目被排序算法误判成"没涨"）
  · stars_today 为 None 是【合法状态】不是错误，搜索池天生没有这个字段
  · 页面结构校验失败 → source 标记 fallback + 写入 warnings，绝不静默降级

依赖：仅 Python 标准库（3.8+），无需 pip install。
"""

import argparse
import datetime
import html
import json
import os
import random
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT, "data")
DAILY_DIR = os.path.join(DATA_DIR, "daily")

# 结构校验阈值：解析出的仓库行数低于此值，判定为页面改版 / 被限流 / 被拦截
MIN_ROWS = 10

TRENDING_CATEGORIES = [
    {"id": "overall", "path": ""},
    {"id": "python", "path": "python"},
    {"id": "typescript", "path": "typescript"},
    {"id": "javascript", "path": "javascript"},
    {"id": "go", "path": "go"},
    {"id": "rust", "path": "rust"},
]

# 每个兴趣组的搜索关键词。⚠️ 需与 config/rules.txt 的分组保持同步
GROUP_SEARCH_KEYWORDS = {
    "ai_skill": ["skill", "skills", "subagent", "slash-command", "prompt-engineering",
                 "agent-skill", "claude", "codex", "cursor", "copilot", "opencode"],
    "ai_agent": ["agent", "智能体", "orchestration", "multi-agent", "mcp",
                 "model-context-protocol", "coding-agent", "autonomous", "rag", "llm-app"],
    "ai_learn": ["tutorial", "handbook", "guide", "roadmap", "course", "beginner",
                 "llm", "大模型", "人工智能"],
    "llm_infer": ["inference", "vllm", "sglang", "tensorrt", "onnx", "llama-cpp",
                  "ollama", "quantization", "kv-cache", "flash-attention", "moe", "transformer"],
    "cn_tech": ["中文", "chinese", "翻译", "写作"],
}

# GitHub Search API 硬限制：一条查询最多 5 个 AND/OR/NOT 运算符 → 最多 6 个关键词
MAX_BOOL_TERMS = 6

# 存量查询：捞已成名的经典（最近 30 天有更新）
# 新增查询：捞刚冒头的新项目（最近 30 天新建）—— 这条才是雷达的发现价值所在
STOCK_SINCE_DAYS = 30
NEW_CREATED_DAYS = 30

USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0",
]

TIMEOUT = 25


# ---------------------------------------------------------------- 基础工具

def http_get(url, headers=None, retries=4, force_ua=None):
    """带退避的 GET。返回 (body, error, status_code)。status 为 None 表示网络层失败。"""
    last_status = None
    last_err = None
    for i in range(retries):
        hdr = {"User-Agent": force_ua or random.choice(USER_AGENTS),
               "Accept-Language": "en-US,en;q=0.9"}
        if headers:
            hdr.update(headers)
        try:
            req = urllib.request.Request(url, headers=hdr)
            with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
                return resp.read().decode("utf-8", errors="replace"), None, resp.status
        except urllib.error.HTTPError as e:
            last_status = e.code
            last_err = "HTTP %s" % e.code
            if e.code in (403, 429):
                # 403/429：换 UA 并加长等待后再试
                force_ua = None
                time.sleep(2.5 * (i + 1) + random.uniform(0.5, 1.5))
            else:
                time.sleep(1.5 * (i + 1))
        except Exception as e:  # noqa: BLE001
            last_err = "%s: %s" % (type(e).__name__, e)
            time.sleep(1.5 * (i + 1))
    return None, last_err, last_status


def strip_tags(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s or "")).strip()


def clean_text(s):
    return re.sub(r"\s+", " ", strip_tags(s)).strip()


def parse_count(text):
    """'32,505' -> 32505 ；'1.2k' -> 1200 ；解析不出返回 None。"""
    if text is None:
        return None
    t = re.sub(r"<[^>]+>", "", text).strip().replace(",", "")
    m = re.match(r"^([\d.]+)\s*([km]?)$", t, re.I)
    if not m:
        return None
    try:
        v = float(m.group(1))
    except ValueError:
        return None
    suffix = m.group(2).lower()
    if suffix == "k":
        v *= 1000
    elif suffix == "m":
        v *= 1000000
    return int(v)


# ------------------------------------------------- 源 1：github.com/trending

def parse_trending_block(block):
    """解析一个 article.Box-row 区块。失败返回 None。"""
    h2 = re.search(r"<h2[^>]*>(.*?)</h2>", block, re.S)
    if not h2:
        return None
    m = re.search(r'href="/([^/"]+)/([^/"]+)"', h2.group(1))
    if not m:
        return None
    owner, name = m.group(1), m.group(2)

    # 注意：<p 后面必须紧跟空白或 >，否则会误匹配 SVG 里的 <path ...>
    desc_m = re.search(r"<p(?:\s[^>]*)?>(.*?)</p>", block, re.S)
    description = clean_text(desc_m.group(1)) if desc_m else ""

    lang_m = re.search(
        r'<span itemprop="programmingLanguage">(.*?)</span>', block, re.S)
    language = clean_text(lang_m.group(1)) if lang_m else ""

    today_m = re.search(r"([\d,]+)\s+stars\s+today", block)
    stars_today = parse_count(today_m.group(1)) if today_m else None
    # 铁律：拿不到就是 None，绝不填 0
    if stars_today == 0:
        stars_today = None

    star_m = re.search(r'href="[^"]*/stargazers"[^>]*>(.*?)</a>', block, re.S)
    total_stars = parse_count(star_m.group(1)) if star_m else None

    fork_m = re.search(
        r'href="[^"]*/(?:forks|network/members)"[^>]*>(.*?)</a>', block, re.S)
    forks = parse_count(fork_m.group(1)) if fork_m else None

    return {
        "id": "%s/%s" % (owner, name),
        "owner": owner,
        "name": name,
        "full_name": "%s/%s" % (owner, name),
        "url": "https://github.com/%s/%s" % (owner, name),
        "description": description,
        "language": language or "",
        "total_stars": total_stars,
        "forks": forks,
        "stars_today": stars_today,      # 可能为 None
        "topics": [],
        "src": "trending",
    }


def fetch_trending(cat):
    """
    抓取单个 trending 类目。返回 (repos, status, note)
    403/429 时会换 UA 再试一轮 —— GitHub 对机房 IP 更严格，这是关键兜底。
    """
    url = "https://github.com/trending" if not cat["path"] \
        else "https://github.com/trending/%s" % cat["path"]
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Referer": "https://github.com/",
        "DNT": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
    }

    def one_round(force_ua):
        body, err, status = http_get(url, headers, retries=4, force_ua=force_ua)
        if body is None:
            return None, err or "unknown error", status
        blocks = re.split(r"<article\s", body)[1:]
        repos = []
        for b in blocks:
            r = parse_trending_block(b)
            if r:
                repos.append(r)
        return repos, None, status

    repos, err, status = one_round(None)
    if repos is None and status in (403, 429):
        print("    ↻ %s 收到 HTTP %s，换 UA 再试一轮" % (cat["id"], status))
        time.sleep(random.uniform(3.0, 6.0))
        repos, err, status = one_round(random.choice(USER_AGENTS))

    if repos is None:
        return [], "error", "%s%s" % (err or "请求失败",
                                      (" (HTTP %s)" % status) if status else "")

    if len(repos) < MIN_ROWS:
        return repos, "suspect", "仅解析出 %d 行（阈值 %d），疑似页面改版或被限流" % (
            len(repos), MIN_ROWS)
    return repos, "ok", ""


# --------------------------------------------- 源 2：GitHub Search API

def build_search_queries():
    """
    每个兴趣组 × 两种查询（存量捞经典 / 新增捞新冒头的）× 关键词分片。
    分片是因为 GitHub 限制每条查询最多 5 个 OR 运算符。
    """
    now = datetime.datetime.now(datetime.timezone.utc)
    since = (now - datetime.timedelta(days=STOCK_SINCE_DAYS)).strftime("%Y-%m-%d")
    recent = (now - datetime.timedelta(days=NEW_CREATED_DAYS)).strftime("%Y-%m-%d")
    out = []
    for gid, kws in GROUP_SEARCH_KEYWORDS.items():
        chunks = [kws[i:i + MAX_BOOL_TERMS]
                  for i in range(0, len(kws), MAX_BOOL_TERMS)]
        for ci, chunk in enumerate(chunks):
            term = " OR ".join(chunk)
            out.append({
                "id": "%s__stock__%d" % (gid, ci), "group": gid, "kind": "stock",
                "q": "stars:>200 pushed:>%s (%s)" % (since, term),
            })
            out.append({
                "id": "%s__new__%d" % (gid, ci), "group": gid, "kind": "new",
                "q": "stars:>50 created:>%s (%s)" % (recent, term),
            })
    return out


def fetch_search(q, token):
    """调用 GitHub Search API。返回 (repos, status, note)"""
    url = ("https://api.github.com/search/repositories?q=%s"
           "&sort=stars&order=desc&per_page=30" % urllib.parse.quote(q["q"]))
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = "Bearer %s" % token

    body, err, status = http_get(url, headers, retries=3)
    if body is None:
        return [], "error", "%s%s" % (err or "请求失败",
                                      (" (HTTP %s)" % status) if status else "")
    try:
        data = json.loads(body)
    except ValueError:
        return [], "error", "响应不是合法 JSON"

    if "items" not in data:
        return [], "error", "响应缺 items 字段：%s" % str(data)[:200]

    repos = []
    for it in data.get("items", []):
        owner = (it.get("owner") or {}).get("login", "")
        name = it.get("name", "")
        if not owner or not name:
            continue
        repos.append({
            "id": "%s/%s" % (owner, name),
            "owner": owner,
            "name": name,
            "full_name": it.get("full_name", "%s/%s" % (owner, name)),
            "url": it.get("html_url", "https://github.com/%s/%s" % (owner, name)),
            "description": (it.get("description") or "").strip(),
            "language": it.get("language") or "",
            "total_stars": it.get("stargazers_count"),
            "forks": it.get("forks_count"),
            "stars_today": None,     # Search API 不提供今日新增，合法留空
            "topics": it.get("topics") or [],
            "created_at": it.get("created_at"),
            "pushed_at": it.get("pushed_at"),
            "src": "search",
            "search_group": q["group"],
            "search_kind": q["kind"],
        })
    return repos, "ok", ""


# ------------------------------------------------------------ 告警

def maybe_open_issue(title, body):
    """在 GitHub Actions 里自动开 issue 告警；已存在同标题 open issue 则跳过。"""
    token = os.getenv("GITHUB_TOKEN")
    repo = os.getenv("GITHUB_REPOSITORY")
    if not token or not repo:
        print("[!] 非 Actions 环境，跳过开 issue：%s" % title)
        return False
    try:
        q = urllib.parse.quote('repo:%s is:issue is:open "%s"' % (repo, title))
        exist, _, _ = http_get(
            "https://api.github.com/search/issues?q=%s&per_page=1" % q,
            {"Authorization": "Bearer %s" % token,
             "Accept": "application/vnd.github+json"})
        if exist:
            if json.loads(exist).get("total_count", 0) > 0:
                print("[=] 已存在同名 issue，跳过")
                return False
        payload = json.dumps({"title": title, "body": body}).encode("utf-8")
        req = urllib.request.Request(
            "https://api.github.com/repos/%s/issues" % repo,
            data=payload,
            headers={"Authorization": "Bearer %s" % token,
                     "Accept": "application/vnd.github+json",
                     "Content-Type": "application/json"})
        urllib.request.urlopen(req, timeout=TIMEOUT)
        print("[+] 已创建告警 issue")
        return True
    except Exception as e:  # noqa: BLE001
        print("[!] 创建 issue 失败：%s" % e)
        return False


# ------------------------------------------------------------ 主流程

def dedupe(repos):
    """按 id 去重，保留 stars_today 最大的那条（其余字段合并）。"""
    out = {}
    for r in repos:
        cur = out.get(r["id"])
        if cur is None:
            out[r["id"]] = dict(r)
            continue
        a, b = cur.get("stars_today"), r.get("stars_today")
        if a is None and b is not None:
            cur["stars_today"] = b
        elif a is not None and b is not None and b > a:
            cur["stars_today"] = b
        for k in ("topics", "description", "language", "created_at", "pushed_at"):
            if not cur.get(k) and r.get(k):
                cur[k] = r[k]
        for k in ("total_stars", "forks"):
            if cur.get(k) is None and r.get(k) is not None:
                cur[k] = r[k]
        # 同一条同时出现在"存量查询"和"新增查询"里时，按新增处理（门槛更严）
        if r.get("search_kind") == "new":
            cur["search_kind"] = "new"
    return list(out.values())


def main():
    ap = argparse.ArgumentParser(description="每日抓取：trending HTML + Search API")
    ap.add_argument("--date", help="快照日期 YYYY-MM-DD，默认 UTC 今天")
    ap.add_argument("--no-search", action="store_true", help="跳过 Search API")
    ap.add_argument("--no-alert", action="store_true", help="不开告警 issue")
    args = ap.parse_args()

    now = datetime.datetime.now(datetime.timezone.utc)
    date_str = args.date or now.strftime("%Y-%m-%d")
    token = os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN") or ""

    print("=== 抓取开始 %s (UTC %s) ===" % (date_str, now.isoformat()))
    print("[i] Search API token: %s"
          % ("已提供" if token else "无（匿名，10 次/分钟）"))

    warnings = []
    categories = {}
    cat_status = {}
    all_trending = []

    for cat in TRENDING_CATEGORIES:
        time.sleep(random.uniform(0.4, 0.9))
        repos, status, note = fetch_trending(cat)
        categories[cat["id"]] = repos
        cat_status[cat["id"]] = {"status": status, "rows": len(repos), "note": note}
        print("  [trending:%-11s] %-8s %2d 条 %s" % (cat["id"], status, len(repos), note))
        all_trending.extend(repos)
        if status == "suspect":
            warnings.append("trending[%s] 结构校验失败：%s" % (cat["id"], note))
        elif status == "error":
            warnings.append("trending[%s] 请求失败：%s" % (cat["id"], note))

    ok_cats = [c for c, s in cat_status.items() if s["status"] == "ok"]
    if not ok_cats:
        overall_source = "fallback"
        warnings.append("所有 trending 类目均失败，今日无 stars_today 数据")
    elif len(ok_cats) < len(TRENDING_CATEGORIES):
        overall_source = "partial"
    else:
        overall_source = "trending"

    search_pool = {}
    search_status = {}
    if not args.no_search:
        gap = random.uniform(2.5, 3.5) if token else random.uniform(6.5, 7.5)
        for q in build_search_queries():
            time.sleep(gap)
            repos, status, note = fetch_search(q, token)
            search_pool[q["id"]] = repos
            search_status[q["id"]] = {"status": status, "rows": len(repos), "note": note}
            print("  [search:%-16s] %-6s %2d 条 %s" % (q["id"], status, len(repos), note))
            if status != "ok":
                warnings.append("search[%s] 失败：%s" % (q["id"], note))

    trending_dedup = dedupe(all_trending)
    search_dedup = dedupe([r for rs in search_pool.values() for r in rs])
    merged = dedupe(trending_dedup + search_dedup)

    t_none = sum(1 for r in trending_dedup if r.get("stars_today") is None)
    s_none = sum(1 for r in search_dedup if r.get("stars_today") is None)

    print("[i] trending 池 %d 条（无 stars_today %d 条）" % (len(trending_dedup), t_none))
    print("[i] 搜索池   %d 条（无 stars_today %d 条 ← 天生没有，属正常）"
          % (len(search_dedup), s_none))
    print("[i] 合并去重 %d 条，其中 %d 条有真实 stars_today，%d 条为 None"
          % (len(merged),
             sum(1 for r in merged if r.get("stars_today") is not None),
             sum(1 for r in merged if r.get("stars_today") is None)))

    snapshot = {
        "updated_at": now.isoformat(),
        "date": date_str,
        "source": overall_source,
        "warnings": warnings,
        "stats": {
            "trending_categories": cat_status,
            "search_queries": search_status,
            "trending_repos": len(trending_dedup),
            "trending_missing_stars_today": t_none,
            "search_repos": len(search_dedup),
            "search_missing_stars_today": s_none,
            "merged_total": len(merged),
            "with_stars_today": sum(
                1 for r in merged if r.get("stars_today") is not None),
        },
        "categories": categories,
        "search_pool": search_pool,
    }

    os.makedirs(DAILY_DIR, exist_ok=True)
    out_path = os.path.join(DAILY_DIR, "%s.json" % date_str)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(snapshot, f, indent=2, ensure_ascii=False)
    print("[+] 快照已写入 %s" % out_path)

    if warnings and not args.no_alert:
        maybe_open_issue(
            "trending selector 失效 / 抓取告警 %s" % date_str,
            "自动抓取发现以下异常：\n\n" + "\n".join("- %s" % w for w in warnings))

    return 0 if overall_source in ("trending", "partial") else 1


if __name__ == "__main__":
    sys.exit(main())
