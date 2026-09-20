/* 每日 GitHub 雷达 · Service Worker
 *
 * 目标：断网也能看上一期。
 *   - 应用外壳（HTML/CSS/JS/图标）：缓存优先，装一次就一直可用
 *   - 数据（data/latest.json）：网络优先，拉不到就回退到上次缓存的那一版
 *   - 推送：收到 push 事件就弹通知
 */

const VERSION = 'v3';
const SHELL_CACHE = `ghradar-shell-${VERSION}`;
const DATA_CACHE = `ghradar-data-${VERSION}`;

const SHELL_ASSETS = [
  './',
  './index.html',
  './style.css',
  './manifest.json',
  './js/app.js',
  './js/config.js',
  './js/api.js',
  './js/store.js',
  './js/filters.js',
  './js/cards.js',
  './js/markdown.js',
  './js/shelf.js',
  './js/obsidian.js',
  './js/feedback.js',
  './js/pwa.js',
];

self.addEventListener('install', (e) => {
  e.waitUntil((async () => {
    const c = await caches.open(SHELL_CACHE);
    // 单个资源失败不能让整次安装失败
    await Promise.allSettled(SHELL_ASSETS.map((u) => c.add(new Request(u, { cache: 'reload' }))));
    self.skipWaiting();
  })());
});

self.addEventListener('activate', (e) => {
  e.waitUntil((async () => {
    const keep = [SHELL_CACHE, DATA_CACHE];
    const names = await caches.keys();
    await Promise.all(names.filter((n) => !keep.includes(n)).map((n) => caches.delete(n)));
    await self.clients.claim();
  })());
});

self.addEventListener('fetch', (e) => {
  const req = e.request;
  if (req.method !== 'GET') return;

  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return;   // 跨域一律不管

  // 数据：网络优先，失败回退缓存
  if (url.pathname.includes('/data/')) {
    e.respondWith((async () => {
      try {
        const fresh = await fetch(req);
        if (fresh && fresh.ok) {
          const c = await caches.open(DATA_CACHE);
          c.put(req, fresh.clone());
        }
        return fresh;
      } catch {
        const cached = await caches.match(req);
        if (cached) return cached;
        return new Response('{"items":[],"offline":true}', {
          headers: { 'Content-Type': 'application/json' },
        });
      }
    })());
    return;
  }

  // 导航请求：网络优先，失败回退到缓存首页（断网也能打开）
  if (req.mode === 'navigate') {
    e.respondWith((async () => {
      try {
        return await fetch(req);
      } catch {
        return (await caches.match('./index.html')) || Response.error();
      }
    })());
    return;
  }

  // 其它静态资源：缓存优先
  e.respondWith((async () => {
    const cached = await caches.match(req);
    if (cached) return cached;
    try {
      const fresh = await fetch(req);
      if (fresh && fresh.ok) {
        const c = await caches.open(SHELL_CACHE);
        c.put(req, fresh.clone());
      }
      return fresh;
    } catch {
      return new Response('', { status: 504 });
    }
  })());
});

/* ─────────── Web Push ─────────── */

self.addEventListener('push', (e) => {
  let d = {};
  try { d = e.data ? e.data.json() : {}; } catch { d = { body: e.data ? e.data.text() : '' }; }
  const title = d.title || 'GitHub 雷达 · 新一期已发布';
  const body = d.body || '点开看看这一期有什么';
  e.waitUntil(self.registration.showNotification(title, {
    body,
    icon: './icon-192.png',
    badge: './icon-192.png',
    data: { url: d.url || './' },
    tag: 'ghradar-issue',
  }));
});

self.addEventListener('notificationclick', (e) => {
  e.notification.close();
  const target = (e.notification.data && e.notification.data.url) || './';
  e.waitUntil((async () => {
    const all = await self.clients.matchAll({ type: 'window', includeUncontrolled: true });
    for (const c of all) {
      if ('focus' in c) { c.navigate(target); return c.focus(); }
    }
    return self.clients.openWindow(target);
  })());
});
