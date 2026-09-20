// 卡片渲染 —— 手机优先的「紧凑模式 + 点击展开」
//
// 紧凑模式（默认，手机上只显示这三行，一屏能放 3-4 条）：
//   ① 仓库名（一行，超出省略）              ⭐
//   ② 中文一句话（最多 2 行，超出省略）
//   ③ 语言 · ★总星 · +今日新增（醒目色）· N 期   [标签1][标签2][+N]
//
// 展开模式（点卡片后）才显示：推荐理由 / 深度摘要 / 展开全文 / 操作按钮行 / 备注输入框。
// 桌面端（≥721px）由 CSS 让展开部分常显，保持原来宽松的样子。

import { CATEGORY_LABEL, BURST_BAR_MAX, mirrorUrl } from './config.js';
import { renderMarkdown } from './markdown.js';

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

/** 手机上才需要「点击展开」；桌面端展开部分常显 */
function isCompact() {
  return window.matchMedia('(max-width: 720px)').matches;
}

/**
 * 创建一张卡片。
 * callbacks: { onStar, onRead, onFeedback, onNote }
 */
export function createCard(item, st, cb) {
  const card = el('div', 'card');
  card.dataset.id = item.id;
  if (st.read) card.classList.add('is-read');
  const cat = item.category || '';
  if (cat) card.classList.add('cat-' + cat);

  const hasToday = item.stars_today != null;
  const burst = item.burst_score;

  /* ─────────── ① 仓库名 + ⭐ ─────────── */
  const row1 = el('div', 'crow1');
  row1.appendChild(el('div', 'crepo', esc(item.full_name || item.id)));

  const starBtn = el('button', 'starbtn' + (st.starred ? ' on' : ''), st.starred ? '★' : '☆');
  starBtn.title = st.starred ? '取消收藏' : '收藏（连同完整信息存进书架）';
  starBtn.setAttribute('aria-label', starBtn.title);
  starBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    cb.onStar(item, starBtn);
  });
  row1.appendChild(starBtn);
  card.appendChild(row1);

  /* ─────────── ② 中文一句话（最多 2 行）─────────── */
  card.appendChild(item.title_cn
    ? el('div', 'csum', esc(item.title_cn))
    : el('div', 'csum pending', '简介待生成'));

  /* ─────────── ③ 元信息一行 + 标签 ─────────── */
  const row3 = el('div', 'crow3');
  const metaBits = [];
  if (item.language) metaBits.push(esc(item.language));
  metaBits.push('★' + (fmtNum(item.total_stars) ?? '—'));
  if (hasToday) {
    metaBits.push(`<span class="hot">+${fmtNum(item.stars_today)} 今日</span>`);
  }
  const p = item.periods_on_board;
  if (p != null) metaBits.push(p <= 1 ? '新上榜' : `${p} 期`);
  const cmeta = el('div', 'cmeta', metaBits.join('<span class="sep">·</span>'));
  if (!hasToday) {
    cmeta.title = '该条来自搜索池，没有「今日新增」字段（合法状态）';
  }
  row3.appendChild(cmeta);

  // 标签：最多 2 个，其余折叠成 +N
  const allTags = [];
  if (cat) allTags.push([CATEGORY_LABEL[cat] || cat, `cat cat-${cat}`]);
  if (item.weak) allTags.push(['降权', 'warn']);
  if (item.periods_on_board <= 1 && item.first_seen) allTags.push(['新上榜', 'new']);
  (item.matched_groups || []).forEach((g) => allTags.push([g, '']));

  const ctags = el('div', 'ctags');
  allTags.slice(0, 2).forEach(([text, cls]) => {
    ctags.appendChild(el('span', 'tag' + (cls ? ' ' + cls : ''), esc(text)));
  });
  if (allTags.length > 2) {
    const more = el('span', 'tag more', `+${allTags.length - 2}`);
    more.title = allTags.slice(2).map((t) => t[0]).join('、');
    ctags.appendChild(more);
  }
  row3.appendChild(ctags);
  card.appendChild(row3);

  /* ═══════════ 展开部分 ═══════════ */
  const body = el('div', 'cardbody');

  if (burst != null) {
    const bar = el('div', 'burstbar');
    const pct = Math.max(2, Math.min(100, (burst / BURST_BAR_MAX) * 100));
    bar.appendChild(el('div', 'track', `<div class="fill" style="width:${pct.toFixed(1)}%"></div>`));
    bar.appendChild(el('span', 'val', `爆发 ${burst}`));
    body.appendChild(bar);
  }

  body.appendChild(item.reason_cn
    ? el('div', 'reason', esc(item.reason_cn))
    : el('div', 'reason pending', '推荐理由待生成'));

  /* L2：深度摘要 */
  if (item.summary_cn) {
    const sumBox = el('div', 'summary');
    const sumBody = el('div', 'summary-body',
      item.summary_cn.split(/\n{2,}/).map((x) => `<p>${esc(x)}</p>`).join(''));
    sumBody.classList.add('clamped');
    sumBox.appendChild(el('div', 'summary-head', '深度摘要'));
    sumBox.appendChild(sumBody);
    const more = el('button', 'ghostlink', '展开摘要 ▾');
    more.addEventListener('click', (e) => {
      e.stopPropagation();
      sumBody.classList.toggle('clamped');
      more.textContent = sumBody.classList.contains('clamped') ? '展开摘要 ▾' : '收起摘要 ▴';
    });
    sumBox.appendChild(more);
    body.appendChild(sumBox);
  }

  /* L3：完整译文 */
  if (item.is_article) {
    const full = el('div', 'fulltext');
    const btn = el('button', 'fullbtn', '📖 展开全文');
    const area = el('div', 'fullarea');
    area.hidden = true;
    const bar = el('div', 'fullbar');
    const origBtn = el('button', 'act', '对照原文');
    let showingOriginal = false;
    const render = () => {
      if (showingOriginal) {
        area.innerHTML = item.readme_en
          ? renderMarkdown(item.readme_en)
          : '<p class="muted">英文原文未随本期数据打包。</p>';
      } else {
        area.innerHTML = item.readme_cn
          ? renderMarkdown(item.readme_cn)
          : '<p class="muted">全文译文待生成——需要在仓库里配置大模型 Key（LLM_API_KEY）。</p>';
      }
    };
    origBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      showingOriginal = !showingOriginal;
      origBtn.classList.toggle('on', showingOriginal);
      origBtn.textContent = showingOriginal ? '看中文译文' : '对照原文';
      render();
    });
    bar.appendChild(el('span', 'muted small',
      `原文 ${item.readme_words || '—'} 词　代码块 ${item.code_block_ratio != null ? Math.round(item.code_block_ratio * 100) + '%' : '—'}`));
    bar.appendChild(origBtn);
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      area.hidden = !area.hidden;
      btn.textContent = area.hidden ? '📖 展开全文' : '📖 收起全文';
      bar.hidden = area.hidden;
      if (!area.hidden && !area.dataset.rendered) {
        render();
        area.dataset.rendered = '1';
      }
    });
    bar.hidden = true;
    full.appendChild(btn);
    full.appendChild(bar);
    full.appendChild(area);
    body.appendChild(full);
  }

  /* 操作按钮行 */
  const actions = el('div', 'cactions');
  const starA = el('button', 'act star' + (st.starred ? ' on' : ''), (st.starred ? '★' : '☆') + ' 收藏');
  starA.addEventListener('click', (e) => { e.stopPropagation(); cb.onStar(item, starBtn); });

  const readBtn = el('button', 'act read' + (st.read ? ' on' : ''), st.read ? '✓ 已读' : '标记已读');
  readBtn.addEventListener('click', (e) => { e.stopPropagation(); cb.onRead(item, readBtn); });

  const upBtn = el('button', 'act up' + (st.feedback === 1 ? ' on' : ''), '👍 有用');
  upBtn.addEventListener('click', (e) => { e.stopPropagation(); cb.onFeedback(item, 1, [upBtn, downBtn]); });

  const downBtn = el('button', 'act down' + (st.feedback === -1 ? ' on' : ''), '👎 没兴趣');
  downBtn.addEventListener('click', (e) => { e.stopPropagation(); cb.onFeedback(item, -1, [upBtn, downBtn]); });

  const link = el('a', 'act primarylink', '原链接 ↗');
  link.href = item.url || '#';
  link.target = '_blank';
  link.rel = 'noopener noreferrer';
  link.addEventListener('click', (e) => e.stopPropagation());

  const mirror = el('a', 'act mirror', '国内加速 ↗');
  mirror.href = mirrorUrl(item.owner || '', item.name || '');
  mirror.target = '_blank';
  mirror.rel = 'noopener noreferrer';
  mirror.title = 'bgithub.xyz 镜像，国内访问更快';
  mirror.addEventListener('click', (e) => e.stopPropagation());

  const detailBtn = el('button', 'act', '详情 ▾');
  [starA, readBtn, upBtn, downBtn, link, mirror, detailBtn].forEach((b) => actions.appendChild(b));
  body.appendChild(actions);

  /* 元数据（默认折叠） */
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
  detailBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    detail.hidden = !detail.hidden;
    detailBtn.textContent = detail.hidden ? '详情 ▾' : '收起详情 ▴';
  });
  body.appendChild(detail);

  /* 备注 */
  const notebox = el('div', 'notebox');
  notebox.appendChild(el('label', null, '我的备注（自动保存）'));
  const ta = document.createElement('textarea');
  ta.value = st.note || '';
  ta.placeholder = '记点什么，比如「这个周末试试」';
  ta.addEventListener('click', (e) => e.stopPropagation());
  let timer = null;
  ta.addEventListener('input', () => {
    clearTimeout(timer);
    timer = setTimeout(() => cb.onNote(item, ta.value), 500);
  });
  notebox.appendChild(ta);
  body.appendChild(notebox);

  card.appendChild(body);

  /* ─────────── 点卡片展开 / 收起（仅手机）─────────── */
  card.addEventListener('click', (e) => {
    if (e.target.closest('a, button, textarea, input')) return;
    if (!isCompact()) return;          // 桌面端展开部分常显，不需要折叠
    card.classList.toggle('is-open');
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
