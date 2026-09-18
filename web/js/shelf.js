// 书架页：收藏条目管理（阅读状态 / 笔记 / 导出）
import { CATEGORY_LABEL, READ_STATE_LABEL, mirrorUrl } from './config.js';
import { esc } from './cards.js';

function el(tag, cls, html) {
  const e = document.createElement(tag);
  if (cls) e.className = cls;
  if (html != null) e.innerHTML = html;
  return e;
}

function fmtTime(iso) {
  if (!iso) return '';
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return '';
  const p = (n) => String(n).padStart(2, '0');
  return `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())} ${p(d.getHours())}:${p(d.getMinutes())}`;
}

/**
 * 渲染书架。
 * callbacks: { onReadState, onNote, onUnstar, onQuickSave, onFullExport }
 */
export function renderShelf(container, entries, cb) {
  container.innerHTML = '';
  if (!entries.length) return false;

  entries.forEach((it) => {
    const card = el('div', 'card');
    if (it.category) card.classList.add('cat-' + it.category);
    if (it.read_state === 'done') card.classList.add('is-read');

    const head = el('div', 'chead');
    const title = el('div', 'ctitle');
    title.appendChild(el('div', 'crepo', esc(it.full_name || it.id)));
    title.appendChild(it.title_cn
      ? el('div', 'csum', esc(it.title_cn))
      : el('div', 'csum pending', '简介待生成'));
    head.appendChild(title);
    card.appendChild(head);

    const badges = el('div', 'cbadges');
    const cat = it.category || '';
    if (cat) badges.appendChild(el('span', `tag cat cat-${cat}`, esc(CATEGORY_LABEL[cat] || cat)));
    if (it.language) badges.appendChild(el('span', 'tag', esc(it.language)));
    badges.appendChild(el('span', 'tag', `收藏于 ${esc(fmtTime(it.saved_at))}`));
    if (it.data_date) badges.appendChild(el('span', 'tag', `数据日期 ${esc(it.data_date)}`));
    if (it.total_stars != null) badges.appendChild(el('span', 'tag', `★ ${Number(it.total_stars).toLocaleString('en-US')}`));
    if (it.stars_today != null) badges.appendChild(el('span', 'tag', `今日 +${Number(it.stars_today).toLocaleString('en-US')}`));
    card.appendChild(badges);

    if (it.reason_cn) card.appendChild(el('div', 'reason', esc(it.reason_cn)));

    /* 操作区 */
    const actions = el('div', 'cactions');

    const sel = document.createElement('select');
    sel.className = 'readsel';
    Object.entries(READ_STATE_LABEL).forEach(([k, label]) => {
      const o = document.createElement('option');
      o.value = k; o.textContent = label;
      if (it.read_state === k) o.selected = true;
      sel.appendChild(o);
    });
    sel.addEventListener('change', () => cb.onReadState(it.id, sel.value, card));

    const obs = el('button', 'act primarylink', '📝 存入 Obsidian');
    obs.addEventListener('click', () => cb.onQuickSave(it));

    const dl = el('button', 'act mirror', '⬇ 下载 .md');
    dl.addEventListener('click', () => cb.onFullExport(it));

    const link = el('a', 'act', '原链接 ↗');
    link.href = it.url; link.target = '_blank'; link.rel = 'noopener noreferrer';

    const mir = el('a', 'act', '加速 ↗');
    mir.href = mirrorUrl(it.owner || (it.full_name || '').split('/')[0], it.name || (it.full_name || '').split('/')[1] || '');
    mir.target = '_blank'; mir.rel = 'noopener noreferrer';

    const un = el('button', 'act', '✕ 取消收藏');
    un.addEventListener('click', () => cb.onUnstar(it.id));

    [sel, obs, dl, link, mir, un].forEach((x) => actions.appendChild(x));
    card.appendChild(actions);

    /* 笔记 */
    const notebox = el('div', 'notebox');
    notebox.innerHTML = '<label>我的笔记（自动保存）</label>';
    const ta = document.createElement('textarea');
    ta.value = it.note || '';
    ta.placeholder = '读完了写两句，导出时一起带走';
    let timer = null;
    ta.addEventListener('input', () => {
      clearTimeout(timer);
      timer = setTimeout(() => cb.onNote(it.id, ta.value), 400);
    });
    notebox.appendChild(ta);
    card.appendChild(notebox);

    container.appendChild(card);
  });
  return true;
}
