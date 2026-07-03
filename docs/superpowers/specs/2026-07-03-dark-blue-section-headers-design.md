# Thiết kế giao diện thanh tiêu đề hộp màu xanh đậm cho Modal phòng

Tài liệu này mô tả chi tiết việc thiết kế lại các tiêu đề phân chia khu vực (như Kích thước, Lỗ cửa, Vật liệu, Ghi chú, Thiết bị điện) bên trong Modal thêm/sửa phòng thành các thanh hộp (block) màu xanh đậm (#0F172A), chữ trắng để tăng tính nhận diện và phân cấp thông tin.

## Yêu cầu
- Đổi kiểu hiển thị của `.section-title` bên trong `#modal-room` từ dạng chữ thường có gạch chân sang dạng hộp có nền (block).
- **Màu nền**: `#0F172A` (Màu xanh đậm theo ảnh đính kèm của người dùng, tương đương với `--color-primary`).
- **Màu chữ và icon**: Màu trắng (`#FFFFFF`).
- **Độ nổi bật**: Cần có padding hợp lý để chữ không sát lề nền, có bo góc nhẹ (`border-radius: 6px`) và khoảng cách (margin) tách biệt rõ ràng với phần nội dung phía trên và dưới.
- **Loại bỏ**: Đường gạch chân ở dưới tiêu đề mặc định (`border-bottom: none`).

## Đề xuất thay đổi

### CSS cần chỉnh sửa
Trong [style.css](file:///d:/Kho%20tri%20th%E1%BB%A9c/khoi-luong-pro/style.css):
Sửa đổi các quy tắc CSS cho `#modal-room .section-title` và `#modal-room .mat-section-title` để hiển thị dạng hộp.

Cụ thể, tại quy tắc hiện tại (dòng ~3246-3261):
```css
#modal-room .section-title,
#modal-room .mat-section-title {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-weight: 700;
  font-size: 14px;
}
#modal-room .section-title svg,
#modal-room .mat-section-header svg {
  width: 16px;
  height: 16px;
  color: var(--text-secondary);
  flex-shrink: 0;
  vertical-align: middle;
}
```

Sẽ được thay thế bằng:
```css
#modal-room .section-title,
#modal-room .mat-section-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 700;
  font-size: 13px;
  text-transform: uppercase;
  color: #FFFFFF !important;
  background-color: #0F172A;
  padding: 8px 12px;
  border-radius: 6px;
  margin: 22px 0 12px 0;
  border-bottom: none !important;
}
#modal-room .section-title svg,
#modal-room .mat-section-header svg {
  width: 16px;
  height: 16px;
  color: #FFFFFF !important;
  flex-shrink: 0;
  vertical-align: middle;
}
```

---

## Kế hoạch kiểm thử

### Kiểm thử tự động / Cú pháp
1. Kiểm tra cấu trúc đóng mở thẻ HTML của toàn dự án bằng script:
   ```powershell
   python check_final.py
   ```
   Expected: Thành công, không có thẻ div nào bị lỗi đóng mở.

### Kiểm thử thủ công
1. Mở ứng dụng trong trình duyệt.
2. Click **Thêm phòng** hoặc **Sửa phòng** (icon bút chì trên card phòng) để mở Modal phòng.
3. Xác nhận trực quan các thanh tiêu đề phân chia khu vực:
   - "Kích thước (mm — nhập thẳng từ AutoCAD)"
   - "Khai báo lỗ cửa (để trừ tường)"
   - "Vật liệu bề mặt"
   - "Ghi chú phòng (tùy chọn)"
   - "Thiết Bị Điện (Khảo sát nhập tay vào ô ghi chú)"
   Đều hiển thị dưới dạng thanh ngang nền màu xanh đậm (#0F172A), chữ trắng và icon trắng, bo góc 6px, chia khoảng cách cân đối.
