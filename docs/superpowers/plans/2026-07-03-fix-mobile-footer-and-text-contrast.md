# Sửa lỗi mất nút Lưu trên Mobile và tăng độ tương phản màu chữ Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Khôi phục hiển thị dính (sticky) cho nút Lưu/Hủy/Tiếp theo trên Mobile, tăng độ đậm màu chữ toàn app, và cấu hình màu xanh đậm `#1E293B` cho nhãn/tiêu đề trong Modal dự án.

**Architecture:** Chỉnh sửa các quy tắc CSS trong `style.css`.

**Tech Stack:** Vanilla CSS3.

## Global Constraints

- Không tự ý thay đổi code đã hoàn tất bên ngoài phạm vi yêu cầu.
- Giữ nguyên cấu trúc, định dạng và công thức Excel.

---

### Task 1: Chỉnh sửa các quy tắc CSS trong style.css

**Files:**
- Modify: [style.css](file:///d:/Kho%20tri%20th%E1%BB%A9c/khoi-luong-pro/style.css)

- [ ] **Step 1: Cập nhật biến màu chữ toàn cục**

Sửa đổi dòng ~19-21 trong `:root` tại `style.css`.
Thay thế:
```css
  --color-text-primary:   #1E293B; /* Đậm hơn để dễ đọc trên nền sáng */
  --color-text-secondary: #475569;
  --color-text-muted:     #64748B;
```
Bằng:
```css
  --color-text-primary:   #0F172A; /* Slate 900 siêu đậm */
  --color-text-secondary: #1E293B; /* Slate 800 xanh xám đậm */
  --color-text-muted:     #334155; /* Slate 700 dễ đọc */
```

- [ ] **Step 2: Thêm CSS cho màu tiêu đề và nhãn trong Modal Dự án**

Thêm đoạn CSS sau vào file `style.css` (đặt ở phần cuối của vùng khai báo `:root` hoặc trước phần `.form-group` khoảng dòng ~1000):
```css
/* Màu tiêu đề và nhãn trong Modal Dự án */
#modal-project .form-group label,
#modal-project .section-title {
  color: #1E293B !important;
}
```

- [ ] **Step 3: Chỉnh sửa chân trang modal trên Mobile**

Sửa đổi đoạn mã tại `style.css` trong `@media (max-width: 768px)` (dòng ~1427-1431).
Thay thế:
```css
  /* An nut footer goc (dua xuong duoi trong modal) */
  .modal-footer {
    display: none;
  }
```
Bằng:
```css
  /* Hiện nút chân trang và ghim dính ở đáy modal trên Mobile */
  .modal-footer {
    display: flex !important;
    position: sticky !important;
    bottom: 0;
    z-index: 100;
    background: var(--bg-card) !important;
    border-top: 1px solid var(--border-light) !important;
    padding: 10px 16px !important;
    box-shadow: 0 -2px 10px rgba(0,0,0,0.05);
  }
```

- [ ] **Step 4: Chạy script kiểm tra dự án**

Chạy script kiểm tra cấu trúc HTML:
```powershell
python check_final.py
```
Expected: Lệnh chạy thành công, không báo lỗi.

- [ ] **Step 5: Commit**

```bash
git add style.css
git commit -m "style: fix mobile modal footer visibility and increase text contrast"
```
