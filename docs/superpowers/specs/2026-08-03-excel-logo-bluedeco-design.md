# Design Spec: Thêm Logo Bluedeco vào File Excel (Cột B Hàng 1 Căn Trái)

**Ngày:** 2026-08-03  
**Trạng thái:** Đã duyệt bởi người dùng (Phương án 1)

---

## 1. Mục tiêu
Tự động nhúng hình ảnh logo thương hiệu BlueDeco (`logo-bluedecor.png`) vào góc trên bên trái của tất cả các trang tính (Sheet 1 *Tổng hợp*, Sheet 2+ *Chi tiết phòng*, *Vật tư cần mua*) trong file Excel xuất ra.

---

## 2. Vị trí & Định dạng Logo trong Excel

- **Vị trí cell**: Bắt đầu tại ô **B1** (Column index = 1, Row index = 0), căn lề trái.
- **Kích thước anchor**: Tọa độ từ ô B1 (Row 0, Col 1) đến B3 (Row 3, Col 1).
- **Tệp nguồn ảnh**: Nạp từ dữ liệu base64/buffer của `logo-bluedecor.png` đã được nạp sẵn trên client-side.

---

## 3. Kiến trúc & Kỹ thuật Triển khai

### 3.1 Hàm helper `injectLogoToBuffer(binBuf)`
Trong `src/excel.js`:
- Nhận mảng nhị phân `ArrayBuffer` tạo ra từ SheetJS (`XLSX.write`).
- Sử dụng `JSZip` giải nén workbook.
- Quét qua tất cả các file trang tính `xl/worksheets/sheet*.xml`.
- Thêm liên kết drawing XML `<drawing r:id="rId2"/>` vào từng worksheet chưa có thẻ drawing.
- Đóng gói file `xl/drawings/drawing1.xml` định vị hình ảnh tại Cột B (Col=1, ColOff=100000), Hàng 1 (Row=0, RowOff=63500) căn trái.
- Đóng gói file ảnh nhị phân vào `xl/media/image1.png`.
- Trả về `ArrayBuffer` hoàn chỉnh chứa logo.

### 3.2 Tích hợp vào `exportExcel()` & `xlsxWriteSheetJS()`
- Chuyển `xlsxWriteSheetJS` thành hàm `async`.
- Sau khi `XLSX.write` tạo ra binary buffer, tự động gọi `await injectLogoToBuffer(buf)` trước khi tạo `Blob` tải xuống cho người dùng.

---

## 4. File Thay Đổi
- `src/excel.js`: Bổ sung helper `injectLogoToBuffer()` và tích hợp vào luồng `exportExcel()` / `xlsxWriteSheetJS()`.
- `main.js`, `index.html`: Cập nhật phiên bản Cache-Buster `?v=20260803-v5`.

---

## 5. Kế hoạch Kiểm tra (Verification)
- [ ] Mở file Excel vừa xuất: Tất cả các sheet (*Tổng hợp*, *PHÒNG XÔNG*...) đều có logo BlueDeco xuất hiện ở cột B hàng 1 căn trái.
- [ ] Đảm bảo không làm ảnh hưởng đến căn lề cột B (hạng mục) và dữ liệu các hàng bên dưới.
- [ ] Chạy `check_final.py` xác minh cú pháp và tính toàn vẹn của ứng dụng.
