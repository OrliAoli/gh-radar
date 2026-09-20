#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Web Push —— 每期发布时给订阅者推一条通知。

⚠️ 这个脚本是**唯一**需要第三方依赖的（`pywebpush`）。
   原因：Web Push 要求 P-256 ECDH + HKDF + AES128GCM 加密，
   Python 标准库没有这些原语，硬写一遍容易写错、也没必要。
   其它脚本仍然只用标准库。

用法：

    # 1) 生成 VAPID 密钥对（只需做一次）
    python3 scripts/push.py --gen-keys

        会打印出公钥和私钥：
        - 公钥 → 写进 web/js/config.js 的 VAPID_PUBLIC_KEY，或 data/push.json
        - 私钥 → 存进仓库 Secrets: VAPID_PRIVATE_KEY（绝对不要提交进仓库）

    # 2) 发送本期通知
    python3 scripts/push.py --notify

        读 data/push-subscriptions.json 里的订阅列表，逐条推送。
        没配密钥、没订阅者、没装 pywebpush → 全部安静跳过，不报错。

环境变量：
    VAPID_PRIVATE_KEY   私钥（必填，否则跳过）
    VAPID_SUBJECT       联系邮箱，形如 mailto:you@example.com
"""

import argparse
import datetime
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SUBS_PATH = os.path.join(ROOT, "data", "push-subscriptions.json")
LATEST_PATH = os.path.join(ROOT, "data", "latest.json")
PUSH_CFG_PATH = os.path.join(ROOT, "data", "push.json")


def load_subs():
    if not os.path.exists(SUBS_PATH):
        return []
    try:
        with open(SUBS_PATH, "r", encoding="utf-8") as f:
            data = json.load(f) or []
        return [s for s in data if isinstance(s, dict) and s.get("endpoint")]
    except Exception as e:  # noqa: BLE001
        print("[!] 订阅表解析失败：%s" % e)
        return []


def save_subs(subs):
    with open(SUBS_PATH, "w", encoding="utf-8") as f:
        json.dump(subs, f, indent=2, ensure_ascii=False)


def gen_keys():
    try:
        from py_vapid import Vapid01  # pywebpush 的依赖
        from cryptography.hazmat.primitives import serialization
    except ImportError:
        print("[x] 需要先安装依赖：pip install pywebpush")
        return 1

    v = Vapid01()
    v.generate_keys()
    priv_pem = v.private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    ).decode()
    pub_raw = v.public_key.public_bytes(
        encoding=serialization.Encoding.X962,
        format=serialization.PublicFormat.UncompressedPoint,
    )
    import base64
    pub_b64 = base64.urlsafe_b64encode(pub_raw).decode().rstrip("=")

    os.makedirs(os.path.dirname(PUSH_CFG_PATH), exist_ok=True)
    with open(PUSH_CFG_PATH, "w", encoding="utf-8") as f:
        json.dump({"publicKey": pub_b64}, f, indent=2, ensure_ascii=False)

    print("=" * 66)
    print("VAPID 密钥已生成。")
    print()
    print("【公钥】—— 可以公开，已写入 data/push.json")
    print(pub_b64)
    print()
    print("【私钥】—— 绝对不要提交进仓库！存成 GitHub Secret：")
    print("  仓库 → Settings → Secrets and variables → Actions")
    print("  → New repository secret → 名字填 VAPID_PRIVATE_KEY")
    print("  值填下面这一整段（含 BEGIN/END 两行）：")
    print()
    print(priv_pem)
    print()
    print("再建一个 Secret：VAPID_SUBJECT = mailto:你的邮箱@example.com")
    print("=" * 66)
    return 0


def notify():
    priv = os.getenv("VAPID_PRIVATE_KEY", "").strip()
    if not priv:
        print("[=] 没有配置 VAPID_PRIVATE_KEY，跳过推送（这是正常的）")
        return 0

    subs = load_subs()
    if not subs:
        print("[=] 还没有订阅者，跳过推送")
        return 0

    try:
        from pywebpush import webpush, WebPushException
    except ImportError:
        print("[!] 没装 pywebpush，跳过推送。安装：pip install pywebpush")
        return 0

    # 通知内容：本期共几条、几条爆发
    total, burst = 0, 0
    if os.path.exists(LATEST_PATH):
        try:
            with open(LATEST_PATH, "r", encoding="utf-8") as f:
                d = json.load(f)
            items = d.get("items") or []
            total = len(items)
            burst = sum(1 for i in items if i.get("category") == "burst")
        except Exception:  # noqa: BLE001
            pass

    payload = json.dumps({
        "title": "GitHub 雷达 · 新一期已发布",
        "body": ("本期 %d 条" % total) + ("，其中 %d 条爆发" % burst if burst else ""),
        "url": "./",
    }, ensure_ascii=False)

    subject = os.getenv("VAPID_SUBJECT", "").strip() or "mailto:noreply@example.com"
    ok, gone = 0, []
    for sub in subs:
        try:
            webpush(
                subscription_info=sub,
                data=payload,
                vapid_private_key=priv,
                vapid_claims={"sub": subject},
            )
            ok += 1
        except WebPushException as e:
            code = getattr(getattr(e, "response", None), "status_code", None)
            if code in (404, 410):
                gone.append(sub)      # 订阅已失效，清掉
            else:
                print("[!] 推送失败（%s）：%s" % (code, e))
        except Exception as e:  # noqa: BLE001
            print("[!] 推送异常：%s" % e)

    if gone:
        keep = [s for s in subs if s not in gone]
        save_subs(keep)
        print("[i] 清理了 %d 个失效订阅" % len(gone))
    print("[+] 推送完成：成功 %d / 共 %d" % (ok, len(subs)))
    return 0


def main():
    ap = argparse.ArgumentParser(description="Web Push：生成密钥 / 发送本期通知")
    ap.add_argument("--gen-keys", action="store_true", help="生成一对 VAPID 密钥")
    ap.add_argument("--notify", action="store_true", help="给所有订阅者推送本期通知")
    ap.add_argument("--list", action="store_true", help="看看现在有多少订阅者")
    args = ap.parse_args()

    if args.gen_keys:
        return gen_keys()
    if args.list:
        subs = load_subs()
        print("[i] 当前订阅设备：%d 个" % len(subs))
        for s in subs:
            print("    %s…  （添加于 %s）"
                  % (str(s.get("endpoint"))[:52], s.get("added_at", "?")))
        return 0
    if args.notify:
        return notify()

    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
