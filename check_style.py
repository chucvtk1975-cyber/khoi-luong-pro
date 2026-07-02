import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app.js', 'r', encoding='utf-8') as f:
    c = f.read()

# Tim applySheetStyles va xem no hoat dong nhu nao
idx = c.find('function applySheetStyles')
print(f"applySheetStyles at: {idx}")
if idx > 0:
    chunk = c[idx:idx+3000]
    lines = [l.strip() for l in chunk.split('\n') if l.strip()]
    for l in lines[:50]:
        print(l[:130])

# Tim where Excel CHI TIẾT room header and elecHeader are STYLED
chi_tiet = c.find('BẢNG CHI TIẾT KHỐI LƯỢNG')
idx2 = c.find('applySheetStyles', chi_tiet)
print(f"\n\napplySheetStyles call in CHI TIẾT at: {idx2}")
if idx2 > 0:
    line_s = c.rfind('\n', 0, idx2) + 1
    line_e = c.find('\n', idx2)
    print(c[line_s:line_e].strip())
