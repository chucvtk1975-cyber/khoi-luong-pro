# Design Spec: Định Dạng Trang In A4 Ngang & Tăng Chiều Cao Hàng Excel 1.5 Lần

**Ngày:** 2026-08-03  
**Trạng thái:** Đã duyệt bởi người dùng (Phương án 1)

---

## 1. Mục tiêu
Cấu hình chuẩn trang in (Print Setup) khổ **A4 Landscape** với các lề in chính xác theo cm và tăng chiều cao tất cả các hàng (Row Heights) lên **1.5 lần** trong 100% các sheet Excel xuất ra (*Tổng hợp*, *Chi tiết phòng*, *Vật tư cần mua*).

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

## 3. Quy tắc Chiều Cao Hàng 1.5 Lần (`ws['!rows']`)

Tất cả các trang tính trong file Excel xuất ra sẽ được thiết lập mảng `ws['!rows']` với chiều cao mở rộng 1.5 lần:

- **Hàng Header Bảng** (STT, HẠNG MỤC...): `36pt` (`{ hpt: 36, hpx: 48 }`).
- **Hàng Tiêu đề Nhóm La Mã** (I, II...): `30pt` (`{ hpt: 30, hpx: 40 }`).
- **Hàng Dữ liệu Hạng mục thường**: `27pt` (`{ hpt: 27, hpx: 36 }`) — tăng 1.5 lần so với 18pt mặc định.
- **Hàng Chữ ký & Tổng cộng**: `30pt` (`{ hpt: 30, hpx: 40 }`).

---

## 4. Các Tệp Thay Đổi

- `src/excel.js`:
  - Cập nhật `applyPageSetup(ws)` với lề in `left: 0.71, right: 0.39, top: 0.55, bottom: 0.55`.
  - Cập nhật hàm `applyRowHeights(ws)` gán `!rows` cho `wsSum`, `wsDetail`, `wsVT`.
  - Cập nhật `triggerAutoSync()` bổ sung XML `<pageMargins left="0.71" right="0.39" top="0.55" bottom="0.55"/>`.
- `main.js`, `index.html`: Bump cache buster query string `?v=20260803-v7`.

---

## 5. Verification Plan

- [ ] Xuất file Excel: Mở trang Page Setup trong Excel kiểm tra Margin (Left 1.8cm, Right 1.0cm, Top 1.4cm, Bottom 1.4cm, A4 Landscape).
- [ ] Kiểm tra chiều cao các dòng dữ liệu trong Excel đạt 27pt (~36px), thoáng và dễ đọc khi in.
- [ ] Chạy `check_final.py` xác minh cú pháp và tính toàn vẹn HTML.
