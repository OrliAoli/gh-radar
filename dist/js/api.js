// 数据加载：只读同源静态 JSON，失败时按日期回溯找最近一份可用数据
import { DATA_URL } from './config.js';

let cache = null;

function shiftDate(iso, days) {
  const d = new Date(iso + 'T00:00:00Z');
  d.setUTCDate(d.getUTCDate() - days);
  return d.toISOString().slice(0, 10);
}

async function fetchJson(url) {
  const res = await fetch(url, { cache: 'no-cache' });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}

/**
 * 取数据。正常情况下读 data/latest.json；
 * 失败则依次尝试前几天的每日快照，最后返回 null。
 */
export async function loadData(force = false) {
  if (cache && !force) return cache;
  const tried = [];

  // 自包含单文件版：数据已经内联在 window.__DATA__ 里，不发任何网络请求
  if (!force && typeof window !== 'undefined' && window.__DATA__
      && Array.isArray(window.__DATA__.items)) {
    cache = { data: window.__DATA__, degradedFrom: null, errors: [], offline: true };
    return cache;
  }

  try {
    const data = await fetchJson(DATA_URL + (force ? `?t=${Date.now()}` : ''));
    if (data && Array.isArray(data.items)) {
      cache = { data, degradedFrom: null, errors: [] };
      return cache;
    }
    tried.push(`${DATA_URL} 返回格式不正确`);
  } catch (e) {
    tried.push(`${DATA_URL} 读取失败：${e.message}`);
  }

  // 降级：往前找最近 6 天的快照
  const today = new Date().toISOString().slice(0, 10);
  for (let i = 1; i <= 6; i++) {
    const d = shiftDate(today, i);
    const url = `./data/daily/${d}.json`;
    try {
      const snap = await fetchJson(url);
      const items = normalizeSnapshot(snap);
      if (items.length) {
        const data = {
          date: snap.date || d,
          updated_at: snap.updated_at,
          source: snap.source || 'fallback',
          warnings: snap.warnings || [],
          stats: snap.stats || {},
          items,
          _degraded: true,
        };
        cache = { data, degradedFrom: d, errors: tried };
        return cache;
      }
    } catch (e) {
      tried.push(`${url} 读取失败：${e.message}`);
    }
  }

  cache = { data: null, degradedFrom: null, errors: tried };
  return cache;
}

/**
 * 快照是原始抓取格式（categories / search_pool 分桶），
 * 这里把它拍平成一个 items 数组，字段尽量对齐 latest.json。
 */
function normalizeSnapshot(snap) {
  const seen = new Map();
  const push = (r) => {
    if (!r || !r.id) return;
    const cur = seen.get(r.id);
    if (!cur) {
      seen.set(r.id, {
        ...r,
        stars_today: r.stars_today ?? null,
        burst_score: null,
        title_cn: null,
        reason_cn: null,
        category: null,
      });
      return;
    }
    const a = cur.stars_today, b = r.stars_today ?? null;
    if (a == null || (b != null && b > a)) cur.stars_today = b;
  };
  Object.values(snap.categories || {}).forEach((arr) => (arr || []).forEach(push));
  Object.values(snap.search_pool || {}).forEach((arr) => (arr || []).forEach(push));
  return [...seen.values()];
}
