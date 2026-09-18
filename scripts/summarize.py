#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中文内容生成 —— 三层结构。

    L1（全部条目）  title_cn   中文一句话：这东西解决什么问题、能干什么
                    reason_cn  这对我有什么用、它在 AI 生态里处在什么位置
    L2（全部条目）  summary_cn 300~500 字深度摘要（改写，不是逐句翻译）
    L3（仅文章型）  readme_cn  README 完整中文译文，最多 max_per_issue 篇

配置全部从环境变量读（GitHub Actions 里配成 Secrets）：
    LLM_API_KEY    必填。没配就【跳过生成】，字段保持为空
    LLM_BASE_URL   可选。默认 https://api.deepseek.com
    LLM_MODEL      可选。默认 deepseek-chat
    ⚠️ BASE_URL 和 MODEL 都不写死：你换渠道时只改 Secrets，不用改代码。

⚠️ 铁律：Key 没配就什么都不做，绝对不要用模板硬凑内容。
   凑出来的"简介"没有价值，不如空着让前端显示「简介待生成」。

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
LATEST = os.path.join(ROOT, "data", "latest.json")
README_DIR = os.path.join(ROOT, "data", "readme")

DEFAULT_BASE_URL = "https://api.deepseek.com"
DEFAULT_MODEL = "deepseek-chat"

# 费用估算用的单价（元 / 百万 token）。可在 thresholds.json 里覆盖。
DEFAULT_PRICE_IN = 2.0
DEFAULT_PRICE_OUT = 8.0

DEFAULT_CFG = {
    "max_per_issue": 10,
    "min_words": 2000,
    "max_words": 30000,
    "max_code_block_ratio": 0.3,
    "preferred_categories": ["growth", "classic"],
}

READER = (
    "读者画像：没有开发基础、不写代码，但对 AI / Agent 领域有兴趣，"
    "想知道「这东西是干嘛的、对我有什么用」。他关注 AI 编程助手（Claude Code、Cursor 等）、"
    "AI Agent、大模型推理这些方向，但看不懂术语。\n"
    "你要用大白话写，遇到术语（MoE、量化、KV cache、上下文工程、MCP、推理加速、RAG）"
    "必须顺带一句解释，例如「MoE（一个大模型内部由很多小专家分工，用哪个激活哪个，所以又快又省）」。\n"
    "禁止写只有程序员才懂的话。\n"
    "禁止写这些空话：「star 数高值得关注」「API 设计优雅」「适合二次开发」「功能强大」「值得学习」。\n"
    "只依据给出的信息，不要编造项目没有的功能。"
)

L1_SYSTEM = """你是一个给「没有开发基础、但对 AI 领域有兴趣」的读者写简介的编辑。

%s

你要为给定的 GitHub 仓库输出两段中文，严格返回 JSON：
{"title_cn": "...", "reason_cn": "..."}

【title_cn】一句话说清「这东西解决什么问题、能干什么」，20~45 字。
【reason_cn】回答「这对我有什么用、它在 AI 生态里处在什么位置」，40~60 字。

只返回 JSON，不要 markdown 代码块，不要多余解释。
""" % READER

L2_SYSTEM = """你是一个给「没有开发基础、但对 AI 领域有兴趣」的读者写深度摘要的编辑。

%s

请为给定的 GitHub 仓库写一段 300~500 字的中文摘要，覆盖这五块：
1. 这东西是什么
2. 能干什么（举具体场景，不要罗列功能名词）
3. 适合谁用
4. 有没有不用写代码的使用方式
5. 里面出现的术语各用一句话解释清楚

⚠️ 这是「改写」不是「翻译」，不要逐句对应原文，用你自己的话讲明白。
直接输出中文正文，不要标题、不要 markdown 标记、不要 JSON。
""" % READER

L3_SYSTEM = """你是技术文档翻译专家。请把下面这篇英文 README 完整翻译成中文。

【硬要求，违反就是失败】
1. 保持 Markdown 结构：标题层级、有序/无序列表、表格、链接、加粗、引用块，全部原样保留
2. 代码块、命令行、变量名、函数名、文件路径、配置项名称 —— 一个字符都不要翻译
3. 链接 URL 原样保留，只翻译链接的显示文字
4. 图片语法 ![](url) 原样保留，只翻译 alt 文字
5. 专业术语首次出现时括注英文原文，例如「KV 缓存（KV cache）」「检索增强生成（RAG）」
6. 专有名词（Claude Code、Cursor、Docker、vLLM 等）保持原文不翻
7. 语气平实自然，不要翻译腔

只输出翻译后的 Markdown 全文，不要任何前言、后记或说明。
"""


# ---------------------------------------------------------------- 工具

def load_cfg():
    cfg = dict(DEFAULT_CFG)
    tpath = os.path.join(ROOT, "config", "thresholds.json")
    if os.path.exists(tpath):
        with open(tpath, "r", encoding="utf-8") as f:
            cfg.update(json.load(f).get("translate_full") or {})
    cfg.setdefault("price_input_per_mtok", DEFAULT_PRICE_IN)
    cfg.setdefault("price_output_per_mtok", DEFAULT_PRICE_OUT)
    return cfg


def call_llm(api_key, base_url, model, system, user, max_tokens=2000, timeout=180):
    url = base_url.rstrip("/") + "/chat/completions"
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "temperature": 0.3,
        "max_tokens": max_tokens,
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": "Bearer %s" % api_key,
                 "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    text = (data.get("choices") or [{}])[0].get("message", {}).get("content", "")
    usage = data.get("usage") or {}
    return text, usage


def parse_json_reply(text):
    if not text:
        return None
    t = text.strip()
    t = re.sub(r"^```(?:json)?\s*", "", t)
    t = re.sub(r"\s*```$", "", t)
    m = re.search(r"\{.*\}", t, re.S)
    if not m:
        return None
    try:
        obj = json.loads(m.group(0))
    except json.JSONDecodeError:
        return None
    a = (obj.get("title_cn") or "").strip()
    b = (obj.get("reason_cn") or "").strip()
    return {"title_cn": a or None, "reason_cn": b or None} if (a or b) else None


def read_readme(item):
    """读回该条目的 README 原文；读不到返回 None。"""
    if item.get("readme_path"):
        p = os.path.join(ROOT, item["readme_path"])
        if os.path.exists(p):
            return open(p, encoding="utf-8").read()
    owner = item.get("owner")
    name = item.get("name")
    if owner and name:
        p = os.path.join(README_DIR, "%s__%s.md" % (owner, name))
        if os.path.exists(p):
            return open(p, encoding="utf-8").read()
    return None


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


def build_user_prompt(item, extra=""):
    d = {
        "repo": item.get("full_name"),
        "description": item.get("description") or "",
        "language": item.get("language") or "",
        "topics": item.get("topics") or [],
        "matched_groups": item.get("matched_groups") or [],
        "total_stars": item.get("total_stars"),
        "stars_today": item.get("stars_today"),
    }
    s = json.dumps(d, ensure_ascii=False)
    return s + extra


# ---------------------------------------------------------------- 主流程

def main():
    ap = argparse.ArgumentParser(description="生成三层中文内容")
    ap.add_argument("--force", action="store_true", help="已有内容也重新生成")
    ap.add_argument("--limit", type=int, default=0, help="只处理前 N 条")
    ap.add_argument("--only", choices=["l1", "l2", "l3"], help="只生成某一层")
    ap.add_argument("--sleep", type=float, default=1.0, help="请求间隔秒数")
    args = ap.parse_args()

    cfg = load_cfg()
    api_key = os.getenv("LLM_API_KEY", "").strip()
    base_url = os.getenv("LLM_BASE_URL", "").strip() or DEFAULT_BASE_URL
    model = os.getenv("LLM_MODEL", "").strip() or DEFAULT_MODEL

    if not api_key:
        print("[=] 没有配置 LLM_API_KEY，跳过中文内容生成。")
        print("    title_cn / reason_cn / summary_cn / readme_cn 保持为空，")
        print("    前端会显示「简介待生成」。这是预期行为 —— 宁可为空，也不用模板硬凑。")
        print("    想启用：仓库 Settings → Secrets and variables → Actions → New repository secret")
        print("      LLM_API_KEY    你的大模型 API Key")
        print("      LLM_BASE_URL   可选，默认 %s" % DEFAULT_BASE_URL)
        print("      LLM_MODEL      可选，默认 %s" % DEFAULT_MODEL)
        return 0

    if not os.path.exists(LATEST):
        print("[x] 找不到 data/latest.json，先跑 scripts/build.py")
        return 1

    with open(LATEST, "r", encoding="utf-8") as f:
        data = json.load(f)
    items = data.get("items") or []
    if args.limit:
        items = items[:args.limit]

    tok_in = tok_out = 0
    n_l1 = n_l2 = n_l3 = 0

    print("=== 中文内容生成：%d 条，模型 %s @ %s ===" % (len(items), model, base_url))

    def charge(usage, fallback_in, fallback_out):
        nonlocal tok_in, tok_out
        tin = usage.get("prompt_tokens") or fallback_in
        tout = usage.get("completion_tokens") or fallback_out
        tok_in += int(tin)
        tok_out += int(tout)

    for idx, item in enumerate(items, 1):
        name = item.get("full_name") or item.get("id")
        try:
            # ── L1
            if not args.only or args.only == "l1":
                if args.force or not (item.get("title_cn") and item.get("reason_cn")):
                    txt, usage = call_llm(api_key, base_url, model, L1_SYSTEM,
                                          build_user_prompt(item), max_tokens=400)
                    parsed = parse_json_reply(txt)
                    if parsed:
                        item["title_cn"] = parsed["title_cn"]
                        item["reason_cn"] = parsed["reason_cn"]
                        n_l1 += 1
                    charge(usage, 600, 200)
                    time.sleep(args.sleep)

            # ── L2
            if not args.only or args.only == "l2":
                if args.force or not item.get("summary_cn"):
                    txt, usage = call_llm(api_key, base_url, model, L2_SYSTEM,
                                          build_user_prompt(item), max_tokens=1200)
                    txt = txt.strip()
                    if txt:
                        item["summary_cn"] = txt
                        n_l2 += 1
                    charge(usage, 700, 600)
                    time.sleep(args.sleep)

            # ── L3
            if not args.only or args.only == "l3":
                rank = item.get("translate_rank")
                if (item.get("is_article") and rank
                        and rank <= cfg["max_per_issue"]
                        and (args.force or not item.get("readme_cn"))):
                    body = read_readme(item)
                    if not body:
                        print("  [%d] %-40s README 缺失，跳过 L3" % (idx, name))
                    else:
                        maxw = cfg["max_words"]
                        truncated = False
                        if (item.get("readme_words") or 0) > maxw:
                            body = clip_words(body, maxw)
                            truncated = True
                        txt, usage = call_llm(api_key, base_url, model, L3_SYSTEM,
                                              body, max_tokens=8000, timeout=300)
                        txt = txt.strip()
                        if txt:
                            if truncated:
                                txt = "> 原文过长，此为节选\n\n" + txt
                            item["readme_cn"] = txt
                            n_l3 += 1
                        charge(usage, 12000, 9000)
                        time.sleep(args.sleep)
        except urllib.error.HTTPError as e:
            body = ""
            try:
                body = e.read().decode("utf-8", "replace")[:160]
            except Exception:  # noqa: BLE001
                pass
            print("  [%d] %-40s HTTP %s %s" % (idx, name, e.code, body))
            if e.code in (401, 403):
                print("[x] 鉴权失败，停止后续请求（检查 LLM_API_KEY）")
                break
        except Exception as e:  # noqa: BLE001
            print("  [%d] %-40s 失败 %s" % (idx, name, e))

    cost = (tok_in / 1e6) * cfg["price_input_per_mtok"] + \
           (tok_out / 1e6) * cfg["price_output_per_mtok"]

    data["summary_stats"] = {
        "generated_l1": n_l1, "generated_l2": n_l2, "generated_l3": n_l3,
        "tokens_in": tok_in, "tokens_out": tok_out,
        "cost_cny_est": round(cost, 4),
        "model": model, "base_url": base_url,
    }
    with open(LATEST, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("\n[+] 完成：L1 %d 条 / L2 %d 条 / L3 %d 篇" % (n_l1, n_l2, n_l3))
    print("[i] token 用量：输入 %s / 输出 %s" % (f"{tok_in:,}", f"{tok_out:,}"))
    print("[i] 费用估算：约 ¥%.4f" % cost)
    return 0


if __name__ == "__main__":
    sys.exit(main())
