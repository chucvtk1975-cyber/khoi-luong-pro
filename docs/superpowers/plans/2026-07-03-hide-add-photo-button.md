# Ẩn nút Thêm ảnh ở Card phòng Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ẩn nút "+ Thêm ảnh" trên card phòng ở trang chủ, giữ lại hiển thị đếm số lượng ảnh.

**Architecture:** Sửa HTML render trong hàm `_renderRoomsList` ở `app.js`.

**Tech Stack:** Vanilla JavaScript.

## Global Constraints

- Không tự ý thay đổi code đã hoàn tất bên ngoài phạm vi yêu cầu.
- Giữ nguyên cấu trúc, định dạng và công thức Excel.

---

### Task 1: Ẩn nút Thêm ảnh trên Card phòng

**Files:**
- Modify: [app.js](file:///d:/Kho%20tri%20th%E1%BB%A9c/khoi-luong-pro/app.js)

- [ ] **Step 1: Xóa nút Thêm ảnh trong _renderRoomsList**

Sửa đổi đoạn mã tại `app.js` (dòng ~2483-2495):
Thay thế đoạn:
```javascript
        <div class="room-card-photos" style="margin-top: 12px; padding-top: 10px; border-top: 1px dashed var(--border-color); display: flex; align-items: center; justify-content: space-between; font-size: 12px;">

          <span style="color: var(--text-secondary);">📷 Ảnh hiện trạng: <strong style="color: var(--brand-blue-light);">${getRoomPhotosCount(room)}</strong> tấm</span>

          <div>

            <input type="file" accept="image/*" multiple id="room-card-file-${room.id}" style="display: none;" onchange="handleRoomCardPhotoSelect(event, '${room.id}')">

            <button class="btn-primary" style="padding: 2px 8px; font-size: 11px; height: auto;" onclick="document.getElementById('room-card-file-${room.id}').click()">+ Thêm ảnh</button>

          </div>

        </div>
```
Bằng:
```javascript
        <div class="room-card-photos" style="margin-top: 12px; padding-top: 10px; border-top: 1px dashed var(--border-color); display: flex; align-items: center; justify-content: space-between; font-size: 12px;">

          <span style="color: var(--text-secondary);">📷 Ảnh hiện trạng: <strong style="color: var(--brand-blue-light);">${getRoomPhotosCount(room)}</strong> tấm</span>

        </div>
```

- [ ] **Step 2: Kiểm tra cú pháp JavaScript**

Run: `node -c app.js`
Expected: SUCCESS

- [ ] **Step 3: Chạy script kiểm tra dự án**

Run: `python check_final.py`
Expected: SUCCESS

- [ ] **Step 4: Commit**

```bash
git add app.js
git commit -m "feat: hide add photo button on room card dashboard"
```
