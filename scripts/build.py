#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
聚合与发布脚本 —— 读最近 N 天的每日快照，聚合成一期榜单，输出给前端。

核心逻辑：

  1. 多日合并：同一仓库取【峰值 stars_today】而非平均值
     （"今天火明天凉"的项目会被自然淘汰，峰值才反映真实爆发）
  2. 双车道计分：
       车道 A（有 stars_today）  → burst_score    → 填 burst 名额
       车道 B（stars_today 为 None，即搜索池）→ 相关度 → 填 ai_skill / growth 名额
     ⚠️ stars_today 为 None 是合法状态，绝不当无效数据丢掉
  3. 硬卡 20 条，类别配额为上限
  4. 维护 data/state.json 记录 first_seen / periods_on_board

依赖：仅 Python 标准库。
"""

import argparse
import datetime
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from filter import load_rules, load_thresholds, evaluate, burst_score  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT, "data")
DAILY_DIR = os.path.join(DATA_DIR, "daily")
STATE_PATH = os.path.join(DATA_DIR, "state.json")

WINDOW_DAYS = 3          # 聚合窗口：最近 3 天

# 类别优先级（一条数据同时命中多个兴趣组时，归到优先级最高的类别）
CATEGORY_PRIORITY = ["ai_skill", "growth"]


# ------------------------------------------------------------ 载入

def assign_rank_score(items):
    """
    给每条算一个"车道内相对排名分"（0~1）。
    作用：burst_score（0~400）和车道 B 的相关度分（0~30）量级差太远、无法直接比较，
    换成"在各自车道里的排名"就能公平比较了。
    """
    for lane in ("A", "B"):
        sub = [i for i in items if i["lane"] == lane]
        sub.sort(key=lambda x: (x["score"] or 0), reverse=True)
        n = len(sub)
        for idx, it in enumerate(sub):
            it["rank_score"] = round((n - idx) / float(n), 6) if n else 0.0


def primary_category(item):
    """一条数据同时命中多个兴趣组时，归到优先级最高的类别。"""
    for c in CATEGORY_PRIORITY:
        if c in item.get("categories", []):
            return c
    return (item.get("categories") or ["ai_skill"])[0]


def list_snapshot_dates():
    if not os.path.exists(DAILY_DIR):
        return []
    return sorted(f[:-5] for f in os.listdir(DAILY_DIR) if f.endswith(".json"))


def load_snapshot(d):
    p = os.path.join(DAILY_DIR, "%s.json" % d)
    if not os.path.exists(p):
        return None
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)


def load_state():
    if os.path.exists(STATE_PATH):
        with open(STATE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"repos": {}, "periods": []}


def save_state(state):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)


# ------------------------------------------------------------ 合并

def collect_all_repos(snapshots):
    """把多日快照合成一份：取峰值 stars_today、最大总星。"""
    pool = {}
    for snap in snapshots:
        d = snap.get("date")
        buckets = []
        for items in (snap.get("categories") or {}).values():
            buckets.append(items or [])
        for items in (snap.get("search_pool") or {}).values():
            buckets.append(items or [])
        for items in buckets:
            for r in items or []:
                rid = r.get("id")
                if not rid:
                    continue
                cur = pool.get(rid)
                if cur is None:
                    cur = dict(r)
                    cur["peak_stars_today"] = r.get("stars_today")
                    cur["days_seen"] = {d}
                    pool[rid] = cur
                    continue
                a, b = cur.get("peak_stars_today"), r.get("stars_today")
                if a is None:
                    cur["peak_stars_today"] = b
                elif b is not None and b > a:
                    cur["peak_stars_today"] = b
                if (r.get("total_stars") or 0) > (cur.get("total_stars") or 0):
                    cur["total_stars"] = r["total_stars"]
                cur["days_seen"].add(d)
                for k in ("topics", "description", "language", "created_at", "pushed_at"):
                    if not cur.get(k) and r.get(k):
                        cur[k] = r[k]
    return pool


def compute_first_seen(pool):
    """扫描所有历史快照，找出每个仓库首次被抓到的日期。"""
    first = {}
    for d in list_snapshot_dates():
        snap = load_snapshot(d)
        if not snap:
            continue
        ids = set()
        for items in (snap.get("categories") or {}).values():
            ids |= {r.get("id") for r in items or []}
        for items in (snap.get("search_pool") or {}).values():
            ids |= {r.get("id") for r in items or []}
        for rid in ids:
            if rid and (rid not in first or d < first[rid]):
                first[rid] = d
    return first


# ------------------------------------------------------------ 打分与分类

def score_pool(pool, rules, th):
    """对全池做过滤 + 打分 + 分类。返回 (items, dropped_stats)"""
    items = []
    stats = {"total": len(pool), "dropped_global": 0,
             "dropped_no_group": 0, "dropped_min_stars": 0,
             "dropped_quality_gate": 0}

    for rid, r in pool.items():
        ev = evaluate(r, rules, th)
        if ev["drop"]:
            reason = ev["drop_reason"] or ""
            if "全局排除" in reason:
                stats["dropped_global"] += 1
            elif "星数低于门槛" in reason:
                stats["dropped_min_stars"] += 1
            else:
                stats["dropped_no_group"] += 1
            continue
        st = r.get("peak_stars_today")
        bs = burst_score(st, r.get("total_stars"))
        item = dict(r)
        item["days_seen"] = sorted(r.get("days_seen") or [])
        item["stars_today"] = st                    # 峰值；可能为 None
        item["burst_score"] = bs                    # 可能为 None
        item["lane"] = "A" if st is not None else "B"
        item["score"] = bs if bs is not None else ev["score"]
        item["relevance_score"] = ev["score"]
        item["matched_groups"] = [h["name"] for h in ev["hit_groups"]]
        item["hit_strength"] = ev["strength"]
        item["weak"] = ev["weak"]
        item["quality_gate"] = ev["quality_gate"]
        item["categories"] = ev["categories"]
        items.append(item)

    # 质量门槛：命中硬核词的，必须 总星 > 阈值 或 本期 burst_score 进前 N
    lane_a = sorted([i for i in items if i["burst_score"] is not None],
                    key=lambda x: x["burst_score"], reverse=True)
    top_ids = {i["id"] for i in lane_a[:th.get("quality_gate_top_n", 3)]}
    min_stars = th.get("quality_gate_min_stars", 50000)
    kept = []
    for i in items:
        if i["quality_gate"]:
            if (i.get("total_stars") or 0) > min_stars or i["id"] in top_ids:
                kept.append(i)
            else:
                stats["dropped_quality_gate"] += 1
        else:
            kept.append(i)
    return kept, stats


def pick_by_group(items, group_names, limit_per_group):
    """组内按 score 取前 N；返回 (组内入选, 组内落选)"""
    chosen, left = [], []
    for gname in group_names:
        g = [i for i in items if gname in i["matched_groups"]]
        g.sort(key=lambda x: (x["score"] or 0), reverse=True)
        n = limit_per_group.get(gname)
        if n is None:
            chosen.extend(g)
        else:
            chosen.extend(g[:n])
            left.extend(g[n:])
    return chosen, left


def allocate(items, rules, th):
    """
    分配算法（严格按 config/thresholds.json 的定义）：

      1. 先按 category_min 分保底名额（默认 8+4+4+1 = 17 条）
      2. 剩余名额按分数（车道内相对排名）给未达 category_quota 上限的类别
      3. 任何类别不超过 category_quota

    类别候选池的来源：
      burst   → 只从车道 A（有今日增量）取，且增速排前 burst_top_n
      其他    → 车道 B 优先（保证搜索池不被饿死），不足时用车道 A 补
    """
    total_limit = th.get("total_limit", 20)
    quota = th.get("category_quota", {})
    cmin = th.get("category_min", {})
    classic_min = th.get("classic_min_stars", 100000)
    burst_top_n = th.get("burst_top_n", 8)

    assign_rank_score(items)

    lane_a = sorted([i for i in items if i["lane"] == "A"],
                    key=lambda x: (x["burst_score"] or 0), reverse=True)
    burst_rank = {i["id"]: idx for idx, i in enumerate(lane_a)}
    lane_b = sorted([i for i in items if i["lane"] == "B"],
                    key=lambda x: (x["score"] or 0), reverse=True)
    classic_pool = sorted(
        [i for i in items if (i.get("total_stars") or 0) > classic_min],
        key=lambda x: (x["rank_score"], x["burst_score"] or 0, x["score"] or 0),
        reverse=True)

    for i in items:
        i["primary"] = primary_category(i)

    def pool_for(cat):
        if cat == "burst":
            return list(lane_a)
        if cat == "classic":
            return list(classic_pool)
        b = [i for i in lane_b if i["primary"] == cat]
        a = [i for i in lane_a if i["primary"] == cat]
        return b + a            # 车道 B 优先

    picked, used, count = [], set(), {}
    report = {}

    def add(item, cat, tag):
        item["category"] = cat
        picked.append(item)
        used.add(item["id"])
        count[cat] = count.get(cat, 0) + 1
        report[tag] = report.get(tag, 0) + 1

    # ---- 第 1 步：保底名额
    for cat in sorted(cmin, key=lambda c: -cmin[c]):
        want = min(cmin[cat], quota.get(cat, cmin[cat]))
        got = 0
        for i in pool_for(cat):
            if got >= want or len(picked) >= total_limit:
                break
            if i["id"] in used:
                continue
            if count.get(cat, 0) >= quota.get(cat, want):
                break
            add(i, cat, "保底_%s" % cat)
            got += 1

    # ---- 第 2 步：剩余名额按分数（车道内相对排名）分配
    rest = [i for i in items if i["id"] not in used]
    rest.sort(key=lambda x: (x["rank_score"], x["burst_score"] or 0, x["score"] or 0),
              reverse=True)
    for i in rest:
        if len(picked) >= total_limit:
            break
        # a) 车道 A 的高增速项优先补 burst
        if (i["lane"] == "A" and burst_rank.get(i["id"], 999) < burst_top_n
                and count.get("burst", 0) < quota.get("burst", 0)):
            add(i, "burst", "补位_burst")
            continue
        # b) 归入自己的主类别
        cat = i["primary"]
        if count.get(cat, 0) < quota.get(cat, 0):
            add(i, cat, "补位_%s" % cat)
            continue
        # c) 总星够高的补 classic
        if ((i.get("total_stars") or 0) > classic_min
                and count.get("classic", 0) < quota.get("classic", 0)):
            add(i, "classic", "补位_classic")

    return picked[:total_limit], report


# ------------------------------------------------------------ 输出

def build_feed(items, date_str, out_path):
    import html as H
    now = datetime.datetime.now(datetime.timezone.utc)
    rfc822 = now.strftime("%a, %d %b %Y %H:%M:%S GMT")
    parts = []
    for i in items[:25]:
        title = H.escape("[%s] %s" % (i.get("language") or "-", i.get("full_name", "")))
        desc = H.escape(i.get("description") or "")
        velo = ("+%s stars today" % i["stars_today"]) if i.get("stars_today") else "无今日增量数据"
        parts.append("""    <item>
      <title>%s</title>
      <link>%s</link>
      <description>%s | 总星 %s | %s</description>
      <guid isPermaLink="false">%s#%s</guid>
      <pubDate>%s</pubDate>
    </item>""" % (title, H.escape(i.get("url", "")), desc,
                  i.get("total_stars"), velo,
                  H.escape(i.get("full_name", "")), date_str, rfc822))
    xml = """<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>每日 GitHub 雷达</title>
    <link>https://github.com/trending</link>
    <description>AI / Agent 领域的每日 GitHub 雷达</description>
    <language>zh-cn</language>
    <lastBuildDate>%s</lastBuildDate>
%s
  </channel>
</rss>
""" % (rfc822, "\n".join(parts))
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(xml)


def main():
    ap = argparse.ArgumentParser(description="聚合最近 N 天快照，生成本期榜单")
    ap.add_argument("--date", help="发布日 YYYY-MM-DD，默认 UTC 今天")
    ap.add_argument("--days", type=int, default=WINDOW_DAYS, help="聚合窗口天数")
    args = ap.parse_args()

    now = datetime.datetime.now(datetime.timezone.utc)
    date_str = args.date or now.strftime("%Y-%m-%d")
    all_dates = list_snapshot_dates()
    if not all_dates:
        print("[x] data/daily 下没有任何快照，先跑 scripts/fetch.py")
        return 1
    window = all_dates[-args.days:]
    snaps = [load_snapshot(d) for d in window]
    snaps = [s for s in snaps if s]

    print("=== 聚合 %s（窗口 %s，共 %d 天快照）===" % (date_str, window[0], len(snaps)))

    pool = collect_all_repos(snaps)
    print("[i] 合并后候选池 %d 条" % len(pool))
    first = compute_first_seen(pool)
    state = load_state()

    rules = load_rules()
    th = load_thresholds()

    items, drop_stats = score_pool(pool, rules, th)
    print("[i] 过滤后 %d 条（全局排除 -%d / 星数门槛 -%d / 未命中兴趣组 -%d / 质量门槛 -%d）"
          % (len(items), drop_stats["dropped_global"], drop_stats["dropped_min_stars"],
             drop_stats["dropped_no_group"], drop_stats["dropped_quality_gate"]))
    print("[i] 车道 A（有今日增量）%d 条 / 车道 B（搜索池）%d 条"
          % (sum(1 for i in items if i["lane"] == "A"),
             sum(1 for i in items if i["lane"] == "B")))

    final, alloc_report = allocate(items, rules, th)
    print("[i] 配额分配：%s" % json.dumps(alloc_report, ensure_ascii=False))

    # 回填 first_seen / periods_on_board
    for i in final:
        fs = first.get(i["id"]) or state["repos"].get(i["id"], {}).get("first_seen")
        i["first_seen"] = fs or date_str
        rec = state["repos"].get(i["id"]) or {}
        rec["first_seen"] = i["first_seen"]
        rec["periods_on_board"] = (rec.get("periods_on_board") or 0) + 1
        rec["last_published"] = date_str
        state["repos"][i["id"]] = rec
        i["periods_on_board"] = rec["periods_on_board"]
        # 前端需要的展示字段（中文简介留空，绝不编造）
        i.setdefault("title_cn", None)
        i.setdefault("reason_cn", None)
        i["days_seen"] = len(i.get("days_seen") or [])

    if date_str not in state["periods"]:
        state["periods"].append(date_str)
    save_state(state)

    latest = {
        "updated_at": now.isoformat(),
        "date": date_str,
        "window": {"from": window[0], "to": window[-1], "days": len(snaps)},
        "source": snaps[-1].get("source"),
        "warnings": [w for s in snaps for w in (s.get("warnings") or [])],
        "stats": {
            "candidates": len(pool),
            "after_filter": len(items),
            "lane_a": sum(1 for i in items if i["lane"] == "A"),
            "lane_b": sum(1 for i in items if i["lane"] == "B"),
            "dropped": drop_stats,
            "allocation": alloc_report,
            "published": len(final),
            "from_trending": sum(1 for i in final if i.get("src") == "trending"),
            "from_search": sum(1 for i in final if i.get("src") == "search"),
        },
        "items": final,
    }

    os.makedirs(DATA_DIR, exist_ok=True)
    with open(os.path.join(DATA_DIR, "latest.json"), "w", encoding="utf-8") as f:
        json.dump(latest, f, indent=2, ensure_ascii=False)
    build_feed(final, date_str, os.path.join(ROOT, "feed.xml"))

    print("[+] 已写出 data/latest.json（%d 条）与 feed.xml" % len(final))
    print("    来源分布：trending %d 条 / search %d 条"
          % (latest["stats"]["from_trending"], latest["stats"]["from_search"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
