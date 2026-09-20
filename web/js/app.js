// 主控制器：串起取数、筛选、渲染与交互
import { CATEGORY_LABEL, CONFIG } from './config.js';
import { loadData } from './api.js';
import { Store } from './store.js';
import { applyFilters, collectLanguages, pickMustSee, defaultFilters } from './filters.js';
import { createCard, esc } from './cards.js';
import { renderShelf } from './shelf.js';
import { registerSW, setupPushButton } from './pwa.js';
import { collectPending, buildIssueUrl, markSynced, pendingCount } from './feedback.js';
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

  registerSW();
  setupPushButton($('pushBtn'), $('pushState'));
  updateFbState();
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
  state.offline = Boolean(res.offline);
  state.canPersist = state.store.backend.name !== 'memory';
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
  $('tbDate').textContent = d ? (d.date || '—') : '无数据';
  $('tbDate').title = d?.window?.from
    ? `聚合窗口 ${d.window.from} ~ ${d.window.to}　本期 ${state.items.length} 条`
    : '';
}

function healthLevel() {
  const d = state.data;
  if (!d) return { level: 'bad', label: '数据读取失败' };
  const warns = d.warnings || [];
  const source = d.source || 'unknown';
  if (state.degraded) return { level: 'warn', label: `正在用 ${state.degraded} 的旧数据` };
  if (source === 'fallback') return { level: 'bad', label: '今日 trending 抓取全部失败' };
  if (source === 'partial' || warns.length) return { level: 'warn', label: '部分数据源异常' };
  return { level: 'ok', label: '数据源正常' };
}

function renderHealth() {
  const dot = $('healthBtn');
  const panel = $('healthPanel');
  const d = state.data;
  const { level, label } = healthLevel();
  dot.classList.toggle('is-warn', level === 'warn');
  dot.title = `数据源健康度：${label}`;

  if (!d) {
    panel.innerHTML = `<div><span class="healthdot bad"></span>无法读取 <code>data/latest.json</code>，也没有找到可用的历史快照。</div>
      <ul>${state.loadErrors.map((e) => `<li>${esc(e)}</li>`).join('')}</ul>`;
    return;
  }

  const st = d.stats || {};
  const warns = d.warnings || [];
  const rows = [];
  rows.push(`<div><span class="healthdot ${level}"></span><span class="k">${esc(label)}</span>　·　趋势源 ${esc(d.source || 'unknown')}</div>`);
  rows.push(`<div style="margin-top:5px">候选池 <span class="k">${st.candidates ?? '—'}</span> 条 →
    过滤后 <span class="k">${st.after_filter ?? '—'}</span> 条 →
    发布 <span class="k">${st.published ?? '—'}</span> 条</div>`);
  if (st.from_trending != null) {
    rows.push(`<div>本期来源：trending <span class="k">${st.from_trending}</span> 条 ·
      search <span class="k">${st.from_search}</span> 条</div>`);
  }
  if (st.dropped) {
    const dd = st.dropped;
    rows.push(`<div>被丢弃：全局排除 ${dd.dropped_global ?? 0} · 星数门槛 ${dd.dropped_min_stars ?? 0} ·
      未命中兴趣组 ${dd.dropped_no_group ?? 0} · 质量门槛 ${dd.dropped_quality_gate ?? 0}</div>`);
  }
  if (warns.length) {
    rows.push('<div style="margin-top:6px"><span class="k">告警</span></div>'
      + `<ul>${warns.map((w) => `<li>${esc(w)}</li>`).join('')}</ul>`);
  } else {
    rows.push('<div style="margin-top:6px">没有告警，所有数据源都正常。</div>');
  }
  if (state.offline) {
    rows.push('<div style="margin-top:6px" class="k">离线单文件版：数据和页面都在这一个文件里，不联网也能看。</div>');
  }
  if (!state.canPersist) {
    rows.push('<div style="margin-top:6px" class="k">⚠️ 当前浏览器不允许本地存储：页面能正常看，'
      + '但收藏 / 已读 / 笔记关掉后会丢。（iOS 的「文件」App 预览有这个问题，改用 Chrome 打开就正常）</div>');
  }
  panel.innerHTML = rows.join('');
}

/* ══════════════ 本期必看（横向滚动）══════════════ */

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
      ? `<span class="mhot">+${Number(it.stars_today).toLocaleString('en-US')} 今日</span>`
      : `<span class="mhot">★ ${Number(it.total_stars || 0).toLocaleString('en-US')}</span>`;
    a.innerHTML = `<span class="rank">${i + 1}</span>
      <div class="mname">${esc(it.full_name || it.id)}</div>${hot}`;
    list.appendChild(a);
  });
  $('mustHint').hidden = top.length <= 2;
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

/** 同步一张卡片上所有 ⭐/收藏 按钮的外观 */
function syncStarUI(item, on) {
  document.querySelectorAll(`.card[data-id="${CSS.escape(item.id)}"]`).forEach((c) => {
    const sb = c.querySelector('.starbtn');
    if (sb) {
      sb.classList.toggle('on', on);
      sb.textContent = on ? '★' : '☆';
    }
    const ab = c.querySelector('.cactions .act.star');
    if (ab) {
      ab.classList.toggle('on', on);
      ab.textContent = (on ? '★' : '☆') + ' 收藏';
    }
  });
}

const cardCallbacks = {
  async onStar(item, _btn) {
    const on = await state.store.toggleStar(item, state.data?.date);
    if (on) state.starred[item.id] = true; else delete state.starred[item.id];
    syncStarUI(item, on);
    updateShelfBadge();
    renderShelfView();
    await state.store.logEvent?.(item, on ? 'star' : 'unstar');
    updateFbState();
    toast(on ? '已收藏（连完整信息一起存进书架）' : '已取消收藏');
  },
  async onRead(item, btn) {
    const nowRead = await state.store.toggleRead(item.id);
    if (nowRead) state.read[item.id] = true; else delete state.read[item.id];
    btn.classList.toggle('on', nowRead);
    btn.textContent = nowRead ? '✓ 已读' : '标记已读';
    btn.closest('.card')?.classList.toggle('is-read', nowRead);
    await state.store.logEvent?.(item, nowRead ? 'read' : 'unread');
    updateFbState();
    if (state.filters.unreadOnly) renderList();
  },
  async onFeedback(item, value, btns) {
    const next = await state.store.setFeedback(item.id, value);
    state.feedback[item.id] = next;
    const [up, down] = btns;
    up.classList.toggle('on', next === 1);
    down.classList.toggle('on', next === -1);
    if (next) await state.store.logEvent?.(item, next === 1 ? 'up' : 'down');
    updateFbState();
    toast(next === 1 ? '👍 已记录，同步后会调高同类权重' : next === -1 ? '👎 已记录，同步后会过滤同类' : '已取消反馈');
  },
  async onNote(item, text) {
    await state.store.setNote(item.id, text);
    if (text && text.trim()) state.notes[item.id] = text; else delete state.notes[item.id];
    if (state.starred[item.id]) await state.store.updateStarred(item.id, { note: text });
  },
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

/* ══════════════ 反馈同步 ══════════════ */

function updateFbState() {
  const el = $('fbState');
  if (!el) return;
  const n = pendingCount();
  el.textContent = n ? `${n} 条待同步` : '没有待同步的';
  const btn = $('syncFbBtn');
  if (btn) btn.disabled = n === 0;
}

function initFeedbackSync() {
  const btn = $('syncFbBtn');
  if (!btn) return;
  btn.addEventListener('click', () => {
    const payload = collectPending();
    if (!payload) return toast('还没有新的 👍 / 👎 / 收藏 / 已读 记录');
    const url = buildIssueUrl(CONFIG.repo, payload);
    window.open(url, '_blank', 'noopener');
    markSynced(payload.__ids);
    updateFbState();
    toast('已打开 GitHub，点绿色按钮提交即可生效');
  });
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

  // 健康度（ⓘ 图标展开）
  $('healthBtn').addEventListener('click', () => {
    const btn = $('healthBtn'), panel = $('healthPanel');
    const open = btn.getAttribute('aria-expanded') === 'true';
    btn.setAttribute('aria-expanded', String(!open));
    panel.hidden = open;
  });

  // 本期必看折叠（手机想把顶部再压扁时点一下，选择会被记住）
  $('mustToggle').addEventListener('click', () => {
    const box = $('mustseeBox'), btn = $('mustToggle');
    const collapsed = box.classList.toggle('collapsed');
    btn.setAttribute('aria-expanded', String(!collapsed));
    try { localStorage.setItem('ghradar.mustsee.v1', collapsed ? '0' : '1'); } catch { /* 忽略 */ }
  });
  try {
    if (localStorage.getItem('ghradar.mustsee.v1') === '0') {
      $('mustseeBox').classList.add('collapsed');
      $('mustToggle').setAttribute('aria-expanded', 'false');
    }
  } catch { /* 忽略 */ }

  // 类别 chips
  $('catRow').addEventListener('click', (e) => {
    const b = e.target.closest('.cat');
    if (!b) return;
    updateFilters({ cat: b.dataset.cat });
    syncFilterUI();
  });

  // 高级筛选折叠
  $('advBtn').addEventListener('click', () => {
    const btn = $('advBtn'), panel = $('advPanel');
    const open = btn.getAttribute('aria-expanded') === 'true';
    btn.setAttribute('aria-expanded', String(!open));
    panel.hidden = open;
    btn.textContent = open ? '筛选 ▾' : '筛选 ▴';
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
  $('tuneSubmit').addEventListener('click', async (e) => {
    e.preventDefault();
    const text = $('tuneText').value.trim();
    if (!text) return toast('先写点什么');
    await state.store.addPreference(text);
    const url = buildTuneIssueUrl(CONFIG.repo, text);
    window.open(url, '_blank', 'noopener');
    $('tuneDlg').close();
    toast('已打开 GitHub，提交后下一期生效');
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
      toast('规则片段已复制，可粘进 config/rules.txt');
    } catch {
      toast('请手动复制下面这段');
    }
  });

  // 设置
  $('settingsBtn').addEventListener('click', () => {
    $('setVault').value = state.settings.obsidianVault || '';
    $('setFolder').value = state.settings.obsidianFolder || '';
    $('settingsDlg').showModal();
    updateFbState();
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

  initFeedbackSync();

  document.addEventListener('keydown', (e) => {
    if (e.key === '/' && document.activeElement.tagName !== 'INPUT'
      && document.activeElement.tagName !== 'TEXTAREA') {
      e.preventDefault();
      $('fSearch').focus();
    }
  });
}

/* ══════════════ 规则片段 ══════════════ */

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
  if (globalFilter.length) out.push('[GLOBAL_FILTER]', ...globalFilter.map((w) => `/${w}/`), '');
  if (want.length) out.push('[AI 学习资源]', ...want.map((w) => `/${w}/`), '');
  out.push('# 提示：上面只是起手式，正式规则建议手改 config/rules.txt');
  return out.join('\n');
}

function buildTuneIssueUrl(repo, text) {
  const title = '[调教] 雷达偏好';
  const body = [
    '<!-- radar-tuning -->', '', '```text', text, '```', '',
    '提交后 GitHub Actions 会自动记录到 config/tuning.txt，下一期生成时生效。',
  ].join('\n');
  const q = new URLSearchParams({ title, body, labels: 'radar-tuning' });
  return `https://github.com/${repo}/issues/new?${q.toString()}`;
}

/* ══════════════ 工具 ══════════════ */

function applyTheme(t) {
  document.documentElement.dataset.theme = t === 'light' ? 'light' : 'dark';
  const meta = document.querySelector('meta[name="theme-color"]');
  if (meta) meta.content = t === 'light' ? '#f6f8fa' : '#0d1117';
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
  $('tbDate').textContent = '初始化失败：' + e.message;
});
