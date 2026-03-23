# 小皮OS · 三省六部管理系统 - 设计规范

> 版本：v1.0  
> 来源：小皮OS-完整可交互原型-最终版.html  
> 更新：2026-03-22

---

## 1. 色彩系统（Color Palette）

### 主色调
| Token | Hex | 用途 |
|-------|-----|------|
| `--bg` | `#07090f` | 页面背景 |
| `--panel` | `#0f1219` | 卡片/面板背景 |
| `--panel2` | `#141824` | 次级面板/输入框背景 |
| `--line` | `#1c2236` | 边框/分割线 |

### 文字色
| Token | Hex | 用途 |
|-------|-----|------|
| `--text` | `#dde4f8` | 主文字 |
| `--muted` | `#5a6b92` | 次级文字/占位符 |

### 功能色
| Token | Hex | 用途 |
|-------|-----|------|
| `--ok` | `#2ecc8a` | 成功/完成状态 |
| `--warn` | `#f5c842` | 警告/进行中 |
| `--danger` | `#ff5270` | 错误/紧急 |
| `--acc` | `#6a9eff` | 主强调色/链接 |
| `--acc2` | `#a07aff` | 次强调色/渐变 |

---

## 2. 文字系统（Typography）

### 字体
```css
font-family: PingFang SC, Inter, -apple-system, Segoe UI, sans-serif;
```

### 字号规范
| Token | 大小 | 用途 |
|-------|------|------|
| `logo` | 20px / 800 | Logo主标题 |
| `h2` | 18px / 800 | 页面标题 |
| `card-title` | 14px / 700 | 卡片标题 |
| `body` | 13-14px / 600 | 正文/按钮 |
| `small` | 11-12px | 次级信息 |
| `micro` | 9-10px | 标签/徽章 |

### 行高
- 标题：`1.3-1.4`
- 正文：`1.5`

---

## 3. 间距系统（Spacing）

### 基础单位：4px

| Token | 值 | 用途 |
|-------|-----|------|
| `xs` | 4px | 微间距 |
| `sm` | 6-8px | 紧凑间距 |
| `md` | 10-12px | 标准间距 |
| `lg` | 14-18px | 宽松间距 |
| `xl` | 20px+ | 大间距 |

### 常用间距
- 卡片内边距：`18px`
- 卡片间距：`16px`
- 网格间距：`12px`
- 按钮内边距：`6px 14px`

---

## 4. 圆角系统（Border Radius）

| Token | 值 | 用途 |
|-------|-----|------|
| `sm` | 4-6px | 徽章/小按钮 |
| `md` | 8-10px | 按钮/输入框 |
| `lg` | 12-14px | 卡片/面板 |
| `xl` | 18px | 模态框 |
| `full` | 999px | 药丸形/胶囊按钮 |

---

## 5. 阴影系统（Shadows）

### Hover 效果
```css
/* 卡片悬停 */
box-shadow: 0 4px 20px #6a9eff1a;
transform: translateY(-2px);

/* 模态框 */
box-shadow: 0 20px 60px #0009;
```

---

## 6. 动效系统（Animation）

### 时长
| Token | 值 | 用途 |
|-------|-----|------|
| `fast` | 0.12s | 微交互 |
| `normal` | 0.15s | 默认过渡 |
| `slow` | 0.2s | 页面切换 |

### 缓动
```css
transition: all 0.15s;  /* 默认 */
animation: fadeIn 0.2s;  /* 淡入 */
animation: tin 0.2s;     /* Toast滑入 */
```

### 动画定义
```css
/* 淡入 */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Toast滑入 */
@keyframes tin {
  from { transform: translate(40px); opacity: 0; }
  to { transform: translate(0); opacity: 1; }
}

/* 脉冲 */
@keyframes pulse {
  0%, to { opacity: 1; }
  50% { opacity: 0.4; }
}
```

---

## 7. 组件库（Components）

### 7.1 按钮（Button）

#### 主要按钮 `.btn-p`
```css
background: var(--acc);  /* #6a9eff */
color: #000;
border-radius: 8px;
padding: 6px 14px;
font-weight: 600;
```

#### 次级按钮 `.btn-g`
```css
background: transparent;
border: 1px solid var(--line);  /* #1c2236 */
color: var(--muted);
```

#### 成功按钮 `.btn-ok`
```css
background: #2ecc8a22;
color: var(--ok);
border: 1px solid #2ecc8a44;
```

#### 警告按钮 `.btn-warn`
```css
background: #f5c84222;
color: var(--warn);
border: 1px solid #f5c84244;
```

#### 危险按钮 `.btn-danger`
```css
background: #ff527022;
color: var(--danger);
border: 1px solid #ff527044;
```

#### 悬停状态
```css
.btn-p:hover { filter: brightness(1.15); }
.btn-g:hover { border-color: #2e3d6a; color: var(--text); }
```

---

### 7.2 标签/徽章（Tag/Badge）

#### 优先级标签
| 类名 | 边框色 | 文字色 | 背景色 |
|------|--------|--------|--------|
| `.st-P0` | `#ff527044` | `--danger` | `#280a10` |
| `.st-P1` | `#f5c84244` | `--warn` | `#201a08` |
| `.st-P2` | `#6a9eff44` | `--acc` | `#0a1428` |

#### 状态标签
| 类名 | 用途 |
|------|------|
| `.st-Inbox` | 待派发 |
| `.st-Doing` | 进行中 |
| `.st-Review` | 待验收 |
| `.st-Done` | 已完成 |
| `.st-Blocked` | 阻塞 |

#### 部门标签
| 类名 | 颜色 |
|------|------|
| `.dt-中书省` | `#a07aff` 紫色 |
| `.dt-门下省` | `#6a9eff` 蓝色 |
| `.dt-尚书省` | `#6aef9a` 绿色 |
| `.dt-礼部` | `#f5c842` 黄色 |
| `.dt-兵部` | `#ff5270` 红色 |
| `.dt-刑部` | `#c44` 深红 |
| `.dt-工部` | `#4af` 青色 |

#### 药丸徽章 `.chip`
```css
font-size: 11px;
padding: 3px 9px;
border: 1px solid var(--line);
border-radius: 999px;
background: var(--panel);
color: var(--muted);
```

#### 状态徽章 `.hb`
```css
font-size: 10px;
padding: 2px 7px;
border-radius: 999px;
border: 1px solid var(--line);

/* 激活态 */
.hb.active { border-color: #2ecc8a44; color: var(--ok); }
.hb.warn { border-color: #f5c84244; color: var(--warn); }
.hb.stalled { border-color: #ff527044; color: var(--danger); }
```

---

### 7.3 卡片（Card）

#### 基础卡片 `.card`
```css
background: var(--panel);
border: 1px solid var(--line);
border-radius: 14px;
padding: 18px;
margin-bottom: 16px;
```

#### 卡片头部 `.card-header`
```css
display: flex;
align-items: center;
justify-content: space-between;
margin-bottom: 14px;
```

#### 统计卡片 `.stat-card`
```css
/* 悬停效果 */
.stat-card:hover {
  border-color: var(--acc);
  transform: translateY(-2px);
}
```

---

### 7.4 表单（Form）

#### 输入框 `.form-input`
```css
width: 100%;
padding: 10px 14px;
background: var(--panel2);
border: 1px solid var(--line);
border-radius: 8px;
color: var(--text);
font-size: 14px;
outline: none;
transition: border-color 0.15s;
```

#### 聚焦状态
```css
.form-input:focus {
  border-color: var(--acc);
}
```

#### 标签 `.form-label`
```css
display: block;
font-size: 12px;
font-weight: 600;
color: var(--muted);
margin-bottom: 8px;
text-transform: uppercase;
letter-spacing: 0.05em;
```

---

### 7.5 模态框（Modal）

#### 遮罩层 `.modal-bg`
```css
position: fixed;
top: 0; right: 0; bottom: 0; left: 0;
background: #000000b3;
backdrop-filter: blur(3px);
z-index: 100;
```

#### 模态框体 `.modal`
```css
background: var(--panel);
border: 1px solid var(--line);
border-radius: 18px;
max-width: 760px;
padding: 28px;
box-shadow: 0 20px 60px #0009;
animation: fadeIn 0.2s;
```

---

### 7.6 流程组件

#### 流程节点 `.ep-node`
```css
/* 完成态 */
.ep-node.done {
  background: #0a2018;
}

/* 激活态 */
.ep-node.active {
  background: #0f1a38;
  border: 1px solid var(--acc);
}

/* 待处理态 */
.ep-node.pending {
  opacity: 0.3;
}
```

#### 流程状态 `.flow-status`
```css
.flow-status.done {
  background: #0a2018;
  color: var(--ok);
  border: 1px solid #2ecc8a44;
}

.flow-status.active {
  background: #0a1428;
  color: var(--acc);
  border: 1px solid var(--acc);
  animation: pulse 1.5s infinite;
}
```

---

### 7.7 看板（Kanban）

#### 看板列 `.kanban-col`
```css
background: var(--panel);
border: 1px solid var(--line);
border-radius: 14px;
overflow: hidden;
```

#### 看板卡片 `.kanban-card`
```css
background: var(--panel2);
border: 1px solid var(--line);
border-radius: 10px;
padding: 12px;
cursor: pointer;
transition: all 0.15s;
```

---

### 7.8 列表（List）

#### 列表项 `.list-item`
```css
display: flex;
align-items: center;
justify-content: space-between;
padding: 12px 0;
border-bottom: 1px solid var(--line);
```

---

### 7.9 Toast 通知

#### Toast容器 `.toaster`
```css
position: fixed;
bottom: 20px;
right: 20px;
display: flex;
flex-direction: column;
gap: 8px;
z-index: 300;
```

#### Toast项 `.toast`
```css
font-size: 13px;
padding: 10px 16px;
border-radius: 10px;
border: 1px solid var(--line);
background: var(--panel);
color: var(--text);
box-shadow: 0 4px 20px #0006;
animation: tin 0.2s;
```

---

## 8. 布局系统（Layout）

### 容器
```css
.wrap {
  max-width: 1400px;
  margin: 0 auto;
  padding: 16px;
}
```

### 响应式断点
```css
@media (max-width: 768px) {
  .stats-grid { grid-template-columns: repeat(2, 1fr); }
  .kanban { grid-template-columns: repeat(2, 1fr); }
  .grid-2 { grid-template-columns: 1fr; }
  .form-row { grid-template-columns: 1fr; }
  .edict-grid { grid-template-columns: 1fr; }
}
```

### 网格布局
```css
/* 双列 */
.grid-2 {
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

/* 四列统计 */
.stats-grid {
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
}

/* 看板四列 */
.kanban {
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
}

/* 旨意网格 */
.edict-grid {
  grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
  gap: 12px;
}
```

---

## 9. 滚动条样式

```css
::-webkit-scrollbar {
  width: 4px;
  height: 4px;
}
::-webkit-scrollbar-track {
  background: transparent;
}
::-webkit-scrollbar-thumb {
  background: #1e2538;
  border-radius: 4px;
}
```

---

## 10. 图标规范

本原型使用 Emoji 作为图标：

### 页面导航
| 图标 | 用途 |
|------|------|
| 📊 | 仪表盘 |
| 📜 | 旨意看板 |
| 📋 | 任务看板 |
| 📚 | 档案馆 |
| ⚙️ | 配置中心 |

### 状态指示
| 图标 | 用途 |
|------|------|
| ● | 状态点（绿=正常，红=异常，黄=警告） |
| ✓ | 完成 |
| ⏰ | 等待/待处理 |
| ⚠️ | 警告 |
| ✕ | 关闭/删除 |

### 部门图标
| 图标 | 部门 |
|------|------|
| 🀄 | 中书省/门下省/尚书省 |
| ⚔️ | 兵部/刑部/工部 |
| 🎨 | 礼部 |

---

## 附录：完整 CSS 变量表

### 深色主题（默认 Dark Mode）
```css
:root {
  /* 背景色 */
  --bg: #07090f;
  --panel: #0f1219;
  --panel2: #141824;
  --line: #1c2236;
  
  /* 文字色 */
  --text: #dde4f8;
  --muted: #5a6b92;
  
  /* 功能色 */
  --ok: #2ecc8a;
  --warn: #f5c842;
  --danger: #ff5270;
  --acc: #6a9eff;
  --acc2: #a07aff;
  
  /* 阴影 */
  --shadow: rgba(0, 0, 0, 0.4);
  --shadow-hover: rgba(106, 158, 255, 0.1);
}
```

### 浅色主题（Light Mode）
```css
[data-theme="light"] {
  /* 背景色 - 浅色系 */
  --bg: #f5f7fa;
  --panel: #ffffff;
  --panel2: #f0f2f5;
  --line: #e4e8ef;
  
  /* 文字色 - 深色系 */
  --text: #1a1d26;
  --muted: #6b7280;
  
  /* 功能色 - 保持对比度 */
  --ok: #10b981;
  --warn: #f59e0b;
  --danger: #ef4444;
  --acc: #3b82f6;
  --acc2: #8b5cf6;
  
  /* 阴影 - 浅色更明显 */
  --shadow: rgba(0, 0, 0, 0.08);
  --shadow-hover: rgba(59, 130, 246, 0.15);
}
```

---

## 11. 明暗色主题切换规范

### 11.1 主题变量映射表

| 用途 | 深色主题 (Dark) | 浅色主题 (Light) |
|------|-----------------|------------------|
| 页面背景 | `#07090f` | `#f5f7fa` |
| 卡片背景 | `#0f1219` | `#ffffff` |
| 次级面板 | `#141824` | `#f0f2f5` |
| 边框/分割线 | `#1c2236` | `#e4e8ef` |
| 主文字 | `#dde4f8` | `#1a1d26` |
| 次级文字 | `#5a6b92` | `#6b7280` |
| 成功色 | `#2ecc8a` | `#10b981` |
| 警告色 | `#f5c842` | `#f59e0b` |
| 危险色 | `#ff5270` | `#ef4444` |
| 主强调色 | `#6a9eff` | `#3b82f6` |
| 次强调色 | `#a07aff` | `#8b5cf6` |

### 11.2 浅色主题组件样式

#### 卡片 `.card`（浅色）
```css
[data-theme="light"] .card {
  background: #ffffff;
  border: 1px solid #e4e8ef;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}
```

#### 按钮（浅色）
```css
[data-theme="light"] .btn-p {
  background: #3b82f6;
  color: #ffffff;
}

[data-theme="light"] .btn-g {
  background: transparent;
  border: 1px solid #e4e8ef;
  color: #6b7280;
}

[data-theme="light"] .btn-g:hover {
  border-color: #3b82f6;
  color: #1a1d26;
}
```

#### 输入框（浅色）
```css
[data-theme="light"] .form-input {
  background: #f0f2f5;
  border: 1px solid #e4e8ef;
  color: #1a1d26;
}

[data-theme="light"] .form-input:focus {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}
```

#### 模态框（浅色）
```css
[data-theme="light"] .modal-bg {
  background: rgba(0, 0, 0, 0.5);
}

[data-theme="light"] .modal {
  background: #ffffff;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
}
```

#### 看板卡片（浅色）
```css
[data-theme="light"] .kanban-card {
  background: #f0f2f5;
  border: 1px solid #e4e8ef;
}

[data-theme="light"] .kanban-card:hover {
  border-color: #3b82f6;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.1);
}
```

### 11.3 主题切换实现方式

#### HTML 属性切换
```html
<!-- 深色主题（默认） -->
<html>

<!-- 浅色主题 -->
<html data-theme="light">
```

#### JavaScript 切换
```javascript
function toggleTheme() {
  const html = document.documentElement;
  const current = html.getAttribute('data-theme');
  const next = current === 'light' ? 'dark' : 'light';
  html.setAttribute('data-theme', next);
  localStorage.setItem('theme', next);
}

// 页面加载时恢复主题
document.addEventListener('DOMContentLoaded', () => {
  const saved = localStorage.getItem('theme') || 'dark';
  document.documentElement.setAttribute('data-theme', saved);
});
```

#### CSS 变量自动切换
```css
/* 根据系统偏好自动选择 */
@media (prefers-color-scheme: light) {
  :root:not([data-theme="dark"]) {
    /* 浅色变量 */
    --bg: #f5f7fa;
    --panel: #ffffff;
    /* ... */
  }
}
```

### 11.4 部门标签浅色版本

| 部门 | 深色背景 | 浅色背景 |
|------|----------|----------|
| 中书省 | `#1a0f38` | `#f3e8ff` |
| 门下省 | `#0f1a38` | `#dbeafe` |
| 尚书省 | `#0a2018` | `#d1fae5` |
| 礼部 | `#201a08` | `#fef3c7` |
| 兵部 | `#280a10` | `#fee2e2` |
| 刑部 | `#280808` | `#fecaca` |
| 工部 | `#081828` | `#e0f2fe` |

### 11.5 优先级标签浅色版本

| 优先级 | 深色背景 | 浅色背景 |
|--------|----------|----------|
| P0 | `#280a10` | `#fee2e2` |
| P1 | `#201a08` | `#fef3c7` |
| P2 | `#0a1428` | `#dbeafe` |

### 11.6 滚动条浅色版本

```css
[data-theme="light"] ::-webkit-scrollbar-thumb {
  background: #d1d5db;
}

[data-theme="light"] ::-webkit-scrollbar-thumb:hover {
  background: #9ca3af;
}
```

---

## 12. 主题使用建议

### 12.1 场景推荐

| 场景 | 推荐主题 |
|------|----------|
| 夜间/暗光环境 | 深色主题（护眼） |
| 白天/强光环境 | 浅色主题（清晰） |
| 长时间办公 | 浅色主题（减少视觉疲劳） |
| 演示/展示 | 浅色主题（更正式） |

### 12.2 切换按钮位置

建议在页面头部（header）放置主题切换按钮：
- 位置：Logo 右侧
- 图标：☀️ / 🌙
- 状态：跟随当前主题显示相反图标

### 12.3 主题持久化

```javascript
// 优先级：用户选择 > 系统偏好 > 默认深色
const getPreferredTheme = () => {
  const saved = localStorage.getItem('theme');
  if (saved) return saved;
  return window.matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark';
};
```
