import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app.js', 'r', encoding='utf-8') as f:
    c = f.read()

# Tim ham export Excel
for kw in ['exportExcel', 'export_excel', 'writeXlsx', 'XLSX', 'ExcelJS', 'xlsx', 
           'CỘNG', 'noteHeader', 'note-woodwork', 'noteItem', 'ghi chú', 'Ghi chú',
           'THIẾT BỊ', 'note-']:
    idx = c.find(kw)
    if idx > 0:
        line_s = c.rfind('\n', 0, idx) + 1
        line_e = c.find('\n', idx)
        line = c[line_s:line_e].strip()
        print(f"[{idx}] '{kw}': {line[:120]}")
