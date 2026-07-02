import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app.js', 'r', encoding='utf-8') as f:
    c = f.read()

# Tim phan Sheet 2 (chi tiet) trong exportExcel
idx = c.find('function exportExcel()')
excel_chunk = c[idx:idx+50000]

# Tim cac section quan trong
markers = [
    'SHEET 2', 'Sheet 2', 'CHI TIẾT', 'chi-tiet', 'boq',
    'noteWoodwork', 'THIẾT BỊ', 'PHẦN NƯỚC', 'CHỐNG THẤM', 
    'note_woodwork', 'woodwork', 'plumbing', 'waterproof',
    'CHI TIET', 'ghi_chu', 'label =', 'subLabel', 'section label',
    'CỘNG  ', 'CỘNG ', 'SÀN', '\\n', 'split'
]

results = []
for kw in markers:
    pos = 0
    while True:
        found = excel_chunk.find(kw, pos)
        if found < 0: break
        line_s = excel_chunk.rfind('\n', 0, found) + 1
        line_e = excel_chunk.find('\n', found)
        line = excel_chunk[line_s:line_e].strip()
        results.append((found, kw, line[:130]))
        pos = found + 1
        if pos > 45000: break

results.sort()
seen = set()
for pos, kw, line in results:
    if line not in seen and line:
        seen.add(line)
        print(f"  +{pos:5d} [{kw:15s}]: {line}")
