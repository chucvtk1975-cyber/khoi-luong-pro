# Thiết kế Sidebar theo Mẫu & Căn giữa Logo Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Đồng bộ thiết kế Sidebar trái của Workspace theo đúng hình ảnh mẫu (card bo góc viền cam khi active, có icon folder, khách hàng và ngày tháng) và đưa logo Blue Decor vào vị trí căn giữa Header.

**Architecture:** Cấu trúc lại thanh Header trong HTML để chuyển logo vào giữa, sửa đổi CSS Header. Cấu trúc lại Sidebar Header bằng HTML để hiển thị thương hiệu, ô tìm kiếm và sắp xếp. Sửa đổi CSS Sidebar để tạo các card dự án bo góc có viền cam phát sáng khi active. Sửa đổi JS để render dữ liệu động theo thiết kế mới và hỗ trợ lọc/sắp xếp trực tiếp trên sidebar.

**Tech Stack:** HTML5, CSS3, JavaScript (SheetJS, Lucide).

## Global Constraints
- Giữ nguyên các chức năng cốt lõi của ứng dụng.
- Đảm bảo tương thích với dữ liệu dự án hiện có (`p.client`, `p.date`, `s.rooms`).

---

### Task 1: Cấu trúc lại Header và Sidebar trong HTML

**Files:**
- Modify: `index.html:737-783`

**Interfaces:**
- Consumes: Cấu trúc HTML hiện tại của app-header và project-sidebar.
- Produces: Giao diện tĩnh mới cho Header (logo căn giữa) và Sidebar (branding, search box, sort controls, plus button).

- [ ] **Step 1: Cập nhật cấu trúc Header và Sidebar trong `index.html`**

Thay thế khối `<header class="app-header">` và `<aside class="project-sidebar">` trong `index.html`:
```html
    <header class="app-header">

      <div class="header-brand">
        <!-- Để trống hoặc nút back tùy ý, giữ cấu trúc flex -->
      </div>

      <div class="header-center">
        <img src="logo-bluedecor.png" alt="Blue Decor" style="height:42px;object-fit:contain;display:block;">
      </div>

      <div class="header-actions">

        <span class="header-badge" id="header-project-count">0 dự án</span>

        <a href="../index.html" class="btn-ghost">

          <i data-lucide="arrow-left"></i> Trợ Lý Thuế

        </a>

      </div>

    </header>

    <!-- Layout chính -->

    <div class="main-layout">

      <!-- Sidebar dự án -->

      <aside class="project-sidebar">

        <div class="sidebar-brand-area">
          <div class="brand-icon-orange">
            <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="2" width="16" height="20" rx="2" ry="2"></rect><line x1="9" y1="22" x2="9" y2="16"></line><line x1="15" y1="22" x2="15" y2="16"></line><line x1="9" y1="16" x2="15" y2="16"></line><path d="M9 12h.01"></path><path d="M15 12h.01"></path><path d="M9 8h.01"></path><path d="M15 8h.01"></path></svg>
          </div>
          <div class="brand-info">
            <div class="brand-title-row">
              <span class="brand-title">BỐC KHỐI LƯỢNG PRO</span>
              <span class="brand-version">v1.2</span>
            </div>
            <div class="brand-copyright">Bản quyền thuộc BluDecor Design & Build</div>
          </div>
        </div>

        <div class="sidebar-controls">
          <div class="sidebar-search-wrapper">
            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="search-icon"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
            <input type="text" id="sidebar-project-search" placeholder="Tìm dự án..." oninput="renderProjectList()">
          </div>
          
          <div class="sidebar-sort-row">
            <div class="sidebar-sort-label">Sắp xếp theo:</div>
            <select id="sidebar-project-sort" onchange="renderProjectList()" class="sidebar-sort-select">
              <option value="newest">Mới nhất</option>
              <option value="az">A → Z</option>
              <option value="za">Z → A</option>
            </select>
            <button class="btn-icon-sm" id="btn-new-project" title="Tạo dự án mới" style="margin-left: auto;">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
            </button>
          </div>
        </div>

        <div class="project-list" id="project-list"></div>

      </aside>
```

- [ ] **Step 2: Kiểm tra cấu trúc đóng mở HTML**

Run: `python check_final.py`
Expected: `Modal divs: opens=92, closes=92, net=0`
```bash
git add index.html
git commit -m "style: structure Header logo and Sidebar static elements in HTML"
```

---

### Task 2: Áp dụng CSS mới cho Sidebar và Cards Dự Án

**Files:**
- Modify: `style.css`

**Interfaces:**
- Consumes: Cấu trúc HTML của Header và Sidebar.
- Produces: CSS hiển thị đúng dải màu navy đậm, bo góc tròn card, viền cam cho card active, chữ tương phản tốt.

- [ ] **Step 1: Viết CSS cho các phần tử Sidebar mới**

Sửa đổi phần CSS Sidebar trong `style.css` (bắt đầu từ `.project-sidebar` khoảng dòng 158):
```css
.project-sidebar {
  width: 280px;
  background: #111827; /* Nền tối sâu Slate 950 */
  border-right: 1px solid #1F2937;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  flex-shrink: 0;
  padding: 16px 12px;
}
.sidebar-brand-area {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 16px;
}
.brand-icon-orange {
  width: 38px;
  height: 38px;
  background: #F97316; /* Màu cam thương hiệu */
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #FFFFFF;
  box-shadow: 0 4px 10px rgba(249, 115, 22, 0.3);
}
.brand-info {
  display: flex;
  flex-direction: column;
  flex: 1;
}
.brand-title-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 4px;
}
.brand-title {
  font-size: 13px;
  font-weight: 800;
  color: #FFFFFF;
  letter-spacing: 0.5px;
}
.brand-version {
  font-size: 10px;
  font-weight: 700;
  background: rgba(249, 115, 22, 0.2);
  color: #F97316;
  padding: 1px 5px;
  border-radius: 4px;
}
.brand-copyright {
  font-size: 10px;
  color: #9CA3AF;
  margin-top: 2px;
}
.sidebar-controls {
  margin-bottom: 16px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.sidebar-search-wrapper {
  position: relative;
  width: 100%;
}
.sidebar-search-wrapper .search-icon {
  position: absolute;
  left: 10px;
  top: 50%;
  transform: translateY(-50%);
  color: #9CA3AF;
}
.sidebar-search-wrapper input {
  width: 100%;
  padding: 8px 12px 8px 32px;
  background: #1F2937;
  border: 1px solid #F97316; /* Viền cam đất theo mẫu */
  border-radius: 20px;
  color: #FFFFFF;
  font-size: 12px;
  outline: none;
  transition: all 0.2s ease;
}
.sidebar-search-wrapper input:focus {
  box-shadow: 0 0 0 2px rgba(249, 115, 22, 0.2);
}
.sidebar-sort-row {
  display: flex;
  align-items: center;
  gap: 6px;
}
.sidebar-sort-label {
  font-size: 11px;
  color: #9CA3AF;
}
.sidebar-sort-select {
  background: transparent;
  border: none;
  color: #FFFFFF;
  font-size: 11px;
  font-weight: 700;
  cursor: pointer;
  outline: none;
}
.sidebar-sort-select option {
  background: #111827;
  color: #FFFFFF;
}

/* Thẻ dự án kiểu mới */
.project-list {
  flex: 1;
  overflow-y: auto;
  padding-right: 4px;
}
.project-item {
  padding: 14px 16px;
  border-radius: 12px; /* Bo góc card */
  background: #1F2937; /* Nền card xám tối */
  border: 1px solid transparent;
  margin-bottom: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.project-item:hover {
  background: #374151;
}
.project-item.active {
  background: #1E293B; /* Navy tối sâu */
  border-color: #F97316; /* Viền cam rực rỡ */
  box-shadow: 0 4px 12px rgba(249, 115, 22, 0.15);
}
.project-item-title-row {
  display: flex;
  align-items: center;
  gap: 8px;
}
.project-folder-icon {
  color: #9CA3AF;
  flex-shrink: 0;
}
.project-item.active .project-folder-icon {
  color: #F97316; /* Folder màu cam */
}
.project-item-name {
  font-weight: 700;
  font-size: 13px;
  color: #FFFFFF; /* Mặc định chữ trắng */
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  margin-bottom: 0; /* Override */
}
.project-item.active .project-item-name {
  color: #F97316; /* Active thì tên màu cam */
}
.project-item-client {
  font-size: 11px;
  color: #9CA3AF;
}
.project-item-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 4px;
}
.project-item-date {
  font-size: 11px;
  color: #6B7280;
}
.project-item-rooms-badge {
  font-size: 10px;
  font-weight: 700;
  background: #374151;
  color: #D1D5DB;
  padding: 2px 8px;
  border-radius: 10px;
}
.project-item.active .project-item-rooms-badge {
  background: #111827;
  color: #93C5FD;
}
```

- [ ] **Step 2: Commit**

```bash
git add style.css
git commit -m "style: apply high fidelity sidebar card styles matching mockup"
```

---

### Task 3: Cập nhật JavaScript để Render Dữ Liệu và Hỗ Trợ Tìm Kiếm/Sắp Xếp

**Files:**
- Modify: `app.js:1980-2050`

**Interfaces:**
- Consumes: Hàm render và các tham số lọc/sắp xếp của sidebar.
- Produces: Giao diện động của danh sách dự án bao gồm icon folder, ngày tạo, khách hàng, số phòng.

- [ ] **Step 1: Cập nhật hàm `renderProjectList` trong `app.js`**

Thay thế hoàn toàn hàm `renderProjectList` để hỗ trợ tìm kiếm, sắp xếp và render các card dự án chi tiết:
```javascript
function renderProjectList() {
  const allProjects = DB.all();
  const list = document.getElementById('project-list');
  const badge = document.getElementById('header-project-count');
  
  if (badge) {
    badge.textContent = `${allProjects.length} dự án`;
  }

  if (allProjects.length === 0) {
    list.innerHTML = `<p style="padding:20px;text-align:center;color:var(--text-muted);font-size:12px;">Chưa có dự án nào</p>`;
    return;
  }

  // 1. Lấy thông tin tìm kiếm và sắp xếp từ UI
  const searchInput = document.getElementById('sidebar-project-search');
  const query = searchInput ? searchInput.value.toLowerCase().trim() : '';

  const sortSelect = document.getElementById('sidebar-project-sort');
  const sortMode = sortSelect ? sortSelect.value : 'newest';

  // 2. Lọc danh sách dự án
  let filtered = allProjects.filter(p => {
    const matchQuery = !query || 
      p.name.toLowerCase().includes(query) || 
      (p.client && p.client.toLowerCase().includes(query));
    return matchQuery;
  });

  // 3. Sắp xếp danh sách dự án
  filtered.sort((a, b) => {
    if (sortMode === 'az') return a.name.localeCompare(b.name, 'vi');
    if (sortMode === 'za') return b.name.localeCompare(a.name, 'vi');
    // newest: mặc định theo ngày tạo mới nhất (hoặc id giảm dần)
    const timeA = a.date ? new Date(a.date).getTime() : 0;
    const timeB = b.date ? new Date(b.date).getTime() : 0;
    return timeB - timeA;
  });

  // 4. Render danh sách dự án
  list.innerHTML = filtered.map(p => {
    const s = CALC.project(p);
    const active = p.id === state.currentProjectId;
    const folderIconSvg = `
      <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="project-folder-icon">
        <path d="M4 20h16a2 2 0 0 0 2-2V8a2 2 0 0 0-2-2h-7.93a2 2 0 0 1-1.66-.9l-.82-1.2A2 2 0 0 0 7.93 3H4a2 2 0 0 0-2 2v13a2 2 0 0 0 2 2z"></path>
      </svg>
    `;

    return `
      <div class="project-item ${active ? 'active' : ''}" data-id="${p.id}" onclick="selectProject('${p.id}')">
        <div class="project-item-title-row">
          ${folderIconSvg}
          <span class="project-item-name" title="${p.name}">${p.name}</span>
        </div>
        <div class="project-item-client">KH: ${p.client || 'Chưa nhập'}</div>
        <div class="project-item-footer">
          <span class="project-item-date">${p.date || ''}</span>
          <span class="project-item-rooms-badge">${s.rooms} phòng</span>
        </div>
      </div>
    `;
  }).join('');
}
```

*Lưu ý: Thêm thuộc tính `onclick="selectProject('${p.id}')"` để người dùng bấm trực tiếp vào card là chuyển đổi dự án tức thì.*

- [ ] **Step 2: Commit**

```bash
git add app.js
git commit -m "feat: implement dynamic project card rendering with search and sort support in sidebar"
```

---

### Task 4: Kiểm Thử & Xác Minh Giao Diện

- [ ] **Step 1: Khởi chạy browser subagent để kiểm thử visual**

Nhiệm vụ:
- Mở `http://localhost:8000/`.
- Chọn dự án để vào Workspace.
- Xác nhận:
  1. Header có logo Bluedeco nằm chính giữa trang.
  2. Sidebar có icon tòa nhà cam, tiêu đề, ô tìm kiếm và sắp xếp.
  3. Thẻ dự án active có viền màu cam, chữ tên dự án màu cam và icon folder màu cam.
  4. Ô tìm kiếm dự án hoạt động chính xác (lọc danh sách tức thì khi gõ).
  5. Chụp ảnh màn hình toàn cảnh.
