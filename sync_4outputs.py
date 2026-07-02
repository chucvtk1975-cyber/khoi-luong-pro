import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app.js', 'r', encoding='utf-8') as f:
    c = f.read()

changes = 0

# ═══════════════════════════════════════════════════════════════
# FIX A: Bỏ emoji trong renderBOQ (web preview + print PDF)
# ═══════════════════════════════════════════════════════════════

# A1: elecHeader - bỏ ⚡
old_elec_web = '}. ⚡ THIẾT BỊ ĐIỆN</'
new_elec_web = '}. THIẾT BỊ ĐIỆN</'
if old_elec_web in c:
    c = c.replace(old_elec_web, new_elec_web)
    print("✓ A1: Removed ⚡ from renderBOQ elecHeader")
    changes += 1
else:
    print(f"✗ A1: not found")

# A2: noteHeader - bỏ 📝
old_note_web = '}. 📝 CHI TIẾT TỪ GHI'
new_note_web = '}. CHI TIẾT TỪ GHI'
if old_note_web in c:
    c = c.replace(old_note_web, new_note_web)
    print("✓ A2: Removed 📝 from renderBOQ noteHeader")
    changes += 1
else:
    print(f"✗ A2: not found")

# A3: ep-elec-hdr (printPreview/another render at 441804)
old_ep = '>⚡ THIẾT BỊ ĐIỆN</td>'
new_ep = '>THIẾT BỊ ĐIỆN</td>'
if old_ep in c:
    c = c.replace(old_ep, new_ep)
    print("✓ A3: Removed ⚡ from ep-elec-hdr")
    changes += 1
else:
    print(f"✗ A3: not found. Searching...")
    idx = c.find('ep-elec-hdr')
    if idx > 0:
        print(f"  Found ep-elec-hdr at {idx}: {c[idx:idx+100]}")

# ═══════════════════════════════════════════════════════════════
# FIX B: Thêm Roman numeral section headers vào Excel CHI TIẾT sheet
# Đồng bộ với web preview (I. SÀN, II. TƯỜNG, III. TRẦN, IV. CỬA ĐI, V. CỬA SỔ)
# ═══════════════════════════════════════════════════════════════

chi_tiet_pos = c.find('BẢNG CHI TIẾT KHỐI LƯỢNG')
item_forEach  = c.find('calc.items.forEach', chi_tiet_pos)

# B1: Them khai bao bien TRUOC items.forEach trong CHI TIET sheet
# Tim doan code ngay truoc calc.items.forEach
# Anchor: "const blkDetail = () => Array(10).fill('');"
anchor_b1 = "const calc = CALC.room(room);"
# Tim vi tri cuoi cung (trong CHI TIET sheet)
b1_pos = c.rfind(anchor_b1, chi_tiet_pos, chi_tiet_pos + 20000)
print(f"\nB1 anchor at: {b1_pos}")

if b1_pos > 0:
    # Tim ket thuc dong
    b1_line_end = c.find('\n', b1_pos)
    insert_after = c[b1_pos:b1_line_end+1]
    
    new_b1 = insert_after + """  // ── Roman numeral section headers (đồng bộ web preview)
  let excelSubRomIdx = 0;
  const seenSurfExcel = new Set();
  const SURF_GRP_EXCEL = {
    floor:    { gid:'san',   label:'SÀN' },
    wall:     { gid:'tuong', label:'TƯỜNG' },
    wallZ1:   { gid:'tuong', label:'TƯỜNG' },
    wallZ2:   { gid:'tuong', label:'TƯỜNG' },
    perimeter:{ gid:'tuong', label:'TƯỜNG' },
    ceiling:  { gid:'tran',  label:'TRẦN' },
    ceilPerim:{ gid:'tran',  label:'TRẦN' },
    door:     { gid:'cuadi', label:'CỬA ĐI' },
    window:   { gid:'cuaso', label:'CỬA SỔ' },
  };
"""
    c = c[:b1_pos] + new_b1 + c[b1_line_end+1:]
    print("✓ B1: SURF_GRP_EXCEL variables declared before forEach in Excel CHI TIẾT")
    changes += 1
else:
    print("✗ B1: anchor not found")

# B2: Trong elecHeader branch - them Roman numeral
# Sau khi B1 insert, vi tri se thay doi - can tim lai
chi_tiet_pos2 = c.find('BẢNG CHI TIẾT KHỐI LƯỢNG')
item_forEach2  = c.find('calc.items.forEach', chi_tiet_pos2)

# Tim "hdr[1] = 'THIẾT BỊ ĐIỆN';" trong forEach block
hdr_elec_pos = c.find("hdr[1] = 'THIẾT BỊ ĐIỆN';", item_forEach2)
if hdr_elec_pos > 0 and hdr_elec_pos < item_forEach2 + 15000:
    old_b2 = "hdr[1] = 'THIẾT BỊ ĐIỆN';"
    new_b2 = "hdr[1] = `${romanNums[excelSubRomIdx++] || excelSubRomIdx}. THIẾT BỊ ĐIỆN`;"
    c = c.replace(old_b2, new_b2, 1)  # Chi replace lan dau (trong CHI TIET sheet)
    print("✓ B2: Added Roman numeral to elecHeader in Excel CHI TIẾT")
    changes += 1
else:
    print(f"✗ B2: elecHeader label not found (pos={hdr_elec_pos})")

# B3: Tim "hdr[1] = 'CHI TIẾT TỪ GHI CHÚ';" trong forEach block
chi_tiet_pos3 = c.find('BẢNG CHI TIẾT KHỐI LƯỢNG')
item_forEach3  = c.find('calc.items.forEach', chi_tiet_pos3)
hdr_note_pos = c.find("hdr[1] = 'CHI TIẾT TỪ GHI CHÚ';", item_forEach3)
if hdr_note_pos > 0 and hdr_note_pos < item_forEach3 + 15000:
    old_b3 = "hdr[1] = 'CHI TIẾT TỪ GHI CHÚ';"
    new_b3 = "hdr[1] = `${romanNums[excelSubRomIdx++] || excelSubRomIdx}. CHI TIẾT TỪ GHI CHÚ`;"
    c = c.replace(old_b3, new_b3, 1)
    print("✓ B3: Added Roman numeral to noteHeader in Excel CHI TIẾT")
    changes += 1
else:
    print(f"✗ B3: noteHeader label not found (pos={hdr_note_pos})")

# B4: Them SURF_GRP detection TRUOC "const noStt" trong forEach (Excel CHI TIẾT)
chi_tiet_pos4 = c.find('BẢNG CHI TIẾT KHỐI LƯỢNG')
item_forEach4  = c.find('calc.items.forEach', chi_tiet_pos4)
noStt_in_detail = c.find("const noStt = ['perimeter','window','ceilPerim','elec','elecManual','noteItem']", item_forEach4)
if noStt_in_detail > 0 and noStt_in_detail < item_forEach4 + 15000:
    old_b4 = "const noStt = ['perimeter','window','ceilPerim','elec','elecManual','noteItem']"
    new_b4 = """// ── Thêm section header nếu là surface group mới (I. SÀN, II. TƯỜNG...)
    const grpE = SURF_GRP_EXCEL[item.surface];
    if (grpE && !seenSurfExcel.has(grpE.gid)) {
      seenSurfExcel.add(grpE.gid);
      const hdrSurf = blkDetail();
      hdrSurf[1] = `${romanNums[excelSubRomIdx++] || excelSubRomIdx}. ${grpE.label}`;
      aoa.push(hdrSurf);
      merges.push({ s: { r: curRow, c: 1 }, e: { r: curRow, c: 9 } });
      curRow++;
    }
    const noStt = ['perimeter','window','ceilPerim','elec','elecManual','noteItem']"""
    c = c.replace(old_b4, new_b4, 1)
    print("✓ B4: SURF_GRP section headers added to Excel CHI TIẾT forEach")
    changes += 1
else:
    print(f"✗ B4: noStt anchor not found (pos={noStt_in_detail})")
    # Debug
    idx_debug = c.find("const noStt", item_forEach4)
    print(f"  'const noStt' at: {idx_debug}, context: {repr(c[idx_debug:idx_debug+100]) if idx_debug > 0 else 'N/A'}")

# ═══════════════════════════════════════════════════════════════
# VERIFY
# ═══════════════════════════════════════════════════════════════
with open('app.js', 'w', encoding='utf-8') as f:
    f.write(c)

print(f"\n✅ Total {changes} changes applied")
print("\nVerification - searching for remaining emoji in Excel/BOQ code:")
for emoji_kw in ['⚡ THIẾT', '📝 CHI TIẾT', '🟫 ', '🟦 ', '⬜ ', '🪟 ', '📐 ', '📋 ']:
    if emoji_kw in c:
        idx_v = c.find(emoji_kw)
        line_s = c.rfind('\n', 0, idx_v) + 1
        line_e = c.find('\n', idx_v)
        print(f"  STILL HAS '{emoji_kw}': {c[line_s:line_e].strip()[:100]}")
