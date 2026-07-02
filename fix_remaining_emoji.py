import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app.js', 'r', encoding='utf-8') as f:
    c = f.read()

changes = 0

# Fix 1: label trong CALC.room push (dùng trong Excel Sheet 1 Tổng Hợp)
old1 = "label: '⚡ THIẾT BỊ ĐIỆN'"
new1 = "label: 'THIẾT BỊ ĐIỆN'"
count1 = c.count(old1)
c = c.replace(old1, new1)
print(f"✓ Fixed elecHeader label in CALC.room ({count1} occurrences): ⚡ removed")
changes += count1

# Fix 2: ep-note-hdr 📝
old2 = ">📝 CHI TIẾT TỪ GHI"
new2 = ">CHI TIẾT TỪ GHI"
count2 = c.count(old2)
c = c.replace(old2, new2)
print(f"✓ Fixed ep-note-hdr ({count2} occurrences): 📝 removed")
changes += count2

# Fix 3: Cũng fix ep-elec-hdr label label in CALC push nếu còn
old3 = "label: '⚡ ĐIỆN'"
new3 = "label: 'ĐIỆN'"
count3 = c.count(old3)
if count3 > 0:
    c = c.replace(old3, new3)
    print(f"✓ Fixed '⚡ ĐIỆN' ({count3} occurrences)")
    changes += count3

# Verify: kiem tra tat ca emoji con sot (ngoa tru UI labels)
print("\n=== Remaining emoji (review) ===")
for emoji_kw in ['⚡', '📝', '🟫', '🟦', '⬜', '🪟', '📐', '📋', '🛋️', '🚿', '🛡️']:
    idx = 0
    while True:
        found = c.find(emoji_kw, idx)
        if found < 0: break
        line_s = c.rfind('\n', 0, found) + 1
        line_e = c.find('\n', found)
        line = c[line_s:line_e].strip()
        print(f"  '{emoji_kw}' at {found}: {line[:100]}")
        idx = found + 1

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(c)

print(f"\n✅ {changes} more fixes applied")
