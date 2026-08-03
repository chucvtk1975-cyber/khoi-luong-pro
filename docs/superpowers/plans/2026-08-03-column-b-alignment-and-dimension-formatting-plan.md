# Implementation Plan: Căn Trái Cột B Thụt 15px & Định Dạng Số Kích Thước Có Dấu Chấm

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Căn trái + thụt vào 15px (indent: 1) cho tất cả các data row ở Cột B (HẠNG MỤC) và định dạng số kích thước DÀI, RỘNG, CAO có dấu chấm phân cách (VD: `6.425`, `2.300`) trên tất cả các sheet (Web UI, PDF Preview, Excel Export).

**Architecture:** 
- Thêm quy tắc CSS trong `style.css` và inline style trong `src/takeoff.js` cho Cột B căn trái `padding-left: 15px !important;`. 
- Cập nhật ô kích thước DÀI, RỘNG, CAO gọi hàm `fmtMM(n)` (`vi-VN` format) trên Web/PDF và `cell.z = '#,##0'` trong `src/excel.js`.
- Áp dụng pattern **Lock-Down Loop Chạy Cuối** trong `src/excel.js` cho tất cả các sheet (`wsDetail`, `wsSum`, `wsVT`) theo đúng quy tắc bất biến `AGENTS.md`.

**Tech Stack:** Vanilla HTML5, CSS3, ES6 JavaScript, SheetJS / XLSX-Style.

## Global Constraints
- **AGENTS.md Rule 1:** Không tự ý thay đổi code đã hoàn tất ngoại trừ yêu cầu được chỉ định.
- **AGENTS.md Rule 2:** Căn lề trái cho Note Rows (`Bằng chữ:...`, `_ Báo giá...`) trong Excel & PDF bắt buộc đứng TRƯỚC.
- **AGENTS.md Rule 4 & 5 & 6:** Vòng lặp Lock-Down cho Cột B (`C=1`) và Header Info Rows (`C=0,4`) phải chạy CUỐI CÙNG sau tất cả các hàm style trong `src/excel.js`.
- **AGENTS.md Rule Cache-Buster:** Tăng tham số `?v=...` cho `main.js` và `style.css` trong `index.html`.

---

### Task 1: Cập Nhật CSS và HTML Table Rendering (`style.css` & `src/takeoff.js`)

**Files:**
- Modify: `style.css`
- Modify: `src/takeoff.js`

**Interfaces:**
- Consumes: `fmtMM(n)` từ `src/calc.js`
- Produces: Web UI & PDF HTML preview với cột B căn trái 15px, kích thước D, R, H định dạng dấu chấm (`6.425`, `2.300`).

- [ ] **Step 1: Cập nhật `style.css` cho Cột B**

Thêm/cập nhật CSS rule trong `style.css`:
```css
/* Align Column B (HẠNG MỤC) data cells to left with 15px indent */
.boq-table td.boq-item-name,
.ep-detail-table td.boq-item-name,
.boq-table tbody tr:not(.boq-room-title):not(.boq-room-header):not(.boq-elec-header):not(.boq-note-header):not(.boq-sub-header):not(.boq-other-header) td:nth-child(2),
.ep-detail-table tbody tr:not(.boq-room-title):not(.boq-room-header):not(.boq-elec-header):not(.boq-note-header):not(.boq-sub-header):not(.boq-other-header) td:nth-child(2) {
  text-align: left !important;
  padding-left: 15px !important;
}
```

- [ ] **Step 2: Cập nhật `src/takeoff.js` renderBOQ & renderSummary**

Trong `src/takeoff.js`:
1. Tại các ô Cột B (HẠNG MỤC) dữ liệu thường trong `renderBOQ`:
   Ensure `style="color:var(--text-main);text-align:left;padding-left:15px;"` hoặc gán class `boq-item-name`.
2. Tại các ô kích thước DÀI (`item.dai`), RỘNG (`item.rong`), CAO (`item.cao`):
   Sử dụng `fmtMM(item.dai)`, `fmtMM(item.rong)`, `fmtMM(item.cao)` thay vì hiển thị số thô.

- [ ] **Step 3: Kiểm tra cú pháp JavaScript**

Chạy: `python check_final.py`
Expected: PASS không có lỗi syntax.

- [ ] **Step 4: Commit Task 1**

```bash
git add style.css src/takeoff.js
git commit -m "feat: align Column B left with 15px indent and format dimensions with fmtMM"
```

---

### Task 2: Cập Nhật Excel Export & Vòng Lặp Lock-Down Cuối (`src/excel.js`)

**Files:**
- Modify: `src/excel.js:1675-1725`, `src/excel.js:2680-2720`

**Interfaces:**
- Consumes: SheetJS `ws` object
- Produces: `.xlsx` file với cột B căn trái + indent 1 và ô kích thước format `#,##0` cho tất cả các sheet (`wsDetail`, `wsSum`, `wsVT`).

- [ ] **Step 1: Đặt format số `z = '#,##0'` cho ô DÀI, RỘNG, CAO trong `wsDetail`**

Trong `src/excel.js`, khi gán các ô `daiNum`, `rongNum`, `caoNum` vào `wsDetail`:
```javascript
['C', 'D', 'E'].forEach(col => {
  const ref = `${col}${aoaRow + 1}`;
  if (wsDetail[ref] && typeof wsDetail[ref].v === 'number') {
    if (!wsDetail[ref].s) wsDetail[ref].s = {};
    wsDetail[ref].s.numFmt = '#,##0';
    wsDetail[ref].z = '#,##0';
  }
});
```

- [ ] **Step 2: Thêm Lock-Down loop cho `wsDetail` và `wsVT` ở cuối `generateWorkbook`**

Trong `src/excel.js`, sau khi `applyBoldSectionRows` và các hàm style hoàn tất, chạy vòng lặp Lock-Down cho Cột B (`C=1`) đối với:
1. `wsDetail` (Tất cả các sheet chi tiết phòng):
```javascript
// ⚠️ LOCK-DOWN: Ép căn TRÁI + indent=1 cho cột HẠNG MỤC (C=1) trong mọi data row của sheet Chi Tiết
{
  const _drng = XLSX.utils.decode_range(wsDetail['!ref']);
  for (let _R = 10; _R <= _drng.e.r; _R++) {
    const _ref1 = XLSX.utils.encode_cell({ r: _R, c: 1 });
    if (!wsDetail[_ref1]) continue;
    const _v = wsDetail[_ref1].v != null ? String(wsDetail[_ref1].v).trim() : '';
    const _cell0 = wsDetail[XLSX.utils.encode_cell({ r: _R, c: 0 })];
    const _valA = _cell0 && _cell0.v != null ? String(_cell0.v).trim() : '';
    const _isRoman = ['I','II','III','IV','V','VI','VII','VIII'].includes(_valA);
    if (!wsDetail[_ref1].s) wsDetail[_ref1].s = {};
    if (_isRoman) {
      wsDetail[_ref1].s.alignment = { horizontal: 'left', vertical: 'center', wrapText: false };
    } else if (_v !== '') {
      wsDetail[_ref1].s.alignment = { horizontal: 'left', vertical: 'center', wrapText: true, indent: 1 };
    }
  }
}
```

2. `wsSum` (Sheet Tổng Hợp) - Giữ nguyên và bảo toàn lock-down loop hiện tại.
3. `wsVT` (Sheet Vật Tư Cần Mua) - Thêm lock-down loop tương tự cho cột HẠNG MỤC.

- [ ] **Step 3: Kiểm tra cú pháp `src/excel.js`**

Chạy: `python check_final.py`
Expected: PASS không lỗi syntax.

- [ ] **Step 4: Commit Task 2**

```bash
git add src/excel.js
git commit -m "feat: add lockdown loop for Column B alignment and dimension number format in excel export"
```

---

### Task 3: Cache-Buster Version Bump & Xác Minh Tổng Thể (`index.html`)

**Files:**
- Modify: `index.html`

- [ ] **Step 1: Cập nhật `index.html` Cache-Buster Query Param**

Trong `index.html`:
- Đổi `style.css?v=...` thành `style.css?v=20260803-v1`
- Đổi `main.js?v=...` thành `main.js?v=20260803-v1`

- [ ] **Step 2: Chạy script kiểm tra tổng thể**

Chạy: `python check_final.py` và `python check_style.py`
Expected: PASS thành công 100%.

- [ ] **Step 3: Commit Task 3**

```bash
git add index.html
git commit -m "chore: bump cache-buster version for CSS and JS in index.html"
```
