// 全局常量与默认设置
export const DATA_URL = './data/latest.json';

export const CATEGORY_LABEL = {
  ai_skill: 'AI Skill',
  burst: '爆发',
  growth: '学习成长',
  classic: '经典',
};

// 「国内加速」链接：GitHub 镜像站
export function mirrorUrl(owner, name) {
  return `https://bgithub.xyz/${owner}/${name}`;
}

// 爆发指数进度条需要一个参照上限，用于把分数画成进度条长度
export const BURST_BAR_MAX = 200;

// Obsidian 默认设置（库名做成设置项，不硬编码）
export const DEFAULT_SETTINGS = {
  obsidianVault: '',
  obsidianFolder: 'GitHub雷达',
};

// 筛选栏默认值（会被记住，下次打开保持）
export const DEFAULT_FILTERS = {
  cat: 'all',
  lang: '',
  time: 'all',
  sort: 'score',
  sortDir: 'desc',
  q: '',
  unreadOnly: false,
  starredOnly: false,
};

// 阅读状态
export const READ_STATE_LABEL = {
  unread: '未读',
  reading: '在读',
  done: '已读',
};

// Obsidian URI 的长度上限（超过就截断，并在末尾附完整链接）
export const OBSIDIAN_URI_SOFT_LIMIT = 2000;

export const STORAGE_KEYS = {
  starred: 'ghradar.starred.v1',
  read: 'ghradar.read.v1',
  feedback: 'ghradar.feedback.v1',
  notes: 'ghradar.notes.v1',
  filters: 'ghradar.filters.v1',
  settings: 'ghradar.settings.v1',
  preferences: 'ghradar.preferences.v1',
  theme: 'ghradar.theme.v1',
};
