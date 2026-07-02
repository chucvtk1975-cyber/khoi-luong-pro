# Đặc tả Thiết kế: Nâng cấp Giao diện & Đổi màu Sidebar (Phương án 2)

Tài liệu đặc tả này mô tả kế hoạch thay đổi màu sắc và nâng cấp thẩm mỹ giao diện ứng dụng Bốc Khối Lượng Pro theo **Phương án 2 (Kính mờ - Hybrid)**, tối ưu hóa cho việc sử dụng thực tế ban ngày tại công trường.

---

## 1. Mục tiêu Thiết kế
- **Cân đối thị giác**: Khắc phục độ chênh lệch ánh sáng lớn giữa Sidebar (rất tối) và vùng nội dung (rất sáng) bằng cách làm sáng thanh Header và bo góc mềm mại các phần tử.
- **Độ tương phản tối đa**: Đảm bảo toàn bộ chữ trên Sidebar có độ tương phản cao, dễ đọc dưới ánh sáng ban ngày.
- **Thẩm mỹ cao cấp (Premium UX)**: Sử dụng các dải màu gradient mượt mà, bo góc hiện đại và hiệu ứng kính mờ (glassmorphism) tinh tế.
- **Thêm nhận diện thương hiệu**: Bổ sung chữ "Khối-Lượng-Pro" căn giữa hoàn hảo ở trên cùng của thanh Header chính.

---

## 2. Chi tiết Thay đổi CSS (Design Tokens)

Chúng ta sẽ điều chỉnh các biến CSS trong `:root` của [style.css](file:///d:/Kho%20tri%20th%E1%BB%A9c/khoi-luong-pro/style.css):

```css
:root {
  /* Tông màu chính mới - Cao cấp và dịu mắt */
  --color-primary:       #0F172A; /* Slate 900 cho các vùng tối sâu */
  --color-primary-hover: #1E293B; /* Slate 800 */
  --color-primary-light: #F1F5F9; /* Slate 100 cho hover ở vùng sáng */
  
  /* Gradient Sidebar trái */
  --sidebar-gradient:    linear-gradient(180deg, #1E293B 0%, #0F172A 100%);
  
  /* Màu nền của Header (Đổi từ tối sang sáng) */
  --bg-header:           #FFFFFF;
  --text-header:         #0F172A;
  
  /* Màu chữ chuyên biệt cho Sidebar tối */
  --sidebar-text-main:    #F8FAFC; /* Trắng sáng */
  --sidebar-text-muted:   #94A3B8; /* Xám xanh mờ */
  --sidebar-active-bg:    rgba(59, 130, 246, 0.15); /* Kính mờ xanh lam */
  --sidebar-active-border: #3B82F6; /* Xanh lam nổi bật */
}
```

---

## 3. Chi tiết Thay đổi theo Thành phần UI

### A. Thanh Header (.app-header)
- **Nền**: Đổi từ `var(--bg-sidebar)` (xanh đậm) sang `#FFFFFF` (trắng).
- **Chữ & Icon**: Chuyển sang màu đen sẫm `#0F172A`.
- **Đường viền dưới**: Thêm viền mỏng `1px solid #E2E8F0` để tách biệt rõ ràng với phần nội dung bên dưới.
- **Nhãn thương hiệu căn giữa**: Chèn thêm `<div class="header-center">Khối-Lượng-Pro</div>` căn giữa bằng thuộc tính absolute:
  ```css
  .header-center {
    position: absolute;
    left: 50%;
    transform: translateX(-50%);
    font-weight: 700;
    font-size: 16px;
    color: var(--text-header);
    letter-spacing: 0.5px;
  }
  ```

### B. Cột Sidebar Trái (.project-sidebar)
- **Nền**: Sử dụng `var(--sidebar-gradient)` mang lại chiều sâu 3D mượt mà.
- **Nút "Thêm dự án" (+)** và các bộ lọc: Chuyển sang viền trắng mờ, chữ trắng để nổi bật trên nền tối.
- **Thẻ dự án (.project-item)**:
  - *Mặc định*: Chữ tên dự án màu `#F8FAFC`, chữ phụ (số phòng, ngày tháng) màu `#94A3B8`.
  - *Khi Hover*: Nền chuyển sang màu xám mờ nhẹ `rgba(255, 255, 255, 0.05)`.
  - *Khi được Chọn (.active)*: 
    - Nền: `rgba(59, 130, 246, 0.15)` kết hợp hiệu ứng kính mờ `backdrop-filter: blur(8px)`.
    - Viền bên trái: Dày `3px solid #3B82F6`.
    - Chữ dự án: Màu trắng tinh `#FFFFFF` kèm font đậm `600`.

### C. Vùng làm việc chính (.workspace)
- **Nền chung**: Giữ tông sáng tinh tươm.
- **Thẻ chỉ số (Dashboard Cards)**: Tinh chỉnh đổ bóng bóng mềm hơn (`box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.05), 0 2px 4px -2px rgb(0 0 0 / 0.05)`).
- **Nút bấm & Trạng thái**: Các nút bấm có bo góc lớn hơn (`8px`), hiệu ứng chuyển màu khi di chuột mượt mà.

---

## 4. Kế hoạch Xác minh
- **Kiểm tra độ tương phản**: Sử dụng công cụ kiểm tra độ tương phản màu để đảm bảo toàn bộ text trên sidebar đạt chuẩn WCAG AA (độ tương phản > 4.5:1).
- **Kiểm thử giao diện**: Chạy app cục bộ và dùng browser subagent chụp ảnh giao diện thực tế gửi người dùng xem xét.
