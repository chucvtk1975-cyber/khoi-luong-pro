import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app.js', 'r', encoding='utf-8') as f:
    c = f.read()

# Tim phan xu ly noteHeader va noteItem trong exportExcel
idx = c.find('function exportExcel()')
excel_chunk = c[idx:idx+40000]  # Lay 40000 ky tu

# Tim trong excel_chunk cac references den note
for kw in ['noteHeader', 'noteItem', 'note-woodwork', 'CHI TIET TU GHI CHU', 
           'CỘNG', 'emoji', 'symbol', 'label.replace', 'toUpperCase',
           'elecHeader', 'surface ==']:
    pos = 0
    while True:
        found = excel_chunk.find(kw, pos)
        if found < 0: break
        line_s = excel_chunk.rfind('\n', 0, found) + 1
        line_e = excel_chunk.find('\n', found)
        line = excel_chunk[line_s:line_e].strip()
        print(f"  +{found:5d} [{kw}]: {line[:130]}")
        pos = found + 1
