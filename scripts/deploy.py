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
import re
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
    用 edgeone CLI 直接发布。需要本机已安装：npm i -g edgeone
    （当前项目走的是「Git 仓库自动连接」方式，一般用不到这个函数）
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


def git_publish():
    """
    把 dist/ 和 data/ 提交并推送。
    项目走的是 EdgeOne Pages 的「Git 仓库自动连接」，推送即发布。
    """
    def run_git(args):
        env = dict(os.environ)
        env.setdefault("GIT_AUTHOR_NAME", "gh-radar")
        env.setdefault("GIT_AUTHOR_EMAIL", "gh-radar@users.noreply.github.com")
        env.setdefault("GIT_COMMITTER_NAME", env["GIT_AUTHOR_NAME"])
        env.setdefault("GIT_COMMITTER_EMAIL", env["GIT_AUTHOR_EMAIL"])
        return subprocess.run(["git"] + args, cwd=ROOT, env=env).returncode

    if subprocess.run(["git", "rev-parse", "--git-dir"], cwd=ROOT,
                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode != 0:
        print("[!] 当前目录不是 git 仓库，跳过推送")
        return 1

    run_git(["add", "-A", "data/", "dist/", "feed.xml"])
    staged = subprocess.run(["git", "diff", "--staged", "--quiet"], cwd=ROOT).returncode
    if staged == 0:
        print("[=] 没有变化，跳过提交")
        return 0

    stamp = __import__("time").strftime("%Y-%m-%d %H:%M UTC", __import__("time").gmtime())
    if run_git(["commit", "-m", "chore(auto): 发布榜单 %s" % stamp]) != 0:
        print("[x] git commit 失败")
        return 1
    if run_git(["push", "origin", "HEAD"]) != 0:
        print("[x] git push 失败（国内网络可能要挂代理：HTTPS_PROXY=http://127.0.0.1:10809）")
        return 1
    print("[+] 已推送，EdgeOne Pages 会自动发布")
    return 0


# ── 自包含单文件打包（给手机本地直接打开用）────────────────────
#
# 为什么需要：ES Modules 和 fetch 在 file:// 协议下会被 CORS 拦死，
# 所以本地版必须是「一个 HTML 里塞下所有东西」：
#   CSS 内联、JS 合并成普通 script、数据内联成 JS 变量、零外部依赖。

JS_BUNDLE_ORDER = [
    "config.js", "api.js", "store.js", "filters.js",
    "markdown.js", "cards.js", "obsidian.js", "shelf.js",
    "feedback.js", "pwa.js", "app.js",
]


def _strip_module_syntax(code):
    """
    把 ES Module 语法去掉，好让它能当普通 <script> 跑。

    ⚠️ import 可能是【跨行】的，例如：
        import {
          a, b,
        } from './x.js';
    所以必须用能跨行的正则，不能逐行判断（这里踩过坑）。
    """
    # 1) import ... from '...';
    code = re.sub(r"^[ \t]*import\s+[\s\S]*?from\s+['\"][^'\"]+['\"]\s*;[ \t]*$",
                  "", code, flags=re.M)
    # 2) import '...';（无绑定）
    code = re.sub(r"^[ \t]*import\s+['\"][^'\"]+['\"]\s*;[ \t]*$",
                  "", code, flags=re.M)
    # 3) export { a, b };
    code = re.sub(r"^[ \t]*export\s*\{[^}]*\}\s*;?[ \t]*$", "", code, flags=re.M)
    # 4) export function / export const / export class ...
    code = re.sub(r"^([ \t]*)export\s+", r"\1", code, flags=re.M)
    return code


def _safe_for_script(text):
    """防止内容里出现 </script> 把标签提前闭合。"""
    return text.replace("</script", "<\\/script").replace("<!--", "<\\!--")


def build_standalone():
    """产出 dist/gh-radar-本地版.html —— 断网、零依赖、手机可直接打开"""
    html_path = os.path.join(WEB_DIR, "index.html")
    css_path = os.path.join(WEB_DIR, "style.css")
    data_path = os.path.join(DATA_DIR, "latest.json")
    for p in (html_path, css_path, data_path):
        if not os.path.exists(p):
            print("[x] 缺少 %s" % p)
            return 1

    html = open(html_path, encoding="utf-8").read()
    css = open(css_path, encoding="utf-8").read()

    parts = []
    for name in JS_BUNDLE_ORDER:
        p = os.path.join(WEB_DIR, "js", name)
        if not os.path.exists(p):
            print("[x] 缺少前端模块 %s" % p)
            return 1
        parts.append("/* ===================== %s ===================== */\n%s"
                     % (name, _strip_module_syntax(open(p, encoding="utf-8").read())))
    bundle = "(function(){\n\"use strict\";\n%s\n})();" % "\n\n".join(parts)

    data = open(data_path, encoding="utf-8").read()

    # 1) CSS 内联
    if '<link rel="stylesheet" href="./style.css">' not in html:
        print("[!] 没找到 style.css 的外链标签，按通用方式替换")
        html = re.sub(r'<link[^>]+href="\./style\.css"[^>]*>', "<style>\n%s\n</style>" % css, html)
    else:
        html = html.replace('<link rel="stylesheet" href="./style.css">',
                            "<style>\n%s\n</style>" % css)

    # 2) 数据内联 + 3) JS 内联成普通 script（绝不带 type="module"）
    inject = (
        "<script>\n"
        "// 离线单文件版：数据已内联，并把网络请求彻底禁掉，\n"
        "// 保证在 file:// 协议下零外部依赖、不会被 CORS 拦。\n"
        "window.__DATA__ = %s;\n"
        "window.fetch = function () {\n"
        "  return Promise.reject(new Error('这是离线单文件版，不联网'));\n"
        "};\n"
        "try { Object.freeze(window.__DATA__); } catch (e) {}\n"
        "</script>\n<script>\n%s\n</script>"
        % (_safe_for_script(data), _safe_for_script(bundle))
    )
    if '<script type="module" src="./js/app.js"></script>' not in html:
        print("[!] 没找到 module 脚本标签，按通用方式替换")
        html = re.sub(r'<script[^>]*src="\./js/app\.js"[^>]*></script>', inject, html)
    else:
        html = html.replace('<script type="module" src="./js/app.js"></script>', inject)

    # 4) 去掉 RSS 外链（本地打开无意义，且避免任何外部请求）
    html = re.sub(r'<link rel="alternate"[^>]*>', "", html)

    os.makedirs(DIST_DIR, exist_ok=True)
    targets = [
        os.path.join(DIST_DIR, "gh-radar-本地版.html"),
        os.path.join(DIST_DIR, "gh-radar-offline.html"),   # 同内容，英文名方便传输
    ]
    for t in targets:
        with open(t, "w", encoding="utf-8") as f:
            f.write(html)

    size_kb = len(html.encode("utf-8")) / 1024.0
    print("[+] 自包含单文件已生成（%.0f KB）：" % size_kb)
    for t in targets:
        print("    %s" % t)

    # 自检：确认没有残留的外部引用
    leftovers = []
    for pat, label in ((r'<script[^>]+src=', "外链 script"),
                       (r'<link[^>]+stylesheet', "外链 CSS"),
                       (r'<link[^>]+rel="alternate"', "RSS 外链"),
                       (r'type="module"', "ES Module"),
                       (r'@import\s+url\(', "CSS @import"),
                       # 只查「真的被引用」的资源，不查正文里提到的网址
                       (r'(?:src|href)="https?://[^"]+\.(?:js|css|woff2?)"',
                        "外部 js/css/字体资源")):
        if re.search(pat, html):
            leftovers.append(label)
    if not re.search(r'window\.fetch\s*=', html):
        leftovers.append("未禁用 fetch")
    if not re.search(r'window\.__DATA__\s*=', html):
        leftovers.append("数据未内联")
    if leftovers:
        print("[!] 自检警告：%s" % "、".join(leftovers))
    else:
        print("[i] 自检通过：无外链脚本/CSS/字体 · 无 ES Module · 数据已内联 · fetch 已禁用")
    return 0


def deploy_tcb(env_id):
    """
    部署到腾讯云 CloudBase 静态托管。
    需要本机已装 CloudBase CLI 并登录过：npm i -g @cloudbase/cli && tcb login
    """
    cli = shutil.which("tcb") or shutil.which("cloudbase")
    if not cli:
        print("[!] 没找到 tcb 命令。先安装：npm install -g @cloudbase/cli")
        return 2

    cmd = [cli, "hosting", "deploy", DIST_DIR, "-e", env_id]
    print("[i] 执行：%s" % " ".join(cmd))
    r = subprocess.run(cmd, cwd=ROOT)
    if r.returncode == 0:
        print("[+] CloudBase 部署完成")
    else:
        print("[x] CloudBase 部署失败，退出码 %d" % r.returncode)
    return r.returncode


def main():
    ap = argparse.ArgumentParser(description="打包（并可选部署）静态站点")
    ap.add_argument("--push", action="store_true",
                    help="打包后把 dist/ 提交并推送（EdgeOne Git 集成即自动发布）")
    ap.add_argument("--standalone", action="store_true",
                    help="额外产出 dist/gh-radar-本地版.html（自包含单文件，手机可离线打开）")
    ap.add_argument("--tcb", metavar="ENV_ID",
                    help="打包后部署到 CloudBase 静态托管，参数是环境 ID")
    ap.add_argument("--deploy", action="store_true",
                    help="打包后用 edgeone CLI 直接部署（需先装 CLI）")
    ap.add_argument("--site-name", help="EdgeOne Pages 站点名（用 --deploy 时必填）")
    ap.add_argument("--token", help="EdgeOne API Token（也可用环境变量 EDGEONE_API_TOKEN）")
    args = ap.parse_args()

    code = assemble()
    if code != 0:
        return code

    if args.standalone:
        code = build_standalone()
        if code != 0:
            return code

    if args.tcb:
        return deploy_tcb(args.tcb)

    if args.deploy:
        if not args.site_name:
            print("[x] --deploy 必须指定 --site-name（站点名一旦创建不可修改）")
            return 2
        return deploy_edgeone(args.site_name, args.token)

    if args.push:
        return git_publish()

    return 0


if __name__ == "__main__":
    sys.exit(main())
