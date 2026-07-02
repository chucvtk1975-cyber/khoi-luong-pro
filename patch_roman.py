import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app.js', 'r', encoding='utf-8') as f:
    c = f.read()

# Tim chinh xac cac doan can sua

# 1. Tim doan khoi tao room, them subRomIdx
old_room_header = """    const roman = romanNums[idx] || (idx + 1);
    // Header: chỉ tên phòng
    html += `
      <tr class="boq-room-header" data-kr="${room.id}">
        <td colspan="10">${roman}. ${room.name.toUpperCase()}</td>
      </tr>`;"""

new_room_header = """    const roman = romanNums[idx] || (idx + 1);
    let subRomIdx = 1; // counter cho cac muc con trong phong (II, III, IV...)
    // Header: chỉ tên phòng — I. TÊN PHÒNG (không cần sub index)
    html += `
      <tr class="boq-room-header" data-kr="${room.id}">
        <td colspan="10">${roman}. ${room.name.toUpperCase()}</td>
      </tr>`;"""

if old_room_header in c:
    c = c.replace(old_room_header, new_room_header, 1)
    print("✓ Added subRomIdx init")
else:
    print("✗ room_header not found exactly")
    # Try simpler
    old2 = "const roman = romanNums[idx] || (idx + 1);\n    // Header: chỉ tên phòng"
    if old2 in c:
        c = c.replace(old2, "const roman = romanNums[idx] || (idx + 1);\n    let subRomIdx = 1; // sub-section counter\n    // Header: chỉ tên phòng", 1)
        print("✓ Added subRomIdx via alt")
    else:
        print("✗ alt also not found")

# 2. Them so La Ma vao elecHeader
old_elec = """        if (item.surface === 'elecHeader') {
          stt = 1; // Reset STT khi vào phần Điện
          html += `<tr class="boq-elec-header" data-key="${key}" data-kr="${room.id}"><td colspan="10">⚡ THIẾT BỊ ĐIỆN</td></tr>`;
          return;"""

new_elec = """        if (item.surface === 'elecHeader') {
          stt = 1; // Reset STT khi vào phần Điện
          const elecRom = romanNums[subRomIdx++] || subRomIdx;
          html += `<tr class="boq-elec-header" data-key="${key}" data-kr="${room.id}"><td colspan="10">${elecRom}. ⚡ THIẾT BỊ ĐIỆN</td></tr>`;
          return;"""

if old_elec in c:
    c = c.replace(old_elec, new_elec, 1)
    print("✓ Added Roman to elecHeader")
else:
    print("✗ elecHeader not found - trying alternate")
    old_elec2 = "⚡ THIẾT BỊ ĐIỆN</td></tr>`;"
    idx_e = c.find(old_elec2)
    if idx_e > 0:
        # Lay dong truoc do
        line_start = c.rfind('\n', 0, idx_e)
        snippet = c[line_start:idx_e + len(old_elec2) + 5]
        print(f"Found context: {repr(snippet[:200])}")

# 3. Them so La Ma vao noteHeader
old_note = """        if (item.surface === 'noteHeader') {
          stt = 1; // Reset STT khi vào phần Ghi chú
          html += `<tr class="boq-note-header" data-key="${key}" data-kr="${room.id}"><td colspan="10">📝 CHI TIẾT TỪ GHI CHÚ</td></tr>`;
          return;"""

new_note = """        if (item.surface === 'noteHeader') {
          stt = 1; // Reset STT khi vào phần Ghi chú
          const noteRom = romanNums[subRomIdx++] || subRomIdx;
          html += `<tr class="boq-note-header" data-key="${key}" data-kr="${room.id}"><td colspan="10">${noteRom}. 📝 CHI TIẾT TỪ GHI CHÚ</td></tr>`;
          return;"""

if old_note in c:
    c = c.replace(old_note, new_note, 1)
    print("✓ Added Roman to noteHeader")
else:
    print("✗ noteHeader not found")

# 4. Them so La Ma vao subHeader (custom IN HOA)
old_sub = """            if (isSubHdr) {
            stt = 1; // reset STT
            html += `
              <tr class="boq-sub-header" data-key="ci:${ci.id}" data-kr="${room.id}" data-ci="${ci.id}">"""

new_sub = """            if (isSubHdr) {
            stt = 1; // reset STT
            const subRom = romanNums[subRomIdx++] || subRomIdx;
            html += `
              <tr class="boq-sub-header" data-key="ci:${ci.id}" data-kr="${room.id}" data-ci="${ci.id}">"""

if old_sub in c:
    c = c.replace(old_sub, new_sub, 1)
    print("✓ Added Roman to subHeader (custom IN HOA)")
else:
    print("✗ subHeader not found - trying alt")
    old_sub2 = "if (isSubHdr) {\n            stt = 1; // reset STT\n            html +="
    if old_sub2 in c:
        c = c.replace(old_sub2, "if (isSubHdr) {\n            stt = 1; // reset STT\n            const subRom = romanNums[subRomIdx++] || subRomIdx;\n            html +=", 1)
        print("✓ Added subRom via alt")

# 5. Tim va sua boq-sub-header-cell de them so La Ma
old_subcell = """                <td colspan="8" class="boq-sub-header-cell" style="font-weight:700;color:var(--brand-purple-light);">${ci.label}"""
new_subcell = """                <td colspan="8" class="boq-sub-header-cell" style="font-weight:700;color:var(--brand-purple-light);">${subRom}. ${ci.label}"""

if old_subcell in c:
    c = c.replace(old_subcell, new_subcell, 1)
    print("✓ Added subRom to sub-header-cell label")
else:
    print("✗ sub-header-cell not found")

# 6. Them Roman vao OC header (boq-room-oc-hdr)
old_oc = "💰 CHI PHÍ KHÁC — ${room.name}"
new_oc = "${romanNums[subRomIdx] || (subRomIdx+1)}. 💰 CHI PHÍ KHÁC — ${room.name}"
if old_oc in c:
    c = c.replace(old_oc, new_oc, 1)
    print("✓ Added Roman to OC header")
else:
    print("✗ OC header not found")

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(c)

print("\n✅ Roman numerals patch done!")
