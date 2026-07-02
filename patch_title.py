import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app.js', 'r', encoding='utf-8') as f:
    c = f.read()

# Đổi size tiêu đề lớn từ 24 → 20
old = "font = { name: 'Times New Roman', sz: 24, bold: true, color: { rgb: '000000' } };"
new = "font = { name: 'Times New Roman', sz: 20, bold: true, color: { rgb: '000000' } };"

if old in c:
    c = c.replace(old, new, 1)
    print("✓ Title font size changed: 24 → 20pt")
else:
    print("✗ Not found, searching...")
    idx = c.find("sz: 24")
    print("sz: 24 at char:", idx)
    if idx > 0:
        print(repr(c[idx-80:idx+80]))

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(c)

print("Done.")
