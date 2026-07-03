# Thiết kế sửa lỗi mất nút Lưu trên Mobile và tăng độ tương phản màu chữ

Tài liệu này mô tả chi tiết phương án sửa lỗi mất nút bấm "Lưu dự án / Tiếp theo" trên điện thoại di động và tăng độ tương phản của chữ trên toàn ứng dụng để giúp người dùng dễ đọc hơn.

## Yêu cầu

### 1. Sửa lỗi mất nút Lưu/Tiếp theo trên Mobile
- **Hiện trạng**: Trên thiết bị di động (màn hình dưới 768px), các nút chức năng ở chân modal (`.modal-footer`) như "Lưu Dự Án", "Hủy", "Tiếp theo", "Quay lại" bị ẩn hoàn toàn (`display: none;`) do thiết kế lỗi trước đó.
- **Giải pháp**: 
  - Khôi phục lại hiển thị của `.modal-footer` trên Mobile.
  - Thiết kế chân trang dạng dính dưới đáy màn hình (`position: sticky; bottom: 0;`) để người dùng luôn nhìn thấy và bấm được các nút chức năng (Lưu, Hủy, Tiếp theo) mà không cần cuộn trang tìm kiếm.

### 2. Tăng độ tương phản màu chữ (Đậm và rõ hơn)
- **Hiện trạng**: Các màu chữ mặc định đang dùng tone xám hơi nhạt (Slate 800/700/600), gây khó đọc trên các màn hình có độ sáng thấp hoặc khi dùng điện thoại ngoài trời.
- **Giải pháp**: Darken (làm đậm hơn) các biến CSS chỉ định màu chữ chính, chữ phụ và chữ ghi chú của hệ thống:
  - Màu chữ chính (`--color-text-primary`): Chuyển từ `#1E293B` sang `#0F172A` (Slate 900 - gần như đen tuyền).
  - Màu chữ phụ (`--color-text-secondary`): Chuyển từ `#475569` sang `#1E293B` (Slate 800 - xám đậm rõ nét).
  - Màu chữ nhạt/ghi chú (`--color-text-muted`): Chuyển từ `#64748B` sang `#334155` (Slate 700 - xám vừa dễ đọc).

---

## Đề xuất thay đổi

### CSS cần chỉnh sửa
Trong [style.css](file:///d:/Kho%20tri%20th%E1%BB%A9c/khoi-luong-pro/style.css):

1. **Thay đổi biến màu chữ (dòng ~19-21)**:
```css
  --color-text-primary:   #1E293B; /* Đậm hơn để dễ đọc trên nền sáng */
  --color-text-secondary: #475569;
  --color-text-muted:     #64748B;
```
Thay thế bằng:
```css
  --color-text-primary:   #0F172A; /* Slate 900 siêu đậm */
  --color-text-secondary: #1E293B; /* Slate 800 xám đậm rõ nét */
  --color-text-muted:     #334155; /* Slate 700 dễ đọc hơn */
```

2. **Chỉnh sửa hiển thị chân trang modal trên Mobile (dòng ~1427-1431)**:
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
2. Thu nhỏ màn hình trình duyệt xuống kích thước Mobile (hoặc mở F12 chế độ Responsive).
3. **Kiểm tra nút bấm**:
   - Click "Tạo dự án mới" -> Xác nhận dưới đáy màn hình xuất hiện thanh chứa nút **"Lưu Dự Án"** và **"Hủy"** dính cố định.
   - Click nút bút chì để sửa một phòng bất kỳ -> Xác nhận chân trang Wizard chứa nút **"Quay lại"** và **"Tiếp theo"** hiển thị rõ ràng và dính cố định ở đáy.
4. **Kiểm tra tương phản màu chữ**:
   - Xác nhận tất cả các nhãn (label), chữ tiêu đề, ghi chú trên ứng dụng hiển thị đậm, sắc nét và dễ nhìn thấy hơn hẳn phiên bản cũ.
