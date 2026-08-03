# Design Spec: Định Dạng Trang In A4 Ngang, Chiều Cao Hàng Mới (24pt/26pt/30pt) & Đánh Số Trang 1/6

**Ngày:** 2026-08-03  
**Trạng thái:** Đã bổ sung yêu cầu đánh số trang 1/6 góc phải

---

## 1. Mục tiêu
1. Tinh chỉnh chiều cao hàng trong 100% các sheet Excel xuất ra: **Hạng mục dữ liệu = 24pt**, **Tiêu đề La Mã = 26pt**, **Tiêu đề Bảng = 30pt**.
2. Định dạng lề in A4 Ngang (Trái 1.8cm, Phải 1.0cm, Trên 1.4cm, Dưới 1.4cm).
3. Đánh số trang góc dưới bên phải theo định dạng **1/6, 2/6 ... đến N/N** (`&P/&N`).

---

## 2. Thông số Định Dạng Trang In (`ws['!margins']` & `ws['!headerFooter']`)

- **Khổ giấy (Paper Size)**: A4 (`paperSize: 9`).
- **Hướng in (Orientation)**: Landscape / Xoay ngang (`orientation: 'landscape'`).
- **Co giãn (Fit to Page)**: Tự động vừa 1 trang ngang (`fitToWidth: 1, fitToHeight: 0`).
- **Lề in (Margins)**:
  - Lề Trái (**Left**): `1.8 cm` = `0.71 inches` (`left: 0.71`).
  - Lề Phải (**Right**): `1.0 cm` = `0.39 inches` (`right: 0.39`).
  - Lề Trên (**Top**): `1.4 cm` = `0.55 inches` (`top: 0.55`).
  - Lề Dưới (**Bottom**): `1.4 cm` = `0.55 inches` (`bottom: 0.55`).
  - Header / Footer: `0.2 inches` (`header: 0.2, footer: 0.2`).
- **Đánh số trang (Footer Right)**:
  - Định dạng hiển thị: **`1/6`, `2/6` ... `&P/&N`** (Góc dưới bên phải).
  - Chuỗi OpenXML Footer: `&L&"Arial,Italic"Du-Toan-BlueAI Lab&R&"Arial,Bold"&P/&N`.

---

## 3. Quy tắc Chiều Cao Hàng Mới (`ws['!rows']`)

- **Hàng Header Bảng** (STT, HẠNG MỤC...): **`30pt`** (`{ hpt: 30, hpx: 40 }`).
- **Hàng Tiêu đề Nhóm La Mã** (I, II...): **`26pt`** (`{ hpt: 26, hpx: 35 }`).
- **Hàng Dữ liệu Hạng mục thường**: **`24pt`** (`{ hpt: 24, hpx: 32 }`).
- **Hàng Chữ ký & Tổng cộng**: **`26pt`** (`{ hpt: 26, hpx: 35 }`).

---

## 4. Các Tệp Thay Đổi

- `src/excel.js`:
  - Cập nhật `applyRowHeights(ws)` với chiều cao 24pt/26pt/30pt.
  - Cập nhật `applyPageSetup(ws)` & `triggerAutoSync()` số trang góc phải `&P/&N`.
- `main.js`, `index.html`: Bump cache buster query string `?v=20260803-v8`.

---

## 5. Verification Plan

- [ ] Xuất file Excel: Mở Print Preview kiểm tra góc dưới bên phải hiển thị số trang `1/6`, `2/6`..., chiều cao hàng `24pt`, lề A4 ngang chuẩn.
- [ ] Chạy `check_final.py` xác minh cú pháp và HTML.
