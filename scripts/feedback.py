#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
反馈学习 —— 把「你在页面上点过的 👍 / 👎 / ⭐ / 已读」和「调教雷达说的话」
变成下一期真正生效的排序权重。

输入：
    data/feedback.jsonl    每行一条行为记录（由 .github/workflows/feedback.yml 从 Issue 追加）
    config/tuning.txt      用户在「调教雷达」里写的自然语言偏好（由同一 workflow 追加）

输出：
    config/learned.json    给 build.py 用的权重表

设计原则（重要）：
    1. 单次点击不改变任何东西。同一语言 / 主题要累计到阈值才生效，避免误点污染。
    2. 👎 只过滤「同类」，不封杀单个仓库 —— 一个仓库可能是偶然，一个主题才是偏好。
    3. 权重有上限，且永远进不了「必看」头部（build.py 里单独处理）。
    4. 全流程只用标准库。

用法：
    python3 scripts/feedback.py            # 重新计算并写出 config/learned.json
    python3 scripts/feedback.py --report   # 打印人类可读的统计，便于排查
"""

import argparse
import datetime
import json
import os
import re
import sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FEEDBACK_PATH = os.path.join(ROOT, "data", "feedback.jsonl")
TUNING_PATH = os.path.join(ROOT, "config", "tuning.txt")
LEARNED_PATH = os.path.join(ROOT, "config", "learned.json")

# ── 调参旋钮 ────────────────────────────────────────────────
THRESHOLD = 2          # 同一特征累计到几次才生效（防误点）
BOOST_PER_HIT = 3.0    # 每命中一次加多少分（累加）
BOOST_CAP = 18.0       # 单一特征最多加多少分
MUTE_THRESHOLD = 2     # 👎 累计到几次开始过滤同类
MAX_WANT = 24          # 调教关键词最多记多少个

# 中文偏好词 → 英文/技术关键词，方便去匹配仓库
SYNONYMS = {
    "rust": ["rust"],
    "go": ["go", "golang"],
    "python": ["python"],
    "typescript": ["typescript"],
    "javascript": ["javascript"],
    "大模型": ["llm", "large-language-model", "generative-ai"],
    "推理": ["inference", "vllm", "sglang", "llama.cpp"],
    "智能体": ["agent", "agents", "multi-agent"],
    "agent": ["agent", "agents"],
    "爬虫": ["crawler", "scraper", "spider"],
    "区块链": ["blockchain", "web3", "crypto"],
    "教程": ["tutorial", "course", "guide", "handbook"],
    "本地部署": ["local", "self-hosted", "ollama", "llama.cpp"],
    "量化": ["quantization", "quant"],
    "工作流": ["workflow", "automation"],
    "设计": ["design", "ui", "ux"],
    "安全": ["security", "audit", "vulnerability"],
    "知识库": ["rag", "knowledge-base", "retrieval"],
    "编程助手": ["claude-code", "cursor", "copilot", "codex"],
}


# ──────────────────────────────────────────────────────── 读输入

def load_feedback():
    """读 data/feedback.jsonl，坏行跳过不炸。"""
    if not os.path.exists(FEEDBACK_PATH):
        return []
    out = []
    with open(FEEDBACK_PATH, "r", encoding="utf-8") as f:
        for ln, line in enumerate(f, 1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                print("[!] feedback.jsonl 第 %d 行不是合法 JSON，跳过" % ln)
                continue
            if isinstance(rec, dict) and rec.get("a"):
                out.append(rec)
    return out


def load_tuning():
    """读 config/tuning.txt —— 每行一句大白话。"""
    if not os.path.exists(TUNING_PATH):
        return []
    lines = []
    with open(TUNING_PATH, "r", encoding="utf-8") as f:
        for line in f:
            s = line.strip()
            if s and not s.startswith("#"):
                lines.append(s)
    return lines


# ──────────────────────────────────────────────────────── 统计

def feature_key(rec):
    """把一条行为记录展开成它涉及的「特征」。"""
    keys = []
    if rec.get("l"):
        keys.append(("lang", str(rec["l"]).lower()))
    for t in (rec.get("t") or []):
        keys.append(("topic", str(t).lower()))
    for g in (rec.get("g") or []):
        keys.append(("group", str(g)))
    if rec.get("c"):
        keys.append(("category", str(rec["c"])))
    return keys


def build_learned(events, tuning):
    up = Counter()      # 点赞过的特征
    down = Counter()    # 点踩过的特征
    up_repos, down_repos = [], []

    for rec in events:
        action = rec.get("a")
        ride = rec.get("r")
        # 「收藏」也算强正反馈：愿意带走的东西，显然想看更多同类
        if action in ("up", "star"):
            for k in feature_key(rec):
                up[k] += 1
            if ride and ride not in up_repos:
                up_repos.append(ride)
        elif action in ("down",):
            for k in feature_key(rec):
                down[k] += 1
            if ride and ride not in down_repos:
                down_repos.append(ride)

    # 👎 和 👍 相互抵消：既赞又踩的特征不生效
    for k in list(down):
        if up.get(k, 0) >= down[k]:
            del down[k]
    for k in list(up):
        if down.get(k, 0) >= up[k]:
            del up[k]

    boost = {f"{kind}:{val}": min(BOOST_CAP, cnt * BOOST_PER_HIT)
             for (kind, val), cnt in up.items() if cnt >= THRESHOLD}
    mute = {f"{kind}:{val}": cnt
            for (kind, val), cnt in down.items() if cnt >= MUTE_THRESHOLD}

    # ── 调教雷达的自然语言 → 想要 / 不想要 关键词 ──
    want, avoid = [], []
    for line in tuning:
        m_avoid = re.match(r"^(?:不要|少推|别再|排除|屏蔽|不想看)\s*[:：]?\s*(.+)$", line)
        m_want = re.match(r"^(?:多推|多想看|多看|关注|想要|希望|多一些)\s*[:：]?\s*(.+)$", line)
        if m_avoid:
            avoid += split_words(m_avoid.group(1))
        elif m_want:
            want += split_words(m_want.group(1))
        else:
            want += split_words(line)

    want = expand_keywords(want)[:MAX_WANT]
    avoid = expand_keywords(avoid)[:MAX_WANT]

    return {
        "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "events_total": len(events),
        "threshold": THRESHOLD,
        "boost": boost,
        "mute": mute,
        "up_repos": up_repos[-40:],
        "down_repos": down_repos[-40:],
        "want": want,
        "avoid": avoid,
        "tuning_lines": tuning,
    }


def split_words(text):
    return [w for w in re.split(r"[、,，;；/\s]+", text) if len(w) >= 2]


def expand_keywords(words):
    """把中文偏好词展开成可匹配的英文/技术词。"""
    out = []
    for w in words:
        low = w.lower()
        if w not in out:
            out.append(w)
        for key, syns in SYNONYMS.items():
            if key in low or low in key:
                for s in syns:
                    if s not in out:
                        out.append(s)
    return out


# ──────────────────────────────────────────────────────── 应用（给 build.py 调用）

def key_of(kind, value):
    return "%s:%s" % (kind, str(value).lower())


def score_item(item, learned):
    """
    返回 (加分, 是否该过滤)。
    加分是叠加在原有评分上的；过滤是硬性的（👎 累计够了才发生）。
    """
    if not learned:
        return 0.0, False, []

    boost = learned.get("boost") or {}
    mute = learned.get("mute") or {}

    keys = [key_of("lang", item.get("language") or "")]
    for t in (item.get("topics") or []):
        keys.append(key_of("topic", t))
    for g in (item.get("matched_groups") or []):
        keys.append(key_of("group", g))
    keys.append(key_of("category", item.get("category") or ""))

    add = 0.0
    hits = []
    for k in keys:
        if k in boost:
            add += boost[k]
            hits.append(k)

    # 直接点赞/收藏过的仓库，下一期直接加分
    if item.get("id") in (learned.get("up_repos") or []):
        add += BOOST_CAP
        hits.append("repo:liked")

    blocked = [k for k in keys if k in mute]

    # 调教雷达：不想要的关键词直接过滤
    haystack = " ".join([
        str(item.get("full_name") or ""),
        str(item.get("description") or ""),
        " ".join(item.get("topics") or []),
        " ".join(item.get("matched_groups") or []),
    ]).lower()
    for w in (learned.get("avoid") or []):
        if w.lower() in haystack:
            blocked.append("avoid:%s" % w)

    # 调教雷达：想要的关键词加分
    for w in (learned.get("want") or []):
        if w.lower() in haystack and ("want:%s" % w) not in hits:
            add += BOOST_PER_HIT
            hits.append("want:%s" % w)

    return round(add, 2), bool(blocked), hits


# ──────────────────────────────────────────────────────── 主流程

def main():
    ap = argparse.ArgumentParser(description="根据反馈计算下一期的排序权重")
    ap.add_argument("--report", action="store_true", help="只打印统计，不写文件")
    args = ap.parse_args()

    events = load_feedback()
    tuning = load_tuning()
    learned = build_learned(events, tuning)

    print("=== 反馈学习 ===")
    print("[i] 读到行为记录 %d 条，调教语句 %d 条" % (len(events), len(tuning)))
    print("[i] 生效加权特征 %d 个，过滤特征 %d 个"
          % (len(learned["boost"]), len(learned["mute"])))
    if learned["want"]:
        print("[i] 想多看：%s" % "、".join(learned["want"][:12]))
    if learned["avoid"]:
        print("[i] 不想看：%s" % "、".join(learned["avoid"][:12]))

    if args.report:
        print()
        print("--- 加权明细 ---")
        for k, v in sorted(learned["boost"].items(), key=lambda x: -x[1]):
            print("   +%-5s %s" % (v, k))
        print("--- 过滤明细 ---")
        for k, v in sorted(learned["mute"].items(), key=lambda x: -x[1]):
            print("   ✕%d     %s" % (v, k))
        return 0

    with open(LEARNED_PATH, "w", encoding="utf-8") as f:
        json.dump(learned, f, indent=2, ensure_ascii=False)
    print("[+] 已写出 %s" % os.path.relpath(LEARNED_PATH, ROOT))

    if not events and not tuning:
        print("    （还没有任何反馈 —— 这是正常的，去页面上点几个 👍/👎，")
        print("      点「同步我的反馈」提交后，下一期开始生效）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
