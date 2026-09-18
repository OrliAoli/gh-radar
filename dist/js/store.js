// 本地状态存储。
//
// 设计成"后端可替换"：所有读写都走异步方法，将来换成云数据库
// （CloudBase / Supabase）时，只要再写一个实现了 get/set 的后端传进来即可，
// 页面代码一行都不用改。
import { STORAGE_KEYS, DEFAULT_SETTINGS } from './config.js';

/* ─────────── 后端：localStorage ─────────── */
export class LocalBackend {
  constructor() { this.name = 'localStorage'; }

  async get(key) {
    try {
      const raw = localStorage.getItem(key);
      return raw == null ? null : JSON.parse(raw);
    } catch { return null; }
  }

  async set(key, value) {
    try { localStorage.setItem(key, JSON.stringify(value)); return true; }
    catch (e) { console.warn('写入本地存储失败', e); return false; }
  }

  async remove(key) {
    try { localStorage.removeItem(key); } catch { /* 忽略 */ }
  }

  async keys() { return Object.values(STORAGE_KEYS); }
}

/* ─────────── 内存后端：localStorage 不可用时的兜底 ─────────── */
export class MemoryBackend {
  constructor() { this.name = 'memory'; this.map = new Map(); }
  async get(k) { return this.map.has(k) ? this.map.get(k) : null; }
  async set(k, v) { this.map.set(k, v); return true; }
  async remove(k) { this.map.delete(k); }
  async keys() { return [...this.map.keys()]; }
}

/* ─────────── 门面 ─────────── */
export class Store {
  constructor(backend = null) {
    this.backend = backend || this._pickBackend();
    this.cache = {};
  }

  _pickBackend() {
    try {
      const probe = '__ghradar_probe__';
      localStorage.setItem(probe, '1');
      localStorage.removeItem(probe);
      return new LocalBackend();
    } catch {
      console.warn('localStorage 不可用，改用内存存储（刷新后会丢失）');
      return new MemoryBackend();
    }
  }

  async init() {
    for (const key of Object.values(STORAGE_KEYS)) {
      this.cache[key] = await this.backend.get(key);
    }
  }

  async _read(key, fallback) {
    if (this.cache[key] === undefined) this.cache[key] = await this.backend.get(key);
    return this.cache[key] ?? fallback;
  }

  async _write(key, value) {
    this.cache[key] = value;
    await this.backend.set(key, value);
    return value;
  }

  /* ─── 收藏（存完整快照，不存 ID） ─── */
  async starred() { return (await this._read(STORAGE_KEYS.starred, {})) || {}; }
  async isStarred(id) { return Boolean((await this.starred())[id]); }

  /**
   * 收藏时必须存完整快照 —— 数据每 3 天换一版，只存 ID 的话
   * 3 天后收藏夹会变成一堆没有标题、没有简介的空条目。
   */
  async star(item, dataDate) {
    const all = { ...(await this.starred()) };
    all[item.id] = {
      id: item.id,
      owner: item.owner,
      name: item.name,
      full_name: item.full_name,
      url: item.url,
      title_cn: item.title_cn ?? null,
      reason_cn: item.reason_cn ?? null,
      description: item.description ?? '',
      total_stars: item.total_stars ?? null,
      stars_today: item.stars_today ?? null,
      burst_score: item.burst_score ?? null,
      language: item.language ?? '',
      topics: item.topics ?? [],
      matched_groups: item.matched_groups ?? [],
      category: item.category ?? null,
      first_seen: item.first_seen ?? null,
      periods_on_board: item.periods_on_board ?? null,
      saved_at: new Date().toISOString(),
      data_date: dataDate || null,     // 收藏时那份数据的日期
      read_state: 'unread',            // unread | reading | done
      note: '',
    };
    await this._write(STORAGE_KEYS.starred, all);
    return all[item.id];
  }

  async unstar(id) {
    const all = { ...(await this.starred()) };
    delete all[id];
    await this._write(STORAGE_KEYS.starred, all);
  }

  async toggleStar(item, dataDate) {
    if (await this.isStarred(item.id)) { await this.unstar(item.id); return false; }
    await this.star(item, dataDate);
    return true;
  }

  async updateStarred(id, patch) {
    const all = { ...(await this.starred()) };
    if (!all[id]) return null;
    all[id] = { ...all[id], ...patch };
    await this._write(STORAGE_KEYS.starred, all);
    return all[id];
  }

  async replaceStarred(map) { return this._write(STORAGE_KEYS.starred, map || {}); }

  /* ─── 已读 ─── */
  async readMap() { return (await this._read(STORAGE_KEYS.read, {})) || {}; }
  async isRead(id) { return Boolean((await this.readMap())[id]); }
  async toggleRead(id) {
    const m = { ...(await this.readMap()) };
    if (m[id]) delete m[id]; else m[id] = new Date().toISOString();
    await this._write(STORAGE_KEYS.read, m);
    return Boolean(m[id]);
  }

  /* ─── 反馈 👍 / 👎 ─── */
  async feedback() { return (await this._read(STORAGE_KEYS.feedback, {})) || {}; }
  async setFeedback(id, value) {
    const m = { ...(await this.feedback()) };
    if (m[id] === value) delete m[id]; else m[id] = value;   // 再点一次取消
    await this._write(STORAGE_KEYS.feedback, m);
    return m[id] ?? 0;
  }

  /* ─── 备注 ─── */
  async notes() { return (await this._read(STORAGE_KEYS.notes, {})) || {}; }
  async setNote(id, text) {
    const m = { ...(await this.notes()) };
    if (text && text.trim()) m[id] = text; else delete m[id];
    await this._write(STORAGE_KEYS.notes, m);
    return m[id] || '';
  }

  /* ─── 筛选状态（下次打开要记住） ─── */
  async filters() {
    return (await this._read(STORAGE_KEYS.filters, null)) || {
      cat: 'all', lang: '', time: 'all', sort: 'score',
      q: '', unreadOnly: false, starredOnly: false,
    };
  }
  async saveFilters(f) { return this._write(STORAGE_KEYS.filters, f); }

  /* ─── 设置 ─── */
  async settings() {
    const s = await this._read(STORAGE_KEYS.settings, null);
    return { ...DEFAULT_SETTINGS, ...(s || {}) };
  }
  async saveSettings(s) { return this._write(STORAGE_KEYS.settings, s); }

  /* ─── 调教雷达：偏好 ─── */
  async preferences() { return (await this._read(STORAGE_KEYS.preferences, [])) || []; }
  async addPreference(text) {
    const list = await this.preferences();
    const entry = { text, at: new Date().toISOString() };
    list.unshift(entry);
    await this._write(STORAGE_KEYS.preferences, list.slice(0, 50));
    return entry;
  }

  /* ─── 主题 ─── */
  async theme() { return (await this._read(STORAGE_KEYS.theme, 'dark')) || 'dark'; }
  async saveTheme(t) { return this._write(STORAGE_KEYS.theme, t); }

  /* ─── 备份 ─── */
  async exportAll() {
    return {
      exported_at: new Date().toISOString(),
      version: 1,
      starred: await this.starred(),
      read: await this.readMap(),
      feedback: await this.feedback(),
      notes: await this.notes(),
      settings: await this.settings(),
      preferences: await this.preferences(),
    };
  }

  async importAll(payload, { merge = true } = {}) {
    if (!payload || typeof payload !== 'object') throw new Error('文件内容不是合法的备份');
    const pick = (k) => (payload[k] && typeof payload[k] === 'object' ? payload[k] : null);
    const tasks = [
      [STORAGE_KEYS.starred, pick('starred')],
      [STORAGE_KEYS.read, pick('read')],
      [STORAGE_KEYS.feedback, pick('feedback')],
      [STORAGE_KEYS.notes, pick('notes')],
    ];
    for (const [key, incoming] of tasks) {
      if (!incoming) continue;
      const existing = merge ? ((await this._read(key, {})) || {}) : {};
      await this._write(key, { ...existing, ...incoming });
    }
    if (pick('settings')) {
      await this._write(STORAGE_KEYS.settings, {
        ...(merge ? await this.settings() : {}), ...payload.settings,
      });
    }
    if (Array.isArray(payload.preferences)) {
      const existing = merge ? await this.preferences() : [];
      await this._write(STORAGE_KEYS.preferences, [...payload.preferences, ...existing].slice(0, 200));
    }
    return true;
  }

  async wipe() {
    for (const key of Object.values(STORAGE_KEYS)) await this.backend.remove(key);
    this.cache = {};
  }
}
