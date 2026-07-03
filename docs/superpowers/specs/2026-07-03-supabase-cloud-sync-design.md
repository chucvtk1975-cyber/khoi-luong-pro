# Thiết kế Đồng bộ Cơ sở dữ liệu đám mây Supabase

Tài liệu này mô tả giải pháp tích hợp cơ sở dữ liệu đám mây Supabase để tự động đồng bộ dự án giữa Máy tính và Điện thoại, giúp người dùng không cần sao lưu thủ công.

## Yêu cầu & Kiến trúc

### 1. Mô hình Local-First kết hợp Cloud Sync
- **Mục tiêu**: Đảm bảo tốc độ tải trang cực nhanh (load dữ liệu từ `localStorage` trước) và khả năng hoạt động offline.
- **Hoạt động**:
  - Khi ứng dụng khởi động: Tải dự án từ `localStorage` ra màn hình ngay lập tức, sau đó gọi API Supabase tải dữ liệu mới nhất ở nền và cập nhật (nếu có dự án mới hoặc thay đổi từ thiết bị khác).
  - Khi người dùng thêm/sửa/xóa dự án hoặc phòng: Lưu dữ liệu vào `localStorage` như cũ để đảm bảo tốc độ phản hồi lập tức, đồng thời gửi yêu cầu lưu (Upsert) lên Supabase để đồng bộ lên đám mây.

### 2. Thiết lập trên Supabase Dashboard
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

### 2. Thêm cấu hình Supabase vào Giao diện/Cấu trúc hệ thống
Để bảo mật và linh hoạt, chúng ta sẽ cấu hình Supabase URL và API Key trực tiếp trong code, hoặc cho phép người dùng cấu hình qua giao diện và lưu vào `localStorage`. 
* **Phương án đề xuất**: Cấu hình cố định trong file `app.js` để ứng dụng tự động chạy ngay khi mở link web trên mọi thiết bị mà không cần nhập lại API Key.

### 3. Tích hợp Logic Đồng bộ trong `app.js`
- **Khởi tạo Supabase Client**:
  ```javascript
  const SUPABASE_URL = 'https://repvqjjptxaofwbzivvj.supabase.co'; // Lấy từ link của người dùng
  const SUPABASE_KEY = 'ANON_KEY_CỦA_ANH_CHỊ'; // Sẽ điền sau khi có thông tin
  let supabase = null;
  if (SUPABASE_URL && SUPABASE_KEY !== 'ANON_KEY_CỦA_ANH_CHỊ') {
    supabase = supabase.createClient(SUPABASE_URL, SUPABASE_KEY);
  }
  ```
- **Hàm đồng bộ dự án**:
  - `syncProjectsFromCloud()`: Tải toàn bộ dự án từ Supabase về, so sánh thời gian cập nhật (`updated_at`), bổ sung các dự án mới vào `localStorage`, rồi render lại danh sách.
  - `syncProjectToCloud(project)`: Gửi dự án lên Supabase bằng lệnh `upsert`.

---

## Kế hoạch kiểm thử

### Kiểm thử thủ công
1. Chạy app trên máy tính, tạo dự án "Dự án Máy Tính".
2. Chờ 2 giây, mở app trên điện thoại (Vercel link).
3. Xác nhận "Dự án Máy Tính" tự động xuất hiện trên màn hình điện thoại mà không cần làm gì thêm!
4. Sửa thông tin dự án trên điện thoại -> kiểm tra xem máy tính có tự động nhận dữ liệu mới không.
