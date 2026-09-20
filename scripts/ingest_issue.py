#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把 GitHub Issue 里的内容搬进仓库文件。

页面是纯静态的（没有后端、也不该把写权限令牌放进前端），
所以所有「用户想写回仓库」的东西都走同一条路：

    页面生成预填 Issue  →  用户点提交  →  本脚本把内容追加进文件

三种 Issue（靠 body 开头的一行 HTML 注释区分）：

    <!-- radar-feedback -->          → data/feedback.jsonl
    <!-- radar-tuning -->            → config/tuning.txt
    <!-- radar-push-subscribe -->    → data/push-subscriptions.json

Issue 没写标记时，按标签（radar-feedback / radar-tuning / radar-push）兜底判断。

环境变量：
    ISSUE_BODY      必填，Issue 正文
    ISSUE_LABELS    可选，逗号分隔的标签名

依赖：仅 Python 标准库。
"""

import base64
import datetime
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FEEDBACK_PATH = os.path.join(ROOT, "data", "feedback.jsonl")
TUNING_PATH = os.path.join(ROOT, "config", "tuning.txt")
SUBS_PATH = os.path.join(ROOT, "data", "push-subscriptions.json")

MARKER_FEEDBACK = "radar-feedback"
MARKER_TUNING = "radar-tuning"
MARKER_PUSH = "radar-push"


def fenced_blocks(body, lang=None):
    """抽出所有 ``` 围栏代码块的内容。lang 给定时只取该语言。"""
    out = []
    for m in re.finditer(r"```([^\n`]*)\n(.*?)```", body, re.S):
        tag = (m.group(1) or "").strip().lower()
        if lang and tag != lang:
            continue
        out.append(m.group(2).strip())
    return out


def detect_kind(body, labels):
    """判断这条 Issue 属于哪一类。"""
    head = body[:2000]
    if MARKER_FEEDBACK in head:
        return "feedback"
    if MARKER_TUNING in head:
        return "tuning"
    if MARKER_PUSH in head:
        return "push"
    if MARKER_FEEDBACK in labels:
        return "feedback"
    if MARKER_TUNING in labels:
        return "tuning"
    if MARKER_PUSH in labels:
        return "push"
    return None


def append_lines(path, lines):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        for ln in lines:
            f.write(ln + "\n")


def do_feedback(body):
    """feedback：正文里有一段 ```json，是个事件数组。"""
    blobs = fenced_blocks(body, "json")
    events = []
    for blob in blobs:
        try:
            data = json.loads(blob)
        except json.JSONDecodeError:
            continue
        if isinstance(data, list):
            events.extend([e for e in data if isinstance(e, dict) and e.get("a")])

    # 兼容：整段正文就是一个 JSON 数组
    if not events:
        try:
            data = json.loads(body.strip())
            if isinstance(data, list):
                events = [e for e in data if isinstance(e, dict) and e.get("a")]
        except Exception:  # noqa: BLE001
            pass

    if not events:
        print("[!] 没解析出任何反馈事件，跳过")
        return 0

    stamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    lines = []
    for e in events:
        rec = dict(e)
        rec.setdefault("ingested_at", stamp)
        rec.setdefault("src", "issue")
        lines.append(json.dumps(rec, ensure_ascii=False))
    append_lines(FEEDBACK_PATH, lines)
    print("[+] 已追加 %d 条反馈到 data/feedback.jsonl" % len(lines))
    return len(lines)


def do_tuning(body):
    """tuning：正文里有一段 ```text，每行一句大白话偏好。"""
    blobs = fenced_blocks(body, "text") or fenced_blocks(body)
    lines = []
    for blob in blobs:
        for raw in blob.split("\n"):
            s = raw.strip()
            if s and "radar-tuning" not in s:
                lines.append(s)
    if not lines:
        print("[!] 没解析出任何调教语句，跳过")
        return 0

    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
    append_lines(TUNING_PATH, ["# %s" % stamp] + lines)
    print("[+] 已追加 %d 条偏好到 config/tuning.txt" % len(lines))
    for s in lines:
        print("      %s" % s)
    return len(lines)


def do_push(body):
    """push：正文里有一段 ```text，是 base64 编码的 PushSubscription。"""
    blobs = fenced_blocks(body, "text") or fenced_blocks(body)
    subs = []
    for blob in blobs:
        raw = blob.strip().split()[-1] if blob.strip() else ""
        if not raw:
            continue
        try:
            decoded = base64.b64decode(raw + "=" * (-len(raw) % 4)).decode("utf-8")
            sub = json.loads(decoded)
        except Exception:  # noqa: BLE001
            continue
        if isinstance(sub, dict) and sub.get("endpoint"):
            sub["added_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
            subs.append(sub)

    if not subs:
        print("[!] 没解析出推送订阅，跳过")
        return 0

    existing = []
    if os.path.exists(SUBS_PATH):
        try:
            existing = json.load(open(SUBS_PATH, encoding="utf-8")) or []
        except Exception:  # noqa: BLE001
            existing = []
    endpoints = {s.get("endpoint") for s in existing}
    for s in subs:
        if s["endpoint"] not in endpoints:
            existing.append(s)
    with open(SUBS_PATH, "w", encoding="utf-8") as f:
        json.dump(existing, f, indent=2, ensure_ascii=False)
    print("[+] 推送订阅已保存，当前共 %d 个设备" % len(existing))
    return len(subs)


def main():
    body = os.getenv("ISSUE_BODY", "") or ""
    labels = os.getenv("ISSUE_LABELS", "") or ""
    if not body.strip():
        print("[=] 没有 ISSUE_BODY（手动触发且未提供内容），什么都不做")
        return 0

    kind = detect_kind(body, labels)
    if not kind:
        print("[=] 这条 Issue 没有 radar-* 标记，不处理")
        return 0

    print("[i] 识别为：%s" % kind)
    if kind == "feedback":
        return 0 if do_feedback(body) >= 0 else 1
    if kind == "tuning":
        return 0 if do_tuning(body) >= 0 else 1
    if kind == "push":
        return 0 if do_push(body) >= 0 else 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
