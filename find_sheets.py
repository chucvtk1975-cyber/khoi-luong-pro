import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app.js', 'r', encoding='utf-8') as f:
    c = f.read()

excel_start = c.find('function exportExcel()')
excel_chunk = c[excel_start:excel_start+50000]

# Tim tat ca SHEET markers va cac ham book_append_sheet
for kw in ['SHEET', 'book_append', 'appendSheet', 'addSheet', 'CHI TIẾT', 'CHI TIET',
           'room.name', 'rooms.forEach', 'noteWoodwork', 'notePlumbing', 'noteWaterproof',
           'note-woodwork', 'THIẾT BỊ NỘI THẤT', 'roomNote']:
    pos = 0
    count = 0
    while count < 5:
        found = excel_chunk.find(kw, pos)
        if found < 0: break
        line_s = excel_chunk.rfind('\n', 0, found) + 1
        line_e = excel_chunk.find('\n', found)
        line = excel_chunk[line_s:line_e].strip()
        print(f"  +{found:5d} [{kw}]: {line[:130]}")
        pos = found + 1
        count += 1
