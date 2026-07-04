# Đặc tả Thiết kế: Tái cấu trúc app.js thành ES6 Modules (Phần 1)

Tài liệu này đặc tả thiết kế kỹ thuật cho việc phân tách file mã nguồn [app.js](file:///d:/Kho%20tri%20th%E1%BB%A9c/khoi-luong-pro/app.js) thành cấu trúc module ES6 gọn gàng, tạo nền tảng vững chắc để phát triển module dự toán `du-toan-pro` mà không làm quá tải mã nguồn.

## 1. Mục tiêu & Phạm vi
- **Mục tiêu:** Chia nhỏ file `app.js` (gần 12,000 dòng) thành các file module chuyên biệt, mỗi file không quá 3,000 dòng.
- **Phạm vi bảo đảm:** Duy trì 100% tính năng hiện tại của phần bóc khối lượng, không thay đổi hành vi hiển thị, không làm ảnh hưởng đến dữ liệu cũ trong `LocalStorage` của người dùng.
- **Cách tiếp cận:** Sử dụng cơ chế ES6 Modules sẵn có của trình duyệt (không sử dụng Webpack/Vite/npm build) để đảm bảo app chạy tĩnh trực tiếp cực kỳ nhẹ và không có phụ thuộc cài đặt phức tạp.

## 2. Cấu trúc thư mục mã nguồn mới
Sau khi tái cấu trúc, thư mục gốc sẽ có các thay đổi sau:

```
d:\Kho tri thức\khoi-luong-pro\
├── index.html            <- [MODIFY] Thay đổi đường dẫn import script
├── main.js               <- [NEW] File chạy chính (Root Controller)
└── src/
    ├── db.js             <- [NEW] Chuyên quản lý cơ sở dữ liệu (LocalStorage)
    ├── calc.js           <- [NEW] Chuyên xử lý công thức toán học khối lượng
    ├── takeoff.js        <- [NEW] Chuyên render giao diện Bóc Khối Lượng
    └── excel.js          <- [NEW] Chuyên xử lý xuất dữ liệu Excel (SheetJS & ExcelJS)
```

> [!NOTE]
> File [app.js](file:///d:/Kho%20tri%20th%E1%BB%A9c/khoi-luong-pro/app.js) gốc sẽ được sao lưu thành `app.js.pre_modular_refactor.bak` và tạm thời giữ lại trong thư mục làm dữ liệu đối chiếu trong suốt quá trình phát triển trước khi dọn dẹp.

## 3. Thiết kế chi tiết phân rã mã nguồn

### 3.1. main.js (Bộ điều phối chính)
- **Nhiệm vụ:**
  - Khai báo đối tượng trạng thái toàn cục `state` và các cấu hình ứng dụng.
  - Lắng nghe sự kiện `DOMContentLoaded` để khởi chạy ứng dụng.
  - Quản lý chuyển tab giao diện (hiện tại là `bkl` / `takeoff`, `export`... và sau này là `dutoan`).
- **Imports:**
  ```javascript
  import { DB } from './src/db.js';
  import { initTakeoffUI } from './src/takeoff.js';
  ```

### 3.2. src/db.js (Quản lý dữ liệu)
- **Nhiệm vụ:**
  - Đóng gói toàn bộ logic tương tác với `localStorage` qua đối tượng `DB`.
  - Hỗ trợ các hàm: `DB.get(id)`, `DB.set(id, data)`, `DB.delete(id)`, `DB.list()`.
  - Cung cấp hàm khởi tạo dữ liệu mặc định cho dự án mới.

### 3.3. src/calc.js (Định mức & Công thức khối lượng)
- **Nhiệm vụ:**
  - Đóng gói đối tượng `CALC` chứa các logic tính toán kích thước phòng.
  - Tính toán diện tích sàn, trần, chu vi tường, khấu trừ diện tích cửa sổ, cửa đi từ kích thước Dài x Rộng x Cao của phòng.

### 3.4. src/takeoff.js (Giao diện Khối lượng)
- **Nhiệm vụ:**
  - Chứa toàn bộ mã nguồn xử lý DOM và hiển thị giao diện bóc khối lượng.
  - Render danh sách phòng, bảng nhập kích thước chi tiết, bộ chọn vật tư cho sàn/trần/tường/thiết bị điện.
  - Quản lý các sự kiện click, nhập liệu trực tiếp trên bảng.
- **Imports:**
  ```javascript
  import { DB } from './db.js';
  import { CALC } from './calc.js';
  import { exportExcel, exportPhotosExcel } from './excel.js';
  ```

### 3.5. src/excel.js (Xuất Excel)
- **Nhiệm vụ:**
  - Chứa logic sinh file Excel `Tổng hợp`, `Chi tiết phòng`, `Vật Tư Cần Mua` sử dụng SheetJS.
  - Chứa logic sinh file Excel ảnh hiện trạng sử dụng ExcelJS.

---

## 4. Kế hoạch kiểm tra & Xác minh (Verification Plan)

### Kiểm tra tính nhất quán chức năng:
1. **Khởi chạy ứng dụng:** Mở `index.html` cục bộ qua server tĩnh và kiểm tra ứng dụng có load dữ liệu cũ lên bình thường không.
2. **Thêm/Sửa/Xóa phòng:** Tạo phòng mới, nhập kích thước `Dài = 4000`, `Rộng = 3000`, `Cao = 2700` xem các giá trị diện tích sàn (`12m2`), perimeter (`14m`) có tự động nhảy công thức đúng không.
3. **Bộ chọn vật tư:** Thử chọn vật liệu ốp lát sàn, sơn tường và kiểm tra xem danh sách có lưu trữ chính xác vào LocalStorage không.
4. **Xuất Excel:** Thực hiện xuất file Excel khối lượng và kiểm tra xem file xuất ra có đầy đủ các tab, căn lề font chữ Times New Roman và các công thức liên kết như cũ không.

### Kiểm thử code tự động:
- Chạy lệnh `python check_final.py` để quét toàn bộ cú pháp JS và đảm bảo không có lỗi thiếu dấu ngoặc hoặc sai logic cú pháp sau khi phân tách.
