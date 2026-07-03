# Thiết kế Đồng bộ Cơ sở dữ liệu đám mây Supabase

Tài liệu này mô tả giải pháp tích hợp cơ sở dữ liệu đám mây Supabase để tự động đồng bộ dự án giữa Máy tính và Điện thoại, giúp người dùng không cần sao lưu thủ công.

## Yêu cầu & Kiến trúc

### 1. Mô hình Local-First kết hợp Cloud Sync
- **Mục tiêu**: Đảm bảo tốc độ tải trang cực nhanh (load dữ liệu từ `localStorage` trước) và khả năng hoạt động offline.
- **Hoạt động**:
  - Khi ứng dụng khởi động: Tải dự án từ `localStorage` ra màn hình ngay lập tức, sau đó gọi API Supabase tải dữ liệu mới nhất ở nền và cập nhật (nếu có dự án mới hoặc thay đổi từ thiết bị khác).
  - Khi người dùng thêm/sửa/xóa dự án hoặc phòng: Lưu dữ liệu vào `localStorage` như cũ để đảm bảo tốc độ phản hồi lập tức, đồng thời gửi yêu cầu lưu (Upsert) lên Supabase để đồng bộ lên đám mây.

### 2. Không lưu cứng khóa bảo mật (Security Best Practice)
Để bảo mật tuyệt đối khóa API của anh/chị và tránh lộ thông tin trên GitHub, chúng ta sẽ **không ghi cứng** Supabase URL và API Key vào mã nguồn.
- Thay vào đó, chúng ta sẽ thêm một phần cài đặt **"Cấu hình đám mây (Supabase)"** trong menu hoặc cài đặt của App.
- Người dùng chỉ cần dán Supabase URL và Anon API Key vào một lần duy nhất trên máy tính và điện thoại. Thông tin này sẽ được lưu bảo mật trong trình duyệt của thiết bị đó.

### 3. Thiết lập trên Supabase Dashboard
Người dùng cần tạo một bảng tên là `projects` trong cơ sở dữ liệu Supabase của họ với cấu trúc sau:

```sql
create table projects (
  id text primary key,
  name text not null,
  client text,
  data jsonb not null,
  updated_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- Tắt RLS để truy cập nhanh không cần đăng nhập tài khoản (phù hợp cho ứng dụng nội bộ)
alter table projects disable row level security;
```

---

## Các thay đổi đề xuất

### 1. Tích hợp Thư viện Supabase CDN
Thêm thư viện Supabase vào thẻ `<head>` của [index.html](file:///d:/Kho%20tri%20th%E1%BB%A9c/khoi-luong-pro/index.html):
```html
<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
```

### 2. Bổ sung giao diện cấu hình trong cài đặt
Thêm giao diện nhập thông tin kết nối Supabase vào Sidebar hoặc cài đặt:
- Hộp nhập: **Supabase URL** (mặc định hiển thị link `https://repvqjjptxaofwbzivvj.supabase.co`).
- Hộp nhập: **Supabase Anon API Key**.
- Trạng thái kết nối: Hiện chấm xanh lá (Đã kết nối) hoặc chấm đỏ (Chưa cấu hình/Lỗi).
- Nút bấm: **Đồng bộ ngay** (Để ép đồng bộ hai chiều lập tức).

### 3. Tích hợp Logic Đồng bộ trong `app.js`
- **Khởi tạo Supabase Client**:
  Đọc thông tin từ `localStorage` để khởi tạo client kết nối.
- **Hàm đồng bộ dự án**:
  - `syncProjectsFromCloud()`: Tải toàn bộ dự án từ Supabase về, so sánh thời gian cập nhật (`updated_at`), bổ sung các dự án mới vào `localStorage`, rồi render lại danh sách.
  - `syncProjectToCloud(project)`: Gửi dự án lên Supabase bằng lệnh `upsert`.

---

## Kế hoạch kiểm thử

### Kiểm thử thủ công
1. Chạy app trên máy tính, mở cài đặt nhập Supabase URL và API Key, bấm lưu.
2. Tạo dự án "Dự án Máy Tính".
3. Mở điện thoại, nhập thông tin kết nối tương tự.
4. Xác nhận "Dự án Máy Tính" tự động xuất hiện trên màn hình điện thoại mà không cần làm gì thêm!
