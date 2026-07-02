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
