import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app.js', 'r', encoding='utf-8') as f:
    c = f.read()

# Verify cac thay doi da duoc ap dung
checks = [
    ("subRomIdx = 1", "subRomIdx initialized"),
    ("subRomIdx++] || subRomIdx}. ⚡ THIẾT BỊ ĐIỆN", "elecHeader Roman"),
    ("subRomIdx++] || subRomIdx}. 📝 CHI TIẾT", "noteHeader Roman"),
    ("subRom = romanNums[subRomIdx++]", "subHeader Roman"),
    ("subRomIdx++] || subRomIdx}. 💰 CHI PHÍ", "OC header Roman"),
    ("subRom}. ${ci.label}", "subHeader label with Roman"),
]

for pattern, name in checks:
    found = pattern in c
    print(f"{'✓' if found else '✗'} {name}: {pattern[:50]}")

# Tim surface group headers - cac kieu header the hien nhom
print("\n\nSurface group headers in renderBOQ:")
# Tim cac pattern dang "THIẾT BỊ" hay surface names
idx = c.find('boq-room-header')
chunk = c[idx:idx+20000]
for keyword in ['NỘI THẤT', 'ĐIỆN', 'PLUMBING', 'VỆ SINH', 'TRẦN', 'TƯỜNG', 'SÀN', 'CỬA', 'surface header', 'surfaceGroupHdr']:
    ki = chunk.find(keyword)
    if ki >= 0:
        print(f"  {keyword} at +{ki}: {repr(chunk[ki-30:ki+80])}")
