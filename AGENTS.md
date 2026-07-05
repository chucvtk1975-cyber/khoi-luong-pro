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
