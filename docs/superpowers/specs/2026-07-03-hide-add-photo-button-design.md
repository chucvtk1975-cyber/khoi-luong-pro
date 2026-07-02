# Thiết kế ẩn nút "Thêm ảnh" trên Card phòng ở Trang chủ

Tài liệu này đặc tả thay đổi giao diện để ẩn nút "+ Thêm ảnh" trên card phòng ở Trang chủ, đồng thời giữ nguyên bộ đếm số lượng ảnh.

## Yêu cầu
- Ẩn/loại bỏ hoàn toàn nút "+ Thêm ảnh" và thẻ `input` file tương ứng trên giao diện card phòng ở Trang chủ.
- Giữ nguyên hiển thị đếm số lượng ảnh: `📷 Ảnh hiện trạng: X tấm` ở góc dưới bên trái card phòng.
- Giữ nguyên các chức năng đính kèm và quản lý ảnh chi tiết bên trong Modal thêm/sửa phòng (Wizard) và tab "Tài liệu".

## Đề xuất thay đổi

### Mã nguồn cần chỉnh sửa
Trong hàm `_renderRoomsList` tại [app.js](file:///d:/Kho%20tri%20th%E1%BB%A9c/khoi-luong-pro/app.js):
- Loại bỏ khối HTML chứa thẻ `input` file và nút bấm `+ Thêm ảnh`.
- Cụ thể, thay thế:
```html
        <div class="room-card-photos" style="margin-top: 12px; padding-top: 10px; border-top: 1px dashed var(--border-color); display: flex; align-items: center; justify-content: space-between; font-size: 12px;">

          <span style="color: var(--text-secondary);">📷 Ảnh hiện trạng: <strong style="color: var(--brand-blue-light);">${getRoomPhotosCount(room)}</strong> tấm</span>

          <div>

            <input type="file" accept="image/*" multiple id="room-card-file-${room.id}" style="display: none;" onchange="handleRoomCardPhotoSelect(event, '${room.id}')">

            <button class="btn-primary" style="padding: 2px 8px; font-size: 11px; height: auto;" onclick="document.getElementById('room-card-file-${room.id}').click()">+ Thêm ảnh</button>

          </div>

        </div>
```
Bằng:
```html
        <div class="room-card-photos" style="margin-top: 12px; padding-top: 10px; border-top: 1px dashed var(--border-color); display: flex; align-items: center; justify-content: space-between; font-size: 12px;">

          <span style="color: var(--text-secondary);">📷 Ảnh hiện trạng: <strong style="color: var(--brand-blue-light);">${getRoomPhotosCount(room)}</strong> tấm</span>

        </div>
```

---

## Kế hoạch kiểm thử

### Kiểm thử thủ công
1. Mở ứng dụng trong trình duyệt.
2. Xác nhận nút "+ Thêm ảnh" biến mất trên các card phòng ở trang chủ.
3. Xác nhận số lượng ảnh của phòng (ví dụ: `📷 Ảnh hiện trạng: 46 tấm`) vẫn hiển thị đầy đủ.
