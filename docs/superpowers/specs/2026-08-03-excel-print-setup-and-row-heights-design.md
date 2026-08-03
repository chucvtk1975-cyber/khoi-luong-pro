# Design Spec: Định Dạng Trang In A4 Ngang & Tinh Chỉnh Chiều Cao Hàng Excel (24pt/26pt/30pt)

**Ngày:** 2026-08-03  
**Trạng thái:** Đã duyệt bởi người dùng (Tinh chỉnh chiều cao hàng mới)

---

## 1. Mục tiêu
Tinh chỉnh chiều cao hàng (Row Heights) trong 100% các sheet Excel xuất ra (*Tổng hợp*, *Chi tiết phòng*, *Vật tư cần mua*) theo bộ kích thước mới: **Hạng mục dữ liệu = 24pt**, **Tiêu đề La Mã = 26pt**, **Tiêu đề Bảng = 30pt**.

---

## 2. Thông số Định Dạng Trang In (`ws['!margins']` & `ws['!pageSetup']`)

- **Khổ giấy (Paper Size)**: A4 (`paperSize: 9`).
- **Hướng in (Orientation)**: Landscape / Xoay ngang (`orientation: 'landscape'`).
- **Co giãn (Fit to Page)**: Tự động vừa 1 trang ngang (`fitToWidth: 1, fitToHeight: 0`).
- **Lề in (Margins)**:
  - Lề Trái (**Left**): `1.8 cm` = `0.71 inches` (`left: 0.71`).
  - Lề Phải (**Right**): `1.0 cm` = `0.39 inches` (`right: 0.39`).
  - Lề Trên (**Top**): `1.4 cm` = `0.55 inches` (`top: 0.55`).
  - Lề Dưới (**Bottom**): `1.4 cm` = `0.55 inches` (`bottom: 0.55`).
  - Header / Footer: `0.2 inches` (`header: 0.2, footer: 0.2`).

---

## 3. Quy tắc Chiều Cao Hàng Mới (`ws['!rows']`)

Tất cả các trang tính trong file Excel xuất ra sẽ được thiết lập mảng `ws['!rows']`:

- **Hàng Header Bảng** (STT, HẠNG MỤC...): **`30pt`** (`{ hpt: 30, hpx: 40 }`).
- **Hàng Tiêu đề Nhóm La Mã** (I, II...): **`26pt`** (`{ hpt: 26, hpx: 35 }`).
- **Hàng Dữ liệu Hạng mục thường**: **`24pt`** (`{ hpt: 24, hpx: 32 }`).
- **Hàng Chữ ký & Tổng cộng**: **`26pt`** (`{ hpt: 26, hpx: 35 }`).

---

## 4. Các Tệp Thay Đổi

- `src/excel.js`: Cập nhật hàm `applyRowHeights(ws)` gán `!rows` theo bộ thông số 24pt/26pt/30pt.
- `main.js`, `index.html`: Bump cache buster query string `?v=20260803-v8`.

---

## 5. Verification Plan

- [ ] Xuất file Excel: Kiểm tra chiều cao các dòng dữ liệu đạt `24pt`, dòng La Mã `26pt`, dòng Header Bảng `30pt`.
- [ ] Chạy `check_final.py` xác minh cú pháp và HTML.
