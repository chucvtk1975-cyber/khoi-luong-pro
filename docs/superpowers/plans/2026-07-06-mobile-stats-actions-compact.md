# Mobile Stats Compact & Full-Width Actions Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Thu nho 4 o thong ke ~50% chieu cao, mo rong hang nut hanh dong full-width, va bat cuon toan trang tren mobile.

**Architecture:** Sua doi style.css (CSS-only cho stats va scroll), sua doi index.html (them 2 wrapper div cho project-actions), them CSS cho wrapper moi trong style.css.

**Tech Stack:** Vanilla CSS, HTML5.

## Global Constraints

- Khong tu y thay doi code da hoan tat ngoai pham vi yeu cau.
- Cap nhat tham so ?v=... trong index.html sau khi sua style.css.
- Khong anh huong den desktop (chi ap dung cho media max-width: 600px).

---

### Task 1: Thu nho 4 o thong ke

**Files:**
- Modify: `style.css` (dong 413-443)

- [ ] **Step 1: Sua CSS stats-bar va stat-item**

Tim doan CSS hien tai (dong ~413-443) trong style.css:
```css
/* ========== STATS BAR ========== */
.stats-bar {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
  margin-bottom: 20px;
}
.stat-item {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 14px 16px;
  text-align: center;
  transition: border-color 0.2s;
}
.stat-item:hover { border-color: var(--brand-blue); }
.stat-value {
  display: block;
  font-size: 22px;
  font-weight: 700;
  color: var(--brand-blue-light);
  line-height: 1.1;
  margin-bottom: 4px;
}
.stat-label {
  font-size: 10px;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.6px;
  font-weight: 500;
}
```

Them vao cuoi block @media (max-width: 600px) (dong ~1449-1456 trong style.css):
```css
  /* === STATS COMPACT (mobile) === */
  .stats-bar {
    gap: 8px;
    margin-bottom: 10px;
  }
  .stat-item {
    padding: 8px 10px;
  }
  .stat-value {
    font-size: 16px;
    margin-bottom: 2px;
  }
  .stat-label {
    font-size: 9px;
  }
```

- [ ] **Step 2: Kiem tra cu phap**

```bash
node -c src/takeoff.js
```
Expected: Khong co loi cu phap.

- [ ] **Step 3: Commit**

```bash
git add style.css
git commit -m "feat: compact stats bar on mobile (~50% height reduction)"
```

---

### Task 2: Mo rong hang nut hanh dong full-width

**Files:**
- Modify: `index.html` (dong ~881-912)
- Modify: `style.css` (them CSS cho .project-btn-row va .project-filter-row)

- [ ] **Step 1: Sua HTML - Them 2 wrapper div**

Tim doan HTML hien tai trong index.html (dong ~881-912):
```html
<div class="project-actions" style="flex-wrap:wrap;gap:8px;">
  <button class="btn-secondary btn-sm" id="btn-edit-project">
    <i data-lucide="edit-2"></i> Sua
  </button>
  <button class="btn-danger btn-sm" id="btn-delete-project">
    <i data-lucide="trash-2"></i> Xoa
  </button>
  <button class="btn-outline btn-sm" onclick="docDepBoNho()" style="font-size:12px;padding:5px 10px;border-color:var(--border-color);color:var(--text-secondary);background:var(--bg-card);" title="Don dep bo nho dem hinh anh khao sat">
    <i data-lucide="trash"></i> Don bo nho
  </button>
  <div style="display:flex;align-items:center;gap:6px;border-left:1px solid var(--border-color);padding-left:8px;margin-left:2px;">
    <label style="font-size:12px;color:var(--text-secondary);white-space:nowrap;">Loc phong:</label>
    <select id="boq-room-filter" onchange="filterBOQByRoom(this.value)"
      style="background:var(--bg-card);color:var(--text-main);border:1px solid var(--border-color);padding:5px 10px;border-radius:4px;font-size:12px;outline:none;cursor:pointer;">
      <option value="all">File tong</option>
    </select>
  </div>
</div>
```

Thay the bang (xoa inline style tren project-actions, them 2 wrapper):
```html
<div class="project-actions">

  <div class="project-btn-row">

    <button class="btn-secondary btn-sm" id="btn-edit-project">
      <i data-lucide="edit-2"></i> Sua
    </button>

    <button class="btn-danger btn-sm" id="btn-delete-project">
      <i data-lucide="trash-2"></i> Xoa
    </button>

    <button class="btn-outline btn-sm" onclick="docDepBoNho()" style="font-size:12px;border-color:var(--border-color);color:var(--text-secondary);background:var(--bg-card);" title="Don dep bo nho dem hinh anh khao sat">
      <i data-lucide="trash"></i> Don bo nho
    </button>

  </div>

  <div class="project-filter-row">

    <label style="font-size:12px;color:var(--text-secondary);white-space:nowrap;">Loc phong:</label>

    <select id="boq-room-filter" onchange="filterBOQByRoom(this.value)"
      style="background:var(--bg-card);color:var(--text-main);border:1px solid var(--border-color);padding:5px 10px;border-radius:4px;font-size:12px;outline:none;cursor:pointer;">
      <option value="all">File tong</option>
    </select>

  </div>

</div>
```

- [ ] **Step 2: Them CSS cho project-btn-row va project-filter-row**

Them vao sau rule `.project-actions` trong style.css (sau dong ~412):
```css
.project-btn-row {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}
.project-filter-row {
  display: flex;
  align-items: center;
  gap: 6px;
  border-left: 1px solid var(--border-color);
  padding-left: 8px;
  margin-left: 2px;
}
.project-filter-row select {
  flex: 1;
}
```

Them vao trong @media (max-width: 600px):
```css
  /* === ACTION BUTTONS FULL-WIDTH (mobile) === */
  .project-actions {
    flex-direction: column;
    width: 100%;
    gap: 8px;
  }
  .project-btn-row {
    width: 100%;
  }
  .project-btn-row .btn-secondary,
  .project-btn-row .btn-danger,
  .project-btn-row .btn-outline {
    flex: 1;
    justify-content: center;
    min-height: 42px;
    padding: 8px 6px !important;
    font-size: 12px !important;
  }
  .project-filter-row {
    width: 100%;
    border-left: none;
    padding-left: 0;
    margin-left: 0;
  }
  .project-filter-row select {
    flex: 1;
    min-height: 42px;
    font-size: 14px !important;
  }
```

- [ ] **Step 3: Kiem tra cu phap va cau truc HTML**

```bash
node -c src/takeoff.js
python check_final.py
```
Expected: Khong co loi.

- [ ] **Step 4: Commit**

```bash
git add index.html style.css
git commit -m "feat: full-width action buttons and filter row on mobile"
```

---

### Task 3: Bat cuon toan trang tren mobile

**Files:**
- Modify: `style.css` (them vao @media max-width: 600px)

- [ ] **Step 1: Them CSS cho cuon toan trang**

Tim block @media (max-width: 600px) hien tai trong style.css (dong ~1449-1456):
```css
@media (max-width: 600px) {
  .main-layout { flex-direction: column; }
  .project-sidebar { width: 100%; height: 160px; border-right: none; border-bottom: 1px solid var(--border); }
  .project-list { display: flex; gap: 6px; flex-direction: row; overflow-x: auto; overflow-y: hidden; }
  .project-item { flex-shrink: 0; }
  /* Cho phep cuon trang chinh tren mobile */
  body { overflow: auto !important; -webkit-overflow-scrolling: touch; }
}
```

Them vao TRONG block @media nay (truoc dau dong):
```css
  /* === FULL PAGE SCROLL (mobile) === */
  .app-wrapper { height: auto !important; overflow: visible !important; }
  .main-layout { overflow: visible !important; }
  .workspace { overflow-y: visible !important; height: auto !important; }
```

- [ ] **Step 2: Cap nhat cache-buster trong index.html**

Tim dong script main.js trong index.html:
```html
<script src="main.js?v=...
```
Tang so phien ban len 1 don vi (vi du ?v=2.4.1 -> ?v=2.4.2).

- [ ] **Step 3: Kiem tra**

```bash
python check_final.py
```
Expected: Khong co loi.

- [ ] **Step 4: Commit**

```bash
git add style.css index.html
git commit -m "feat: enable full-page scroll on mobile"
```

---

## Kiem tra Tong Hop Sau Khi Hoan Thanh

- [ ] Mo DevTools Chrome -> Toggle device toolbar -> chon iPhone 12 Pro (390px)
- [ ] Xac nhan 4 o thong ke nho gon, doc so ro rang
- [ ] Xac nhan 3 nut Sua/Xoa/Don bo nho chiem full chieu ngang, cao >= 42px
- [ ] Xac nhan Loc phong select chiem full chieu ngang
- [ ] Cuon trang tu tren xuong duoi: header -> stats -> tabs -> bang KL
- [ ] Kiem tra desktop (Chrome, 1280px): khong bi anh huong
