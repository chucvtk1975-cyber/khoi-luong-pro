import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app.js', 'r', encoding='utf-8') as f:
    c = f.read()

# Doc 2000 ky tu sau vi tri 585627 (forEach end)
print("=== After forEach ends (585627 → 589000) ===")
chunk = c[585627:589000]
lines = [l.strip() for l in chunk.split('\n') if l.strip()]
for l in lines[:60]:
    print(l[:130])

# Tim cac unique strings de anchor
print("\n\n=== Unique strings to anchor insertion ===")
for kw in ['roomTotal', 'TỔNG TIỀN', 'Tổng tiền', 'totalRow', 'totalDetail',
           'book_append_sheet', 'wsDetail', 'room.name.toUpperCase',
           'wsDe', 'appendSheet']:
    idx = c.find(kw, 585000)
    if idx > 0 and idx < 595000:
        line_s = c.rfind('\n', 0, idx) + 1
        line_e = c.find('\n', idx)
        print(f"  [{idx}] {kw}: {c[line_s:line_e].strip()[:120]}")
