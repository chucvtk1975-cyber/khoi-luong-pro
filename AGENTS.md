# AGENTS.md

This file provides context and instructions for AI coding agents working on the **khoi-luong-pro** project.

## Setup commands
- **Serve project locally**: Run a local static file server.
  - Python: `python -m http.server 8000`
  - Node.js (npx): `npx serve .`
- **Run verification / helper scripts**: Execute specific Python scripts for checking code logic and parenthesizing (e.g., `python check_final.py` or `python check_paren.py`).

## Tech Stack & Architecture
- **Frontend Core**: Vanilla HTML5, Vanilla CSS3, and ES6 JavaScript (built with pure web technologies without a build step or framework).
- **Core Script**: [app.js](file:///d:/Kho%20tri%20th%E1%BB%A9c/khoi-luong-pro/app.js) — Contains all logic, calculations, state, SheetJS-based Vietnamese Excel takeoff templates, and page renderings.
- **Styling**: [style.css](file:///d:/Kho%20tri%20th%E1%BB%A9c/khoi-luong-pro/style.css) — Custom layouts and UI elements.

## Critical Project Rules (Rules)
- **Không tự ý thay đổi code đã hoàn tất**: Những tính năng, thành phần giao diện hay logic nghiệp vụ đã được code xong và hoạt động ổn định tuyệt đối không được tự ý sửa đổi khi chưa có sự xác nhận của người dùng.
- **Hỏi lại khi chưa rõ**: Trong quá trình nhận công việc hoặc yêu cầu, nếu có bất kỳ điểm nào chưa rõ ràng, mơ hồ hoặc thiếu thông tin, bắt buộc phải hỏi lại người dùng để làm rõ trước khi triển khai, không được tự ý phán đoán hay giả định.
- **Giữ nguyên vẹn cấu trúc, định dạng và công thức Excel**: Tuyệt đối giữ nguyên cấu trúc cột, định dạng lề, căn lề, font chữ (Times New Roman), và các liên kết công thức tự động giữa các sheet (Tổng hợp, Chi tiết phòng, Vật Tư Cần Mua) đã hoạt động ổn định, không tự ý thay đổi cho tới khi có chỉ thị rõ ràng từ người dùng.
- **Cập nhật phiên bản Cache-Buster khi sửa CSS/JS**: Mỗi khi chỉnh sửa file `style.css` hoặc bất kỳ file nào trong thư mục `src/` (excel.js, takeoff.js, calc.js, db.js...) hoặc `main.js`, bắt buộc phải tăng hoặc cập nhật tham số phiên bản (Query Parameter `?v=...`) của `main.js` trong thẻ script tại [index.html](file:///d:/Kho%20tri%20th%E1%BB%A9c/khoi-luong-pro/index.html) để ép trình duyệt người dùng xóa cache và tải phiên bản mới nhất.

## Known Regression Risks (KHÔNG được làm hỏng)

### 1. GitHub Pages Deployment
- File `.github/workflows/static.yml` là bắt buộc để deploy tự động lên GitHub Pages.
- **TUYỆT ĐỐI KHÔNG XÓA** file này. Nếu xóa, trang web sẽ ngừng deploy.
- Settings GitHub Pages phải để Source = **"GitHub Actions"** (không phải "Deploy from a branch").

### 2. Căn lề trái cho Note Rows trong Excel & PDF
- Trong hàm `applySheetStyles` của [excel.js](file:///d:/Kho%20tri%20th%E1%BB%A9c/khoi-luong-pro/src/excel.js), có một khối kiểm tra **explicit** ở đầu alignment section cho các giá trị:
  - `Bằng chữ:...`
  - `_ Báo giá trên...`
  - `_ Thời gian thi công:`
- Khối này **BẮT BUỘC phải đứng TRƯỚC** tất cả các `else if` khác (signatureStartRow, footerStartRow...). Nếu bị xóa hoặc di chuyển sau, các dòng này sẽ bị căn giữa.
- Trong [takeoff.js](file:///d:/Kho%20tri%20th%E1%BB%A9c/khoi-luong-pro/src/takeoff.js), td của dòng `boq-words-row` (Bằng chữ) phải có `text-align:left` tường minh.

### 3. Checklist sau khi sửa excel.js hoặc takeoff.js
Sau mỗi lần thay đổi liên quan đến xuất Excel hoặc PDF, **bắt buộc** kiểm tra:
- [ ] Dòng "Bằng chữ: ..." → **căn trái**
- [ ] Dòng "_ Báo giá trên..." → **căn trái** (italic)
- [ ] Dòng "_ Thời gian thi công:" → **căn trái** (italic)
- [ ] Dòng "Giám đốc" / "VŨ THỊ KIM CHÚC" → **căn giữa** (KHÔNG thay đổi)
- [ ] Hàng header bảng (STT, HẠNG MỤC...) → **căn giữa**
- [ ] Cột HẠNG MỤC (C=1) trong mọi data row (R≥9) → **căn trái + indent=1** (xem mục #4)
- [ ] Header info rows Cột A (C=0): "Từ:", "Công Ty:", "Địa chỉ:" → **căn trái** (xem mục #5)
- [ ] Header info rows Cột E (C=4): "Kính gởi:", "Công Ty:", "Địa chỉ:" → **căn trái** (xem mục #5)

### 4. Lock-down Loop cho cột HẠNG MỤC (C=1) trong sheet Tổng Hợp
- **Vấn đề đã xảy ra**: Cột HẠNG MỤC (C=1) trong `wsSum` bị căn giữa, dù `applySheetStyles` đã set LEFT. Nguyên nhân: `applySheetStyles` và `applyBoldSectionRows` tương tác không đảm bảo kết quả cuối cùng là LEFT+indent.
- **Fix pattern**: Sau khi gọi `applyBoldSectionRows(wsSum, 7)`, có một **lock-down loop** (`// ⚠️ DEFENSIVE FIX`) trong [excel.js](file:///d:/Kho%20tri%20th%E1%BB%A9c/khoi-luong-pro/src/excel.js) tại ~L2680 chạy SAU CÙNG, ép buộc:
  - `_isRoman` (section header): `horizontal='left'`, không indent
  - data row thường: `horizontal='left', indent=1`
  - total row (`tổng cộng`, `Bằng chữ:`): giữ nguyên
- **TUYỆT ĐỐI KHÔNG XÓA hoặc di chuyển** vòng lặp lock-down này lên trước `applyBoldSectionRows`.
- **Khi thêm sheet mới hoặc refactor**: Phải đảm bảo lock-down loop vẫn chạy CUỐI CÙNG sau mọi hàm style khác.

### 5. Lock-down Loop cho Header Info Rows (R=4,5,6) — Cột A & E
- **Vấn đề đã xảy ra**: SheetJS merged cell behavior reset alignment của các cell đã merge trong header rows R=4,5,6 về CENTER, dù `applySheetStyles` (L762-764) đã set LEFT.
  - C=0 ("Từ:", "Công Ty:", "Địa chỉ:") — merge A4:D4, A5:D5, A6:D6
  - C=4 ("Kính gởi:", "Công Ty:", "Địa chỉ:") — merge E4:I4, E5:I5, E6:I6
- **Fix pattern**: Sau mỗi `applyBoldSectionRows(wsXXX, 7)` cho **cả 3 sheets** (wsDetail, wsSum, wsVT), có **lock-down loop** (`// ⚠️ LOCK-DOWN`) ép `horizontal='left'` cho `[0, 4]` tại `[4, 5, 6]`.
- **TUYỆT ĐỐI KHÔNG XÓA** 3 lock-down loops này. Nếu thêm sheet mới có cùng cấu trúc header, phải thêm lock-down tương tự.
- **Nguyên nhân gốc**: `applyBorders` là dead function (không bao giờ được gọi). `applySheetStyles` set LEFT nhưng SheetJS merge override. Chỉ lock-down loop chạy CUỐI mới đảm bảo kết quả đúng.

### 6. Quy tắc Bất Biến: "Lock-Down Cuối Cùng"
Khi nhiều hàm style (`applySheetStyles`, `applyBoldSectionRows`, v.v.) có thể override nhau theo thứ tự không rõ ràng, **LUÔN dùng pattern "lock-down loop chạy CUỐI"**:
```javascript
// Sau TẤT CẢ các hàm style:
someRows.forEach(r => {
  someCols.forEach(c => {
    const ref = XLSX.utils.encode_cell({ r, c });
    if (ws[ref]) {
      if (!ws[ref].s) ws[ref].s = {};
      ws[ref].s.alignment = { horizontal: 'left', ... };
    }
  });
});
```
Đây là pattern đã được kiểm chứng cho cả HẠNG MỤC lẫn header rows. Không dùng CSS class hay hàm style thông thường cho các cell alignment quan trọng — dùng lock-down.
