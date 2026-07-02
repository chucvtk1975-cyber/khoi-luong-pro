# Đồng Bộ Số Liệu Cột Phòng Phần Chi Phí Khác ở Bản Xem Trước Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Hiển thị đúng số liệu cột phòng cho phần Chi Phí Khác trong Bản xem trước để đồng bộ 100% với dữ liệu xuất PDF/Excel.

**Architecture:** Cập nhật hàm `_renderPreviewSummary` để tính toán diện tích/số lượng định mức cho từng phòng thay vì in ra dấu gạch ngang (`—`).

**Tech Stack:** Vanilla JavaScript.

## Global Constraints

- Không tự ý thay đổi code đã hoàn tất bên ngoài phạm vi yêu cầu.
- Giữ nguyên cấu trúc, định dạng và công thức Excel.

---

### Task 1: Cập nhật render các cột phòng trong Chi Phí Khác tại Bản Xem Trước

**Files:**
- Modify: [app.js](file:///d:/Kho%20tri%20th%E1%BB%A9c/khoi-luong-pro/app.js)

**Interfaces:**
- Consumes: `_renderPreviewSummary(project, rooms)`
- Produces: Bản xem trước hiển thị đúng số liệu chi phí khác của từng phòng.

- [ ] **Step 1: Sửa logic kết xuất cột phòng cho chi phí khác**

Sửa đổi đoạn mã tại `app.js` (dòng ~9507) trong hàm `_renderPreviewSummary`:
Thay thế đoạn:
```javascript
      const blankCols = rooms.map(() => '<td>—</td>').join('');
```
Bằng:
```javascript
      const roomQtyCells = rooms.map(r => {
        const tf = (+r.D || 0) / 1000 * (+r.R || 0) / 1000;
        const roomQty = tmpl.autoQty ? +(tf.toFixed(2)) : +(saved.qty != null ? saved.qty : tmpl.defaultQty);
        return `<td style="text-align:right;font-size:12px;padding:4px 8px;">${roomQty > 0 ? fmt(roomQty) : '—'}</td>`;
      }).join('');
```
Đồng thời cập nhật chuỗi HTML ghép cột:
Thay thế `${blankCols}` bằng `${roomQtyCells}`.

- [ ] **Step 2: Kiểm tra cú pháp JavaScript**

Chạy lệnh kiểm tra cú pháp:
`node -c app.js`
Yêu cầu: Không có lỗi cú pháp.

- [ ] **Step 3: Chạy script kiểm tra code dự án**

Chạy script kiểm tra:
`python check_final.py`
Yêu cầu: Thành công, các cặp thẻ HTML đóng mở cân bằng.

- [ ] **Step 4: Commit thay đổi**

```bash
git add app.js
git commit -m "feat: render room quantities for other costs in summary preview"
```
