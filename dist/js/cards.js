// 卡片渲染
import { CATEGORY_LABEL, BURST_BAR_MAX, mirrorUrl } from './config.js';

export function esc(s) {
  return String(s ?? '').replace(/[&<>"']/g, (c) => (
    { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]
  ));
}

function fmtNum(n) {
  if (n == null || n === '') return null;
  return Number(n).toLocaleString('en-US');
}

/** 「9月17日首次发现 / 持续 2 期」 */
export function freshnessText(item) {
  const parts = [];
  if (item.first_seen) {
    const [, m, d] = item.first_seen.split('-');
    parts.push(`${Number(m)}月${Number(d)}日首次发现`);
  }
  const p = item.periods_on_board;
  if (p != null) parts.push(p <= 1 ? '本期新上榜' : `持续 ${p} 期`);
  return parts.join(' / ');
}

function el(tag, cls, html) {
  const e = document.createElement(tag);
  if (cls) e.className = cls;
  if (html != null) e.innerHTML = html;
  return e;
}

/**
 * 创建一张卡片。
 * callbacks: { onStar, onRead, onFeedback, onNote, onOpen }
 */
export function createCard(item, st, cb) {
  const card = el('div', 'card');
  card.dataset.id = item.id;
  if (st.read) card.classList.add('is-read');
  const cat = item.category || '';
  if (cat) card.classList.add('cat-' + cat);

  const starsToday = item.stars_today;
  const hasToday = starsToday != null;
  const burst = item.burst_score;

  /* ── 头部 ── */
  const head = el('div', 'chead');
  const title = el('div', 'ctitle');
  title.appendChild(el('div', 'crepo', esc(item.full_name || item.id)));

  const summary = item.title_cn
    ? el('div', 'csum', esc(item.title_cn))
    : el('div', 'csum pending', '简介待生成');
  title.appendChild(summary);
  head.appendChild(title);
  card.appendChild(head);

  /* ── 徽标 ── */
  const badges = el('div', 'cbadges');
  if (cat) badges.appendChild(el('span', `tag cat cat-${cat}`, esc(CATEGORY_LABEL[cat] || cat)));
  if (item.language) badges.appendChild(el('span', 'tag', esc(item.language)));
  if (item.periods_on_board <= 1 && item.first_seen) badges.appendChild(el('span', 'tag new', '新上榜'));
  const ftext = freshnessText(item);
  if (ftext) badges.appendChild(el('span', 'tag', esc(ftext)));
  (item.matched_groups || []).forEach((g) => badges.appendChild(el('span', 'tag', esc(g))));
  if (item.weak) badges.appendChild(el('span', 'tag warn', '降权'));
  card.appendChild(badges);

  /* ── 指标 ── */
  const metrics = el('div', 'metrics');
  const mk = (label, value, cls) => el('span', 'metric' + (cls ? ' ' + cls : ''),
    `${label} <b>${value}</b>`);
  metrics.appendChild(mk('总星', fmtNum(item.total_stars) ?? '—'));
  metrics.appendChild(hasToday
    ? mk('今日新增', '+' + fmtNum(starsToday), 'hot')
    : (() => {
        const m = mk('今日新增', '—');
        m.classList.add('null');
        m.title = '该数据来自搜索池，没有「今日新增」字段（合法状态）';
        return m;
      })());
  if (item.forks != null) metrics.appendChild(mk('Fork', fmtNum(item.forks)));
  card.appendChild(metrics);

  /* ── 爆发指数进度条 ── */
  if (burst != null) {
    const bar = el('div', 'burstbar');
    const pct = Math.max(2, Math.min(100, (burst / BURST_BAR_MAX) * 100));
    bar.appendChild(el('div', 'track', `<div class="fill" style="width:${pct.toFixed(1)}%"></div>`));
    bar.appendChild(el('span', 'val', `爆发 ${burst}`));
    card.appendChild(bar);
  }

  /* ── 推荐理由 ── */
  card.appendChild(item.reason_cn
    ? el('div', 'reason', esc(item.reason_cn))
    : el('div', 'reason pending', '推荐理由待生成'));

  /* ── 操作区 ── */
  const actions = el('div', 'cactions');

  const starBtn = el('button', 'act' + (st.starred ? ' on' : ''),
    (st.starred ? '★' : '☆') + ' 收藏');
  starBtn.title = '收藏（会连同完整信息一起存进书架）';
  starBtn.addEventListener('click', () => cb.onStar(item, starBtn));

  const readBtn = el('button', 'act read' + (st.read ? ' on' : ''), st.read ? '✓ 已读' : '标记已读');
  readBtn.addEventListener('click', () => cb.onRead(item, readBtn));

  const upBtn = el('button', 'act up' + (st.feedback === 1 ? ' on' : ''), '👍 有用');
  upBtn.title = '这条对我有用';
  upBtn.addEventListener('click', () => cb.onFeedback(item, 1, [upBtn, downBtn]));

  const downBtn = el('button', 'act down' + (st.feedback === -1 ? ' on' : ''), '👎 没兴趣');
  downBtn.title = '这条对我没用';
  downBtn.addEventListener('click', () => cb.onFeedback(item, -1, [upBtn, downBtn]));

  const link = el('a', 'act primarylink', '原链接 ↗');
  link.href = item.url || '#';
  link.target = '_blank';
  link.rel = 'noopener noreferrer';

  const mirror = el('a', 'act mirror', '国内加速 ↗');
  mirror.href = mirrorUrl(item.owner || '', item.name || '');
  mirror.target = '_blank';
  mirror.rel = 'noopener noreferrer';
  mirror.title = 'bgithub.xyz 镜像，国内访问更快';

  const expandBtn = el('button', 'act expand', '详情 ▾');

  [starBtn, readBtn, upBtn, downBtn, link, mirror, expandBtn].forEach((b) => actions.appendChild(b));
  card.appendChild(actions);

  /* ── 详情（默认折叠） ── */
  const detail = el('div', 'cdetail');
  detail.hidden = true;
  const topics = (item.topics || []).length ? (item.topics || []).join(', ') : '—';
  detail.innerHTML = `
    <dl>
      <dt>原始描述</dt><dd class="desc">${esc(item.description) || '（无）'}</dd>
      <dt>Topics</dt><dd>${esc(topics)}</dd>
      <dt>仓库 ID</dt><dd>${esc(item.id)}</dd>
      <dt>数据来源</dt><dd>${esc(sourceLabel(item))}</dd>
      <dt>评分</dt><dd>${esc(scoreText(item))}</dd>
    </dl>`;
  const notebox = el('div', 'notebox');
  notebox.innerHTML = `<label>我的备注（自动保存）</label>`;
  const ta = document.createElement('textarea');
  ta.value = st.note || '';
  ta.placeholder = '记点什么，比如「这个周末试试」';
  let timer = null;
  ta.addEventListener('input', () => {
    clearTimeout(timer);
    timer = setTimeout(() => cb.onNote(item, ta.value), 500);
  });
  notebox.appendChild(ta);
  detail.appendChild(notebox);
  card.appendChild(detail);

  function toggleDetail() {
    detail.hidden = !detail.hidden;
    card.classList.toggle('is-open', !detail.hidden);
    expandBtn.textContent = detail.hidden ? '详情 ▾' : '收起 ▴';
  }
  expandBtn.addEventListener('click', toggleDetail);
  card.addEventListener('click', (e) => {
    if (e.target.closest('a, button, textarea, input')) return;
    toggleDetail();
  });

  return card;
}

function sourceLabel(item) {
  if (item.src === 'trending') return 'GitHub Trending（含今日新增）';
  if (item.src === 'search') return 'GitHub 搜索池（无今日新增，属正常）';
  return item.src || '—';
}

function scoreText(item) {
  const bits = [];
  if (item.burst_score != null) bits.push(`爆发指数 ${item.burst_score}`);
  if (item.relevance_score != null) bits.push(`相关度 ${item.relevance_score}`);
  if (item.hit_strength != null) bits.push(`命中强度 ${item.hit_strength}`);
  return bits.join('　') || '—';
}
