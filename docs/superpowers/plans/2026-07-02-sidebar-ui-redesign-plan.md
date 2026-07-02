# Nâng cấp Giao diện & Đổi màu Sidebar (Phương án 2) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Cập nhật màu sắc giao diện Bốc Khối Lượng Pro theo Phương án 2 (Kính mờ - Hybrid) và thêm nhãn thương hiệu "Khối-Lượng-Pro" căn giữa trên Header.

**Architecture:** Sử dụng Design Tokens qua biến CSS để thiết lập hệ màu sắc mới sáng sủa hơn ở Header và Vùng làm việc, kết hợp với Sidebar tối màu dạng Gradient. Sử dụng định vị tuyệt đối (absolute positioning) để căn giữa nhãn thương hiệu mà không ảnh hưởng tới bố cục flex có sẵn.

**Tech Stack:** Vanilla HTML5, Vanilla CSS3, ES6 JavaScript.

## Global Constraints
- Không tự ý thay đổi code đã hoàn tất ngoại trừ phần CSS variables và cấu trúc màu sắc của Sidebar/Header.
- Mọi thay đổi về CSS phải sử dụng CSS variables kế thừa để đảm bảo tính đồng bộ.
- Đảm bảo font chữ Inter và kiểu hiển thị bảng tính Excel dễ đọc dưới ánh sáng ban ngày.

---

### Task 1: Cập nhật Design Tokens (CSS Variables)

**Files:**
- Modify: `style.css:1-56`

**Interfaces:**
- Consumes: CSS variables hiện tại.
- Produces: Các biến CSS mới: `--sidebar-gradient`, `--bg-header`, `--text-header`, `--sidebar-text-main`, `--sidebar-text-muted`, `--sidebar-active-bg`, `--sidebar-active-border`.

- [ ] **Step 1: Cập nhật các biến CSS màu sắc mới**

Thay đổi các biến trong `:root` tại đầu file `style.css`:
```css
:root {
  /* Design Tokens */
  --color-primary:       #0F172A; /* Slate 900 */
  --color-primary-hover: #1E293B; /* Slate 800 */
  --color-primary-light: #F1F5F9; /* Slate 100 */
  --color-accent:        #2D6A4F;
  --color-accent-hover:  #245740;
  --color-accent-light:  #E8F4EE;
  --color-warning:       #D97706;
  --color-warning-light: #FEF3C7;
  --color-danger:        #DC2626;
  --color-danger-light:  #FEE2E2;
  --color-success:       #16A34A;
  --color-success-light: #DCFCE7;
  --color-text-primary:   #1E293B; /* Đậm hơn để dễ đọc trên nền sáng */
  --color-text-secondary: #475569;
  --color-text-muted:     #64748B;
  --color-text-inverse:   #FFFFFF;
  --color-bg:             #F8FAFC; /* Slate 50 sáng sủa sạch sẽ */
  --color-bg-card:        #FFFFFF;
  --color-border:         #E2E8F0; /* Slate 200 */
  --color-border-strong:  #CBD5E1; /* Slate 300 */
  --font-family: 'Inter', system-ui, -apple-system, sans-serif;
  --font-size-xs:   11px;
  --font-size-sm:   13px;
  --font-size-base: 15px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-full: 9999px;
  --shadow-sm: 0 1px 3px rgba(0,0,0,0.05), 0 1px 2px rgba(0,0,0,0.02);
  --tap-min: 44px;

  /* Backward Compatibility Mappings & Premium Elements */
  --bg-base:        var(--color-bg);
  --bg-card:        var(--color-bg-card);
  --bg-card-hover:  var(--color-primary-light);
  
  /* Gradient Sidebar trái */
  --sidebar-gradient:    linear-gradient(180deg, #1E293B 0%, #0F172A 100%);
  --bg-sidebar:     #0F172A;
  
  /* Màu nền của Header (Đổi từ tối sang sáng) */
  --bg-header:           #FFFFFF;
  --text-header:         #0F172A;
  
  /* Màu chữ chuyên biệt cho Sidebar tối */
  --sidebar-text-main:    #F8FAFC; 
  --sidebar-text-muted:   #94A3B8; 
  --sidebar-active-bg:    rgba(59, 130, 246, 0.15); 
  --sidebar-active-border: #3B82F6; 

  --bg-input:       var(--color-bg-card);
  --border:         var(--color-border-strong);
  --border-light:   var(--color-border);
  --text-primary:   var(--color-text-primary);
  --text-secondary: var(--color-text-secondary);
  --text-muted:     var(--color-text-muted);
  --brand-blue:       #2563EB;
  --brand-blue-light: #3B82F6;
  --brand-gold:       var(--color-warning);
  --brand-green:      var(--color-success);
  --brand-red:        var(--color-danger);
  --radius:    var(--radius-lg);
  --radius-sm: var(--radius-md);
  --shadow:    var(--shadow-sm);
}
```

- [ ] **Step 2: Chạy kiểm tra cú pháp và commit**

Run: `node -c app.js` (không ảnh hưởng JS nhưng đảm bảo an toàn)
```bash
git add style.css
git commit -m "style: update design tokens and css variables for Option 2"
```

---

### Task 2: Nâng cấp Header & Thêm Nhãn Thương Hiệu "Khối-Lượng-Pro"

**Files:**
- Modify: `index.html:737-757`
- Modify: `style.css:74-86` (Cập nhật CSS Header)
- Modify: `style.css` (Thêm CSS `.header-center`)

**Interfaces:**
- Consumes: CSS variables của Header.
- Produces: Nhãn hiệu căn giữa "Khối-Lượng-Pro" trên giao diện Workspace.

- [ ] **Step 1: Cập nhật CSS cho `.app-header` và thêm `.header-center`**

Thay đổi các dòng 74-86 của `style.css`:
```css
.app-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  height: 62px;
  background: var(--bg-header); /* Đổi sang màu nền trắng */
  border-bottom: 1px solid var(--color-border); /* Viền xám mỏng */
  position: sticky;
  top: 0;
  z-index: 100;
  flex-shrink: 0;
}
```

Và thêm định nghĩa cho `.header-center` vào cuối file `style.css`:
```css
.header-center {
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  font-weight: 800;
  font-size: 16px;
  color: var(--text-header);
  letter-spacing: 0.5px;
  text-transform: uppercase;
}
```

- [ ] **Step 2: Chèn nhãn "Khối-Lượng-Pro" vào `index.html`**

Chèn thẻ `.header-center` vào trong `<header class="app-header">` của file `index.html`:
```html
    <header class="app-header">

      <div class="header-brand">

        <img src="logo-bluedecor.png" alt="Blue Decor" style="height:42px;object-fit:contain;display:block;" onerror="this.style.display='none'">

      </div>

      <div class="header-center">Khối-Lượng-Pro</div>

      <div class="header-actions">

        <span class="header-badge" id="header-project-count">0 dự án</span>
```

- [ ] **Step 3: Kiểm tra cấu trúc HTML và commit**

Run: `python check_final.py`
Expected: `Modal divs: opens=92, closes=92, net=0`
```bash
git add index.html style.css
git commit -m "style: redesign app-header and add centered brand title"
```

---

### Task 3: Redesign Sidebar & Active Project Item States

**Files:**
- Modify: `style.css:144-203`

**Interfaces:**
- Consumes: `--sidebar-gradient` và các biến `--sidebar-text-*`.
- Produces: Sidebar trái màu tối rực rỡ với độ tương phản văn bản hoàn hảo.

- [ ] **Step 1: Cập nhật CSS của Sidebar trái**

Sửa đổi phần cấu trúc `.project-sidebar` và các lớp bên trong trong file `style.css`:
```css
.project-sidebar {
  width: 270px;
  background: var(--sidebar-gradient); /* Áp dụng Gradient */
  border-right: 1px solid var(--color-primary-hover);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  flex-shrink: 0;
}
.sidebar-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 14px 12px;
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: var(--sidebar-text-muted); /* Chữ xám sáng */
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}
.project-list {
  flex: 1;
  overflow-y: auto;
  padding: 8px;
}
.project-item {
  padding: 11px 13px;
  border-radius: var(--radius-sm);
  cursor: pointer;
  margin-bottom: 3px;
  border: 1px solid transparent;
  transition: all 0.15s ease;
}
.project-item:hover {
  background: rgba(255, 255, 255, 0.05); /* Hover sáng nhẹ */
  border-color: rgba(255, 255, 255, 0.08);
}
.project-item.active {
  background: var(--sidebar-active-bg); /* Kính mờ */
  border-color: var(--sidebar-active-border);
  backdrop-filter: blur(8px);
}
.project-item-name {
  font-weight: 600;
  font-size: 13px;
  color: var(--sidebar-text-main); /* Chữ trắng sáng */
  margin-bottom: 4px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.project-item.active .project-item-name {
  color: #FFFFFF; /* Chọn thì trắng tinh */
  font-weight: 700;
}
.project-item-meta {
  font-size: 11px;
  color: var(--sidebar-text-muted); /* Chữ xám sáng */
  display: flex;
  gap: 10px;
}
```

- [ ] **Step 2: Commit**

```bash
git add style.css
git commit -m "style: redesign project-sidebar with gradient background and high contrast text"
```

---

### Task 4: Kiểm Thử & Xác Minh Giao Diện

**Files:**
- Test: Dùng browser subagent để chụp ảnh giao diện thực tế.

- [ ] **Step 1: Khởi chạy browser subagent để kiểm thử visual**

Nhiệm vụ:
- Mở `http://localhost:8000/`.
- Tạo một dự án mới hoặc chọn dự án hiện có để chuyển vào màn hình Workspace.
- Chụp ảnh màn hình toàn cảnh giao diện để xác minh:
  1. Sidebar có nền chuyển màu tối sâu, chữ dự án rõ ràng, màu tương phản tốt.
  2. Thẻ dự án đang chọn có màu highlight xanh lam kính mờ tinh tế.
  3. Header có màu trắng, chữ đen sẫm và nhãn hiệu **"Khối-Lượng-Pro"** căn giữa rực rỡ.
  4. Vùng nội dung có màu nền sáng sủa, dễ đọc số liệu.

- [ ] **Step 2: Xác nhận giao diện đạt chuẩn và kết thúc**
