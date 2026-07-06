# Design Spec: Thêm Logo Bluedeco vào Excel Sheets

**Ngày:** 2026-07-07  
**Trạng thái:** Chờ duyệt

---

## 1. Bối cảnh & Vấn đề

Logo Bluedeco hiện có mặt trong **PDF print preview** (`takeoff.js`) ở vị trí cột B, hàng 1-3.  
Trong **Excel export** thì logo đã bị mất ở cả hai luồng:

| Export type | Function | Trạng thái logo |
|-------------|----------|----------------|
| SheetJS regular | `exportExcel()` → `xlsxWriteSheetJS()` | ❌ Không có |
| ExcelJS photos | `exportPhotosExcel()` → `xlsxWritePhotos()` | ❌ Không có |
| Server sync | `autoSyncProjectFiles()` | ✅ Có (JSZip inject) — nhưng chỉ sync server |

**Root cause:** Code JSZip logo injection đã tồn tại và hoạt động tốt trong `autoSyncProjectFiles()` nhưng KHÔNG được gọi trong hai hàm download thực tế.

---

## 2. Vị trí Logo trong Excel

Giống PDF preview:
- **Cột B (index C=1)**, hàng 1-3 (R=0,1,2) — căn lề trái
- Drawing XML anchor hiện tại (excel.js L3330) đã đúng vị trí này

---

## 3. Thiết kế Giải pháp (Hướng A — Shared Helper)

### 3.1 Tạo `injectLogoToBuffer(binBuf)` — Function mới

**Vị trí:** `src/excel.js`, sau phần khai báo `logoArrayBuffer` (~L32)

- Nhận SheetJS binary ArrayBuffer  
- Load vào JSZip  
- Inject logo drawing XML vào MỌI worksheet (chỉ khi chưa có `<drawing`)  
- Trả về ArrayBuffer mới đã có logo  
- **Graceful fallback**: nếu JSZip hoặc logoArrayBuffer không có → trả về buffer gốc

### 3.2 Sửa `exportExcel()` — SheetJS regular download

- Thêm `async`
- Thay `xlsxWriteSheetJS()` bằng: write binary → `injectLogoToBuffer()` → tạo Blob → download

### 3.3 Sửa `xlsxWritePhotos()` — ExcelJS download

- Sau khi workbook được tạo, thêm logo bằng ExcelJS API:
  ```javascript
  const logoId = workbook.addImage({ base64: LOGO_BASE64, extension: 'png' });
  workbook.worksheets.forEach(sheet => {
    sheet.addImage(logoId, { tl: { col: 1, row: 0 }, br: { col: 2, row: 3 } });
  });
  ```

### 3.4 Refactor `autoSyncProjectFiles()` — Dùng shared helper

- Xóa code JSZip logo trùng lặp (L3300-3343)  
- Thay bằng: `const finalBuf = await injectLogoToBuffer(s2ab(out));`

---

## 4. Files thay đổi

| File | Loại | Mô tả |
|------|------|-------|
| `src/excel.js` | MODIFY | Thêm `injectLogoToBuffer()`, sửa 3 functions |
| `index.html` | MODIFY | Bump cache-buster v17 |

---

## 5. Điểm cần lưu ý

- Drawing XML dùng chung `drawing1.xml` cho tất cả sheets — kiểm tra `!xmlStr.includes('<drawing')` trước khi inject để tránh duplicate
- ExcelJS `addImage` với `tl/br` chỉ định vị trí theo cell reference
- `logoImageId` được tạo 1 lần và tái sử dụng cho tất cả ExcelJS sheets

---

## 6. Checklist Regression

- [ ] Xuất Excel thường → logo xuất hiện cột B, hàng 1-3 ở MỌI sheet
- [ ] Xuất Excel ảnh → logo xuất hiện ở header mỗi sheet ảnh
- [ ] Alignment đã fix trước không bị ảnh hưởng (header rows, HẠNG MỤC)
- [ ] File download bình thường (không lỗi JS console)
- [ ] Fallback: JSZip chưa load → file vẫn download được (không có logo)
