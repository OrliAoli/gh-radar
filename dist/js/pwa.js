// PWA：Service Worker 注册 + Web Push 订阅
//
// 推送能不能用取决于两端：
//   浏览器侧：需要 HTTPS（已有）+ iOS 16.4 且「已添加到主屏幕」
//   服务端侧：需要一对 VAPID 密钥，公钥写在 ./data/push.json 里
// 密钥没配时，按钮会明确显示「推送未配置」，而不是假装能用。

import { VAPID_PUBLIC_KEY } from './config.js';

const PUSH_CFG_URL = './data/push.json';

/* ─────────── Service Worker ─────────── */

export function registerSW() {
  if (!('serviceWorker' in navigator)) return;
  // file:// 下 SW 不可用（离线单文件版就是这种情况），静默跳过
  if (location.protocol !== 'https:' && location.hostname !== 'localhost'
      && location.hostname !== '127.0.0.1') return;
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('./sw.js').catch((e) => {
      console.warn('Service Worker 注册失败：', e.message);
    });
  });
}

/* ─────────── Web Push ─────────── */

function urlBase64ToUint8Array(base64) {
  const pad = '='.repeat((4 - (base64.length % 4)) % 4);
  const s = (base64 + pad).replace(/-/g, '+').replace(/_/g, '/');
  const raw = atob(s);
  const out = new Uint8Array(raw.length);
  for (let i = 0; i < raw.length; i += 1) out[i] = raw.charCodeAt(i);
  return out;
}

async function loadVapidKey() {
  if (VAPID_PUBLIC_KEY) return VAPID_PUBLIC_KEY;
  try {
    const r = await fetch(PUSH_CFG_URL, { cache: 'no-store' });
    if (!r.ok) return '';
    const j = await r.json();
    return j.publicKey || '';
  } catch { return ''; }
}

/** 判断当前环境能不能订阅推送，返回 { ok, reason } */
function pushSupport() {
  if (!('serviceWorker' in navigator) || !('PushManager' in window)) {
    const iOS = /iPad|iPhone|iPod/.test(navigator.userAgent);
    const standalone = window.navigator.standalone === true
      || window.matchMedia('(display-mode: standalone)').matches;
    if (iOS && !standalone) {
      return { ok: false, reason: 'iPhone 需先「添加到主屏幕」再从主屏幕打开' };
    }
    return { ok: false, reason: '这个浏览器不支持推送' };
  }
  return { ok: true, reason: '' };
}

async function currentSubscription() {
  try {
    const reg = await navigator.serviceWorker.ready;
    return await reg.pushManager.getSubscription();
  } catch { return null; }
}

/**
 * 绑定「开启推送」按钮。
 * @param {HTMLButtonElement} btn
 * @param {HTMLElement} label
 */
export async function setupPushButton(btn, label) {
  if (!btn || !label) return;

  const sup = pushSupport();
  const key = await loadVapidKey();

  if (!sup.ok) {
    btn.disabled = true;
    label.textContent = sup.reason;
    return;
  }
  if (!key) {
    btn.disabled = true;
    label.textContent = '推送未配置（缺 VAPID 密钥）';
    btn.title = '仓库里还没有配置推送密钥，见 README 的「开启推送」一节';
    return;
  }

  const sub = await currentSubscription();
  if (sub) {
    btn.disabled = true;
    label.textContent = '✅ 已开启';
    btn.textContent = '🔕 关闭推送';
    btn.disabled = false;
    btn.dataset.on = '1';
  } else {
    label.textContent = '未开启';
  }

  btn.addEventListener('click', async () => {
    if (btn.dataset.on === '1') {
      const s = await currentSubscription();
      if (s) await s.unsubscribe();
      btn.dataset.on = '';
      btn.textContent = '🔔 开启新一期推送';
      label.textContent = '已关闭';
      return;
    }

    const perm = await Notification.requestPermission();
    if (perm !== 'granted') {
      label.textContent = '你拒绝了通知权限，可在浏览器设置里改';
      return;
    }
    try {
      const reg = await navigator.serviceWorker.ready;
      const s = await reg.pushManager.subscribe({
        userVisibleOnly: true,
        applicationServerKey: urlBase64ToUint8Array(key),
      });
      // 把订阅回传：同样走「预填 Issue」，由 Actions 存进 data/push-subscriptions.json
      const payload = btoa(unescape(encodeURIComponent(JSON.stringify(s))));
      const body = [
        '<!-- radar-push-subscribe -->', '',
        '把下面这段贴进去提交即可，Actions 会存进 `data/push-subscriptions.json`。', '',
        '```text', payload, '```',
      ].join('\n');
      const q = new URLSearchParams({
        title: '[订阅] 新一期推送', body, labels: 'radar-push',
      });
      window.open(`https://github.com/OrliAoli/gh-radar/issues/new?${q.toString()}`,
        '_blank', 'noopener');

      btn.dataset.on = '1';
      btn.textContent = '🔕 关闭推送';
      label.textContent = '已订阅，还需在 GitHub 提交一次以绑定到服务器';
    } catch (e) {
      label.textContent = '订阅失败：' + e.message;
    }
  });
}
