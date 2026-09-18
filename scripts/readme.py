#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
README 抓取 + 「文章型 / 工具型」自动判定。

只处理【最终入选】的条目（data/latest.json 里的 20 条），不给全部候选都抓。

为什么需要判定：
    GitHub 上绝大多数仓库是「工具」——README 里 60~80% 是安装命令和代码块，
    翻出来对你没价值。少数是「文章」（如 LLM-wiki）——通篇是观点和知识，
    才是你最需要的行业经验。
    这两类的分水岭就是【代码块占比】：工具型 60-80%，文章型通常不到 10%。

产出：
    data/readme/{owner}__{repo}.md      抓到的 README 原文（抓不到就不写）
    data/latest.json 里每条补上：
        readme_ok / readme_words / code_block_ratio / is_article / translate_rank

⚠️ 铁律：抓不到就记 readme_ok: false，绝不编造内容填进去。

依赖：仅 Python 标准库。
"""

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT, "data")
LATEST = os.path.join(DATA_DIR, "latest.json")
README_DIR = os.path.join(DATA_DIR, "readme")

DEFAULT_CFG = {
    "enabled": True,
    "max_per_issue": 10,
    "min_words": 2000,
    "max_words": 30000,
    "max_code_block_ratio": 0.3,
    "preferred_categories": ["growth", "classic"],
}

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 " \
     "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"


# ---------------------------------------------------------------- 抓取

def http_get(url, timeout=25, retries=3, accept=None):
    headers = {"User-Agent": UA}
    if accept:
        headers["Accept"] = accept
    last = None
    for i in range(retries):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read().decode("utf-8", "replace"), r.status
        except urllib.error.HTTPError as e:
            if e.code in (403, 404):
                return None, e.code
            last = e
            time.sleep(1.5 * (i + 1))
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(1.5 * (i + 1))
    print("    读取失败：%s" % last)
    return None, None


def fetch_readme(owner, name, token):
    """
    用 GitHub API 拿默认 README 的下载地址，再抓原文。
    拿不到就返回 None（绝不编造）。
    """
    api = "https://api.github.com/repos/%s/%s/readme" % (owner, name)
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = "Bearer %s" % token

    meta = None
    for attempt in range(3):
        try:
            req = urllib.request.Request(api, headers=headers)
            with urllib.request.urlopen(req, timeout=25) as r:
                meta = json.loads(r.read().decode("utf-8", "replace"))
            break
        except urllib.error.HTTPError as e:
            if e.code in (403, 404):
                print("    README 元数据 HTTP %s" % e.code)
                return None, None
            if attempt < 2:
                time.sleep(2.0 * (attempt + 1))
            else:
                print("    README 元数据 HTTP %s" % e.code)
                return None, None
        except Exception as e:  # noqa: BLE001
            if attempt < 2:
                time.sleep(2.0 * (attempt + 1))
            else:
                print("    README 元数据失败：%s" % e)
                return None, None

    if not meta:
        return None, None

    url = meta.get("download_url")
    if not url:
        return None, None
    body, status = http_get(url, accept="text/plain", retries=4)
    if not body:
        return None, status
    return body, meta.get("name") or "README.md"


# ---------------------------------------------------------------- 统计

FENCED = re.compile(r"```.*?```", re.S)
INLINE_CODE = re.compile(r"`[^`\n]{1,200}`")
IMAGE = re.compile(r"!\[[^\]]*\]\([^)]*\)")
HTML_COMMENT = re.compile(r"<!--.*?-->", re.S)
HTML_TAG = re.compile(r"<[^>]{1,300}>")
TABLE_SEP = re.compile(r"^\s*\|?[\s:\-\|]+\|[\s:\-\|]*$", re.M)
LINK_URL = re.compile(r"https?://\S+")


def clip_words(text, limit):
    """按词数截断（中英混排：中文按字，英文按词）。"""
    out, count = [], 0
    for line in text.split("\n"):
        c = len(re.findall(r"[\u4e00-\u9fff]", line)) + \
            len(re.findall(r"[A-Za-z][A-Za-z0-9\-_.]*", line))
        if count + c > limit:
            break
        out.append(line)
        count += c
    return "\n".join(out)


def analyze(text):
    """
    返回 (纯文本词数, 代码块占比)。
    先剔除代码块、内联代码、图片、HTML、表格分隔线，再数词。
    """
    total_chars = max(1, len(text))

    # 代码块字符数：围栏块 + 4 空格缩进块
    fenced = "".join(FENCED.findall(text))
    indented = "".join(
        l for l in text.split("\n")
        if l.startswith("    ") and l.strip()
    )
    code_chars = len(fenced) + len(indented)

    # 剔除后用于数词的纯文本
    plain = FENCED.sub(" ", text)
    plain = INLINE_CODE.sub(" ", plain)
    plain = IMAGE.sub(" ", plain)
    plain = HTML_COMMENT.sub(" ", plain)
    plain = HTML_TAG.sub(" ", plain)
    plain = TABLE_SEP.sub(" ", plain)
    plain = LINK_URL.sub(" ", plain)

    cjk = len(re.findall(r"[\u4e00-\u9fff\u3040-\u30ff]", plain))
    english = len(re.findall(r"[A-Za-z][A-Za-z0-9\-_.]*", plain))
    words = cjk + english

    return words, round(code_chars / float(total_chars), 4)


# ---------------------------------------------------------------- 主流程

def main():
    ap = argparse.ArgumentParser(description="抓取入选条目的 README 并判定是否为文章")
    ap.add_argument("--limit", type=int, default=0, help="只处理前 N 条")
    ap.add_argument("--sleep", type=float, default=1.0, help="每次抓取间隔秒数")
    args = ap.parse_args()

    if not os.path.exists(LATEST):
        print("[x] 找不到 data/latest.json，先跑 scripts/build.py")
        return 1

    with open(LATEST, "r", encoding="utf-8") as f:
        data = json.load(f)
    items = data.get("items") or []
    if args.limit:
        items = items[:args.limit]

    cfg = dict(DEFAULT_CFG)
    cfg.update(data.get("translate_full") or {})
    # 也允许从 config/thresholds.json 读（那里是权威配置）
    tpath = os.path.join(ROOT, "config", "thresholds.json")
    if os.path.exists(tpath):
        with open(tpath, "r", encoding="utf-8") as f:
            cfg.update(json.load(f).get("translate_full") or {})

    token = os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN") or ""
    os.makedirs(README_DIR, exist_ok=True)

    print("=== README 抓取：共 %d 条 ===" % len(items))
    print("[i] 判定阈值：词数 %d~%d，代码块占比 < %.0f%%"
          % (cfg["min_words"], cfg["max_words"], cfg["max_code_block_ratio"] * 100))

    ok = fail = 0
    for idx, item in enumerate(items, 1):
        owner = item.get("owner") or (item.get("full_name", "").split("/")[0])
        name = item.get("name") or (item.get("full_name", "").split("/")[1] if "/" in item.get("full_name", "") else "")
        label = item.get("full_name") or item.get("id")

        body, _ = fetch_readme(owner, name, token)
        time.sleep(args.sleep)

        # 幂等：这次抓不到，但以前抓过 —— 直接复用已有文件，不浪费、不丢数据
        local = os.path.join(README_DIR, "%s__%s.md" % (owner, name))
        reused = False
        if (not body or not body.strip()) and os.path.exists(local):
            body = open(local, encoding="utf-8").read()
            reused = True

        if not body or not body.strip():
            item["readme_ok"] = False
            item["readme_words"] = 0
            item["code_block_ratio"] = None
            item["is_article"] = False
            item["translate_rank"] = None
            fail += 1
            print("  [%2d/%d] %-42s 抓取失败（本地也无缓存）" % (idx, len(items), label))
            continue

        path = os.path.join(README_DIR, "%s__%s.md" % (owner, name))
        with open(path, "w", encoding="utf-8") as f:
            f.write(body)

        words, ratio = analyze(body)
        is_article = (cfg["min_words"] <= words <= cfg["max_words"]
                      and ratio < cfg["max_code_block_ratio"])

        item["readme_ok"] = True
        item["readme_words"] = words
        item["code_block_ratio"] = ratio
        item["is_article"] = bool(is_article)
        item["readme_path"] = os.path.relpath(path, ROOT)

        flag = "文章 ✓" if is_article else "工具（跳过）"
        print("  [%2d/%d] %-42s %6d 词  代码块 %5.1f%%  %s%s"
              % (idx, len(items), label, words, ratio * 100, flag,
                 "（复用已有文件）" if reused else ""))
        ok += 1

    # 排序：优先 preferred_categories，其次词数多的排前面
    pref = cfg.get("preferred_categories") or []
    cands = [i for i in items if i.get("is_article")]
    cands.sort(key=lambda i: (
        0 if i.get("category") in pref else 1,
        -(i.get("readme_words") or 0),
    ))
    for rank, i in enumerate(cands, 1):
        i["translate_rank"] = rank

    # 把「要翻译的文章」的英文原文一并写进 latest.json，
    # 前端「对照原文」开关要用。只写前 max_per_issue 篇，并按 max_words 截断，控制体积。
    maxw = cfg["max_words"]
    for i in items:
        if not i.get("is_article") or not i.get("translate_rank"):
            i.pop("readme_en", None)
            continue
        if i["translate_rank"] > cfg["max_per_issue"]:
            i.pop("readme_en", None)
            continue
        p = i.get("readme_path") and os.path.join(ROOT, i["readme_path"])
        if p and os.path.exists(p):
            i["readme_en"] = clip_words(open(p, encoding="utf-8").read(), maxw)

    stats = {
        "readme_fetched": ok,
        "readme_failed": fail,
        "is_article": len(cands),
    }
    data["readme_stats"] = stats

    with open(LATEST, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("\n[+] 抓取成功 %d 条，失败 %d 条；判定为「文章」%d 条" % (ok, fail, len(cands)))
    if cands:
        print("    文章清单（按优先级）：")
        for i in cands[:cfg["max_per_issue"]]:
            print("      %d. %-42s %d 词  代码块 %.1f%%  [%s]"
                  % (i["translate_rank"], i["full_name"], i["readme_words"],
                     (i["code_block_ratio"] or 0) * 100, i.get("category")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
