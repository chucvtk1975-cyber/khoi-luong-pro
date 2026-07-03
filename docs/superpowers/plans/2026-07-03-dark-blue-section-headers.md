# Thiết kế thanh tiêu đề hộp màu xanh đậm trong Modal phòng Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Chuyển đổi các tiêu đề phân khu chức năng trong Modal thêm/sửa phòng sang dạng thanh hộp màu xanh đậm (#0F172A), chữ và icon màu trắng.

**Architecture:** Thay đổi các thuộc tính CSS của `#modal-room .section-title` và `#modal-room .mat-section-title` trong `style.css`.

**Tech Stack:** Vanilla CSS3.

## Global Constraints

- Không tự ý thay đổi code đã hoàn tất bên ngoài phạm vi yêu cầu.
- Giữ nguyên cấu trúc, định dạng và công thức Excel.

---

### Task 1: Cập nhật CSS cho các tiêu đề trong Modal phòng

**Files:**
- Modify: [style.css](file:///d:/Kho%20tri%20th%E1%BB%A9c/khoi-luong-pro/style.css)

- [ ] **Step 1: Sửa đổi CSS của các tiêu đề trong modal**

Sửa đổi đoạn mã tại `style.css` (dòng ~3246-3261).
Thay thế đoạn CSS sau:
```css
#modal-room .section-title,
#modal-room .mat-section-title {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-weight: 700;
  font-size: 14px;
}
#modal-room .section-title svg,
#modal-room .mat-section-header svg {
  width: 16px;
  height: 16px;
  color: var(--text-secondary);
  flex-shrink: 0;
  vertical-align: middle;
}
```
Bằng:
```css
#modal-room .section-title,
#modal-room .mat-section-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 700;
  font-size: 13px;
  text-transform: uppercase;
  color: #FFFFFF !important;
  background-color: #0F172A;
  padding: 8px 12px;
  border-radius: 6px;
  margin: 22px 0 12px 0;
  border-bottom: none !important;
}
#modal-room .section-title svg,
#modal-room .mat-section-header svg {
  width: 16px;
  height: 16px;
  color: #FFFFFF !important;
  flex-shrink: 0;
  vertical-align: middle;
}
```

- [ ] **Step 2: Chạy script kiểm tra dự án**

Chạy script kiểm tra cấu trúc HTML:
```powershell
python check_final.py
```
Expected: Lệnh chạy thành công, không báo lỗi.

- [ ] **Step 3: Commit**

```bash
git add style.css
git commit -m "style: change room modal section headers to dark blue blocks"
```
