// 筛选与排序（纯函数，不碰 DOM）
import { DEFAULT_FILTERS } from './config.js';

export const defaultFilters = () => ({ ...DEFAULT_FILTERS });

function daysBetween(isoA, isoB) {
  if (!isoA || !isoB) return null;
  const a = Date.parse(isoA + 'T00:00:00Z');
  const b = Date.parse(isoB + 'T00:00:00Z');
  if (Number.isNaN(a) || Number.isNaN(b)) return null;
  return Math.round((b - a) / 86400000);
}

function haystack(item) {
  return [
    item.full_name, item.owner, item.name, item.description,
    (item.topics || []).join(' '), (item.matched_groups || []).join(' '),
    item.language, item.title_cn, item.reason_cn,
  ].filter(Boolean).join(' ').toLowerCase();
}

// 排序用的分数。stars_today 为 null 是合法状态，排序时按 -1 处理而不是当 0 丢掉
function sortValue(item, key) {
  switch (key) {
    case 'burst': return item.burst_score ?? -1;
    case 'today': return item.stars_today ?? -1;
    case 'stars': return item.total_stars ?? -1;
    case 'score':
    default:      return (item.burst_score ?? (item.rank_score != null ? item.rank_score * 100 : 0));
  }
}

export function applyFilters(items, f, ctx) {
  const { dataDate, starredSet, readSet } = ctx;
  const q = (f.q || '').trim().toLowerCase();

  const out = items.filter((item) => {
    if (f.cat && f.cat !== 'all') {
      if ((item.category || '') !== f.cat) return false;
    }
    if (f.lang && (item.language || '') !== f.lang) return false;

    if (f.time && f.time !== 'all' && dataDate) {
      const d = daysBetween(item.first_seen, dataDate);
      if (d == null) return true;                 // 拿不到首次发现日期就不按时间过滤
      const limit = f.time === 'today' ? 0 : f.time === 'week' ? 7 : 30;
      if (d > limit) return false;
    }

    if (q && !haystack(item).includes(q)) return false;

    if (f.unreadOnly && readSet.has(item.id)) return false;
    if (f.starredOnly && !starredSet.has(item.id)) return false;
    return true;
  });

  const dir = f.sort === 'stars' || f.sort === 'today' || f.sort === 'burst'
    ? (f.sortDir === 'asc' ? 1 : -1)
    : -1;

  out.sort((a, b) => {
    const va = sortValue(a, f.sort), vb = sortValue(b, f.sort);
    if (va !== vb) return (va - vb) * dir;
    // 同分时：有今日增量的排前面，再按总星
    const ha = a.stars_today ?? -1, hb = b.stars_today ?? -1;
    if (ha !== hb) return hb - ha;
    return (b.total_stars ?? -1) - (a.total_stars ?? -1);
  });

  return out;
}

export function collectLanguages(items) {
  const s = new Set();
  items.forEach((i) => { if (i.language) s.add(i.language); });
  return [...s].sort((a, b) => a.localeCompare(b));
}

/** 「本期必看」：综合评分最高的 5 条 */
export function pickMustSee(items, n = 5) {
  return [...items]
    .sort((a, b) => {
      const sa = a.burst_score ?? (a.rank_score != null ? a.rank_score * 100 : 0);
      const sb = b.burst_score ?? (b.rank_score != null ? b.rank_score * 100 : 0);
      if (sb !== sa) return sb - sa;
      return (b.total_stars ?? 0) - (a.total_stars ?? 0);
    })
    .slice(0, n);
}
