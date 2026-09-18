#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
打包与部署。

打包（默认动作）：把 web/ 和数据组装成一个可直接托管的静态目录 dist/：

    dist/
    ├── index.html
    ├── style.css
    ├── js/*.js
    ├── feed.xml
    └── data/latest.json      ← 与前端同源，不走任何外部 CDN

为什么要"同源"：前端和数据放在同一个国内 CDN 上，
浏览器取数据不跨洋、不依赖 jsDelivr，国内打开快且稳。

部署：把 dist/ 发布到 EdgeOne Pages。
站点名一旦创建不可修改，所以需要显式传入 --site-name 才会真的创建。
依赖：仅 Python 标准库。
"""

import argparse
import json
import os
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WEB_DIR = os.path.join(ROOT, "web")
DATA_DIR = os.path.join(ROOT, "data")
DIST_DIR = os.path.join(ROOT, "dist")

IGNORE = shutil.ignore_patterns("node_modules", ".git", ".DS_Store", "*.pyc", "__pycache__")


def copy_tree(src, dst):
    if not os.path.isdir(src):
        return 0
    n = 0
    for name in os.listdir(src):
        if name in ("node_modules", ".git", ".DS_Store", "__pycache__"):
            continue
        s, d = os.path.join(src, name), os.path.join(dst, name)
        if os.path.isdir(s):
            shutil.copytree(s, d, dirs_exist_ok=True, ignore=IGNORE)
            n += 1
        else:
            os.makedirs(os.path.dirname(d), exist_ok=True)
            shutil.copy2(s, d)
            n += 1
    return n


def assemble():
    """组装 dist/"""
    latest = os.path.join(DATA_DIR, "latest.json")
    if not os.path.exists(latest):
        print("[x] 找不到 data/latest.json，先跑 scripts/build.py")
        return 1

    if os.path.isdir(DIST_DIR):
        shutil.rmtree(DIST_DIR)
    os.makedirs(DIST_DIR, exist_ok=True)

    cs = copy_tree(WEB_DIR, DIST_DIR)
    print("[i] 复制前端 %d 项" % cs)

    # 数据放在 dist/data/ 下，和 index.html 同源
    os.makedirs(os.path.join(DIST_DIR, "data"), exist_ok=True)
    shutil.copy2(latest, os.path.join(DIST_DIR, "data", "latest.json"))

    # 每日快照也一起带上，前端在 latest.json 读取失败时会回溯
    daily_src = os.path.join(DATA_DIR, "daily")
    if os.path.isdir(daily_src):
        dst = os.path.join(DIST_DIR, "data", "daily")
        os.makedirs(dst, exist_ok=True)
        files = sorted(f for f in os.listdir(daily_src) if f.endswith(".json"))
        for f in files[-7:]:                      # 只带最近 7 天，控制体积
            shutil.copy2(os.path.join(daily_src, f), os.path.join(dst, f))
        print("[i] 附带最近 %d 天快照" % min(len(files), 7))

    feed = os.path.join(ROOT, "feed.xml")
    if os.path.exists(feed):
        shutil.copy2(feed, os.path.join(DIST_DIR, "feed.xml"))

    # 写个版本标记，方便确认线上是不是最新一版
    with open(os.path.join(DIST_DIR, "version.json"), "w", encoding="utf-8") as f:
        data = json.load(open(latest, encoding="utf-8"))
        json.dump({
            "date": data.get("date"),
            "updated_at": data.get("updated_at"),
            "published": len(data.get("items") or []),
        }, f, ensure_ascii=False, indent=2)

    total = sum(len(fs) for _, _, fs in os.walk(DIST_DIR))
    print("[+] 打包完成：%s（%d 个文件）" % (DIST_DIR, total))
    return 0


def deploy_edgeone(site_name, token=None):
    """
    发布到 EdgeOne Pages。
    需要本机已安装 edgeone CLI：npm i -g edgeone
    """
    cli = shutil.which("edgeone")
    if not cli:
        print("[!] 没找到 edgeone 命令。先安装：")
        print("    npm install -g edgeone")
        print("    然后重新运行：python3 scripts/deploy.py --deploy --site-name %s" % site_name)
        return 2

    env = dict(os.environ)
    if token:
        env["EDGEONE_API_TOKEN"] = token

    cmd = [cli, "pages", "deploy", DIST_DIR, "--name", site_name]
    print("[i] 执行：%s" % " ".join(cmd))
    r = subprocess.run(cmd, env=env)
    if r.returncode == 0:
        print("[+] 部署完成")
    else:
        print("[x] 部署失败，退出码 %d" % r.returncode)
    return r.returncode


def main():
    ap = argparse.ArgumentParser(description="打包（并可选部署）静态站点")
    ap.add_argument("--deploy", action="store_true", help="打包后部署到 EdgeOne Pages")
    ap.add_argument("--site-name", help="EdgeOne Pages 站点名（创建后不可改）")
    ap.add_argument("--token", help="EdgeOne API Token（也可用环境变量 EDGEONE_API_TOKEN）")
    args = ap.parse_args()

    code = assemble()
    if code != 0 or not args.deploy:
        return code

    if not args.site_name:
        print("[x] 部署必须指定 --site-name（站点名一旦创建不可修改）")
        return 2
    return deploy_edgeone(args.site_name, args.token)


if __name__ == "__main__":
    sys.exit(main())
