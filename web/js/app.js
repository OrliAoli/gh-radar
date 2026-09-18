// 主控制器：串起取数、筛选、渲染与交互
import { CATEGORY_LABEL } from './config.js';
import { loadData } from './api.js';
import { Store } from './store.js';
import { applyFilters, collectLanguages, pickMustSee, defaultFilters } from './filters.js';
import { createCard, esc } from './cards.js';
import { renderShelf } from './shelf.js';
import {
  itemToMarkdown, shelfToMarkdown, quickSave, downloadMarkdown,
  downloadBlob, fileStamp,
} from './obsidian.js';

const $ = (id) => document.getElementById(id);

const state = {
  store: null,
  data: null,
  items: [],
  starred: {},
  read: {},
  feedback: {},
  notes: {},
  settings: {},
  filters: defaultFilters(),
  degraded: null,
  loadErrors: [],
  shelfReadFilter: 'all',
  shelfQuery: '',
};

/* ══════════════ 启动 ══════════════ */

async function boot() {
  state.store = new Store();
  await state.store.init();

  applyTheme(await state.store.theme());
  state.settings = await state.store.settings();
  state.filters = { ...defaultFilters(), ...(await state.store.filters()) };
  syncFilterUI();

  wireEvents();
  await refreshUserState();
  await reload();
}

async function refreshUserState() {
  state.starred = await state.store.starred();
  state.read = await state.store.readMap();
  state.feedback = await state.store.feedback();
  state.notes = await state.store.notes();
  updateShelfBadge();
}

async function reload() {
  const res = await loadData();
  state.data = res.data;
  state.degraded = res.degradedFrom;
  state.loadErrors = res.errors || [];
  state.items = res.data?.items || [];

  renderMeta();
  renderHealth();
  renderLanguageOptions();
  renderMustSee();
  renderList();
  renderShelfView();
}

/* ══════════════ 顶部信息 ══════════════ */

function renderMeta() {
  const d = state.data;
  if (!d) {
    $('dataDate').textContent = '暂无数据';
    $('dataWindow').textContent = '';
    return;
  }
  $('dataDate').textContent = `数据日期 ${d.date || '—'}`;
  const w = d.window;
  const bits = [];
  if (w?.from && w?.to && w.from !== w.to) bits.push(`聚合窗口 ${w.from} ~ ${w.to}`);
  bits.push(`本期 ${state.items.length} 条`);
  $('dataWindow').textContent = bits.join(' · ');
}

function renderHealth() {
  const dot = $('healthDot'), text = $('healthText'), panel = $('healthPanel');
  const d = state.data;

  if (!d) {
    dot.className = 'healthdot bad';
    text.textContent = '数据读取失败';
    panel.innerHTML = `<div>无法读取 <code>data/latest.json</code>，也没有找到可用的历史快照。</div>
      <ul>${state.loadErrors.map((e) => `<li>${esc(e)}</li>`).join('')}</ul>`;
    return;
  }

  const st = d.stats || {};
  const warns = d.warnings || [];
  const source = d.source || 'unknown';

  let level = 'ok', label = '数据源正常';
  if (state.degraded) { level = 'warn'; label = `正在用 ${state.degraded} 的旧数据`; }
  else if (source === 'fallback') { level = 'bad'; label = '今日 trending 抓取全部失败'; }
  else if (source === 'partial' || warns.length) { level = 'warn'; label = '部分数据源异常'; }

  dot.className = 'healthdot ' + level;
  text.textContent = `${label}　·　趋势源 ${source}`;

  const rows = [];
  rows.push(`<div><span class="k">候选池</span> ${st.candidates ?? '—'} 条 →
    <span class="k">过滤后</span> ${st.after_filter ?? '—'} 条 →
    <span class="k">发布</span> ${st.published ?? '—'} 条</div>`);
  if (st.lane_a != null) {
    rows.push(`<div><span class="k">车道 A</span> ${st.lane_a} 条（有今日新增）　
      <span class="k">车道 B</span> ${st.lane_b} 条（搜索池，无今日新增）</div>`);
  }
  if (st.from_trending != null) {
    rows.push(`<div>本期来源：trending <span class="k">${st.from_trending}</span> 条 ·
      search <span class="k">${st.from_search}</span> 条</div>`);
  }
  if (st.dropped) {
    const dd = st.dropped;
    rows.push(`<div>被丢弃：全局排除 ${dd.dropped_global ?? 0} · 星数门槛 ${dd.dropped_min_stars ?? 0} ·
      未命中兴趣组 ${dd.dropped_no_group ?? 0} · 质量门槛 ${dd.dropped_quality_gate ?? 0}</div>`);
  }
  if (st.allocation) {
    rows.push(`<div>名额分配：${Object.entries(st.allocation).map(([k, v]) => `${k} ${v}`).join(' · ')}</div>`);
  }
  if (warns.length) {
    rows.push(`<div style="margin-top:6px"><span class="k">告警</span></div>
      <ul>${warns.map((w) => `<li>${esc(w)}</li>`).join('')}</ul>`);
  } else {
    rows.push('<div style="margin-top:6px">没有告警，所有数据源都正常。</div>');
  }
  if (state.degraded) {
    rows.push(`<div style="margin-top:6px" class="k">注意：最新一期读取失败，当前显示的是 ${esc(state.degraded)} 的快照。</div>`);
  }
  panel.innerHTML = rows.join('');
}

/* ══════════════ 本期必看 ══════════════ */

function renderMustSee() {
  const box = $('mustseeBox'), list = $('mustlist');
  const top = pickMustSee(state.items, 5);
  if (!top.length) { box.hidden = true; return; }
  box.hidden = false;
  list.innerHTML = '';
  top.forEach((it, i) => {
    const a = document.createElement('a');
    a.className = 'must';
    a.href = it.url || '#';
    a.target = '_blank';
    a.rel = 'noopener noreferrer';
    const hot = it.stars_today != null
      ? `<span class="mhot">+${Number(it.stars_today).toLocaleString('en-US')}</span> 今日`
      : `★ ${Number(it.total_stars || 0).toLocaleString('en-US')}`;
    a.innerHTML = `
      <span class="rank">${i + 1}</span>
      <div class="mname">${esc(it.full_name || it.id)}</div>
      <div class="mmeta">${esc(CATEGORY_LABEL[it.category] || '')} · ${esc(it.language || '—')}</div>
      <div class="mmeta">${hot}</div>`;
    list.appendChild(a);
  });
}

/* ══════════════ 雷达列表 ══════════════ */

function context() {
  return {
    dataDate: state.data?.date,
    starredSet: new Set(Object.keys(state.starred)),
    readSet: new Set(Object.keys(state.read)),
  };
}

function renderList() {
  const list = $('list');
  const visible = applyFilters(state.items, state.filters, context());
  list.innerHTML = '';
  $('resultCount').textContent = `显示 ${visible.length} / ${state.items.length} 条`;
  $('emptyRadar').hidden = visible.length > 0;

  const frag = document.createDocumentFragment();
  visible.forEach((item) => frag.appendChild(createCard(item, itemState(item), cardCallbacks)));
  list.appendChild(frag);
}

function itemState(item) {
  return {
    starred: Boolean(state.starred[item.id]),
    read: Boolean(state.read[item.id]),
    feedback: state.feedback[item.id] || 0,
    note: state.notes[item.id] || '',
  };
}

const cardCallbacks = {
  async onStar(item, btn) {
    const on = await state.store.toggleStar(item, state.data?.date);
    if (on) state.starred[item.id] = true; else delete state.starred[item.id];
    btn.classList.toggle('on', on);
    btn.innerHTML = (on ? '★' : '☆') + ' 收藏';
    updateShelfBadge();
    renderShelfView();
    toast(on ? '已收藏（连同完整信息一起存进书架）' : '已取消收藏');
  },
  async onRead(item, btn) {
    const nowRead = await state.store.toggleRead(item.id);
    if (nowRead) state.read[item.id] = true; else delete state.read[item.id];
    btn.classList.toggle('on', nowRead);
    btn.textContent = nowRead ? '✓ 已读' : '标记已读';
    btn.closest('.card')?.classList.toggle('is-read', nowRead);
    if (state.filters.unreadOnly) renderList();
  },
  async onFeedback(item, value, btns) {
    const next = await state.store.setFeedback(item.id, value);
    state.feedback[item.id] = next;
    const [up, down] = btns;
    up.classList.toggle('on', next === 1);
    down.classList.toggle('on', next === -1);
    toast(next === 1 ? '👍 已记录，会影响后续排序' : next === -1 ? '👎 已记录' : '已取消反馈');
  },
  async onNote(item, text) {
    await state.store.setNote(item.id, text);
    if (text && text.trim()) state.notes[item.id] = text; else delete state.notes[item.id];
    if (state.starred[item.id]) await state.store.updateStarred(item.id, { note: text });
  },
  onOpen() { /* 展开由卡片内部处理 */ },
};

/* ══════════════ 筛选栏 ══════════════ */

function renderLanguageOptions() {
  const sel = $('fLang');
  const langs = collectLanguages(state.items);
  const cur = state.filters.lang;
  sel.innerHTML = '<option value="">全部</option>' +
    langs.map((l) => `<option value="${esc(l)}"${l === cur ? ' selected' : ''}>${esc(l)}</option>`).join('');
}

function syncFilterUI() {
  const f = state.filters;
  document.querySelectorAll('#catRow .cat').forEach((b) => {
    b.classList.toggle('is-active', b.dataset.cat === f.cat);
  });
  $('fLang').value = f.lang || '';
  $('fTime').value = f.time || 'all';
  $('fSort').value = f.sort || 'score';
  $('fSearch').value = f.q || '';
  $('fUnread').checked = Boolean(f.unreadOnly);
  $('fStarred').checked = Boolean(f.starredOnly);
}

let saveTimer = null;
function updateFilters(patch, rerender = true) {
  state.filters = { ...state.filters, ...patch };
  clearTimeout(saveTimer);
  saveTimer = setTimeout(() => state.store.saveFilters(state.filters), 300);
  if (rerender) renderList();
}

/* ══════════════ 书架 ══════════════ */

function updateShelfBadge() {
  const n = Object.keys(state.starred).length;
  const b = $('shelfBadge');
  b.hidden = n === 0;
  b.textContent = String(n);
}

function sortedShelfEntries() {
  let list = Object.values(state.starred);
  list.sort((a, b) => Date.parse(b.saved_at || 0) - Date.parse(a.saved_at || 0));
  if (state.shelfReadFilter !== 'all') {
    list = list.filter((e) => (e.read_state || 'unread') === state.shelfReadFilter);
  }
  const q = state.shelfQuery.trim().toLowerCase();
  if (q) {
    list = list.filter((e) => [e.full_name, e.title_cn, e.reason_cn, e.note]
      .filter(Boolean).join(' ').toLowerCase().includes(q));
  }
  return list;
}

function renderShelfView() {
  const entries = sortedShelfEntries();
  const total = Object.keys(state.starred).length;
  $('shelfCount').textContent = total ? `（${entries.length} / ${total} 条）` : '';
  const any = renderShelf($('shelfList'), entries, shelfCallbacks);
  $('emptyShelf').hidden = Boolean(any);
}

const shelfCallbacks = {
  async onReadState(id, value, card) {
    await state.store.updateStarred(id, { read_state: value });
    state.starred[id] = { ...state.starred[id], read_state: value };
    card.classList.toggle('is-read', value === 'done');
    toast('阅读状态已更新');
  },
  async onNote(id, text) {
    await state.store.updateStarred(id, { note: text });
    state.starred[id] = { ...state.starred[id], note: text };
  },
  async onUnstar(id) {
    await state.store.unstar(id);
    delete state.starred[id];
    updateShelfBadge();
    renderShelfView();
    renderList();
    toast('已移出书架');
  },
  onQuickSave(entry) { doQuickSave(entry, entry.note); },
  onFullExport(entry) {
    downloadMarkdown(
      `${(entry.full_name || entry.id).replace(/[\\/:*?"<>|]/g, '-')}.md`,
      itemToMarkdown(entry, { savedAt: entry.saved_at, note: entry.note, dataDate: entry.data_date }),
    );
    toast('已下载 .md 文件');
  },
};

/* ══════════════ Obsidian ══════════════ */

function doQuickSave(item, note) {
  try {
    const { uri, truncated, file } = quickSave(item, state.settings, {
      savedAt: item.saved_at, note, dataDate: item.data_date,
    });
    window.location.href = uri;
    toast(truncated
      ? `内容过长已截断，已唤起 Obsidian 创建 ${file}`
      : `已唤起 Obsidian 创建 ${file}`);
  } catch (e) {
    toast(e.message || '保存失败');
    if (/库名/.test(e.message || '')) $('settingsDlg').showModal();
  }
}

/* ══════════════ 事件绑定 ══════════════ */

function wireEvents() {
  // 视图切换
  document.querySelectorAll('.viewtab').forEach((b) => {
    b.addEventListener('click', () => {
      document.querySelectorAll('.viewtab').forEach((x) => x.classList.toggle('is-active', x === b));
      const v = b.dataset.view;
      $('view-radar').hidden = v !== 'radar';
      $('view-shelf').hidden = v !== 'shelf';
      if (v === 'shelf') renderShelfView();
      window.scrollTo({ top: 0 });
    });
  });

  // 主题
  $('themeBtn').addEventListener('click', async () => {
    const next = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
    applyTheme(next);
    await state.store.saveTheme(next);
  });

  // 健康度展开
  $('healthBtn').addEventListener('click', () => {
    const btn = $('healthBtn'), panel = $('healthPanel');
    const open = btn.getAttribute('aria-expanded') === 'true';
    btn.setAttribute('aria-expanded', String(!open));
    panel.hidden = open;
  });

  // 类别 Tab
  $('catRow').addEventListener('click', (e) => {
    const b = e.target.closest('.cat');
    if (!b) return;
    updateFilters({ cat: b.dataset.cat });
    syncFilterUI();
  });

  $('fLang').addEventListener('change', (e) => updateFilters({ lang: e.target.value }));
  $('fTime').addEventListener('change', (e) => updateFilters({ time: e.target.value }));
  $('fSort').addEventListener('change', (e) => updateFilters({ sort: e.target.value }));
  let searchTimer = null;
  $('fSearch').addEventListener('input', (e) => {
    clearTimeout(searchTimer);
    const v = e.target.value;
    searchTimer = setTimeout(() => updateFilters({ q: v }), 180);
  });
  $('fUnread').addEventListener('change', (e) => updateFilters({ unreadOnly: e.target.checked }));
  $('fStarred').addEventListener('change', (e) => updateFilters({ starredOnly: e.target.checked }));
  $('resetFilters').addEventListener('click', () => {
    updateFilters(defaultFilters());
    syncFilterUI();
    toast('筛选已重置');
  });

  // 书架筛选
  document.querySelectorAll('.shelffilter .cat').forEach((b) => {
    b.addEventListener('click', () => {
      document.querySelectorAll('.shelffilter .cat').forEach((x) => x.classList.toggle('is-active', x === b));
      state.shelfReadFilter = b.dataset.read;
      renderShelfView();
    });
  });
  let shelfTimer = null;
  $('shelfSearch').addEventListener('input', (e) => {
    clearTimeout(shelfTimer);
    const v = e.target.value;
    shelfTimer = setTimeout(() => { state.shelfQuery = v; renderShelfView(); }, 180);
  });

  // 导出 / 导入
  $('exportMd').addEventListener('click', () => {
    const entries = sortedShelfEntries();
    if (!entries.length) return toast('书架是空的');
    downloadMarkdown(`GitHub雷达书架-${fileStamp()}.md`, shelfToMarkdown(entries));
    toast(`已导出 ${entries.length} 条`);
  });
  $('exportJson').addEventListener('click', async () => {
    const payload = await state.store.exportAll();
    downloadBlob(`github-radar-backup-${fileStamp()}.json`,
      new Blob([JSON.stringify(payload, null, 2)], { type: 'application/json' }));
    toast('备份已下载');
  });
  $('importJson').addEventListener('click', () => $('importFile').click());
  $('importFile').addEventListener('change', async (e) => {
    const file = e.target.files?.[0];
    if (!file) return;
    try {
      const payload = JSON.parse(await file.text());
      await state.store.importAll(payload, { merge: true });
      await refreshUserState();
      renderList();
      renderShelfView();
      toast('导入成功');
    } catch (err) {
      toast('导入失败：' + err.message);
    }
    e.target.value = '';
  });

  // 调教雷达
  $('tuneBtn').addEventListener('click', async () => {
    const prefs = await state.store.preferences();
    $('tuneText').value = prefs.map((p) => p.text).join('\n');
    $('tuneSnippet').hidden = true;
    $('tuneDlg').showModal();
  });
  $('tuneSave').addEventListener('click', async (e) => {
    e.preventDefault();
    const text = $('tuneText').value.trim();
    if (!text) return toast('先写点什么');
    await state.store.addPreference(text);
    toast('偏好已保存');
    $('tuneDlg').close();
  });
  $('tuneCopy').addEventListener('click', async (e) => {
    e.preventDefault();
    const text = $('tuneText').value.trim();
    if (!text) return toast('先写点什么');
    await state.store.addPreference(text);
    const snippet = buildRuleSnippet(text);
    $('tuneSnippet').hidden = false;
    $('tuneSnippet').textContent = snippet;
    try {
      await navigator.clipboard.writeText(snippet);
      toast('规则片段已复制，粘进 config/rules.txt 后 push 即可生效');
    } catch {
      toast('请手动复制下面这段');
    }
  });

  // 设置
  $('settingsBtn').addEventListener('click', () => {
    $('setVault').value = state.settings.obsidianVault || '';
    $('setFolder').value = state.settings.obsidianFolder || '';
    $('settingsDlg').showModal();
  });
  $('settingsSave').addEventListener('click', async (e) => {
    e.preventDefault();
    state.settings = {
      ...state.settings,
      obsidianVault: $('setVault').value.trim(),
      obsidianFolder: $('setFolder').value.trim() || 'GitHub雷达',
    };
    await state.store.saveSettings(state.settings);
    toast('设置已保存');
    $('settingsDlg').close();
  });
  $('settingsWipe').addEventListener('click', async (e) => {
    e.preventDefault();
    if (!confirm('会清空收藏、已读、反馈、笔记和设置。确定吗？')) return;
    await state.store.wipe();
    await refreshUserState();
    state.settings = await state.store.settings();
    applyTheme(await state.store.theme());
    renderList();
    renderShelfView();
    $('settingsDlg').close();
    toast('已清空');
  });

  // 键盘：Esc 关弹窗由 dialog 原生处理
  document.addEventListener('keydown', (e) => {
    if (e.key === '/' && document.activeElement.tagName !== 'INPUT'
      && document.activeElement.tagName !== 'TEXTAREA') {
      e.preventDefault();
      $('fSearch').focus();
    }
  });
}

/**
 * 把自然语言偏好转成可粘贴的规则片段。
 * 静态网页改不了仓库文件，所以这里只生成文本，由用户粘一次。
 */
function buildRuleSnippet(text) {
  const lines = text.split(/\n+/).map((s) => s.trim()).filter(Boolean);
  const globalFilter = [];
  const want = [];
  lines.forEach((ln) => {
    const m = ln.match(/^(?:不要|少推|别再|排除|屏蔽)\s*[:：]?\s*(.+)$/);
    if (m) {
      m[1].split(/[、,，;；\s]+/).filter(Boolean).forEach((w) => { if (!globalFilter.includes(w)) globalFilter.push(w); });
      return;
    }
    const m2 = ln.match(/^(?:多推|多看|关注|想要|希望)\s*[:：]?\s*(.+)$/);
    if (m2) {
      m2[1].split(/[、,，;；\s]+/).filter(Boolean).forEach((w) => { if (!want.includes(w)) want.push(w); });
      return;
    }
    want.push(ln);
  });

  const out = ['# 由「调教雷达」生成，粘进 config/rules.txt 后 commit + push 才生效', ''];
  if (globalFilter.length) {
    out.push('[GLOBAL_FILTER]', ...globalFilter.map((w) => `/${w}/`), '');
  }
  if (want.length) {
    out.push('[AI 学习资源]', ...want.map((w) => `/${w}/`), '');
  }
  out.push('# 提示：上面只是起手式，正式规则建议手改 config/rules.txt');
  return out.join('\n');
}

/* ══════════════ 工具 ══════════════ */

function applyTheme(t) {
  document.documentElement.dataset.theme = t === 'light' ? 'light' : 'dark';
  const meta = document.querySelector('meta[name="color-scheme"]');
  if (meta) meta.content = t === 'light' ? 'light dark' : 'dark light';
}

let toastTimer = null;
function toast(msg) {
  const t = $('toast');
  t.textContent = msg;
  t.hidden = false;
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => { t.hidden = true; }, 2600);
}

boot().catch((e) => {
  console.error(e);
  $('healthText').textContent = '初始化失败：' + e.message;
  $('healthDot').className = 'healthdot bad';
});
