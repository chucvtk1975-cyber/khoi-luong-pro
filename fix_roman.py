import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app.js', 'r', encoding='utf-8') as f:
    c = f.read()

# === FIX 1: subRomIdx = 1 → 0 ===
old1 = 'let subRomIdx = 1; // sub-section Roman counter'
new1 = """let subRomIdx = 0; // sub-section Roman counter (0-indexed)
  // Map surface → group id + label cho section headers
  const SURF_GRP = {
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
  const seenSurfGrp = new Set(); // group ids da hien header"""

if old1 in c:
    c = c.replace(old1, new1, 1)
    print("✓ Fix 1: subRomIdx = 0 + SURF_GRP added")
else:
    print(f"✗ Fix 1 NOT found. Searching for partial...")
    idx = c.find('subRomIdx = 1')
    print(f"  Found at: {idx}, context: {repr(c[idx:idx+80])}")

# === FIX 2: Them section header cho standard surfaces ===
# Doan code ngay truoc "// --- Regular items ---"
old2 = '// --- Regular items ---'
new2 = """// --- Section header cho standard surface groups (I. SAN, II. TUONG...) ---
    const grp = SURF_GRP[item.surface];
    if (grp && !seenSurfGrp.has(grp.gid)) {
      seenSurfGrp.add(grp.gid);
      const romHdr = romanNums[subRomIdx++] || subRomIdx;
      html += `
<tr class="boq-surf-header" data-kr="${room.id}">
  <td></td>
  <td colspan="8" style="font-weight:700;padding:6px 10px;color:var(--brand-light);background:rgba(255,255,255,0.03);border-left:3px solid var(--brand);">${romHdr}. ${grp.label}</td>
  <td></td>
</tr>`;
    }
    // --- Regular items ---"""

if old2 in c:
    c = c.replace(old2, new2, 1)
    print("✓ Fix 2: Surface section headers added")
else:
    print("✗ Fix 2 NOT found")

# === FIX 3: Fix elecHeader + noteHeader dung subRomIdx (van dung, khong doi) ===
# Nhung can dam bao khong dung subRomIdx khi custom sub-header cung dung
# (elecHeader va noteHeader da co "subRomIdx++", van OK)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(c)

print("\n✅ app.js updated with Roman numeral section headers")
print("   Sections will show: I. SÀN → II. TƯỜNG → III. TRẦN → IV. CỬA ĐI → V. CỬA SỔ")
print("   Then elecHeader and noteHeader continue the numbering")
