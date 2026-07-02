import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app.js', 'r', encoding='utf-8') as f:
    c = f.read()

excel_start = c.find('function exportExcel()')
# Tim doan per-room sheet (BẢNG CHI TIẾT KHỐI LƯỢNG)
chi_tiet_pos = c.find('BẢNG CHI TIẾT KHỐI LƯỢNG', excel_start)
print(f"CHI TIẾT sheet starts at: {chi_tiet_pos}")

# Doc 8000 ky tu tu day
chunk = c[chi_tiet_pos:chi_tiet_pos+8000]
lines = [l.strip() for l in chunk.split('\n') if l.strip()]
print("\n=== Per-room CHI TIẾT sheet code ===")
for l in lines[:120]:
    print(l[:130])
