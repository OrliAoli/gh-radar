// 反馈回流 —— 把手机上的 👍 / 👎 / 收藏 / 已读 送回仓库
//
// 为什么用 GitHub Issue 而不是直接 POST：
//   这是个纯静态站点，没有服务器，前端也拿不到任何写权限的令牌
//   （把令牌放进前端 = 谁都能改你的仓库）。
//   所以走「预填 Issue」这条路：用户点一下 → GitHub 打开一个已经填好内容的
//   新建 Issue 页面 → 用户点绿色提交 → Actions 收到后在仓库里追加一条记录。
//   全程零后端、零密钥、零成本。
//
// 回传格式：data/feedback.jsonl（每行一条 JSON）

import { STORAGE_KEYS } from './config.js';

const MARKER = '<!-- radar-feedback -->';

/** 读本地待回传队列 */
function readQueue() {
  try {
    return JSON.parse(localStorage.getItem(STORAGE_KEYS.events) || '[]') || [];
  } catch { return []; }
}

function writeQueue(list) {
  try {
    localStorage.setItem(STORAGE_KEYS.events, JSON.stringify(list.slice(-500)));
  } catch { /* 存不进去就只影响同步，不影响使用 */ }
}

/** 待同步条数（给设置面板显示） */
export function pendingCount() {
  return readQueue().length;
}

/**
 * 打包待回传的反馈。
 * 返回 null 表示没有新记录。
 */
export function collectPending() {
  const list = readQueue();
  if (!list.length) return null;
  // 只回传对「排序」有意义的动作，已读/取消读意义不大但保留成本极低，一并带上
  const payload = {
    v: 1,
    at: new Date().toISOString(),
    events: list.map((e) => ({
      a: e.action,
      r: e.id,
      l: e.lang || undefined,
      t: e.topics && e.topics.length ? e.topics : undefined,
      g: e.groups && e.groups.length ? e.groups : undefined,
      c: e.category || undefined,
      at: e.ts,
    })),
  };
  payload.__ids = list.map((e) => e.ts);   // 仅本地用，不会写进 Issue
  return payload;
}

/** 生成「新建 Issue」的跳转地址 */
export function buildIssueUrl(repo, payload) {
  const up = payload.events.filter((e) => e.a === 'up').length;
  const down = payload.events.filter((e) => e.a === 'down').length;
  const star = payload.events.filter((e) => e.a === 'star').length;

  const title = `[反馈] ${up}👍 ${down}👎 ${star}⭐`;
  const body = [
    MARKER,
    '',
    `共 ${payload.events.length} 条行为记录：👍 ${up} · 👎 ${down} · ⭐ ${star} · 其他 ${payload.events.length - up - down - star}`,
    '',
    '提交后 GitHub Actions 会自动把它追加到 `data/feedback.jsonl`，**下一期生成时按它调权**。',
    '',
    '```json',
    JSON.stringify(payload.events, null, 1),
    '```',
  ].join('\n');

  const q = new URLSearchParams({ title, body, labels: 'radar-feedback' });
  return `https://github.com/${repo}/issues/new?${q.toString()}`;
}

/** 提交后把队列清掉（这些记录已经进 Issue 了） */
export function markSynced(ids) {
  if (!Array.isArray(ids)) return;
  const rest = readQueue().filter((e) => !ids.includes(e.ts));
  writeQueue(rest);
}

export { MARKER };
