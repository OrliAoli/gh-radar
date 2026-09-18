#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一入口脚本 —— 给定时任务（WorkBuddy / cron / GitHub Actions）调用。

两条命令：
    python3 scripts/radar.py --fetch-only
        只抓取当日快照并写入 data/daily/YYYY-MM-DD.json，不生成页面。
        每天跑一次。

    python3 scripts/radar.py --fetch-and-deploy
        抓取 + 聚合最近 3 天 + 生成 data/latest.json 与 feed.xml + 部署。
        每 3 天跑一次。
"""

import argparse
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY = sys.executable or "python3"


def run(cmd, cwd=ROOT):
    print("\n$ %s" % " ".join(cmd))
    r = subprocess.run(cmd, cwd=cwd)
    if r.returncode != 0:
        print("[x] 命令失败，退出码 %d" % r.returncode)
    return r.returncode


def main():
    ap = argparse.ArgumentParser(description="每日 GitHub 雷达 · 统一入口")
    ap.add_argument("--fetch-only", action="store_true",
                    help="只抓取存快照（每天跑）")
    ap.add_argument("--fetch-and-deploy", action="store_true",
                    help="抓取 + 聚合 + 生成页面 + 部署（每 3 天跑）")
    ap.add_argument("--no-alert", action="store_true", help="不开 GitHub 告警 issue")
    ap.add_argument("--days", type=int, default=3, help="聚合窗口天数，默认 3")
    args = ap.parse_args()

    if not args.fetch_only and not args.fetch_and_deploy:
        ap.print_help()
        return 2

    fetch_cmd = [PY, "scripts/fetch.py"]
    if args.no_alert:
        fetch_cmd.append("--no-alert")

    code = run(fetch_cmd)
    if code != 0:
        print("[!] 抓取有告警（可能部分类目失败），继续执行")

    if args.fetch_only:
        print("\n=== 完成：仅抓取，未生成页面 ===")
        return 0

    code = run([PY, "scripts/build.py", "--days", str(args.days)])
    if code != 0:
        return code

    print("\n=== 完成：已生成 data/latest.json 与 feed.xml ===")
    print("[i] 部署步骤尚未接入，当前需手动部署到 EdgeOne Pages")
    return 0


if __name__ == "__main__":
    sys.exit(main())
