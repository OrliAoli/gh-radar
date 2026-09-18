#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
过滤与打分脚本 —— 只负责"判断一条数据该不该留、归哪一类、得多少分"。

解析 config/rules.txt 的语法（扩展版 TrendRadar 语法）：

  [GLOBAL_FILTER]   全局排除区，命中即丢弃（整榜生效，不加 !）
  [WEAK]            降权区，命中不排除，score *= weak_multiplier（默认 0.5）
  [QUALITY_GATE]    质量门槛区，命中后必须满足放行条件，否则丢弃
  [组名]            兴趣组，命中决定 category 和分类配额

  组内规则行：
    关键词            普通词，命中即算（同组多个之间是 OR）
    /正则/            正则匹配，忽略大小写
    +关键词           必须词，所有 + 词都要命中（AND）
    !关键词           过滤词，命中即排除，【仅当前组生效】
    @数字             该组最多取多少条
    [别名]            写在组第一行，给整组起显示名
    关键词 => 别名     给单个关键词起别名

设计要点：
  · GLOBAL_FILTER 是全局的；! 只在组内生效 —— 这两层不能混
  · stars_today 为 None 是【合法状态】，不是错误，绝不当无效数据丢掉
  · 未命中任何兴趣组的条目一律丢弃（require_group_match_all_categories）
"""

import json
import math
import os
import re
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RULES_PATH = os.path.join(ROOT, "config", "rules.txt")
THRESHOLDS_PATH = os.path.join(ROOT, "config", "thresholds.json")

# 分组 → 类别
GROUP_CATEGORY = {
    "AI 编程 Skill": "ai_skill",
    "AI Agent 应用": "ai_skill",
    "AI 学习资源": "growth",
    "LLM 推理优化": "growth",
    "中文技术": "growth",
}

# 分组权重：AI 编程 Skill 最高（用户最关心）
GROUP_WEIGHT = {
    "AI 编程 Skill": 1.6,
    "AI Agent 应用": 1.3,
    "AI 学习资源": 1.0,
    "LLM 推理优化": 1.1,
    "中文技术": 0.9,
}

DEFAULT_THRESHOLDS = {
    "weak_multiplier": 0.5,
    "quality_gate_min_stars": 50000,
    "quality_gate_top_n": 3,
    "classic_min_stars": 100000,
    "classic_require_group_match": True,
    "require_group_match_all_categories": True,
    "burst_top_n": 8,
    "total_limit": 20,
    "category_quota": {"ai_skill": 12, "burst": 5, "growth": 9, "classic": 3},
}


# ------------------------------------------------------------ 解析

def _compile_rule(line):
    """把一行规则文本编译成 (kind, matcher, raw)。返回 None 表示不是规则行。"""
    s = line.strip()
    if not s or s.startswith("#"):
        return None
    if s.startswith("/") and s.endswith("/") and len(s) > 2:
        inner = s[1:-1]
        try:
            return ("regex", re.compile(inner, re.I), s)
        except re.error:
            return None
    if s.startswith("+"):
        return ("required", s[1:].lower(), s)
    if s.startswith("!"):
        return ("exclude", s[1:].lower(), s)
    return ("plain", s.lower(), s)


def _match_rule(rule, text):
    kind, matcher, _ = rule
    if kind == "regex":
        return bool(matcher.search(text))
    return matcher in text


def load_rules(path=RULES_PATH):
    """
    返回 dict：
      {
        "global_filter": [rule...],
        "weak":          [rule...],
        "quality_gate":  [rule...],
        "groups": [{"name","alias","limit","rules","category","weight"}...]
      }
    """
    if not os.path.exists(path):
        raise FileNotFoundError("找不到规则文件：%s" % path)

    result = {"global_filter": [], "weak": [], "quality_gate": [], "groups": []}
    section = None
    cur = None

    with open(path, "r", encoding="utf-8") as f:
        for raw in f:
            line = raw.rstrip("\n")
            s = line.strip()
            if not s or s.startswith("#"):
                continue

            # 区块头
            m = re.match(r"^\[([^\]]+)\]$", s)
            if m:
                name = m.group(1).strip()
                if name in ("GLOBAL_FILTER", "WEAK", "QUALITY_GATE"):
                    section = name.lower()
                    cur = None
                elif cur is not None and s and not re.match(r"^\[", s):
                    pass
                # 组名区块：先落地上一个组
                if name not in ("GLOBAL_FILTER", "WEAK", "QUALITY_GATE"):
                    if cur is not None:
                        result["groups"].append(cur)
                    cur = {"name": name, "alias": name, "limit": None, "rules": []}
                    section = "group"
                continue

            # @N 限条
            m = re.match(r"^@(\d+)$", s)
            if m and section == "group" and cur is not None:
                cur["limit"] = int(m.group(1))
                continue

            # 别名：关键词 => 别名
            if "=>" in s:
                s = s.split("=>")[0].strip()

            rule = _compile_rule(s)
            if rule is None:
                continue

            if section == "global_filter":
                result["global_filter"].append(rule)
            elif section == "weak":
                result["weak"].append(rule)
            elif section == "quality_gate":
                result["quality_gate"].append(rule)
            elif section == "group" and cur is not None:
                cur["rules"].append(rule)

    if cur is not None:
        result["groups"].append(cur)

    for g in result["groups"]:
        g["category"] = GROUP_CATEGORY.get(g["name"], "growth")
        g["weight"] = GROUP_WEIGHT.get(g["name"], 1.0)
    return result


def load_thresholds(path=THRESHOLDS_PATH):
    t = dict(DEFAULT_THRESHOLDS)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            t.update(json.load(f))
    return t


# ------------------------------------------------------------ 评估

def _repo_text(repo):
    parts = [repo.get("full_name", ""), repo.get("description", ""),
             " ".join(repo.get("topics") or []), repo.get("language", "")]
    return " ".join(p for p in parts if p).lower()


def _freshness(repo):
    """created_at 越近分越高：90 天内 1.0，1 年内 0.7，更早 0.4，未知 0.6"""
    c = repo.get("created_at")
    if not c:
        return 0.6
    try:
        dt = datetime.strptime(c, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    except ValueError:
        return 0.6
    days = (datetime.now(timezone.utc) - dt).days
    if days <= 90:
        return 1.0
    if days <= 365:
        return 0.7
    return 0.4


def evaluate(repo, rules, th):
    """
    对单条仓库做过滤与打分，返回 dict：
      {"drop": bool, "drop_reason": str|None,
       "categories": [...], "hit_groups": [...],
       "strength": float, "weak": bool, "quality_gate": bool, "score": float}
    """
    text = _repo_text(repo)
    stars = repo.get("total_stars") or 0

    # 1) 全局排除
    for r in rules["global_filter"]:
        if _match_rule(r, text):
            return {"drop": True, "drop_reason": "命中全局排除：%s" % r[2],
                    "categories": [], "hit_groups": [], "strength": 0.0,
                    "weak": False, "quality_gate": False, "score": 0.0}

    # 2) 分组匹配
    hit_groups = []
    strength = 0.0
    for g in rules["groups"]:
        required = [r for r in g["rules"] if r[0] == "required"]
        excludes = [r for r in g["rules"] if r[0] == "exclude"]
        positives = [r for r in g["rules"] if r[0] in ("plain", "regex")]

        if any(_match_rule(r, text) for r in excludes):
            continue                                  # ! 仅本组生效
        if required and not all(_match_rule(r, text) for r in required):
            continue
        hits = [r for r in positives if _match_rule(r, text)]
        if not hits and not required:
            continue
        hit_groups.append({"name": g["name"], "category": g["category"],
                           "hits": len(hits), "limit": g["limit"]})
        strength += len(hits) * g["weight"]

    # 3) 必须命中至少一个兴趣组
    if th.get("require_group_match_all_categories", True) and not hit_groups:
        return {"drop": True, "drop_reason": "未命中任何兴趣组",
                "categories": [], "hit_groups": [], "strength": 0.0,
                "weak": False, "quality_gate": False, "score": 0.0}

    # 4) 弱匹配降权
    weak = any(_match_rule(r, text) for r in rules["weak"])

    # 5) 质量门槛标记（是否放行在 build.py 里按本期排名决定）
    qg = any(_match_rule(r, text) for r in rules["quality_gate"])

    # 6) 相关度打分（车道 B 用）：命中强度 × log(总星) × 新鲜度
    relevance = strength * math.log10(stars + 10) * _freshness(repo)
    if weak:
        relevance *= th.get("weak_multiplier", 0.5)

    categories = sorted({h["category"] for h in hit_groups})
    return {"drop": False, "drop_reason": None, "categories": categories,
            "hit_groups": hit_groups, "strength": round(strength, 3),
            "weak": weak, "quality_gate": qg, "score": round(relevance, 3)}


def burst_score(peak_stars_today, total_stars):
    """爆发指数：round(peak_stars_today / sqrt(total_stars + 100) * 10, 1)"""
    if peak_stars_today is None:
        return None
    return round(peak_stars_today / math.sqrt((total_stars or 0) + 100) * 10, 1)


if __name__ == "__main__":
    r = load_rules()
    t = load_thresholds()
    print("全局排除规则 %d 条 / 降权 %d 条 / 质量门槛 %d 条"
          % (len(r["global_filter"]), len(r["weak"]), len(r["quality_gate"])))
    print("兴趣组：")
    for g in r["groups"]:
        print("  %-16s → %-9s 权重 %.1f  限额 %s  规则 %d 条"
              % (g["name"], g["category"], g["weight"], g["limit"], len(g["rules"])))
    print("阈值：%s" % json.dumps(t, ensure_ascii=False))
