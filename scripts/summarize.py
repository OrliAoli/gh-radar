#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中文简介生成 —— 给 data/latest.json 里的每条补上 title_cn / reason_cn。

配置从环境变量读（GitHub Actions 里配成 Secrets）：
    LLM_API_KEY    必填。没配就【跳过生成】，字段保持为空
    LLM_BASE_URL   可选，默认 https://api.openai.com/v1（OpenAI 兼容接口都行）
    LLM_MODEL      可选，默认 gpt-4o-mini

⚠️ 铁律：Key 没配就什么都不做，绝对不要用模板硬凑内容。
   凑出来的"简介"没有价值，不如空着让前端显示「简介待生成」。

写作要求（这直接决定用户能不能读懂）：
    title_cn   说清"这东西解决什么问题、能干什么"
    reason_cn  回答"这对我有什么用、它在 AI 生态里处在什么位置"
    禁止：「star 数高值得关注」「API 设计优雅」「适合二次开发」这类空话
    术语（MoE、量化、KV cache、上下文工程、MCP、推理加速）必须顺带一句大白话解释
    读者没有开发基础，不要写只有程序员才懂的话

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

DEFAULT_BASE_URL = "https://api.openai.com/v1"
DEFAULT_MODEL = "gpt-4o-mini"

SYSTEM_PROMPT = """你是一个给"没有开发基础、但对 AI 领域有兴趣"的读者写简介的编辑。

读者画像：不写代码，想知道"这东西是干嘛的、对我有什么用"。他关注 AI 编程助手（Claude Code、Cursor 等）、
AI Agent、大模型推理这些方向，但看不懂术语。

你要为给定的 GitHub 仓库输出两个中文短句，严格返回 JSON：
{"title_cn": "...", "reason_cn": "..."}

【title_cn】一句话说清"这东西解决什么问题、能干什么"
- 20~45 个字
- 用大白话，不要出现函数名、参数、设计模式
- 反面例子：一个基于 RAG 的检索增强生成框架
- 正面例子：给 AI 编程助手用的技能包，装上后它会自动按这套规则写代码

【reason_cn】回答"这对我有什么用、它在 AI 生态里处在什么位置"
- 25~60 个字
- 说清它在整个 AI 工具链里的角色，或者为什么值得花时间看
- 禁止写：「star 数高值得关注」「API 设计优雅」「适合二次开发」「功能强大」「值得学习」
- 正面例子：这是给 AI 编程助手的"记忆"插件，解决它转头就忘的毛病，装上后不用每次重新交代背景

【术语处理】如果项目涉及 MoE、量化、KV cache、上下文工程、MCP、推理加速、RAG 这类词，
必须顺带用一句大白话解释，例如："MoE（一个大模型内部由很多小专家分工，用哪个激活哪个，所以又快又省）"

【注意】
- 不要编造项目没有的功能，只依据给出的信息
- 只返回 JSON，不要 markdown 代码块，不要多余解释
- 如果信息不足以判断用途，就如实说"看不出具体用途，可能是……"，不要硬编
"""


def build_user_prompt(item):
    return json.dumps({
        "repo": item.get("full_name"),
        "description": item.get("description") or "",
        "language": item.get("language") or "",
        "topics": item.get("topics") or [],
        "matched_groups": item.get("matched_groups") or [],
        "total_stars": item.get("total_stars"),
        "stars_today": item.get("stars_today"),
    }, ensure_ascii=False)


def call_llm(api_key, base_url, model, user_prompt, timeout=60):
    url = base_url.rstrip("/") + "/chat/completions"
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0.3,
        "max_tokens": 400,
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": "Bearer %s" % api_key,
            "Content-Type": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    text = (data.get("choices") or [{}])[0].get("message", {}).get("content", "")
    return text


def parse_json_reply(text):
    """模型有时会包一层 ```json，这里稳妥地把 JSON 抠出来。"""
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
    title = (obj.get("title_cn") or "").strip()
    reason = (obj.get("reason_cn") or "").strip()
    if not title and not reason:
        return None
    return {"title_cn": title or None, "reason_cn": reason or None}


def main():
    ap = argparse.ArgumentParser(description="为 latest.json 补中文简介")
    ap.add_argument("--force", action="store_true", help="连已有简介的也重新生成")
    ap.add_argument("--limit", type=int, default=0, help="只处理前 N 条，0 表示全部")
    ap.add_argument("--sleep", type=float, default=1.2, help="每次请求之间的间隔秒数")
    args = ap.parse_args()

    api_key = os.getenv("LLM_API_KEY", "").strip()
    base_url = os.getenv("LLM_BASE_URL", "").strip() or DEFAULT_BASE_URL
    model = os.getenv("LLM_MODEL", "").strip() or DEFAULT_MODEL

    if not api_key:
        print("[=] 没有配置 LLM_API_KEY，跳过中文简介生成。")
        print("    title_cn / reason_cn 保持为空，前端会显示「简介待生成」。")
        print("    这是预期行为 —— 宁可为空，也不用模板硬凑。")
        return 0

    if not os.path.exists(LATEST):
        print("[x] 找不到 data/latest.json，先跑 scripts/build.py")
        return 1

    with open(LATEST, "r", encoding="utf-8") as f:
        data = json.load(f)
    items = data.get("items") or []
    print("=== 中文简介生成：共 %d 条，模型 %s @ %s ===" % (len(items), model, base_url))

    targets = [i for i in items if args.force or not (i.get("title_cn") and i.get("reason_cn"))]
    if args.limit:
        targets = targets[:args.limit]
    if not targets:
        print("[=] 所有条目都已有简介，无需生成。")
        return 0
    print("[i] 需要生成 %d 条" % len(targets))

    ok = fail = 0
    for idx, item in enumerate(targets, 1):
        name = item.get("full_name") or item.get("id")
        try:
            reply = call_llm(api_key, base_url, model, build_user_prompt(item))
            parsed = parse_json_reply(reply)
            if not parsed:
                print("  [%d/%d] %-38s 模型返回无法解析，跳过" % (idx, len(targets), name))
                fail += 1
                continue
            item["title_cn"] = parsed["title_cn"]
            item["reason_cn"] = parsed["reason_cn"]
            print("  [%d/%d] %-38s ✓" % (idx, len(targets), name))
            ok += 1
        except urllib.error.HTTPError as e:
            body = ""
            try:
                body = e.read().decode("utf-8", "replace")[:200]
            except Exception:  # noqa: BLE001
                pass
            print("  [%d/%d] %-38s HTTP %s %s" % (idx, len(targets), name, e.code, body))
            fail += 1
            if e.code in (401, 403):
                print("[x] 鉴权失败，停止后续请求（检查 LLM_API_KEY）")
                break
        except Exception as e:  # noqa: BLE001
            print("  [%d/%d] %-38s 失败 %s" % (idx, len(targets), name, e))
            fail += 1
        time.sleep(args.sleep)

    # 只把成功的写回去，失败的保持原样（绝不填假内容）
    data["summarized_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    data["summary_stats"] = {"generated": ok, "failed": fail, "pending": len(items) - ok}
    with open(LATEST, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("\n[+] 完成：成功 %d 条，失败 %d 条，仍待生成 %d 条"
          % (ok, fail, len(items) - sum(1 for i in items if i.get("title_cn"))))
    return 0


if __name__ == "__main__":
    sys.exit(main())
