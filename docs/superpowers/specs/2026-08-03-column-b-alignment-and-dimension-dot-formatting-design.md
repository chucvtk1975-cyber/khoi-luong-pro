# Design Spec: Căn trái Cột B (Hạng Mục) Thụt 15px & Định Dạng Kích Thước DÀI, RỘNG, CAO Có Dấu Chấm

**Ngày tạo:** 03/08/2026  
**Trạng thái:** Đã thống nhất với người dùng (Phương án 1)

---

## 1. Mục Tiêu & Yêu Cầu

### 1.1. Căn lề Cột B (HẠNG MỤC)
- **Trên Web UI / Preview / PDF Export:**
  - Tất cả các data row ở Cột B (HẠNG MỤC) trên tất cả các bảng (Bảng Chi Tiết Phòng, Bảng Tổng Hợp, Bảng Vật Tư Cần Mua, Popup Preview, In PDF) phải được **căn trái (left-aligned)** và **thụt vào 15px** (`padding-left: 15px !important;`).
  - Tiêu đề La Mã (Section header như `I. XÂY DỰNG CƠ BẢN`): Căn trái, in đậm, không thụt lề.
  - Các dòng ghi chú (Note rows `Bằng chữ: ...`, `_ Báo giá trên...`, `_ Thời gian thi công...`): Giữ nguyên căn trái theo quy tắc bất biến trong `AGENTS.md`.
- **Trong File Excel Export (`.xlsx`):**
  - Áp dụng **vòng lặp Lock-Down ở bước xuất cuối cùng** cho tất cả các sheet (`wsDetail`, `wsSum`, `wsVT`).
  - Mọi data row tại cột B (`C=1`): Căn trái (`horizontal: 'left'`) và thụt lề 1 bậc (`indent: 1`).
  - Tiêu đề La Mã: Căn trái, không indent (`indent: 0`).

### 1.2. Định dạng Kích thước DÀI, RỘNG, CAO
- **Trên Web UI / Preview / PDF Export:**
  - Tất cả ô kích thước DÀI, RỘNG, CAO trên các bảng chi tiết phải được định dạng hiển thị phân cách hàng ngàn bằng dấu chấm (ví dụ: `6.425`, `3.207`, `1.760`, `2.300`).
  - Sử dụng thống nhất hàm `fmtMM(n)` (`v.toLocaleString('vi-VN')`).
- **Trong File Excel Export (`.xlsx`):**
  - Ô số liệu DÀI, RỘNG, CAO (Cột C, D, E hoặc `c=2,3,4` trong sheet chi tiết) được gán định dạng số `cell.z = '#,##0'`. Khi mở trên Excel Việt Nam/Hệ thống chuẩn, số sẽ tự động phân cách bằng dấu chấm (ví dụ: `6.425`, `2.300`).

---

## 2. Phạm Vi Ảnh Hưởng & Các File Chỉnh Sửa

1. **`src/takeoff.js`**:
   - Cập nhật render HTML cho bảng chi tiết phòng (`renderBOQ`), bảng tổng hợp dự án, bảng xem trước HTML (`previewHtml`), bảng xuất PDF.
   - Thêm class hoặc inline style `text-align: left; padding-left: 15px;` cho `td` Cột B của data rows.
   - Đảm bảo các ô DÀI, RỘNG, CAO đều gọi `fmtMM()` khi render giá trị số.

2. **`src/excel.js`**:
   - Thiết lập `z: '#,##0'` cho ô kích thước D, R, H trong `wsDetail`.
   - Cập nhật Vòng Lặp Lock-Down ở cuối hàm tạo sheet Excel (`wsDetail`, `wsSum`, `wsVT`): Ép căn trái `horizontal: 'left'`, `indent: 1` cho Cột B (`C=1`) dữ liệu.

3. **`style.css`**:
   - Thêm quy tắc CSS cho `.boq-dim`, `.ep-detail-table td.boq-item-name`, `.boq-table td:nth-child(2)` đảm bảo `text-align: left; padding-left: 15px;`.

4. **`index.html`**:
   - Tăng tham số version cache-buster (`?v=...`) trong thẻ script `main.js` và `style.css` lên phiên bản mới nhất theo đúng quy tắc `AGENTS.md`.

---

## 3. Quy Tắc An Toàn & Tuân Thủ (AGENTS.md)
- Không làm hỏng các vòng lặp Lock-Down căn trái cho Note rows (`Bằng chữ:...`, `_ Báo giá...`) và Header Info Rows (`Từ:`, `Kính gởi:`).
- Lock-down loop cho Cột B (`C=1`) và alignment phải được đặt chạy SAU CÙNG trước khi ghi workbook/trả về worksheet.
- Cập nhật tham số query version `?v=...` trên `index.html`.
