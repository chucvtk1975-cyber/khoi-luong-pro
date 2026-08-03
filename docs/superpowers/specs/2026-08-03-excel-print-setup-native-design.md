# Design Spec: Native SheetJS Excel Print Setup & Row Heights (No XML Manipulation)

**Ngày:** 2026-08-03  
**Trạng thái:** Đã được phê duyệt bởi người dùng  

---

## 1. Mục tiêu

1. Định dạng trang in trong **100% file Excel export** (Sheet 1 Tổng hợp, Sheet 2 Chi tiết phòng, Sheet 3 Vật tư cần mua và các sheet phòng) thành **Khổ A4 Ngang (Landscape)**, tự động **co vừa 1 trang ngang** khi mở Print Preview trong Microsoft Excel.
2. Thiết lập lề in chuẩn:
   - Lề Trái (**Left**): `1.8 cm` (`0.71 in`)
   - Lề Phải (**Right**): `1.0 cm` (`0.39 in`)
   - Lề Trên (**Top**): `1.4 cm` (`0.55 in`)
   - Lề Dưới (**Bottom**): `1.4 cm` (`0.55 in`)
3. Đánh số trang ở góc dưới bên phải theo định dạng **`1/6`, `2/6` ... `&P/&N`** (không chứa từ "Trang").
4. Thiết lập chiều cao hàng chuẩn:
   - Hàng dữ liệu hạng mục: **`24pt`** (`hpt: 24, hpx: 32`)
   - Hàng tiêu đề nhóm La Mã: **`26pt`** (`hpt: 26, hpx: 35`)
   - Hàng tiêu đề bảng: **`34pt`** (`hpt: 34, hpx: 45`)
5. **Tuyệt đối an toàn**: 100% sử dụng thuộc tính native của `xlsx-js-style` (SheetJS). **Bỏ hoàn toàn** mọi thao tác can thiệp chuỗi XML Zip trong `triggerAutoSync()` để loại bỏ rủi ro làm hỏng file Excel hoặc đè lỗi lên ứng dụng web.

---

## 2. Thông số Chi tiết

### 2.1. Cấu hình Trang in (`ws['!pageSetup']`)
```javascript
ws['!pageSetup'] = {
  paperSize:     9,           // 9 = A4
  orientation:   'landscape', // In ngang
  fitToPage:     true,
  fitToWidth:    1,           // Co vừa 1 trang ngang
  fitToHeight:   0,           // Tự do theo chiều dọc
  autoBreaks:    true,
  horizontalDpi: 300,
  verticalDpi:   300,
};
```

### 2.2. Lề in (`ws['!margins']`)
```javascript
ws['!margins'] = {
  left:   0.71, // 1.8 cm
  right:  0.39, // 1.0 cm
  top:    0.55, // 1.4 cm
  bottom: 0.55, // 1.4 cm
  header: 0.2,
  footer: 0.2,
};
```

### 2.3. Footer Đánh số trang (`ws['!headerFooter']`)
```javascript
ws['!headerFooter'] = {
  oddFooter:  '&L&"Arial,Italic"Du-Toan-BlueAI Lab&R&"Arial,Bold"&P/&N',
  evenFooter: '&L&"Arial,Italic"Du-Toan-BlueAI Lab&R&"Arial,Bold"&P/&N',
};
```

### 2.4. Chiều cao hàng (`ws['!rows']`)
Tự động tạo mảng `ws['!rows']` trong hàm `applyRowHeights(ws, headerCount)`:
- `R < 4`: `20pt` (`hpt: 20`)
- `R >= 4 && R <= 6`: `19pt` (`hpt: 19`)
- `R >= 8 && R <= headerCount`: `34pt` (`hpt: 34`)
- Hàng số La Mã (I, II, III...): `26pt` (`hpt: 26`)
- Hàng dữ liệu thường: `24pt` (`hpt: 24`)

---

## 3. Các Tệp Thay Đổi

- `src/excel.js`:
  - Cập nhật `applyPageSetup(ws)` với thông số Lề in và Footer `&P/&N`.
  - Thêm helper `applyRowHeights(ws, headerCount)` và gọi cho `wsDetail`, `wsSum`, `wsVT`.
  - Xóa bỏ hoàn toàn phần can thiệp chuỗi XML thay thế `<pageSetup>` trong `triggerAutoSync()`.
- `main.js`, `src/takeoff.js`, `index.html`: Cập nhật tham số Cache-Buster `?v=20260803-v28`.

---

## 4. Verification Plan

1. **Khảo sát cấu trúc HTML/JS**: Chạy `python check_final.py` xác minh cú pháp không có lỗi thẻ đóng mở hay lặp modal.
2. **Kiểm tra ứng dụng web**: Sử dụng browser verification trên `http://localhost:8000/` đảm bảo giao diện web và các modal hoạt động 100% mượt mà.
3. **Kiểm tra file Excel xuất ra**: Kiểm tra mảng `ws['!margins']`, `ws['!pageSetup']`, `ws['!rows']` và `ws['!headerFooter']` đảm bảo tạo đúng cấu trúc SheetJS.
