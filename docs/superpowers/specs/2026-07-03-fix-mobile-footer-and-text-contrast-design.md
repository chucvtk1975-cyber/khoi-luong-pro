# Thiết kế sửa lỗi mất nút Lưu trên Mobile và tăng độ tương phản màu chữ

Tài liệu này mô tả chi tiết phương án sửa lỗi mất nút bấm "Lưu dự án / Tiếp theo" trên điện thoại di động, tăng độ tương phản của chữ trên toàn ứng dụng và đổi màu các tiêu đề/nhãn trong Modal dự án thành màu xanh đậm rõ nét (#1E293B).

## Yêu cầu

### 1. Sửa lỗi mất nút Lưu/Tiếp theo trên Mobile
- **Hiện trạng**: Trên thiết bị di động (màn hình dưới 768px), các nút chức năng ở chân modal (`.modal-footer`) như "Lưu Dự Án", "Hủy", "Tiếp theo", "Quay lại" bị ẩn hoàn toàn (`display: none;`) do thiết kế lỗi trước đó.
- **Giải pháp**: 
  - Khôi phục lại hiển thị của `.modal-footer` trên Mobile.
  - Thiết kế chân trang dạng dính dưới đáy màn hình (`position: sticky; bottom: 0;`) để người dùng luôn nhìn thấy và bấm được các nút chức năng (Lưu, Hủy, Tiếp theo) mà không cần cuộn trang tìm kiếm.

### 2. Tăng độ tương phản màu chữ (Đậm và rõ hơn)
- **Giải pháp**: Làm đậm các biến màu chữ chính trên toàn ứng dụng để đảm bảo độ sắc nét trên mọi loại màn hình.
  - Màu chữ chính (`--color-text-primary`): Chuyển từ `#1E293B` sang `#0F172A` (Slate 900 - đen xanh cực đậm).
  - Màu chữ phụ (`--color-text-secondary`): Chuyển từ `#475569` sang `#1E293B` (Slate 800 - xanh xám đậm rõ nét).
  - Màu chữ nhạt/ghi chú (`--color-text-muted`): Chuyển từ `#64748B` sang `#334155` (Slate 700).

### 3. Đổi màu tiêu đề/nhãn trong Modal Dự Án thành màu `#1E293B`
- **Yêu cầu**: Thiết lập màu của các tiêu đề hạng mục và thông tin bên lập/nhận trong Modal tạo/sửa dự án (`#modal-project`) thành màu `#1E293B` để hiển thị đồng bộ và sắc nét.
- **Các tiêu đề/nhãn áp dụng**:
  - `TÊN HẠNG MỤC`
  - `CÔNG TRÌNH`
  - `NGÀY LẬP DỰ TOÁN`
  - `LOẠI HÌNH CÔNG TRÌNH`
  - `HÌNH THỨC THI CÔNG`
  - `THÔNG TIN BÊN LẬP`
  - `THÔNG TIN BÊN NHẬN`

---

## Đề xuất thay đổi

### CSS cần chỉnh sửa
Trong [style.css](file:///d:/Kho%20tri%20th%E1%BB%A9c/khoi-luong-pro/style.css):

1. **Thay đổi biến màu chữ toàn cục (dòng ~19-21)**:
```css
  --color-text-primary:   #1E293B; /* Đậm hơn để dễ đọc trên nền sáng */
  --color-text-secondary: #475569;
  --color-text-muted:     #64748B;
```
Thay thế bằng:
```css
  --color-text-primary:   #0F172A; /* Slate 900 siêu đậm */
  --color-text-secondary: #1E293B; /* Slate 800 xanh xám đậm */
  --color-text-muted:     #334155; /* Slate 700 dễ đọc */
```

2. **Cấu hình cứng màu các nhãn/tiêu đề trong Modal dự án thành `#1E293B`**:
Thêm đoạn mã CSS sau vào file `style.css`:
```css
/* Màu tiêu đề và nhãn trong Modal Dự án */
#modal-project .form-group label,
#modal-project .section-title {
  color: #1E293B !important;
}
```

3. **Chỉnh sửa hiển thị chân trang modal trên Mobile (dòng ~1427-1431)**:
```css
  /* An nut footer goc (dua xuong duoi trong modal) */
  .modal-footer {
    display: none;
  }
```
Thay thế bằng:
```css
  /* Hiện nút chân trang và ghim dính ở đáy modal trên Mobile */
  .modal-footer {
    display: flex !important;
    position: sticky !important;
    bottom: 0;
    z-index: 100;
    background: var(--bg-card) !important;
    border-top: 1px solid var(--border-light) !important;
    padding: 10px 16px !important;
    box-shadow: 0 -2px 10px rgba(0,0,0,0.05);
  }
```

---

## Kế hoạch kiểm thử

### Kiểm thử tự động / Cú pháp
1. Kiểm tra cấu trúc thẻ đóng mở:
   ```powershell
   python check_final.py
   ```
   Expected: SUCCESS.

### Kiểm thử thủ công
1. Mở ứng dụng trong trình duyệt.
2. Click nút **"Tạo Dự Án Mới"** -> Xác nhận các nhãn "Tên hạng mục", "Công trình", "Ngày lập dự toán", "Loại hình công trình", "Hình thức thi công" và hai tiêu đề phụ "Thông tin bên lập", "Thông tin bên nhận" đều có màu xanh đậm `#1E293B` rõ nét.
3. Thu nhỏ màn hình xuống kích thước điện thoại di động:
   - Click "Tạo dự án mới" -> Xác nhận dưới đáy màn hình xuất hiện thanh chứa nút **"Lưu Dự Án"** và **"Hủy"** dính cố định.
   - Click nút sửa một phòng bất kỳ -> Xác nhận chân trang Wizard chứa nút **"Quay lại"** và **"Tiếp theo"** hiển thị rõ ràng và dính cố định ở đáy.
