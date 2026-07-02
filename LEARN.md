# 📘 BÀI HỌC KINH NGHIỆM PHÁT TRIỂN (LEARN)
*Dự án: Bốc Khối Lượng Pro (du-toan)*

Tài liệu này lưu trữ các bài học xương máu trong quá trình phát triển dự án nhằm đảm bảo các AI agent tiếp theo không lặp lại các sai lầm cũ.

---

## 1. Đồng bộ ký tự Unicode & HTML Entities (Nút di chuyển)
* **Vấn đề đã gặp**: Các nút di chuyển hàng trong bảng BOQ (`moveBoqRow`) sử dụng ký tự unicode trực tiếp `↑` và `↓`. Điều này khiến một số hệ điều hành (như Windows PowerShell) hoặc trình soạn thảo dịch sai thành khoảng trắng hoặc ký tự lỗi, gây mất hiển thị nút bấm.
* **Bài học**:
  - Đối với tất cả ký tự đặc biệt hiển thị trên UI HTML (đặc biệt là các icon/mũi tên), **bắt buộc** sử dụng thực thể HTML (HTML Entities).
  - Sử dụng `&#8593;` cho `↑` (mũi tên lên) và `&#8595;` cho `↓` (mũi tên xuống).

---

## 2. Tránh lỗi mã hóa UTF-8 tiếng Việt khi ghi/sửa file (Crucial)
* **Vấn đề đã gặp**: File `app.js` chứa nhiều chuỗi tiếng Việt có dấu (như `HẠNG MỤC`, `SỐ LƯỢNG`, `ĐƠN GIÁ`). Khi dùng công cụ thay thế file trực tiếp (`replace_file_content` hoặc `multi_replace_file_content`), API AI đôi khi phân tích sai ký tự hoặc dòng cuối (LF vs CRLF) dẫn tới lỗi `proto: field contains invalid UTF-8` hoặc `target content not found`.
* **Bài học**:
  - Nếu cần thay thế các khối văn bản lớn hoặc chứa tiếng Việt có dấu, hãy **viết và chạy một script Python tự động** để đọc/ghi file bằng mã hóa `utf-8`.
  - Luôn chuẩn hóa định dạng dòng (`\r\n` vs `\n`) trước khi thực hiện so khớp và thay thế.

---

## 3. Khai báo trùng lặp hàm (Duplicate Declarations)
* **Vấn đề đã gặp**: Hàm `openAddItemDialog`, `saveAddItem`, và `closeAddItem` từng bị định nghĩa 2 lần ở các dòng khác nhau. JavaScript tự động ghi đè định nghĩa cuối cùng lên định nghĩa đầu tiên, dẫn đến việc ứng dụng chạy logic cũ (Legacy modal) thay vì logic mới (Inline Row Editing), gây lỗi thêm hạng mục.
* **Bài học**:
  - Không khai báo hàm trùng tên trong cùng một tệp hoặc cùng phạm vi (global scope).
  - Trước khi viết hàm mới, cần tìm kiếm (`Ctrl+F` hoặc `Select-String`) để kiểm tra xem hàm đó đã tồn tại chưa.

---

## 4. Đồng bộ cấu trúc Chi Phí Khác (OC_TEMPLATE)
* **Vấn đề đã gặp**: Cấu hình `autoQty` của hạng mục `scaffold` (giàn giáo) bị khai báo không đồng nhất giữa các chỗ trong file (lúc `true`, lúc `false`). Điều này dẫn đến tính toán sai lệch giữa màn hình nhập liệu và file Excel xuất ra.
* **Bài học**:
  - Khi cập nhật cấu trúc hoặc thuộc tính của một đối tượng mẫu (như `OC_TEMPLATE`), phải thực hiện rà soát tất cả các khai báo tương tự trên toàn bộ file để đảm bảo tính đồng bộ hoàn toàn.

---

## 5. Xuất Excel Khổ Giấy A4 Ngang (Landscape Layout)
* **Vấn đề đã gặp**: Khi người dùng yêu cầu nội dung file Excel phải luôn nằm trong khổ giấy A4 ngang để in ấn, độ rộng cột của các sheet chi tiết phòng (`wsDetail['!cols']`) ban đầu lên tới 167 ký tự, dẫn đến bị tràn trang khi in.
* **Bài học**:
  - Để vừa vặn hoàn hảo trong khổ giấy A4 ngang của Excel (khoảng 134-148 ký tự rộng tối đa):
    - Đặt cấu hình `ws['!pageSetup']` với `fitToWidth: 1`, `fitToHeight: 0` và `orientation: 'landscape'`.
    - Giới hạn tổng độ rộng các cột (`wch`) của sheet chi tiết khoảng **134 ký tự**.
    - Sử dụng cấu hình cột đã tối ưu:
      ```javascript
      wsDetail['!cols'] = [
        { wch: 5  },  // STT
        { wch: 36 },  // HẠNG MỤC
        { wch: 9  },  // DÀI (mm)
        { wch: 9  },  // RỘNG (mm)
        { wch: 9  },  // CAO (mm)
        { wch: 6  },  // Đ. VỊ
        { wch: 10 },  // SỐ LƯỢNG
        { wch: 12 },  // ĐƠN GIÁ
        { wch: 14 },  // THÀNH TIỀN
        { wch: 24 },  // ĐỊNH MỨC HAO HỤT
      ];
      ```

---

## 6. Lỗi Thư Viện Xuất Excel (xlsx-style vs xlsx-js-style)
* **Vấn đề đã gặp**: Thư viện `xlsx-style@0.8.13` tải qua CDN chứa một lỗi nghiêm trọng trong cơ chế viết file (`XLSX.write`). Khi ứng dụng cố gắng xuất Excel kèm theo style (như viền kẻ cell, font chữ), thư viện bị lỗi `TypeError: Cannot read property 'biff' of undefined` (do biến `copt` không được định nghĩa), khiến nút "Xuất Excel" hoàn toàn không hoạt động.
* **Bài học**:
  - **Không sử dụng** thư viện đã ngưng bảo trì `xlsx-style`.
  - **Thay thế hoàn toàn bằng `xlsx-js-style`** (URL CDN: `https://cdn.jsdelivr.net/npm/xlsx-js-style@1.2.0/dist/xlsx.bundle.js`). Đây là thư viện fork hiện đại, sửa hoàn toàn các lỗi runtime của `xlsx-style` cũ nhưng giữ nguyên 100% các hàm và cấu trúc cấu hình style/borders.

---

## 7. Kiểm tra lại danh sách bug cũ — Tất cả đã được sửa (2026-06-21)

Sau khi kiểm tra toàn bộ codebase thực tế, các bug được ghi trong TODO list cũ **đều đã được sửa** hoặc **không tồn tại**:

| Bug | Trạng thái | Ghi chú |
|-----|-----------|---------|
| `openAddItemDialog` khai báo 2 lần | ✅ Đã sửa | Chỉ còn 1 khai báo duy nhất, gọi `startInsertRow`/`startEditRow` |
| Nút ↑↓ hiện "U"/"D" | ✅ Đã sửa | Tất cả dùng `&#8593;`/`&#8595;` đúng chuẩn |
| `scaffold` autoQty không nhất quán | ✅ Không có lỗi | Tất cả 6 chỗ đều `autoQty: true` nhất quán |
| VAT Rate chưa có UI | ✅ Đã có UI | Input `id="proj-vat-rate"` trong modal dự án, min=0 max=30 step=0.5 |

**Bài học**: Trước khi sửa bất kỳ bug nào từ danh sách cũ, hãy **kiểm tra thực tế code** trước bằng Python script. Danh sách TODO có thể đã lỗi thời sau nhiều lần cập nhật.

---

## 8. OC_TEMPLATE khai báo nhiều lần — Không phải lỗi

* **Phát hiện**: `OC_TEMPLATE` được khai báo `const` tới 5 lần trong `app.js`.
* **Lý do không phải lỗi**: Mỗi khai báo nằm trong **scope function riêng** (`renderBOQ`, `updateOtherCost`, `exportExcel`...) — không phải global scope. JavaScript `const` trong function scope không xung đột nhau.
* **Bài học**: Khai báo `const` trùng tên **chỉ lỗi** khi cùng scope. Khác function/block = hoàn toàn độc lập.

---

## 9. Số La Mã tự động cho các mục lớn trong BOQ

* **Tính năng thêm**: Mỗi phòng có counter `subRomIdx` bắt đầu từ 1, tự tăng theo thứ tự xuất hiện:
  - `I.` → Tên phòng (từ `romanNums[idx]` của vòng lặp phòng)
  - `II.` → Custom sub-header IN HOA (tùy người dùng tạo)
  - `III.` → `⚡ THIẾT BỊ ĐIỆN` (elecHeader)
  - `IV.` → `📝 CHI TIẾT TỪ GHI CHÚ` (noteHeader)
  - `V.` → `💰 CHI PHÍ KHÁC — PHÒNG ...` (OC header)
* **Lưu ý kỹ thuật**: Dùng `subRomIdx++` (post-increment) để lấy giá trị hiện tại rồi mới tăng. Mảng `romanNums[]` đã được khai báo sẵn trong global scope.

---

## 10. Lỗi CHI PHÍ KHÁC hiện 2 lần khi lọc theo phòng

* **Vấn đề**: Khi filter theo phòng cụ thể, UI hiện cả `boq-room-oc-hdr` (CHI PHÍ KHÁC của phòng) lẫn `boq-other-header` (CHI PHÍ KHÁC cấp dự án).
* **Nguyên nhân**: Trong `filterBOQByRoom`, vòng lặp `forEach(row)` kiểm tra `!kr → return` sớm trước khi check class `boq-other-header`. Các row `boq-other-header` không có `data-kr` nên bị bỏ qua (không bị ẩn).
* **Fix**: Thêm check `boq-other-header/item` TRƯỚC khi check `!kr`:
  ```javascript
  if (row.classList.contains('boq-other-header') || row.classList.contains('boq-other-item')) {
    row.style.display = 'none'; // Luôn ẩn khi xem từng phòng
    return;
  }
  if (!kr) return;
  ```
* **Bài học**: Khi filter row theo `data-kr`, luôn xử lý các "special rows" không có `data-kr` trước, tránh bị bỏ qua bởi early return.


---

## BÀI HỌC: Modal Footer Bug (2026-06-21)

### Vấn đề
Nút "Hủy" / "Thêm Phòng" của modal-room bị hiển thị RA NGOÀI modal-card, sang phải màn hình.

### Root cause
1. Script `move_footer.py` đã lấy footer_block bằng `c.find('</div>', footer_start) + 6` — chỉ tìm closing tag ĐẦU TIÊN.
2. Nhưng `</div>` đầu tiên sau `<div class="modal-footer">` KHÔNG phải là close của footer mà là close của modal-card (do file có nhiều `

` xen kẽ làm lệch parse).
3. Kết quả: đã move footer + modal-card closing tag ra khỏi vị trí gốc → HTML mất cân bằng.
4. Browser auto-corrected → đưa `modal-footer` thành SIBLING của `modal-card` trong flex overlay → hiển thị sang phải.

### Tại sao Python count 89/89 vẫn không fix được
- Python count `'<div'` và `'</div>'` trong chuỗi raw — không bị ảnh hưởng bởi browser parsing rules.
- Tuy nhiên browser có thể parse HTML KHÁC với Python count (do element nesting rules, auto-close behaviors, v.v.).
- File có `

` sau mỗi ký tự (encoding corruption) khiến browser dễ parse sai hơn.

### Fix cuối cùng hoạt động
**JavaScript runtime DOM fix** — chạy ngay khi script load:
```javascript
(function fixModalLayout() {
  var overlay = document.getElementById('modal-room');
  var card = overlay.querySelector('.modal-room-card');
  var footer = overlay.querySelector('.modal-footer');
  if (card && footer && footer.parentElement !== card) {
    card.appendChild(footer);  // kéo về đúng chỗ
  }
  // Dọn bất kỳ thứ gì bị parse ra ngoài card
  Array.from(overlay.children).forEach(function(child) {
    if (child !== card) card.appendChild(child);
  });
})();
```

### Mobile top-buttons
Thêm `<div class="modal-footer-mobile-top">` TRONG modal-body (ngay đầu form):
- Desktop: ẩn bằng CSS `display: none`
- Mobile (≤768px): hiện bằng CSS `display: flex`
→ User luôn thấy nút ngay khi mở modal, không cần scroll xuống cuối.

### Bài học rút ra
1. **Không dùng position hardcode** khi đã modify file nhiều lần — vị trí thay đổi sau mỗi lần save.
2. **File có encoding corruption** (`

` xen kẽ ký tự): luôn dùng Python utf-8 để đọc/ghi, nhưng kết quả count DIV có thể khác với browser parsing.
3. **JS DOM fix > HTML manipulation** khi HTML phức tạp và bị corrupt — JavaScript chạy SAU khi browser đã parse, nên nó luôn thắng.
4. **Luôn deploy bằng zip mới** trước khi test trên mobile — mobile dùng Netlify URL, không phải file local.


---

## BÀI HỌC: Đồng bộ 4 output (2026-06-21)

### Tổng quan
App có 4 output cần đồng bộ nội dung:
1. **Web preview** (renderBOQ → HTML dark theme)
2. **PDF app** (ep- print view → window.print())
3. **Excel CHI TIẾT sheet** (per-room, 10 cột)
4. **Excel VẬT TƯ sheet** (consolidated material list)

### Nguyên tắc đồng bộ đã xác lập

#### Cấu trúc BOQ (áp dụng cho cả 4 output):
```
I.  TÊN PHÒNG               ← Roman numeral = vị trí phòng trong dự án
    1. Item (có STT)
    2. Item (có STT)
       Sub-item (không STT)  ← surface: 'perimeter','window','ceilPerim'
    3. ...
II. THIẾT BỊ ĐIỆN           ← subRomIdx = 1 → romanNums[1] = 'II'
    Item (không STT)
III. CHI TIẾT TỪ GHI CHÚ   ← noteHeader
    Item (không STT)
```

#### Items KHÔNG có STT:
`['perimeter','window','ceilPerim','elec','elecManual','noteItem']`

#### subRomIdx = 1 (KHÔNG phải 0):
- I = ẩn (implied cho phần construction items)
- II = THIẾT BỊ ĐIỆN (elecHeader)
- III = CHI TIẾT TỪ GHI CHÚ (noteHeader)
- Tiếp theo = custom ALL CAPS sub-headers

### Các symbol/emoji ĐÃ XÓA khỏi tất cả output:
| Cũ | Mới |
|----|-----|
| ⚡ THIẾT BỊ ĐIỆN | THIẾT BỊ ĐIỆN |
| 📝 CHI TIẾT TỪ GHI CHÚ | CHI TIẾT TỪ GHI CHÚ |
| 🟫 SÀN | SÀN |
| 🟦 TƯỜNG SƠN NƯỚC | TƯỜNG SƠN NƯỚC |
| 🪟 CỬA | CỬA |
| 📋 KHÁC | KHÁC |
| 🛋️ THIẾT BỊ NỘI THẤT | THIẾT BỊ NỘI THẤT |
| 🚿 PHẦN NƯỚC | PHẦN NƯỚC |
| 🛡️ CHỐNG THẤM | CHỐNG THẤM |

### Ghi chú Mộc/Nước/Chống thấm trong Excel → từng dòng:
```javascript
// ĐÚNG: mỗi dòng textarea = 1 row riêng
[{text: room.noteWoodwork, label: 'THIẾT BỊ NỘI THẤT'}, ...].forEach(...)
text.split('\n').forEach(line => { lr[0] = li+1; lr[1] = line; })

// SAI (cũ): ghép tất cả thành 1 dòng duy nhất
wr[1] = `🛋️ THIẾT BỊ NỘI THẤT: ${room.noteWoodwork}`;
```

### BÀI HỌC QUAN TRỌNG: Không thêm sub-section headers không cần thiết
- User hỏi "thêm số La Mã cho các mục lớn" → CHỈ có nghĩa là:
  - Phòng: I, II, III (theo room index)
  - ĐIỆN: II, NỘI THẤT: III... (theo subRomIdx)
- KHÔNG có nghĩa là thêm I.SÀN, II.TƯỜNG, III.TRẦN... sub-headers
- Khi uncertain → hỏi lại hoặc deploy và chờ user confirm

### Cách đặt file để dễ patch bằng Python:
- Dùng anchor text (comment duy nhất) thay vì position
- VD: `// ── Ghi chú Mộc / Nước / Chống thấm` làm anchor
- Tránh hardcode byte offset vì thay đổi sau mỗi lần edit

---

## BÀI HỌC: Roman numeral implementation (2026-06-21)

### Nguyên nhân bug ban đầu (chưa fix được)
- `subRomIdx = 1` + `romanNums[subRomIdx++]` → elecHeader hiện 'II' (ĐÚNG)
- User báo bug → tôi nghĩ subRomIdx=1 là bug → sửa thành 0 → SAI
- Thực ra 'II' là ĐÚNG vì 'I' ngầm định cho phần construction

### Giải thích đúng:
```
subRomIdx = 1  →  elecHeader: romanNums[1] = 'II'  ✓
subRomIdx = 0  →  elecHeader: romanNums[0] = 'I'   ✗ (sai với UI mong đợi)
```

### Vị trí code cần sync khi thay đổi structure:
1. `renderBOQ` (web preview + print PDF) - app.js ~179399
2. Excel CHI TIẾT `calc.items.forEach` - app.js ~574000
3. `ep-elec-hdr` render (another view) - app.js ~441804
4. `CALC.room` item labels - app.js ~134000

---

## BÀI HỌC: Excel export architecture (2026-06-21)

### 3 sheets trong Excel export:
| Sheet | Tên | Nội dung |
|-------|-----|---------|
| 1 | "Tổng hợp" | Summary theo phòng, có cột từng phòng |
| 2 | "Vật Tư Cần Mua" | Consolidated material list (by type) |
| 3+ | "Tên Phòng" (×N) | CHI TIẾT từng phòng (như web BOQ) |

### GROUP_LABEL trong VẬT TƯ sheet:
```javascript
// Phải bỏ emoji để in đẹp
const GROUP_LABEL = {
  floor: 'SÀN',           // (không phải '🟫 SÀN')
  wall:  'TƯỜNG SƠN NƯỚC',
  // ...
};
```

### Note textareas → fields trong room object:
```javascript
room.noteWoodwork   // THIẾT BỊ NỘI THẤT
room.notePlumbing   // PHẦN NƯỚC  
room.noteWaterproof // CHỐNG THẤM
```
Cả 3 trường này phải được handle riêng trong Excel (không chỉ dùng `parseNoteItems(room)`)

---

## 11. BÀI HỌC: Cột đệm trống A (Spacer Column) và Dịch chuyển cột (2026-06-23)

### Vấn đề đã gặp
Khách hàng yêu cầu thay đổi cách trình bày các sheet chi tiết phòng (như sheet `Khám tư vấn`) theo thiết kế của **Hình 2**:
- Tạo một cột A trống, rất hẹp, hoàn toàn không có đường viền (borderless) làm khoảng đệm lề trái.
- Dịch chuyển bảng biểu thực tế bắt đầu từ Cột B (STT) sang Cột K (Ghi chú).

### Giải pháp kỹ thuật đã áp dụng
1. **Dịch chuyển chỉ số cột**:
   - Tăng toàn bộ chỉ số cột trong sheet phòng chi tiết lên `colOffset = 1`.
   - Cột A có độ rộng `wch: 3` và được loại bỏ border bằng cấu hình `style: 'none'` cho tất cả các ô trong `applySheetStyles` khi `sheetType === 'detail' && C === 0`.
2. **Cập nhật công thức**:
   - Dịch chuyển các chữ cái cột tham chiếu trong công thức tính số lượng từ `C` và `D` cũ sang `D` và `E` mới (vd: `D{row}*E{row}*hao_hut`) để tham chiếu chính xác các cột Dài và Rộng đã dịch chuyển.
3. **Cập nhật gộp ô (`merges`)**:
   - Các tiêu đề lớn, thông tin liên hệ và các dòng tổng tiền/chữ ký cuối trang được cập nhật lại toạ độ gộp ô theo 11 cột mới (bao gồm cột đệm).
4. **Đồng bộ Web Preview & PDF Print**:
   - Hàm `renderWorksheetToHtml` và xem trước cục bộ (`_renderPreviewDetail`) được bổ sung cột `<td>` trống, không viền ở đầu mỗi hàng của các sheet chi tiết.
   - Logo Blue Decor dịch chuyển từ cột A sang cột B để căn chỉnh thẳng hàng với bảng biểu đã dịch.

### Bài học kinh nghiệm
- **Đồng bộ hóa tuyệt đối**: Khi dịch chuyển bất kỳ cột nào trong cấu trúc bảng, phải dịch chuyển đồng thời ở 3 nơi: Logic sinh file Excel, Giao diện xem trước trên Web và Định dạng trang in PDF.
- **Xóa viền triệt để**: Cột đệm lề chỉ đẹp tự nhiên khi không chứa bất kỳ đường viền lưới hay viền nét liền/nét đứt nào. Thiết lập `{ style: 'none' }` cho cả 4 phía của ô là lựa chọn bắt buộc.
- **Nhận diện loại sheet**: Chỉ áp dụng cột đệm A cho sheet phòng chi tiết (`sheetType === 'detail'`), các sheet còn lại như `Tổng hợp` và `Vật Tư Cần Mua` cần giữ nguyên xuất phát từ cột A để tránh lãng phí diện tích hiển thị.


---

## 12. Quy tắc phát triển và tương tác với khách hàng (2026-06-23)
* **Quy tắc 1 (Không tự ý thay đổi code hoàn tất)**: Tuyệt đối không tự ý chỉnh sửa hay thay đổi các tính năng, logic hoặc giao diện đã được code xong và hoạt động ổn định khi chưa có sự xác nhận chính thức từ khách hàng.
* **Quy tắc 2 (Hỏi lại khi chưa rõ)**: Trong quá trình nhận công việc từ khách hàng, nếu gặp bất kỳ yêu cầu nào chưa rõ ràng, còn mơ hồ hoặc thiếu thông tin, bắt buộc phải đặt câu hỏi làm rõ với khách hàng trước khi bắt tay vào triển khai thực tế, tránh việc tự ý phán đoán hoặc giả định.


---

## 13. Sửa công thức Số lượng và Đồng bộ tất cả các sheet (2026-06-24)

### Vấn đề đã gặp
- Cột Số Lượng cho Tường Vùng 1 (`wallZ1`) và Tường Vùng 2 (`wallZ2`) chưa có công thức động trong các sheet chi tiết phòng khi xuất Excel.
- Các sheet "Tổng hợp" (wsSum) và "Vật Tư Cần Mua" (wsVT) chứa các giá trị tĩnh cho phần số lượng/khối lượng thay vì công thức liên kết động với các sheet phòng chi tiết.
- Số lượng hiển thị có quá nhiều số thập phân lẻ, không đồng bộ định dạng chuyên nghiệp.

### Giải pháp kỹ thuật đã áp dụng
1. **Thêm công thức Tường Vùng 1/2**:
   - Cập nhật điều kiện lọc trong `generateWorkbook` để áp dụng công thức cho cả `wallZ1` và `wallZ2`:
     `qtyFormula = C{exR}/1000*E{exR}/1000*waste`
2. **Đồng bộ hóa thứ tự tạo Sheet**:
   - Thay đổi trình tự kết xuất: các sheet chi tiết phòng được dựng trước để ghi nhận chính xác toạ độ dòng của từng hạng mục vào một bản đồ dòng (`rowMap`).
   - Dựng sheet **Tổng hợp** sau để viết công thức động liên kết sang các sheet chi tiết phòng (ví dụ: `='Khám tư vấn'!G12`).
   - Dựng sheet **Vật Tư Cần Mua** sau cùng, sử dụng công thức cộng dồn của hạng mục đó ở các phòng (ví dụ: `='Khám tư vấn'!G12+'Phòng khám'!G15`).
3. **Sử dụng công thức Excel cho Tổng cộng và Thành tiền**:
   - Sử dụng `=SUM(...)` cho các dòng cộng và tổng số lượng.
   - Sử dụng phép nhân `=[Số lượng]*[Đơn giá]` cho cột Thành tiền.
4. **Định dạng hiển thị 2 chữ số thập phân (`#,##0.00`)**:
   - Sử dụng thuộc tính `.z` của thư viện `xlsx-js-style` để áp dụng định dạng hiển thị `ws[ref].z = '#,##0.00'` cho toàn bộ các ô dữ liệu của cột Số lượng trong cả 3 loại sheet (sum, detail, vt).

### Bài học kinh nghiệm
- **Toạ độ dòng động**: Các dòng chi tiết trong Excel có thể thay đổi tùy theo dữ liệu thực tế. Do đó, việc lưu trữ toạ độ dòng (`rowMap`) trong pass 1 là điều kiện tiên quyết để tạo các liên kết công thức liên trang chính xác trong pass 2.
- **Visual formatting vs Data rounding**: Thay vì làm tròn cứng giá trị số bằng JS (làm mất độ chính xác của các phép tính liên hoàn phía sau), hãy thiết lập định dạng hiển thị `.z = '#,##0.00'` trong Excel. Excel sẽ tự động làm tròn hiển thị ra màn hình nhưng vẫn giữ nguyên giá trị số chính xác bên trong cho các công thức tính tổng.
- **Bảo toàn cấu trúc Header**: Khi tái cơ cấu hàm xuất Excel, luôn đảm bảo giữ nguyên vẹn toạ độ gộp ô (merges) và nội dung của hàng 1 đến 7 của header thông tin dự án để tránh visual regression.


---

## 14. Đánh số trang và cấu hình Footer file Excel bằng JSZip post-processing (2026-06-24)

### Vấn đề đã gặp
- Thư viện `xlsx-js-style` (dựa trên phiên bản cộng đồng của SheetJS) không hỗ trợ ghi các thuộc tính trang in như `!pageSetup` (khổ giấy, hướng trang) và `!headerFooter` (đánh số trang, chữ ký footer) vào file Excel xuất ra.
- Thiết lập trực tiếp `ws['!pageSetup']` hay `ws['!headerFooter']` trong mã JS sẽ bị thư viện bỏ qua khi chuyển đổi và ghi file nhị phân.

### Giải pháp kỹ thuật đã áp dụng
1. **Sử dụng JSZip làm thư viện post-processing**:
   - Thêm thư viện `JSZip` vào file giao diện HTML `du-toan/index.html`.
   - Trong hàm `xlsxWrite`, khi có sẵn `JSZip`, thực hiện tải mảng byte nhị phân của workbook được sinh ra bởi `XLSX.write`.
   - Tìm kiếm tất cả các file XML mô tả sheet (`xl/worksheets/sheet*.xml`) trong tệp lưu trữ ZIP.
   - Phân tích chuỗi XML, tìm thẻ `<pageMargins .../>` và tiêm thêm các thẻ XML cấu hình trang in đúng thứ tự OpenXML quy định:
     - Thêm `<pageSetup paperSize="9" orientation="landscape" fitToWidth="1" fitToHeight="0" fitToPage="1"/>`
     - Thêm `<headerFooter oddFooter="&amp;L&amp;&quot;Arial,Italic&quot;Du-Toan-BlueAI Lab&amp;R&amp;&quot;Arial,Bold&quot;Trang &amp;P/&amp;N" evenFooter="&amp;L&amp;&quot;Arial,Italic&quot;Du-Toan-BlueAI Lab&amp;R&amp;&quot;Arial,Bold&quot;Trang &amp;P/&amp;N"/>`
   - Nén lại workbook đã chỉnh sửa và tiến hành tải xuống qua `FileSaver.js`.
2. **Đồng bộ hóa bản xem trước HTML**:
   - Cập nhật footer của các trang xem trước in ấn HTML từ `"Du-Toan- BlueAI Lab"` sang `"Du-Toan-BlueAI Lab"` cho đồng nhất tuyệt đối.

### Bài học kinh nghiệm
- **Giới hạn thư viện Open-source**: Khi các thư viện Excel JS gọn nhẹ (như SheetJS CE) bị giới hạn tính năng nâng cao, phương pháp giải nén và chỉnh sửa XML trực tiếp (Zip post-processing) là giải pháp mạnh mẽ và tối ưu nhất để bổ sung tính năng mà không cần chuyển đổi toàn bộ kiến trúc sang một thư viện nặng nề khác (như ExcelJS).
- **Thứ tự thẻ OpenXML nghiêm ngặt**: Cấu trúc XML của Excel (.xlsx) đòi hỏi vị trí của các thẻ con trong `<worksheet>` phải tuân thủ thứ tự chuẩn xác. Thẻ `<pageSetup>` và `<headerFooter>` phải nằm ngay dưới `<pageMargins .../>`. Tiêm sai vị trí sẽ dẫn đến lỗi Excel báo file bị hỏng ("corrupted file") khi mở.



---

## 15. Đơn giản hóa cột Ghi chú và Chèn Logo Blue Deco vào Excel (2026-06-25)

### Vấn đề đã gặp
- Cột **Ghi chú (Note)** trong các sheet chi tiết phòng trước đây hiển thị cả phần trăm hao hụt và khối lượng đã tính toán (ví dụ: `+5% hao hụt → 23,20 m²`), gây lặp thông tin không cần thiết với cột Số lượng và làm bảng tính trông chật chội.
- Người dùng mong muốn chèn logo **Blue Deco** (`logo-bluedecor.png`) vào các ô `A1:B3` trên tất cả các sheet Excel xuất ra để tăng tính nhận diện thương hiệu. Tuy nhiên, thư viện `xlsx-js-style` không hỗ trợ chèn hình ảnh (cell drawings) vào trang tính.
- Đánh số trang và footer ở Excel cần hiển thị dạng số trang (`Trang &P/&N`) ở lề phải và `"Du-Toan-BlueAI Lab"` ở lề trái cho đồng bộ với file xuất PDF.

### Giải pháp kỹ thuật đã áp dụng
1. **Rút gọn cột Ghi chú**:
   - Thay đổi logic định dạng chuỗi ghi chú của hạng mục sàn, tường, trần trong `du-toan/app.js` (tại các dòng tương ứng của `floor`, `wall`, `ceiling`).
   - Loại bỏ hoàn toàn ký tự mũi tên `→` và phần số lượng m² tính toán, chỉ giữ lại chuỗi tỉ lệ phần trăm hao hụt (ví dụ: `+5% hao hụt` hoặc rỗng).
2. **Chèn Logo bằng JSZip Post-processing nâng cao**:
   - Nạp trước tệp tin `logo-bluedecor.png` trên client-side lưu vào biến `logoArrayBuffer` khi tải trang.
   - Khi người dùng xuất Excel, giải nén dữ liệu nhị phân Excel thô thông qua `JSZip`.
   - Lưu trữ byte ảnh logo vào đường dẫn zip `xl/media/image1.png`.
   - Tạo file drawing XML xác định toạ độ neo hình ảnh ở vùng `A1:B3` tại `xl/drawings/drawing1.xml`.
   - Định nghĩa liên kết vẽ tại `xl/drawings/_rels/drawing1.xml.rels` trỏ tới file media của logo.
   - Với mỗi file sheet XML (`xl/worksheets/sheet*.xml`), tiêm thẻ `<drawing r:id="rId2"/>` ngay trước `</worksheet>` và tạo file liên kết quan hệ tương ứng `xl/worksheets/_rels/sheet*.xml.rels` liên kết `rId2` với `../drawings/drawing1.xml`.
   - Bổ sung định nghĩa Override cho file drawing trong tệp tin cấu trúc `[Content_Types].xml`.
3. **Đồng bộ hóa footer và đánh số trang**:
   - Tiêm thiết lập thẻ `<headerFooter>` trong tệp tin XML của mỗi sheet đặt nội dung `&L&"Arial,Italic"Du-Toan-BlueAI Lab&R&"Arial,Bold"Trang &P/&N` để tự động tính toán số trang thực tế khi in ấn Excel.

### Bài học kinh nghiệm
- **Tinh giản thông tin giao diện**: Chỉ hiển thị những thông tin thực sự có ích trong cột Ghi chú (tỉ lệ hao hụt dự phòng) và để các cột Số lượng tự làm nhiệm vụ hiển thị con số cụ thể, giúp bảng tính thoáng đãng và dễ đọc hơn.
- **Can thiệp OpenXML drawing**: Excel yêu cầu các thẻ và tệp tin quan hệ vẽ (`drawing`) phải được ánh xạ đúng ID quan hệ (`rId`) và đăng ký kiểu nội dung (Content Types) chuẩn xác. Bất kỳ sự thiếu sót nào trong việc đăng ký drawing trong `[Content_Types].xml` hay thẻ `<drawing>` đặt sai thứ tự XML trong worksheet đều khiến Excel từ chối mở file.
- **Tiền tải tài nguyên hình ảnh**: Việc tải trước hình ảnh logo (fetch logo) lưu vào bộ đệm `ArrayBuffer` giúp thao tác xuất Excel diễn ra tức thì, không bị trễ hoặc lỗi bất đồng bộ khi nén zip.


---

## 16. Phục hồi Chi phí khác cho tất cả các sheet Excel (2026-06-25)

### Vấn đề đã gặp
- Ở phiên bản trước, hạng mục **Chi phí khác (Other Costs)** (như phí vận chuyển, tháo dỡ trần, giàn giáo, thiết kế, giám sát) bị ẩn hoàn toàn hoặc biến mất trên các sheet chi tiết phòng của file Excel xuất ra.
- Nguyên nhân là do trong logic sinh workbook của `du-toan/app.js` đã áp dụng điều kiện kiểm tra thuộc tính phòng cụ thể `saved.roomActive?.[room.id]` và `saved.roomQty?.[room.id]`. Tuy nhiên, cơ sở dữ liệu và giao diện UI hiện tại quản lý Chi phí khác ở mức độ toàn dự án (global) chứ không hỗ trợ cấu hình kích hoạt hay nhập số lượng riêng cho từng phòng. Điều này dẫn đến thuộc tính `roomActive` luôn mang giá trị `false` và phần chi phí khác bị lược bỏ khỏi các sheet chi tiết.

### Giải pháp kỹ thuật đã áp dụng
1. **Phục hồi logic kiểm tra Chi phí khác**:
   - Thay thế việc kiểm tra `saved.roomActive?.[room.id]` bằng việc kiểm tra sự tồn tại của đơn giá hoặc số lượng toàn cục: `if (price > 0 || qty > 0)`.
   - Sử dụng lại số lượng toàn cục `saved.qty` thay cho `saved.roomQty?.[room.id]`.
   - Sử dụng lại ghi chú toàn cục `saved.note` thay cho `saved.roomNote?.[room.id]`.
2. **Kiểm thử và xác thực**:
   - Sử dụng mock project có dữ liệu chi phí khác có đơn giá để chạy kiểm thử xuất Excel qua `node test_excel_gen.js`.
   - Xác thực bằng openpyxl (`verify_other_costs_values.py`) và xác nhận rằng phần "CHI PHÍ KHÁC" đã xuất hiện tại dòng 31 của sheet phòng chi tiết ('Khám tư vấn') với đúng đơn giá, số lượng, thành tiền và ghi chú đã nhập.

### Bài học kinh nghiệm
- **Nhất quán giữa DB, UI và Logic Excel**: Khi thay đổi logic xuất file Excel (như thêm kiểm tra thuộc tính cấp phòng), phải đảm bảo cấu trúc dữ liệu tương ứng đã được hỗ trợ trong DB và có giao diện nhập liệu tương ứng trên UI. Nếu không, logic xuất Excel sẽ bị đứt gãy và dữ liệu sẽ bị mất khi xuất file.
- **Tính toán diện tích tự động**: Đối với các chi phí tự động tính theo diện tích sàn (như phí thiết kế, tháo dỡ trần, giàn giáo), logic sinh file Excel sử dụng tổng diện tích của phòng đó (`tf = D/1000 * R/1000`) làm khối lượng mặc định, đảm bảo tính toán cục bộ chính xác cho từng phòng.

---

## 17. Căn lề giữa nhãn tổng kết, In đậm dòng Bằng chữ & Nhúng Logo dạng Base64 (2026-06-25)

### Vấn đề đã gặp
- Dòng chữ đọc số tiền `"Bằng chữ: ..."` hiển thị ở dạng thường, không được in đậm.
- Các nhãn tổng cộng `"Cộng trước VAT"`, `"Thuế VAT"`, `"TỔNG CỘNG"` hiển thị lệch vị trí. Yêu cầu thiết kế muốn **căn lề giữa** (`align=center`) cho các nhãn này.
- Tự động bôi đậm hàng tiêu đề phần (Section header) nhận diện sai `"TỔNG CỘNG"` là tiêu đề phần và ghi đè kiểu dáng căn lề trái lên nó.
- Tải tệp logo `logo-bluedecor.png` qua mạng (`fetch`) bị lỗi CORS khi người dùng mở tệp HTML cục bộ trực tiếp qua giao thức `file://` (offline), dẫn đến không thể chèn logo vào tệp Excel được tạo ra.

### Giải pháp kỹ thuật đã áp dụng
1. **In đậm Bằng chữ và Tổng cộng**:
   - Trong hàm `applySheetStyles`, bổ sung điều kiện nhận diện chuỗi bắt đầu bằng `"Bằng chữ:"`, chuỗi bằng `"TỔNG CỘNG"`, và chuỗi bắt đầu bằng `"TỔNG CỘNG VẬT TƯ"` để thiết lập thuộc tính font chữ in đậm (`bold: true`).
2. **Căn lề giữa nhãn tổng kết**:
   - Thiết lập thuộc tính alignment `horizontal: 'center'` cho các cột nhãn nằm trước cột số tiền (tức cột `< 8` cho detail sheet, và `< 6` cho sum/vt sheet) khi dòng đó là dòng tổng kết (`totalRows.has(R)`). Điều này giúp nhãn văn bản hiển thị căn giữa trong vùng ô gộp (merge).
3. **Loại trừ TỔNG CỘNG khỏi Section Rows**:
   - Cập nhật logic trong `applyBoldSectionRows` để loại trừ các hàng có chứa từ khóa `"TỔNG CỘNG"` (bằng cách kiểm tra `!valB.toLowerCase().includes('tổng cộng')`). Điều này ngăn không cho hàm ghi đè định dạng căn lề trái lên dòng `"TỔNG CỘNG"`.
4. **Mã hóa Logo sang Base64**:
   - Chuyển đổi và nhúng tĩnh chuỗi base64 của ảnh `logo-bluedecor.png` trực tiếp vào biến `LOGO_BASE64` và chuyển đổi sang `logoArrayBuffer` một cách đồng bộ trong `app.js`. Cách này loại bỏ hoàn toàn việc fetch qua mạng và sửa được lỗi CORS trên giao thức `file://`.

### Bài học kinh nghiệm
- **Xung đột kiểu dáng**: Khi có nhiều hàm cùng chỉnh sửa thuộc tính của ô trong Excel (như `applySheetStyles` và `applyBoldSectionRows`), hàm chạy sau sẽ ghi đè lên hàm chạy trước. Do đó, cần thiết lập các điều kiện loại trừ cụ thể (như loại trừ `"TỔNG CỘNG"` ra khỏi bộ lọc section) để đảm bảo độ chính xác của giao diện cuối cùng.
- **Sử dụng Base64 cho ứng dụng Offline/Local**: Đối với các ứng dụng web dạng đơn trang (SPA) chạy trực tiếp từ file trên đĩa cứng mà không cần server (`file://`), mọi thao tác tải tài nguyên ngoài qua `fetch` đều bị CORS chặn. Việc đóng gói tài nguyên tĩnh (như logo thương hiệu) thành các chuỗi Base64 nhúng trực tiếp là giải pháp tối ưu và an toàn nhất.

---

## 18. Đồng bộ hóa cấu trúc mục lớn I, II, III, IV và gộp Chống thấm + Nước vào Nhà Vệ Sinh (2026-06-25)

### Vấn đề đã gặp
- Cấu trúc và thứ tự các hạng mục lớn giữa trang Tổng hợp (Summary) và các sheet Chi tiết phòng (Detail sheets) không đồng bộ và không phản ánh chính xác form nhập liệu từ trên xuống dưới của ứng dụng.
- Phần nước (Thiết bị vệ sinh) và phần chống thấm bị tách rời thành 2 mục lớn riêng biệt ở các sheet phòng chi tiết (lần lượt là mục V và VI), trong khi yêu cầu thực tế muốn gộp chung thành mục **IV. NHÀ VỆ SINH: THIẾT BỊ VỆ SINH VÀ CHỐNG THẤM**.
- Trên giao diện nhập liệu (Form input), việc để 2 ô nhập liệu "Phần nước" và "Chống thấm" riêng biệt gây rườm rà và không đồng bộ với cấu trúc gộp ở báo cáo.

### Giải pháp kỹ thuật đã áp dụng
1. **Gộp ô nhập liệu trên UI (Form input)**:
   - Loại bỏ hoàn toàn ô nhập liệu `note-waterproof` (Chống Thấm) riêng biệt trong tệp [du-toan/index.html](file:///d:/Kho%20tri%20th%E1%BB%A9c/du-toan/index.html).
   - Chuyển ô nhập liệu `note-plumbing` thành ô nhập liệu duy nhất đại diện cho cả mục dưới tiêu đề **`🚾 NHÀ VỆ SINH: THIẾT BỊ VỆ SINH VÀ CHỐNG THẤM`**.
   - Cập nhật ví dụ gợi ý (placeholder) kết hợp cả phần nước và chống thấm để người dùng dễ hình dung cấu trúc nhập.
2. **Tự động chuyển đổi và di trú dữ liệu cũ**:
   - Khi tải dữ liệu phòng lên form (`openRoomModal`), tự động cộng dồn và nối chuỗi các ghi chú cũ từ hai trường: `[room?.notePlumbing, room?.noteWaterproof].filter(Boolean).join('\n')` và điền vào ô nhập liệu duy nhất.
   - Khi lưu lại phòng (`getRoomDataFromUI`), chỉ lưu vào trường `notePlumbing` và đặt trường `noteWaterproof` thành chuỗi rỗng `''`.
3. **Phân loại hạng mục chống thấm**:
   - Trong hàm `categorizeSummaryItem`, thay đổi giá trị trả về của `item.surface === 'waterproofNote'` từ `'construction'` thành `'sanitary'`. Việc này giúp gộp các ghi chú chống thấm vào chung nhóm vệ sinh trên bảng Tổng hợp.
4. **Đồng bộ hóa nhãn La Mã cố định**:
   - Cập nhật định nghĩa mảng `categoriesConfig` ở 3 nơi (`renderBOQ`, `generateWorkbook`, và `_renderPreviewSummary`) để cố định 4 mục lớn:
     - `I` -> `XÂY DỰNG CƠ BẢN`
     - `II` -> `THIẾT BỊ ĐIỆN`
     - `III` -> `THIẾT BỊ NỘI THẤT`
     - `IV` -> `NHÀ VỆ SINH: THIẾT BỊ VỆ SINH VÀ CHỐNG THẤM`
   - Dùng thuộc tính `rom` cố định (ví dụ: `catConf.rom`) thay cho biến đếm tăng dần `catRomIdx++` để đảm bảo thứ tự La Mã trên Excel và Web luôn khớp nhau tuyệt đối.
5. **Tái cấu trúc sheet Chi tiết phòng Excel và Web thành danh sách đơn**:
   - Sắp xếp thứ tự in các phần trong room detail (cả Excel và Web preview) thành 4 mục lớn tuần tự.
   - In tất cả hạng mục thuộc phần vệ sinh và chống thấm thành một danh sách duy nhất được đánh số thứ tự liên tục dưới mục `IV. NHÀ VỆ SINH: THIẾT BỊ VỆ SINH VÀ CHỐNG THẤM` (tương tự như cách hiển thị của đồ gỗ nội thất ở mục III) mà không chia nhỏ thành tiêu đề phụ.
   - Theo dõi số La Mã của mục tiếp theo (ví dụ: mục `CHI PHÍ KHÁC` ở cuối) bằng biến đếm động `nextSectionNum` được cập nhật sau khi in mỗi mục II, III, IV. Điều này đảm bảo mục `CHI PHÍ KHÁC` luôn được đánh số La Mã liên tục chính xác.
   - Bảo toàn cơ chế `rowMap` ánh xạ dòng để giữ nguyên vẹn liên kết công thức tự động giữa sheet Tổng hợp và sheet Chi tiết.

### Bài học kinh nghiệm
- **Đơn giản hóa giao diện nhập liệu (UI)**: Hạn chế chia nhỏ quá nhiều ô nhập tự do nếu các dữ liệu đó có chung bản chất tính toán hoặc được gom nhóm trong báo cáo. Việc gom thành một ô nhập chung kèm placeholder chi tiết giúp tăng trải nghiệm người dùng khảo sát.
- **Di trú dữ liệu tự động ở tầng giao diện**: Khi loại bỏ một trường trong database, có thể tận dụng cơ chế nối chuỗi khi load form để gom dữ liệu cũ của người dùng vào ô mới mà không cần chạy các câu lệnh cập nhật DB phức tạp ở backend.
- **Đồng bộ mã La Mã cố định vs Động**: Khi các sheet chi tiết và bảng tổng hợp cần có sự tương ứng 1-1 về ký hiệu mục lớn, việc dùng mã La Mã cố định (`I`, `II`, `III`, `IV`) cho các phần chính là giải pháp an toàn nhất, tránh lệch nhãn do một sheet phòng cụ thể thiếu một hạng mục.
- **Đánh số động cho phần đuôi**: Với những phần ở cuối sheet (như `CHI PHÍ KHÁC`) có số La Mã phụ thuộc vào số lượng các phần trước đó được hiển thị, việc sử dụng một biến đếm động (`nextSectionNum`) tăng dần theo các khối nội dung thực tế xuất hiện là giải pháp tối ưu để giữ thứ tự liên tục mà không làm đứt gãy cấu trúc hiển thị.


---

## 19. Nâng cấp Modal Tạo / Sửa Dự Án (Vĩ mô) và Ẩn giao diện nhập Thuế VAT (2026-06-25)

### Vấn đề đã gặp
- Cần thu thập thêm các thông số vĩ mô cho dự án (Loại hình công trình, Phân cấp / Hạng sao, và Hình thức thi công) phục vụ công tác áp dụng tiêu chuẩn ngầm và quản lý báo giá.
- Yêu cầu thiết kế ẩn/hiện động trường **Phân cấp / Hạng sao** và hiển thị cảnh báo an toàn cháy nổ & cách âm đặc thù khi chọn phân cấp `4-5 Sao` cho Khách sạn / Resort.
- Lược bỏ trường nhập "Thuế VAT (%)" trên giao diện vì giá trị này đã được mặc định trong file Excel (8%). Tuy nhiên, các hàm logic trong JS và cơ sở dữ liệu Excel vẫn cần thuộc tính `vatRate` để tính toán nhằm duy trì tính tương thích ngược và chạy chính xác các công thức.

### Giải pháp kỹ thuật đã áp dụng
1. **Bổ sung các trường UI mới (`index.html`)**:
   - Thêm dropdown `<select id="proj-type">` với 9 loại hình công trình.
   - Thêm dropdown `<select id="proj-stars">` trong khung container `#proj-stars-group` (mặc định ẩn).
   - Thêm hộp cảnh báo `#proj-stars-warning` (mặc định ẩn) để hiển thị cảnh báo cháy nổ & cách âm cho công trình 4 - 5 sao.
   - Thêm cụm radio button `name="proj-nature"` cho phép chọn hình thức thi công (`Thiết kế & Xây mới` / `Cải tạo / Sửa chữa hiện trạng`).
2. **Ẩn trường nhập Thuế VAT (`index.html`)**:
   - Thay thế thẻ div `.form-group` chứa phần giao diện nhập Thuế VAT cũ bằng một input ẩn: `<input type="hidden" id="proj-vat-rate" value="8">`.
   - Giải pháp này giúp JS vẫn đọc và lưu trữ được `vatRate = 8` thông qua `document.getElementById('proj-vat-rate').value` mà không bị crash ứng dụng do lỗi tham chiếu `null`.
3. **Logic ẩn hiện động và đồng bộ dữ liệu (`app.js`)**:
   - Trong `init()`, đăng ký sự kiện `change` trên `#proj-type` và `#proj-stars` để cập nhật hiển thị động cho khung chọn sao và khối cảnh báo khắt khe.
   - Trong `openProjectModal`, nạp dữ liệu từ dự án cũ (hoặc gán mặc định `residential`, `1-2`, `new`) và cập nhật ngay trạng thái hiển thị của các khối UI động dựa theo giá trị đó.
   - Trong `saveProject`, đọc các trường `type`, `stars` (nếu là hotel/resort, ngược lại là `null`) và `nature` để lưu trữ đồng bộ vào LocalStorage.
4. **Định dạng CSS đẹp mắt (`style.css`)**:
   - Viết các rule CSS làm đẹp cho các radio button (`.radio-group`, `.radio-label`) và khung cảnh báo cao cấp (`.alert-warning`) sử dụng tông màu hổ phách (`--brand-gold`) và nền mờ chuyên nghiệp.

### Bài học kinh nghiệm
- **Cách thức ẩn trường UI an toàn**: Khi muốn loại bỏ một trường nhập liệu trên giao diện nhưng trường đó vẫn được dùng trong logic tính toán hay lưu trữ, việc thay thế nó bằng `<input type="hidden">` là giải pháp an toàn và nhanh gọn nhất. Tránh việc xóa hoàn toàn thẻ HTML dẫn đến lỗi runtime `Cannot read property 'value' of null` trong JS trừ khi chấp nhận viết lại toàn bộ logic liên quan.
- **Lưu trữ dữ liệu có điều kiện**: Với những trường dữ liệu đặc thù (như số sao chỉ thuộc về Khách sạn / Resort), khi lưu trữ cần kiểm tra điều kiện để gán `null` cho các trường hợp không phù hợp, giúp làm sạch cơ sở dữ liệu và tối ưu hóa cấu trúc JSON trong LocalStorage.

---

## 20. Đồng bộ hóa logic UI, xem trước Web và xuất file Excel / PDF (2026-06-25)

### Vấn đề đã gặp
- Khi thực hiện thay đổi bất kỳ trường thông tin nào trên giao diện (nhập liệu UI), ví dụ như đổi nhãn **"Chủ đầu tư"** thành **"Công trình"** (trường `proj-client`) hoặc ẩn các tính năng (như Thuế VAT, Địa chỉ công trình), nếu không cập nhật đồng bộ ở các module xử lý đầu ra, dữ liệu trong file Excel xuất ra và giao diện xem trước Web (PDF preview) sẽ bị lệch cấu trúc hoặc hiển thị sai lệch nhãn so với ý muốn của người dùng.
- Nguyên nhân là do tệp Excel và Web preview lấy nguồn dữ liệu từ các biến dữ liệu lưu trữ (`project.client`, `project.name`, `project.address`), nhưng các hàm sinh tiêu đề (`buildHeader`) và hiển thị preview (`openPreview`) trước đó sử dụng các nhãn cứng cũ hoặc ánh xạ sai vị trí các trường dữ liệu mới (ví dụ: dùng tên dự án thay thế cho tên công trình).

### Giải pháp kỹ thuật đã áp dụng
1. **Kiểm soát tính tương thích ngược bằng thẻ ẩn**:
   - Khi ẩn các tính năng trên giao diện nhập liệu (như Địa chỉ, Thuế VAT), chuyển chúng thành các thẻ ẩn (`<input type="hidden">`) thay vì xóa bỏ hoàn toàn. Điều này giúp hệ thống vẫn tự động thu thập và đồng bộ hóa dữ liệu xuống localStorage mà không bị lỗi crash script.
2. **Đồng bộ hóa ánh xạ trong file Excel (`generateWorkbook`)**:
   - Cập nhật hàm tạo header Excel `buildHeader` để lấy giá trị từ các trường thích hợp sau khi đổi nhãn: Dòng 3 hiển thị `CÔNG TRÌNH: ${project.client || ''}` (giá trị mới của trường Công trình) thay vì `project.name` (Tên dự án) như trước.
   - Sửa đổi dòng 5 `Kính gởi: ${project.recipient || ''}` để loại bỏ fallback sang `project.client`, vì `project.client` hiện tại đang làm nhiệm vụ lưu trữ tên Công trình chứ không phải người nhận.
3. **Đồng bộ hóa giao diện Web Preview / PDF (`openPreview`)**:
   - Cập nhật các phần tử HTML xem trước (`pv-project-name`, `pv-client-name`) đồng nhất 100% với logic ánh xạ của Excel để bản in PDF xuất ra từ trình duyệt luôn đồng bộ hoàn toàn với tệp Excel tải về.

### Bài học kinh nghiệm
- **Đồng bộ hóa dữ liệu từ đầu vào đến đầu ra**: Bất cứ khi nào thực hiện một thay đổi nhỏ về nhãn (label) hoặc cấu trúc trên form UI, lập tức rà soát lại tất cả các luồng xử lý xuất bản (sinh file Excel, hiển thị preview bản in PDF) để cập nhật logic hiển thị tương ứng. Dữ liệu đầu ra (Excel/PDF) phải luôn lấy đúng nguồn từ các trường nhập liệu tương ứng trên giao diện để tránh tình trạng lệch thông tin.


---

## 21. Đồng bộ hóa tệp Excel/PDF thời gian thực qua FastAPI & Excel COM (2026-06-25)

### Vấn đề đã gặp
- Trình duyệt chạy trong môi trường Sandbox bảo mật nghiêm ngặt nên không thể tự ý ghi hoặc lưu các tệp tin Excel/PDF âm thầm xuống đĩa cứng của người dùng mà không hiển thị hộp thoại tải về liên tục (gây phiền toái cực lớn khi nhập liệu thời gian thực).
- Việc tự động chuyển đổi từ bảng tính Excel phức tạp (chứa các công thức liên kết động, định dạng độ rộng, đường viền, gộp ô, màu nền, font chữ Times New Roman và logo ảnh nhúng) sang tệp PDF bằng các thư viện Python thuần túy thường bị lỗi định dạng nghiêm trọng hoặc không hỗ trợ OpenXML đầy đủ.

### Giải pháp kỹ thuật đã áp dụng
1. **Thiết lập luồng đồng bộ gián tiếp (API Bridge)**:
   - Viết hàm `triggerAutoSync()` trong JS để tự động tạo tệp Excel đã định dạng (dùng `generateWorkbook` và `JSZip`), mã hóa sang chuỗi Base64 và gửi yêu cầu POST đến cổng API nội bộ của FastAPI (`/api/sync-project-files`).
   - Móc nối (hook) trực tiếp hàm này vào trong phương thức lưu cơ sở dữ liệu `DB.save(data)`. Do mọi hoạt động thay đổi trên UI (thêm phòng, sửa kích thước, đổi hạng mục, cập nhật chi phí...) đều gọi qua `DB.save` để cập nhật `localStorage`, giải pháp này đảm bảo đồng bộ hóa tức thời trên mỗi thao tác lưu của người dùng.
2. **Xuất PDF qua Excel COM Automation (Background Task)**:
   - Trên backend Python của FastAPI, ghi file Excel đã giải mã vào thư mục `exports/` tương ứng.
   - Sử dụng thư viện `pywin32` (`win32com.client`) để khởi chạy một phiên ứng dụng Microsoft Excel ẩn (`Visible = False`, `DisplayAlerts = False`), nạp bảng tính và gọi hàm API chính chủ của Excel để xuất PDF: `wb.ExportAsFixedFormat(0, pdf_path)`.
   - Đưa tác vụ gọi COM này vào hàng đợi nền `BackgroundTasks` của FastAPI để trả về phản hồi HTTP cho giao diện người dùng ngay lập tức, triệt tiêu hoàn toàn độ trễ 1-2 giây khi Excel khởi chạy.

### Bài học kinh nghiệm
- **Tận dụng API local làm cầu nối**: Đối với ứng dụng Web chạy cục bộ (offline/local), việc xây dựng một API cục bộ gọn nhẹ (FastAPI/NodeJS) là giải pháp tốt nhất để vượt qua các giới hạn bảo mật của trình duyệt, hỗ trợ lưu trữ tệp tin và thực hiện các tác vụ hệ thống âm thầm.
- **Tận dụng engine gốc của hệ điều hành**: Thay vì cố gắng tái tạo hoặc biên dịch lại cách hiển thị Excel phức tạp sang PDF bằng các thư viện dựng hình HTML/PDF không hoàn hảo, hãy gọi trực tiếp ứng dụng bản quyền đã cài đặt trên máy (như Microsoft Excel qua COM) để đảm bảo kết quả chính xác 100% về mặt mỹ thuật và bố cục in ấn.
- **Bất đồng bộ hóa tác vụ COM**: COM Automation của Windows là một tiến trình đơn luồng và có độ trễ lớn khi khởi động. Luôn thực hiện bất đồng bộ hóa (asynchronous/background execution) đối với các tác vụ này để bảo vệ trải nghiệm mượt mà của giao diện người dùng.

---

## 22. Đưa tên phòng vào tiêu đề phụ của các sheet chi tiết (2026-06-25)

### Vấn đề đã gặp
- Khi xuất Excel hoặc in ấn PDF cho các phòng chi tiết riêng biệt (như sheet `Phòng khám thai 01`), tiêu đề phụ (hàng thứ 2 của Excel) trước đây chỉ hiển thị tên dự án chung (ví dụ: `KHU KHÁM SẢN VIP`), làm người đọc bảng tính khó phân biệt nhanh tên phòng nếu không nhìn vào tiêu đề chính.

### Giải pháp kỹ thuật đã áp dụng
1. **Bổ sung tham số roomName vào buildHeader**:
   - Cập nhật hàm tạo header Excel `buildHeader` để nhận thêm tham số tên phòng `roomName` (mặc định là `null`).
   - Nếu `roomName` có giá trị, định dạng dòng phụ thành: `[Tên dự án] - [Tên phòng viết hoa]`.
2. **Đồng bộ hóa các đầu ra**:
   - Excel: Truyền `room.name` từ vòng lặp phòng chi tiết vào lệnh gọi `buildHeader`.
   - Web/PDF Preview: Trong `openPreview()`, khi xem tab chi tiết cho một phòng cụ thể (`selRoomId !== 'all'`), thay thế nội dung thẻ phụ `#pv-subtitle` bằng tên dự án kết hợp tên phòng viết hoa.
   - Do PDF in ấn lấy nguồn trực tiếp từ các sheet Excel (`renderWorksheetToHtml`), thay đổi này tự động đồng bộ hóa trên cả file Excel tải về lẫn tệp PDF in ra từ trình duyệt.

### Bài học kinh nghiệm
- **Thiết kế API Header linh hoạt**: Các hàm tiện ích tạo tiêu đề bảng biểu nên hỗ trợ các tham số tùy chọn động (như tên hạng mục con/phòng) để tránh việc phải viết lại nhiều hàm header trùng lặp cho các loại sheet khác nhau.

---

## 23. Quản lý hình ảnh hiện trạng theo từng phòng và nén ảnh qua Canvas (2026-06-25)

### Vấn đề đã gặp
- Khi kỹ sư đi hiện trường khảo sát và đính kèm trực tiếp các ảnh chụp gốc từ điện thoại thông minh (dung lượng thường từ 3MB - 5MB mỗi ảnh) vào đối tượng phòng rồi lưu trữ trực tiếp vào LocalStorage, trình duyệt sẽ nhanh chóng bị tràn bộ nhớ (do giới hạn lưu trữ LocalStorage chỉ khoảng 5MB cho toàn bộ ứng dụng). Việc này làm crash ứng dụng, mất dữ liệu và làm chậm đáng kể hiệu năng bốc khối lượng khi có nhiều phòng.

### Giải pháp kỹ thuật đã áp dụng
1. **Ràng buộc nén ảnh Canvas bắt buộc**:
   - Khi tệp tin được kéo thả hoặc tải lên thông qua vùng đính kèm (`room-photo-zone`), gọi ngầm hàm xử lý canvas để tải ảnh lên một đối tượng ảnh trong bộ nhớ, co chiều rộng tối đa về **800px** (giữ nguyên tỷ lệ chiều cao).
   - Xuất dữ liệu ảnh thông qua `canvas.toDataURL('image/jpeg', 0.7)` để nén chất lượng xuống 70% dạng JPEG. Điều này giúp giảm dung lượng tệp tin ảnh từ 5MB xuống chỉ còn **~50KB** (giảm 100 lần) trước khi lưu vào mảng Base64 `room.photos`.
2. **Đồng bộ hóa hiển thị giao diện và các báo cáo đầu ra**:
   - **Giao diện**: Hiển thị các thumbnail ảnh nhỏ kèm nút xóa trực quan `✕` ở góc ngay trong modal phòng để người dùng kiểm soát.
   - **Web / PDF Preview**: Trong hàm `_renderPreviewDetail`, tự động duyệt mảng ảnh của phòng và render thành một hàng đính kèm đặc thù `pv-room-photos-row` chứa gallery các ô ảnh hiện trạng trực quan ngay dưới phần bảng kê chi tiết phòng.
   - **Excel**: Trong quá trình dựng sheet phòng, tự động chèn thêm một dòng liệt kê tên các ảnh hiện trạng đã đính kèm ở cuối bảng tính chi tiết để báo cáo đồng bộ hoàn hảo.

### Bài học kinh nghiệm
- **Kiểm soát dung lượng lưu trữ Offline**: Đối với các ứng dụng Single Page chạy offline lưu dữ liệu qua LocalStorage/IndexedDB, việc nén và tối ưu hóa tài nguyên media (hình ảnh, tài liệu) ngay tại client-side trước khi ghi vào DB là bắt buộc để duy trì tính ổn định của hệ thống.
- **Canvas-based compression**: Sử dụng Canvas kết hợp với `toDataURL` JPEG là giải pháp nhẹ nhàng, không cần thư viện ngoài, giúp nén và thay đổi kích thước ảnh cực nhanh trên cả trình duyệt máy tính và các thiết bị di động.


---

## 24. Đồng bộ in hoa các dòng tiêu đề báo cáo (2026-06-25)

### Vấn đề đã gặp
- Khi người dùng nhập tên dự án, tên phòng, hay tên công trình dưới dạng chữ thường hoặc chữ hoa lẫn lộn, các dòng tiêu đề trên xuất bản Excel, giao diện Web Preview và file PDF in ra sẽ hiển thị thiếu đồng nhất (ví dụ: dòng chữ thường xen kẽ dòng chữ in hoa), làm giảm độ chuyên nghiệp của sản phẩm bàn giao.

### Giải pháp kỹ thuật đã áp dụng
1. **Ép kiểu in hoa trực tiếp khi tạo Header Excel**:
   - Trong hàm `buildHeader` của `app.js`, gọi hàm `.toUpperCase()` cho tham số tiêu đề chính `title` và giá trị của dòng 2 (`project.subtitle || project.name`).
2. **Ép kiểu in hoa trên giao diện Web Preview và PDF**:
   - Cập nhật hàm `openPreview` và logic đổi tab trong `app.js` để tự động biến đổi chuỗi của phần tử `#pv-subtitle` và `#pv-project-name` thành chữ in hoa bằng phương thức `.toUpperCase()`.
   - Bổ sung quy tắc CSS `text-transform: uppercase;` trực tiếp vào style nội tuyến của hai thẻ div này trong `index.html` để làm lớp bảo vệ hiển thị, đảm bảo không có nội dung chữ thường nào xuất hiện trong 3 dòng đầu của báo cáo.
3. **Đồng bộ hóa**:
   - Áp dụng đồng thời trên mã nguồn của cả hai thư mục `du-toan` và `du-toan - v1` để giữ cho các tệp tin hoàn toàn đồng bộ byte-for-byte.

### Bài học kinh nghiệm
- **Đảm bảo tính nhất quán thẩm mỹ**: Đối với các tài liệu xuất bản chính thức như báo cáo khối lượng, dự toán công trình, các phần tiêu đề chính và phụ nên được chuẩn hóa in hoa hoặc định dạng thống nhất từ phía mã nguồn/giao diện thay vì phụ thuộc hoàn toàn vào dữ liệu nhập của người dùng.


---

## 25. Quản lý hình ảnh hiện trạng trực tiếp trên từng ô phòng ở màn hình chính (2026-06-25)

### Vấn đề đã gặp
- Trước đây, để thêm ảnh hiện trạng cho một phòng, người dùng bắt buộc phải mở Modal chỉnh sửa chi tiết phòng. Việc này qua nhiều bước nhấp chuột gây bất tiện khi kỹ sư khảo sát thực tế muốn tải nhanh nhiều ảnh trực tiếp ngay tại danh sách phòng ở màn hình chính.

### Giải pháp kỹ thuật đã áp dụng
1. **Nâng cấp giao diện ô phòng (Room Card UI)**:
   - Trong template HTML sinh ra từ hàm `renderRooms(project)`, chèn thêm một phần hiển thị ảnh hiện trạng dưới chân card.
   - Thêm dòng chữ hiển thị số lượng ảnh hiện tại: `📷 Ảnh hiện trạng: [Số lượng] tấm.` (mặc định hiển thị 0 nếu chưa có ảnh).
   - Thiết lập một thẻ input file ẩn (`<input type="file" accept="image/*" multiple style="display: none;">`) và nút bấm nổi bật `+ Thêm ảnh` để người dùng kích hoạt hộp thoại chọn file trên thiết bị.
2. **Hàm xử lý nén và lưu trữ bất đồng bộ độc lập**:
   - Viết hàm `handleRoomCardPhotoSelect(event, roomId)` để lắng nghe và xử lý sự kiện chọn file.
   - Sử dụng `FileReader` đọc file ảnh và truyền sang đối tượng `Canvas` dựng lại với kích thước chiều rộng tối đa **600px**, nén chất lượng **60% dạng JPEG** để bảo toàn dung lượng siêu nhẹ (~30-50KB).
   - Đẩy mảng Base64 đã nén trực tiếp vào trường `photos` của đối tượng phòng (`room.photos`).
   - Khai báo hai hàm alias `saveDataToStorage()` và `updateUIWorkspace()` để thực thi các logic đồng bộ hóa LocalStorage và re-render giao diện dự án ngay lập tức.
3. **Đồng bộ hóa**:
   - Tương thích 100% với logic hiển thị ảnh ở PDF/Web Preview và Excel đã cài đặt trước đó. Đồng thời đồng bộ tuyệt đối trên cả hai thư mục `du-toan` và `du-toan - v1`.

### Bài học kinh nghiệm
- **Tối ưu hóa thao tác người dùng (UX)**: Đưa các thao tác thường dùng (như đính kèm ảnh hiện trường khảo sát) ra màn hình chính dạng widget/quick actions giúp nâng cao trải nghiệm người dùng cuối rất nhiều so với việc bắt buộc đi sâu vào các lớp modal cài đặt chi tiết.

---

## 26. Khắc phục lỗi ẩn khuất nội dung Modal Phòng do độ tương phản thanh cuộn (2026-06-25)

### Vấn đề đã gặp
- Khi nâng cấp thêm vùng đính kèm hình ảnh hiện trạng trực tiếp vào Modal Phòng (ở cuối modal-body), các trường thông tin Thiết Bị Nội Thất, Nhà Vệ Sinh, và Ảnh Hiện Trạng Phòng bị ẩn khuất ở phía dưới và không hiển thị trên màn hình người dùng.
- Nguyên nhân là do thanh cuộn dọc (`overflow-y: auto`) của `.modal-body` trong chế độ tối (dark mode) được thiết kế quá mảnh (chỉ 5px) và sử dụng màu của biến `--border` (`#30363D` trên nền card `#161B22`), dẫn đến việc thanh cuộn gần như vô hình trên màn hình máy tính. Người dùng nghĩ rằng modal đã kết thúc ở khu vực đính kèm ảnh điện và không thực hiện thao tác cuộn xuống.

### Giải pháp kỹ thuật đã áp dụng
1. **Cải tiến thanh cuộn CSS (Scrollbar UX)**:
   - Thay đổi các thuộc tính webkit scrollbar trong `style.css` để nâng kích thước bề rộng từ 5px lên **8px** giúp dễ thao tác cuộn.
   - Thay thế màu nền thanh cuộn từ biến tối `--border` thành một lớp màu bán trong suốt có độ tương phản cao hơn (`rgba(255, 255, 255, 0.22)` và `rgba(255, 255, 255, 0.38)` khi di chuột qua).
   - Thiết lập màu nền track cuộn là `rgba(0, 0, 0, 0.15)` để định vị rõ vùng cuộn được.
2. **Triển khai Cache-Buster**:
   - Thêm tham số truy vấn phiên bản `?v=20260625-v2` vào các đường dẫn nạp tệp `style.css` và `app.js` trong tệp `index.html` của cả 2 thư mục `du-toan` và `du-toan - v1`. Điều này giúp bắt buộc trình duyệt của người dùng xóa bộ nhớ đệm cũ và tải ngay phiên bản giao diện và xử lý mới nhất.

---

## 27. Loại bỏ trường nhập liệu không cần thiết và bảo vệ an toàn DOM (2026-06-25)

### Vấn đề đã gặp
- Người dùng yêu cầu loại bỏ trường nhập liệu "Tiêu đề bảng" (Table Title) trong Modal tạo/sửa dự án do thông tin này có thể được đồng bộ tự động từ Tên dự án.
- Việc xóa bỏ thẻ HTML trực tiếp có thể gây ra lỗi runtime crash trong Javascript (`Cannot set properties of null` hoặc `Cannot read properties of null`) nếu mã nguồn JS vẫn truy vấn phần tử DOM bằng ID cũ (`proj-subtitle`).

### Giải pháp kỹ thuật đã áp dụng
1. **Lược bỏ HTML & Căn chỉnh UI**:
   - Xóa bỏ khối `form-group` chứa ô nhập liệu `proj-subtitle` trong tệp `index.html`.
   - Chuyển đổi khung chứa `form-row-2` thành một khối đơn lẻ để ô nhập liệu "Người lập (Từ:)" (`proj-sender`) hiển thị rộng toàn bộ chiều ngang vách, khớp hoàn hảo với các trường thông tin khác bên dưới.
2. **Xử lý An toàn Javascript (DOM Guarding)**:
   - Trong `app.js` (cả hai thư mục `du-toan` và `du-toan - v1`), cập nhật các hàm `openProjectModal` và `saveProject` bằng cách thêm các điều kiện kiểm tra tồn tại của phần tử (`if (document.getElementById('proj-subtitle'))`).
   - Khi lưu thông tin dự án, nếu ô nhập liệu không tồn tại, trường `subtitle` được mặc định gán chuỗi rỗng `''`. Logic sẵn có của hệ thống sẽ tự động chuyển hướng và lấy Tên dự án (`project.name`) làm tiêu đề chính cho các bản in Web/PDF và tệp xuất Excel dưới dạng chữ in hoa.

---

## 28. Loại bỏ phần Đơn giá tùy chọn trong Modal Phòng và bảo vệ truy cập DOM (2026-06-25)

### Vấn đề đã gặp
- Người dùng yêu cầu loại bỏ hoàn toàn phần "Đơn giá (tùy chọn — dùng cho báo giá)" bao gồm 3 trường (Đơn giá sàn, Đơn giá tường, Đơn giá trần) trong Modal Phòng.
- Việc xóa bỏ các phần tử này trong tệp HTML sẽ dẫn đến lỗi Javascript nếu mã nguồn cố gắng đọc hoặc ghi thuộc tính `.value` của chúng, gây treo hoặc lỗi chức năng mở/lưu thông tin phòng.

### Giải pháp kỹ thuật đã áp dụng
1. **Dọn dẹp HTML**:
   - Xóa bỏ thẻ tiêu đề `💰 Đơn giá (tùy chọn — dùng cho báo giá)` và khung `dim-grid` chứa 3 input liên quan trong tệp `index.html`.
2. **Cập nhật JS an toàn với Optional Chaining và Null Guarding**:
   - Trong `app.js` (cả hai thư mục `du-toan` và `du-toan - v1`), cập nhật hàm `getRoomDataFromUI` sử dụng toán tử optional chaining (`?.value`) để tránh lỗi khi đọc giá trị của các phần tử không còn tồn tại trong DOM.
   - Trong hàm `openRoomModal`, thêm điều kiện kiểm tra sự tồn tại của phần tử trước khi gán dữ liệu mặc định (`if (floorPriceEl) ...`), đảm bảo modal mở bình thường và dữ liệu cũ trong cơ sở dữ liệu vẫn được bảo toàn nguyên vẹn mà không gây lỗi giao diện.

---

## 29. Thay đổi nhãn giao diện Tên công trình thành Tên hạng mục (2026-06-25)

### Vấn đề đã gặp
- Người dùng phản hồi và yêu cầu thay đổi nhãn "Tên công trình" (Project Name) trong Modal dự án thành "Tên hạng mục" (Item Name/Scope Name) để phân biệt rõ ràng hơn giữa công trình lớn tổng thể (ví dụ: Bệnh viện Thiện Hạnh) và phần hạng mục công việc cụ thể đang lập dự toán (ví dụ: Khu khám sản VIP).

### Giải pháp kỹ thuật đã áp dụng
1. **Cập nhật HTML**:
   - Trong `index.html` của cả hai thư mục `du-toan` và `du-toan - v1`, thay thế nội dung nhãn `<label>Tên công trình ...</label>` thành `<label>Tên hạng mục ...</label>`.
   - Cập nhật văn bản gợi ý (placeholder) của input `proj-name` từ `VD: Biệt thự Quận 9 — Anh Minh` thành `VD: KHU KHÁM SẢN VIP` để đồng bộ ngữ cảnh sử dụng thực tế.

---

## 30. Tối ưu hóa chính sách lưu đệm đầu cuối bằng Middleware Backend (2026-06-25)

### Vấn đề đã gặp
- Khi chỉnh sửa nhãn "Tên công trình" thành "Tên hạng mục" và cập nhật HTML/JS tĩnh, trình duyệt của người dùng vẫn tiếp tục sử dụng phiên bản bộ nhớ đệm (disk cache) cũ đã được lưu từ trước, dẫn đến việc giao diện thực tế không thay đổi mặc dù tệp nguồn trên đĩa đã được sửa.

### Giải pháp kỹ thuật đã áp dụng
1. **Bổ sung Middleware chống lưu đệm (No-Cache Middleware) trên FastAPI**:
   - Ở tệp `api/index.py`, chèn thêm một middleware HTTP dạng `http` chặn bắt các yêu cầu nạp tài nguyên.
   - Nhận diện các đường dẫn tĩnh có đuôi tệp `.html`, `.js`, `.css` hoặc trang chủ (`/`, `/du-toan/`).
   - Thiết lập các header trả về bắt buộc trình duyệt bỏ qua bộ nhớ đệm và liên hệ trực tiếp máy chủ để lấy tệp mới nhất:
     - `Cache-Control: no-store, no-cache, must-revalidate, max-age=0`
     - `Pragma: no-cache`
     - `Expires: 0`
   - Nhờ vậy, từ nay bất kỳ chỉnh sửa nào về giao diện hay logic JS sẽ được phản ánh ngay lập tức trên máy khách mà không bị kẹt bộ nhớ đệm.


---

## 31. Phân loại ảnh hiện trạng chi tiết theo từng hạng mục thiết bị và hiển thị tương ứng (2026-06-25)

### Vấn đề đã gặp
- Người dùng muốn quản lý ảnh hiện trạng của phòng một cách chi tiết hơn bằng cách đính kèm ảnh phân loại trực tiếp dưới từng nhóm thiết bị nhập liệu (Đèn, Tủ điện, Máy lạnh, Toàn cảnh, Thiết bị nội thất, Phòng vệ sinh/TBVS/Chống thấm, và Khác).
- Khi render bảng BOQ, Web/PDF Preview, hoặc xuất Excel, ảnh hoặc tên ảnh của nhóm nào phải tự động hiển thị tương ứng ở cột **Ghi Chú** của dòng hạng mục đó (thu nhỏ về 120px trên giao diện và hiển thị dạng text [📷 Tên_Hạng_Mục: tên_ảnh] trên Excel).

### Giải pháp kỹ thuật đã áp dụng
1. **Cải tiến giao diện Modal Phòng (HTML)**:
   - Thay thế khung tải ảnh chung của phòng bằng 7 nút đính kèm độc lập cùng 7 vùng preview thumbnail tương ứng trực tiếp dưới các ô ghi chú văn bản của từng mục: Toàn cảnh (overview), Đèn (den), Tủ điện (	udien), Máy lạnh (maylanh), Nội thất (
oithat), Phòng vệ sinh (wc), và Khác (other).
2. **Cập nhật Logic Lưu Trữ & Xử lý Ảnh (JS)**:
   - Cấu trúc lại trường dữ liệu photos của phòng thành một đối tượng chứa 7 mảng độc lập.
   - Thêm hàm bổ trợ getRoomPhotosCount và getRoomPhotos để tự động xử lý tương thích ngược cả kiểu mảng ảnh phẳng cũ và kiểu đối tượng phân loại mới.
   - Hàm handleRoomPhotoSelect thực hiện nén ảnh về chiều rộng tối đa 600px, chất lượng 60% và đưa vào đúng mảng phân loại của phòng.
3. **Gán nhãn Phân Loại và hiển thị cột Ghi Chú**:
   - Trong hàm CALC.room(room), gán thuộc tính photoCategory cho các dòng hạng mục tương ứng được bóc tách từ ghi chú hoặc custom: Đèn (den), Tủ điện (	udien), Máy lạnh (maylanh), Nội thất (
oithat), Vệ sinh và Chống thấm (wc), Hạng mục tự chọn (other).
   - Hàm 
enderBOQ và _renderPreviewDetail bốc ảnh dựa trên thuộc tính photoCategory của dòng để hiển thị thumbnail 120px trực tiếp trong ô Ghi chú của dòng đó.
   - Cập nhật phần vẽ tất cả ảnh hiện trạng phòng ở chân trang Web/PDF Preview và sheet Chi tiết phòng trên Excel để duyệt qua cả 7 phân loại.
   - Hàm generateWorkbook (xuất Excel) cập nhật labelMap để chèn thông tin đính kèm (ví dụ: [📷 Nội thất: anh1.jpg, anh2.jpg]) ở cột Ghi chú của dòng hạng mục tương ứng.
4. **Đồng bộ hóa mã nguồn**:
   - Đồng bộ hóa 100% byte-for-byte các tệp index.html, pp.js và style.css giữa hai thư mục du-toan và du-toan - v1.
