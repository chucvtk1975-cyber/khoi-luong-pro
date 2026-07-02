import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('app.js', 'r', encoding='utf-8') as f:
    c = f.read()

changes = 0

# ═══════════════════════════════════════════════════════════════
# FIX 1: Web BOQ - revert subRomIdx từ 0 → 1
# (⚡ ĐIỆN cần là "II." không phải "I." như screenshot)
# ═══════════════════════════════════════════════════════════════
old_sub0 = 'let subRomIdx = 0; // sub-section Roman counter (0-indexed)'
new_sub1 = 'let subRomIdx = 1; // sub-section Roman counter (1-indexed, I=construction, II=elec)'
if old_sub0 in c:
    c = c.replace(old_sub0, new_sub1, 1)
    print("✓ Fix 1: subRomIdx 0 → 1 (elecHeader will show II.)")
    changes += 1
else:
    # Tim bat ky dang nao cua subRomIdx declaration
    idx = c.find('let subRomIdx = ')
    print(f"✗ Fix 1: Pattern not found. Current: {repr(c[idx:idx+80]) if idx>0 else 'N/A'}")

# ═══════════════════════════════════════════════════════════════
# FIX 2: Web BOQ - Xóa SURF_GRP block và seenSurfGrp
# ═══════════════════════════════════════════════════════════════
# Tim va xoa doan: const SURF_GRP = {...}; const seenSurfGrp = new Set();
# No nam ngay sau subRomIdx declaration
surf_grp_start = c.find('// Map surface → group id + label cho section headers')
surf_grp_end_marker = 'const seenSurfGrp = new Set(); // group ids da hien header'
surf_grp_end = c.find(surf_grp_end_marker)
if surf_grp_start > 0 and surf_grp_end > 0:
    # Include the marker line
    surf_grp_end_full = c.find('\n', surf_grp_end) + 1
    removed = c[surf_grp_start:surf_grp_end_full]
    c = c[:surf_grp_start] + c[surf_grp_end_full:]
    print(f"✓ Fix 2: SURF_GRP block removed ({len(removed)} chars)")
    changes += 1
else:
    print(f"✗ Fix 2: SURF_GRP block not found (start={surf_grp_start}, end={surf_grp_end})")

# ═══════════════════════════════════════════════════════════════
# FIX 3: Web BOQ - Xóa section header generation block
# (đoạn if(grp && !seenSurfGrp...) chèn I.SÀN, II.TƯỜNG rows)
# ═══════════════════════════════════════════════════════════════
surf_detect_start = c.find('// --- Section header cho standard surface groups (I. SAN, II. TUONG...) ---')
surf_detect_end_marker = '// --- Regular items ---'
surf_detect_end = c.find(surf_detect_end_marker, surf_detect_start if surf_detect_start > 0 else 0)

if surf_detect_start > 0 and surf_detect_end > surf_detect_start:
    removed2 = c[surf_detect_start:surf_detect_end]
    c = c[:surf_detect_start] + c[surf_detect_end:]
    print(f"✓ Fix 3: Surface section header detection removed ({len(removed2)} chars)")
    changes += 1
else:
    print(f"✗ Fix 3: Section detection block not found (start={surf_detect_start})")

# ═══════════════════════════════════════════════════════════════
# FIX 4: Excel CHI TIẾT - Thay SURF_GRP_EXCEL (với excelSubRomIdx=0)
# bằng chỉ "let excelSubRomIdx = 1;"
# ═══════════════════════════════════════════════════════════════
excel_surf_start = c.find('// ── Roman numeral section headers (đồng bộ web preview)')
excel_surf_end_marker = '  };\n'  # ends with SURF_GRP_EXCEL closing brace
if excel_surf_start > 0:
    # Tim ket thuc cua SURF_GRP_EXCEL block
    # No ket thuc sau "};" cua SURF_GRP_EXCEL
    excel_surf_end_approx = c.find('};', excel_surf_start) + 2
    # Tim ky tu newline tiep theo
    excel_surf_end_approx = c.find('\n', excel_surf_end_approx) + 1
    
    old_excel_surf_block = c[excel_surf_start:excel_surf_end_approx]
    print(f"\nExcel SURF block ({len(old_excel_surf_block)} chars): {repr(old_excel_surf_block[:200])}")
    
    # Thay bang chi khai bao excelSubRomIdx = 1
    new_excel_surf = '  let excelSubRomIdx = 1; // II. THIẾT BỊ ĐIỆN\n'
    c = c[:excel_surf_start] + new_excel_surf + c[excel_surf_end_approx:]
    print("✓ Fix 4: SURF_GRP_EXCEL replaced with excelSubRomIdx = 1")
    changes += 1
else:
    print("✗ Fix 4: Excel SURF_GRP block not found")

# ═══════════════════════════════════════════════════════════════
# FIX 5: Excel CHI TIẾT - Xóa SURF_GRP detection trước "const noStt"
# ═══════════════════════════════════════════════════════════════
excel_grp_detect = c.find('// ── Thêm section header nếu là surface group mới (I. SÀN, II. TƯỜNG...)')
excel_grp_end_marker = 'const noStt = [\'perimeter\',\'window\',\'ceilPerim\',\'elec\',\'elecManual\',\'noteItem\']'
excel_grp_end = c.find(excel_grp_end_marker, excel_grp_detect if excel_grp_detect > 0 else 0)

if excel_grp_detect > 0 and excel_grp_end > excel_grp_detect:
    removed3 = c[excel_grp_detect:excel_grp_end]
    c = c[:excel_grp_detect] + c[excel_grp_end:]
    print(f"✓ Fix 5: Excel SURF_GRP detection removed ({len(removed3)} chars)")
    changes += 1
else:
    print(f"✗ Fix 5: Excel detection block not found (detect={excel_grp_detect}, end={excel_grp_end})")

# Save
with open('app.js', 'w', encoding='utf-8') as f:
    f.write(c)

print(f"\n✅ {changes} changes applied")
print("\nVerify: elecHeader in Excel:")
idx_v = c.find("romanNums[excelSubRomIdx++]")
if idx_v > 0:
    print(f"  {c[idx_v:idx_v+80]}")
print("\nVerify: subRomIdx in renderBOQ:")
idx_v2 = c.find("let subRomIdx = ")
if idx_v2 > 0:
    print(f"  {c[idx_v2:idx_v2+80]}")
