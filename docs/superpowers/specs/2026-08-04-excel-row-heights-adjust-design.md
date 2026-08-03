# Design Spec: Điều Chỉnh Chiều Cao Hàng Excel Export (Data 20pt, Header 30pt/19pt, Roman 26pt)

**Ngày:** 2026-08-04  
**Trạng thái:** Đã được phê duyệt bởi người dùng  

---

## 1. Mục tiêu

Điều chỉnh chiều cao hàng (`ws['!rows']`) trong 100% các sheet Excel export (Sheet 1 Tổng Hợp, Sheet 2 Chi Tiết Phòng, Sheet 3 Vật Tư Cần Mua và các sheet phòng) theo đúng thông số đã được duyệt:
- **Hàng dữ liệu hạng mục**: **`20pt`** (`{ hpt: 20, hpx: 27 }`).
- **Hàng tiêu đề bảng (Single-line)**: **`30pt`** (`{ hpt: 30, hpx: 40 }`) cho `wsSum` và `wsVT`.
- **Hàng tiêu đề bảng (Multi-line)**: **`19pt`/hàng** (`{ hpt: 19, hpx: 25 }`) cho `wsDetail` và các room sheets.
- **Hàng tiêu đề nhóm La Mã**: **`26pt`** (`{ hpt: 26, hpx: 35 }`).
- **Hàng thông tin dự án (R=0..3)**: **`20pt`**, Hàng thông tin khách hàng (R=4..6): **`19pt`**.

---

## 2. Thông số Chi tiết Cấu hình Hàng (`applyRowHeights`)

```javascript
function applyRowHeights(ws, headerCount = 8) {
  if (!ws || !ws['!ref']) return;
  const range = XLSX.utils.decode_range(ws['!ref']);
  const rows = [];
  const romanSet = new Set(['I','II','III','IV','V','VI','VII','VIII','IX','X','XI','XII']);
  const isMultiHeader = (headerCount > 8); // Room detail sheets có 2 hàng header (R=8,9)

  for (let R = 0; R <= range.e.r; R++) {
    if (R < 4) {
      rows.push({ hpt: 20, hpx: 27 });
    } else if (R >= 4 && R <= 6) {
      rows.push({ hpt: 19, hpx: 25 });
    } else if (R >= 8 && R <= headerCount) {
      if (isMultiHeader) {
        rows.push({ hpt: 19, hpx: 25 }); // 2 hàng header: 19pt/hàng
      } else {
        rows.push({ hpt: 30, hpx: 40 }); // 1 hàng header: 30pt
      }
    } else {
      const cellA = ws[XLSX.utils.encode_cell({ r: R, c: 0 })];
      const valA = cellA && cellA.v != null ? String(cellA.v).trim() : '';
      const isRoman = romanSet.has(valA);
      if (isRoman) {
        rows.push({ hpt: 26, hpx: 35 }); // Section headers (26pt)
      } else {
        rows.push({ hpt: 20, hpx: 27 }); // Data rows (20pt)
      }
    }
  }
  ws['!rows'] = rows;
}
```

---

## 3. Các Tệp Thay Đổi

- `src/excel.js`: Cập nhật hàm `applyRowHeights(ws, headerCount)` với các giá trị 20pt/30pt/19pt/26pt.
- `main.js`, `src/takeoff.js`, `index.html`: Cập nhật tham số Cache-Buster `?v=20260804-v1`.

---

## 4. Verification Plan

1. **Khảo sát cấu trúc HTML/JS**: Chạy `python check_final.py` xác minh cú pháp.
2. **Kiểm tra ứng dụng web**: Mở `http://localhost:8000/` bằng trình duyệt tự động kiểm tra giao diện web.
3. **Kiểm tra mảng rows trong SheetJS**: Kiểm tra mảng `ws['!rows']` của `wsSum`, `wsDetail`, `wsVT` có đúng hpt 20pt/30pt/19pt/26pt.
