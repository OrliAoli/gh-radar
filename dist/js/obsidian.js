// Obsidian 导出
//
// 浏览器沙箱无法直接写本地文件，所以走两条路：
//   1. 快速保存（主）：obsidian://new URI 协议，唤起本地 Obsidian 直接建笔记
//   2. 完整导出（备）：触发浏览器下载 .md 文件，用户自己拖进库
// URI 有长度限制，超长时截断正文并在末尾附上完整链接。
import { OBSIDIAN_URI_SOFT_LIMIT } from './config.js';

function pad(n) { return String(n).padStart(2, '0'); }

export function stamp(d = new Date()) {
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())} ${pad(d.getHours())}:${pad(d.getMinutes())}`;
}

export function fileStamp(d = new Date()) {
  return `${d.getFullYear()}${pad(d.getMonth() + 1)}${pad(d.getDate())}`;
}

function yamlList(arr) {
  const list = (arr || []).filter(Boolean);
  return list.length ? `[${list.join(', ')}]` : '[]';
}

function safe(s) {
  // YAML 值里出现特殊字符时加引号
  const v = String(s ?? '');
  return /[:#\[\]{}",&*?|\-]|^\s|\s$/.test(v) ? JSON.stringify(v) : v;
}

/** 单条 -> Obsidian Markdown（带 YAML frontmatter） */
export function itemToMarkdown(item, extra = {}) {
  const savedAt = extra.savedAt || new Date().toISOString();
  const note = extra.note || item.note || '';
  const title = item.full_name || item.id;
  const lines = [
    '---',
    `title: ${safe(title)}`,
    `category: ${safe(item.category || '')}`,
    `stars: ${item.total_stars ?? ''}`,
    `stars_today: ${item.stars_today ?? ''}`,
    `language: ${safe(item.language || '')}`,
    `url: ${item.url || ''}`,
    `topics: ${yamlList(item.topics)}`,
    `first_seen: ${item.first_seen || ''}`,
    `saved_at: ${stamp(new Date(savedAt))}`,
    `tags: [github-radar, ${item.category || 'uncategorized'}]`,
    '---',
    '',
    '## 一句话',
    '',
    item.title_cn || '（简介待生成）',
    '',
    '## 为什么值得看',
    '',
    item.reason_cn || '（简介待生成）',
    '',
    '## 我的笔记',
    '',
    note || '',
    '',
    '---',
    '',
    `原始链接：${item.url || ''}`,
  ];
  if (extra.dataDate) lines.push(`数据日期：${extra.dataDate}`);
  if (item.matched_groups?.length) lines.push(`命中关键词组：${item.matched_groups.join(' / ')}`);
  lines.push('');
  return lines.join('\n');
}

/** 书架整体 -> 一个大 Markdown 文件（批量导入 Obsidian） */
export function shelfToMarkdown(entries) {
  const now = new Date();
  const head = [
    '---',
    'title: GitHub 雷达书架',
    `exported_at: ${stamp(now)}`,
    `count: ${entries.length}`,
    'tags: [github-radar, 导出]',
    '---',
    '',
    '# GitHub 雷达 · 书架导出',
    '',
    `导出时间：${stamp(now)}　共 ${entries.length} 条`,
    '',
    '## 目录',
    '',
  ];
  entries.forEach((e, i) => {
    head.push(`${i + 1}. [${e.full_name || e.id}](#${(e.full_name || e.id).replace(/[^\w\u4e00-\u9fa5-]/g, '').toLowerCase()})`);
  });
  head.push('', '---', '');
  const body = entries.map((e) => {
    const md = itemToMarkdown(e, { savedAt: e.saved_at, note: e.note, dataDate: e.data_date });
    return `\n<a id="${(e.full_name || e.id).replace(/[^\w\u4e00-\u9fa5-]/g, '').toLowerCase()}"></a>\n\n${md}\n---\n`;
  });
  return head.join('\n') + body.join('\n');
}

/** 生成 obsidian:// URI */
export function buildObsidianUri({ vault, file, content }) {
  const q = new URLSearchParams();
  q.set('vault', vault);
  q.set('file', file);
  q.set('content', content);
  // URLSearchParams 会把空格编成 +，Obsidian 认 %20，换掉
  return `obsidian://new?${q.toString().replace(/\+/g, '%20')}`;
}

/**
 * 快速保存：走 URI。超长则截断正文并在末尾附完整链接。
 * 返回 { uri, truncated }
 */
export function quickSave(item, settings, extra = {}) {
  const vault = (settings.obsidianVault || '').trim();
  if (!vault) throw new Error('还没设置 Obsidian 库名，先点右上角 ⚙ 填一下');

  const folder = (settings.obsidianFolder || '').trim().replace(/^\/+|\/+$/g, '');
  const fname = `${(item.full_name || item.id).replace(/[\\/:*?"<>|]/g, '-')}.md`;
  const file = folder ? `${folder}/${fname}` : fname;

  let content = itemToMarkdown(item, extra);
  let truncated = false;
  if (content.length > OBSIDIAN_URI_SOFT_LIMIT) {
    const tail = `\n\n---\n\n> ⚠️ 内容过长已截断，完整内容请用「完整导出」按钮，或直接访问：${item.url || ''}\n`;
    content = content.slice(0, Math.max(0, OBSIDIAN_URI_SOFT_LIMIT - tail.length)) + tail;
    truncated = true;
  }
  return { uri: buildObsidianUri({ vault, file, content }), truncated, file };
}

/** 完整导出：浏览器下载单个 .md */
export function downloadMarkdown(filename, text) {
  const blob = new Blob([text], { type: 'text/markdown;charset=utf-8' });
  downloadBlob(filename, blob);
}

export function downloadBlob(filename, blob) {
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 4000);
}
