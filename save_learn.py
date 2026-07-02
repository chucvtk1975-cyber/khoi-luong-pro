import sys
sys.stdout.reconfigure(encoding='utf-8')

lesson = """

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
text.split('\\n').forEach(line => { lr[0] = li+1; lr[1] = line; })

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
"""

with open('LEARN.md', 'r', encoding='utf-8') as f:
    existing = f.read()

with open('LEARN.md', 'w', encoding='utf-8') as f:
    f.write(existing + lesson)

print("✅ LEARN.md updated with lessons from 2026-06-21 session")
