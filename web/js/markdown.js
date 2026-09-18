// 极简 Markdown 渲染器
//
// 为什么自己写：页面不能引任何外部库（要能当单文件离线打开、不能挂 CDN 字体/JS），
// 而 L3 是完整译文，要求「Markdown 正确渲染，不是显示源码」。
// 所以这里实现一个够用的子集：标题、粗斜体、行内代码、代码块、列表、链接、图片、
// 引用、表格、分割线、段落。

export function escHtml(s) {
  return String(s ?? '').replace(/[&<>"']/g, (c) => (
    { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]
  ));
}

function inline(text) {
  let s = escHtml(text);

  // 行内代码优先，避免里面的 * _ 被当强调处理
  const codes = [];
  s = s.replace(/`([^`\n]+)`/g, (m, c) => {
    codes.push(c);
    return '\u0000CODE' + (codes.length - 1) + '\u0000';
  });

  // 图片 ![alt](url)
  s = s.replace(/!\[([^\]]*)\]\(([^)\s]+)(?:\s+"[^"]*")?\)/g,
    (m, alt, url) => `<img src="${url}" alt="${alt}" loading="lazy">`);

  // 链接 [text](url)
  s = s.replace(/\[([^\]]+)\]\(([^)\s]+)(?:\s+"[^"]*")?\)/g,
    (m, t, url) => `<a href="${url}" target="_blank" rel="noopener noreferrer">${t}</a>`);

  // 自动链接
  s = s.replace(/(^|[\s(])((?:https?:\/\/)[^\s<)]+)/g,
    (m, p, url) => `${p}<a href="${url}" target="_blank" rel="noopener noreferrer">${url}</a>`);

  // 强调
  s = s.replace(/\*\*\*([^*]+)\*\*\*/g, '<strong><em>$1</em></strong>');
  s = s.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
  s = s.replace(/(^|[^*])\*([^*\n]+)\*/g, '$1<em>$2</em>');
  s = s.replace(/(^|[^_])_([^_\n]+)_/g, '$1<em>$2</em>');
  s = s.replace(/~~([^~]+)~~/g, '<del>$1</del>');

  // 还原行内代码
  s = s.replace(/\u0000CODE(\d+)\u0000/g, (m, i) => `<code>${codes[Number(i)]}</code>`);
  return s;
}

function splitRow(line) {
  return line.replace(/^\s*\|/, '').replace(/\|\s*$/, '').split('|').map((c) => c.trim());
}

function isTableSep(line) {
  return /^\s*\|?[\s:\-|]+\|[\s:\-|]*$/.test(line) && line.includes('-');
}

export function renderMarkdown(src) {
  if (!src) return '';
  const lines = String(src).replace(/\r\n?/g, '\n').split('\n');
  const out = [];
  let i = 0;

  while (i < lines.length) {
    const line = lines[i];

    // 代码块（围栏）—— 内容一字不动
    const fence = line.match(/^\s*```([A-Za-z0-9_+-]*)\s*$/);
    if (fence) {
      const lang = fence[1];
      const buf = [];
      i++;
      while (i < lines.length && !/^\s*```\s*$/.test(lines[i])) {
        buf.push(lines[i]);
        i++;
      }
      i++; // 跳过收尾围栏
      const cls = lang ? ` class="lang-${escHtml(lang)}"` : '';
      out.push(`<pre><code${cls}>${escHtml(buf.join('\n'))}</code></pre>`);
      continue;
    }

    // 空行
    if (!line.trim()) { i++; continue; }

    // 分割线
    if (/^\s*([-*_])\s*\1\s*\1[\s\-*_]*$/.test(line)) {
      out.push('<hr>');
      i++;
      continue;
    }

    // 标题
    const h = line.match(/^(#{1,6})\s+(.*)$/);
    if (h) {
      const lv = h[1].length;
      out.push(`<h${lv}>${inline(h[2])}</h${lv}>`);
      i++;
      continue;
    }

    // 表格
    if (line.includes('|') && i + 1 < lines.length && isTableSep(lines[i + 1])) {
      const head = splitRow(line);
      i += 2;
      const rows = [];
      while (i < lines.length && lines[i].includes('|') && lines[i].trim()) {
        rows.push(splitRow(lines[i]));
        i++;
      }
      let html = '<div class="mdtable"><table><thead><tr>';
      head.forEach((c) => { html += `<th>${inline(c)}</th>`; });
      html += '</tr></thead><tbody>';
      rows.forEach((r) => {
        html += '<tr>';
        r.forEach((c) => { html += `<td>${inline(c)}</td>`; });
        html += '</tr>';
      });
      html += '</tbody></table></div>';
      out.push(html);
      continue;
    }

    // 引用
    if (/^\s*>/.test(line)) {
      const buf = [];
      while (i < lines.length && /^\s*>/.test(lines[i])) {
        buf.push(lines[i].replace(/^\s*>\s?/, ''));
        i++;
      }
      out.push(`<blockquote>${inline(buf.join(' '))}</blockquote>`);
      continue;
    }

    // 无序列表
    if (/^\s*[-*+]\s+/.test(line)) {
      const items = [];
      while (i < lines.length && /^\s*[-*+]\s+/.test(lines[i])) {
        let t = lines[i].replace(/^\s*[-*+]\s+/, '');
        i++;
        while (i < lines.length && /^\s{2,}\S/.test(lines[i]) && !/^\s*[-*+]\s+/.test(lines[i])) {
          t += ' ' + lines[i].trim();
          i++;
        }
        items.push(`<li>${inline(t)}</li>`);
      }
      out.push(`<ul>${items.join('')}</ul>`);
      continue;
    }

    // 有序列表
    if (/^\s*\d+[.)]\s+/.test(line)) {
      const items = [];
      while (i < lines.length && /^\s*\d+[.)]\s+/.test(lines[i])) {
        let t = lines[i].replace(/^\s*\d+[.)]\s+/, '');
        i++;
        while (i < lines.length && /^\s{2,}\S/.test(lines[i]) && !/^\s*\d+[.)]\s+/.test(lines[i])) {
          t += ' ' + lines[i].trim();
          i++;
        }
        items.push(`<li>${inline(t)}</li>`);
      }
      out.push(`<ol>${items.join('')}</ol>`);
      continue;
    }

    // 普通段落：连续非空行合并成一段
    const buf = [];
    while (i < lines.length && lines[i].trim()
           && !/^\s*```/.test(lines[i])
           && !/^\s*>/.test(lines[i])
           && !/^(#{1,6})\s+/.test(lines[i])
           && !/^\s*[-*+]\s+/.test(lines[i])
           && !/^\s*\d+[.)]\s+/.test(lines[i])) {
      buf.push(lines[i].trim());
      i++;
    }
    if (buf.length) out.push(`<p>${inline(buf.join(' '))}</p>`);
    else i++;
  }

  return out.join('\n');
}
