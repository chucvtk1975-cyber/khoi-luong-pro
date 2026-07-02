# Thiết kế hiển thị số liệu phòng cho phần Chi Phí Khác ở Bản Xem Trước

Tài liệu này đặc tả thiết kế hiển thị số liệu cột phòng cho phần **Chi Phí Khác** trên Bản xem trước (Web Preview) đồng bộ với file PDF/Excel.

## Yêu cầu
- Khi xem bảng tổng hợp khối lượng trong phần "Xem Trước", các cột đại diện cho từng phòng của phần **CHI PHÍ KHÁC** phải hiển thị số liệu thực tế thay vì hiển thị dấu gạch ngang (`—`).
- Số liệu hiển thị trên Web Preview phải trùng khớp hoàn toàn với số liệu trong file Excel/PDF đã xuất.

## Đề xuất thay đổi

### Cấu trúc dữ liệu và logic kết xuất
Trong hàm `_renderPreviewSummary(project, rooms)` tại [app.js](file:///d:/Kho%20tri%20th%E1%BB%A9c/khoi-luong-pro/app.js):
- Thay thế biến tĩnh `blankCols` bằng việc lặp qua danh sách `rooms` để tính toán số lượng cho từng phòng:
  - Diện tích sàn cho từng phòng: `const tf = (+r.D || 0) / 1000 * (+r.R || 0) / 1000;`
  - Số lượng hạng mục: `const roomQty = tmpl.autoQty ? +(tf.toFixed(2)) : +(saved.qty != null ? saved.qty : tmpl.defaultQty);`
  - Định dạng hiển thị bằng hàm `fmt(roomQty)`.

---

## Kế hoạch kiểm thử

### Kiểm thử thủ công
1. Mở ứng dụng trong trình duyệt.
2. Chọn dự án thử nghiệm có từ 2 phòng trở lên.
3. Chuyển sang tab **Bảng Dự Toán** và nhấn nút **Xem Trước**.
4. Cuộn xuống phần **CHI PHÍ KHÁC** và xác nhận số liệu ở cột từng phòng hiển thị diện tích/đơn vị tương ứng thay vì dấu gạch ngang.
