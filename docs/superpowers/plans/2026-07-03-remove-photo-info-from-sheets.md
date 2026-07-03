# Loại bỏ thông tin ảnh ở sheet PDF và Excel Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Loại bỏ dòng thông tin `📸 Ảnh hiện trạng: ...` ở dưới cùng bảng khối lượng của mỗi phòng trong cả file Excel và PDF xuất ra.

**Architecture:** Sửa đổi hàm `generateWorkbook` trong `app.js` để không đưa dòng chứa thông tin danh sách ảnh hiện trạng và các dòng trống bổ trợ của nó vào cấu trúc sheet Excel chi tiết phòng.

**Tech Stack:** Vanilla JavaScript.

## Global Constraints

- Không tự ý thay đổi code đã hoàn tất bên ngoài phạm vi yêu cầu.
- Giữ nguyên cấu trúc, định dạng và công thức Excel.

---

### Task 1: Loại bỏ photoRow trong generateWorkbook

**Files:**
- Modify: [app.js](file:///d:/Kho%20tri%20th%E1%BB%A9c/khoi-luong-pro/app.js)

- [ ] **Step 1: Xóa khối lệnh photoRow trong generateWorkbook**

Sửa đổi đoạn mã tại `app.js` (dòng ~7960-7975).
Xóa bỏ hoàn toàn đoạn code sau:
```javascript
    const allCatPhotos = [];
    ['overview', 'den', 'tudien', 'maylanh'].forEach(cat => {
      const catPhotos = getRoomPhotos(room, cat);
      if (catPhotos.length > 0) {
        allCatPhotos.push(...catPhotos);
      }
    });

    if (allCatPhotos.length > 0) {
      aoa.push(blkDetail()); curRow++;
      const photoRow = blkDetail();
      photoRow[1] = `📸 Ảnh hiện trạng: ${allCatPhotos.map(p => p.name).join(', ')}`;
      aoa.push(photoRow);
      merges.push({ s: { r: curRow, c: 1 }, e: { r: curRow, c: 9 } });
      curRow++;
    }
```

- [ ] **Step 2: Kiểm tra cú pháp JavaScript**

Chạy lệnh kiểm tra cú pháp:
```bash
node -c app.js
```
Expected: Lệnh chạy thành công và không báo lỗi cú pháp.

- [ ] **Step 3: Chạy script kiểm tra logic dự án**

Chạy script:
```powershell
python check_final.py
```
Expected: Lệnh chạy thành công, không báo lỗi liên quan đến cấu trúc.

- [ ] **Step 4: Commit**

```bash
git add app.js
git commit -m "feat: remove photo info list from excel and pdf room sheets"
```
