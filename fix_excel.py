import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app.js', 'r', encoding='utf-8') as f:
    c = f.read()

changes = 0

# ═══════════════════════════════════════════════════════
# FIX 1: Bỏ emoji khỏi group headers trong CHI TIẾT sheet
# ═══════════════════════════════════════════════════════
replacements_simple = [
    ("hdr[1] = '⚡ THIẾT BỊ ĐIỆN';",    "hdr[1] = 'THIẾT BỊ ĐIỆN';"),
    ("hdr[1] = '📝 CHI TIẾT TỪ GHI CHÚ';", "hdr[1] = 'CHI TIẾT TỪ GHI CHÚ';"),
]
for old, new in replacements_simple:
    if old in c:
        c = c.replace(old, new, 1)
        print(f"✓ Fixed: {old[:50]} → {new[:50]}")
        changes += 1
    else:
        print(f"✗ NOT FOUND: {old[:60]}")

# ═══════════════════════════════════════════════════════
# FIX 2: Bỏ emoji khỏi GROUP_LABEL trong VẬT TƯ sheet
# ═══════════════════════════════════════════════════════
old_group = """const GROUP_LABEL = {
floor:      '🟫 SÀN',
wall:       '🟦 TƯỜNG SƠN NƯỚC',
ceiling:    '⬜ TRẦN SƠN NƯỚC',
perimeter:  '📐 CHU VI / ĐỊA ĐẲNG',
ceilPerim:  '📐 CHU VI TRẦN',
window:     '🪟 CỬA',
ceilMat:    '🔳 ỐP TRẦN VẬT LIỆU',
floorMat:   '🔲 ỐP SÀN VẬT LIỆU',
wallMat:    '🔵 ỐP TƯỜNG VẬT LIỆU',
elec:       '⚡ THIẾT BỊ ĐIỆN',
elecManual: '⚡ THIẾT BỊ ĐIỆN',
noteItem:   '📝 VẬT TƯ KHÁC',
};"""

new_group = """const GROUP_LABEL = {
floor:      'SÀN',
wall:       'TƯỜNG SƠN NƯỚC',
ceiling:    'TRẦN SƠN NƯỚC',
perimeter:  'CHU VI / ĐỊA ĐẲNG',
ceilPerim:  'CHU VI TRẦN',
window:     'CỬA',
ceilMat:    'ỐP TRẦN VẬT LIỆU',
floorMat:   'ỐP SÀN VẬT LIỆU',
wallMat:    'ỐP TƯỜNG VẬT LIỆU',
elec:       'THIẾT BỊ ĐIỆN',
elecManual: 'THIẾT BỊ ĐIỆN',
noteItem:   'VẬT TƯ KHÁC',
};"""

# Tim bang cach strip newlines (vi file co nhieu \r\n)
def find_flexible(text, pattern):
    """Tim pattern trong text, bo qua so luong newline"""
    import re
    # Tao regex tu pattern, escape cac ky tu dac biet, thay \n bang \s+
    escaped = re.escape(pattern)
    # Thay \\n trong escaped bang \s+ de match bat ky whitespace
    flex = escaped.replace('\\\n', r'\s+')
    m = re.search(flex, text)
    return m

m = find_flexible(c, 'floor:      ')
if m:
    # Tim doan GROUP_LABEL chinh xac
    start = c.rfind('const GROUP_LABEL', 0, m.start())
    end = c.find('};', m.start()) + 2
    if start > 0 and end > 2:
        old_actual = c[start:end]
        print(f"\nFound GROUP_LABEL at {start}:{end} ({len(old_actual)} chars)")
        print("First 200:", repr(old_actual[:200]))
        
        # Build new version: remove emoji characters
        import re
        # Remove emoji (Unicode ranges for emoji)
        def remove_emoji(s):
            emoji_pattern = re.compile("["
                u"\U0001F300-\U0001F9FF"  # misc symbols
                u"\U00002600-\U000027BF"  # misc symbols
                u"\U0001F000-\U0001F02F"  # mahjong
                u"\u26AA-\u26FF"
                u"\u2700-\u27BF"          # dingbats
                "]+", flags=re.UNICODE)
            return emoji_pattern.sub('', s).replace('  ', ' ').strip()
        
        # Replace line by line
        new_actual = old_actual
        emoji_map = {
            '🟫 ': '', '🟦 ': '', '⬜ ': '', '📐 ': '',
            '🪟 ': '', '🔳 ': '', '🔲 ': '', '🔵 ': '',
            '⚡ ': '', '📝 ': '', '📋 ': '', '🛋️ ': '',
            '🚿 ': '', '🛡️ ': '',
        }
        for emoji, replacement in emoji_map.items():
            new_actual = new_actual.replace(emoji, replacement)
        
        if new_actual != old_actual:
            c = c[:start] + new_actual + c[end:]
            print("✓ GROUP_LABEL emojis removed")
            changes += 1
        else:
            print("✗ No emoji found in GROUP_LABEL section")
else:
    print("✗ GROUP_LABEL not found via flexible search")

# ═══════════════════════════════════════════════════════
# FIX 3: Nội dung ghi chú → liệt kê từng hạng mục
# ═══════════════════════════════════════════════════════
# Tim doan hien tai
note_section_marker = '// ── Ghi chú Mộc / Nước / Chống thấm'
note_end_marker = '// ── Cộng phòng + VAT + Tổng + Bằng chữ'

ns_start = c.find(note_section_marker)
ns_end = c.find(note_end_marker, ns_start)

if ns_start > 0 and ns_end > ns_start:
    old_note_section = c[ns_start:ns_end]
    print(f"\nFound note section at {ns_start}:{ns_end}")
    print("Old section:", repr(old_note_section[:300]))
    
    new_note_section = """// ── Ghi chú Mộc / Nước / Chống thấm → mỗi dòng = 1 hạng mục
[
  { text: room.noteWoodwork,   label: 'THIẾT BỊ NỘI THẤT' },
  { text: room.notePlumbing,   label: 'PHẦN NƯỚC' },
  { text: room.noteWaterproof, label: 'CHỐNG THẤM' },
].forEach(({ text, label }) => {
  if (!text || !text.trim()) return;
  // Dòng tiêu đề section
  const hdrN = blkDetail();
  hdrN[1] = label;
  aoa.push(hdrN);
  merges.push({ s: { r: curRow, c: 1 }, e: { r: curRow, c: 9 } });
  curRow++;
  // Mỗi dòng textarea → 1 hàng riêng
  const noteLines = text.split('\\n').map(l => l.trim()).filter(l => l);
  noteLines.forEach((line, li) => {
    const lr = blkDetail();
    lr[0] = li + 1;   // STT
    lr[1] = line;     // Nội dung
    aoa.push(lr);
    merges.push({ s: { r: curRow, c: 1 }, e: { r: curRow, c: 9 } });
    curRow++;
  });
});
"""
    c = c[:ns_start] + new_note_section + c[ns_end:]
    print("✓ Note sections restructured (each line = 1 row)")
    changes += 1
else:
    print(f"✗ Note section markers not found. ns_start={ns_start}, ns_end={ns_end}")
    # Debug
    idx = c.find('Ghi chú Mộc')
    print(f"  'Ghi chú Mộc' at: {idx}")
    idx2 = c.find('noteWoodwork')
    print(f"  'noteWoodwork' at: {idx2}, context: {repr(c[idx2:idx2+100]) if idx2 > 0 else 'N/A'}")

# ═══════════════════════════════════════════════════════
# FIX 4: Bỏ emoji khỏi GROUP_LABEL fallback '📋 KHÁC'
# ═══════════════════════════════════════════════════════
c = c.replace("'📋 KHÁC'", "'KHÁC'")
c = c.replace('"📋 KHÁC"', '"KHÁC"')
c = c.replace('`📋 KHÁC`', '`KHÁC`')
print("✓ Removed 📋 KHÁC → KHÁC")
changes += 1

# Save
with open('app.js', 'w', encoding='utf-8') as f:
    f.write(c)

print(f"\n✅ Done! {changes} changes applied to app.js")
