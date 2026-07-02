import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app.js', 'r', encoding='utf-8') as f:
    c = f.read()

changes = 0

# Fix emoji trong BOQ note display (ep- print view)
emoji_content_map = [
    ('🛋️ <b>THIẾT BỊ NỘI THẤT', '<b>THIẾT BỊ NỘI THẤT'),
    ('🚿 <b>PHẦN NƯỚC',         '<b>PHẦN NƯỚC'),
    ('🛡️ <b>CHỐNG THẤM',       '<b>CHỐNG THẤM'),
    ('🛋️ THIẾT BỊ NỘI THẤT',   'THIẾT BỊ NỘI THẤT'),
    ('🚿 PHẦN NƯỚC',            'PHẦN NƯỚC'),
    ('🛡️ CHỐNG THẤM',          'CHỐNG THẤM'),
]

for old, new in emoji_content_map:
    count = c.count(old)
    if count > 0:
        c = c.replace(old, new)
        print(f"✓ Fixed {count}x: '{old[:30]}' → '{new[:30]}'")
        changes += count

# Verify content emoji gone
print("\n=== Remaining CONTENT emoji ===")
content_emojis = ['🛋️', '🚿', '🛡️', '⚡ THIẾT', '📝 CHI']
for kw in content_emojis:
    idx = c.find(kw)
    if idx > 0:
        line_s = c.rfind('\n', 0, idx) + 1
        line_e = c.find('\n', idx)
        print(f"  '{kw}': {c[line_s:line_e].strip()[:100]}")
    else:
        print(f"  '{kw}': ✓ CLEAN")

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(c)

print(f"\n✅ {changes} additional fixes applied")
