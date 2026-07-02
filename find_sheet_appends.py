import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app.js', 'r', encoding='utf-8') as f:
    c = f.read()

excel_start = c.find('function exportExcel()')
excel_chunk = c[excel_start:excel_start+60000]

# Tim tat ca book_append_sheet
print("=== All book_append_sheet calls ===")
pos = 0
while True:
    found = excel_chunk.find('book_append_sheet', pos)
    if found < 0: break
    line_s = excel_chunk.rfind('\n', 0, found) + 1
    line_e = excel_chunk.find('\n', found)
    print(f"  +{found:5d}: {excel_chunk[line_s:line_e].strip()[:120]}")
    pos = found + 1

# Doc tu vi tri 47000 - 60000 de xem phan cuoi cua exportExcel
print("\n=== End of exportExcel (excel +47000 to +60000) ===")
chunk_end = excel_chunk[47000:]
lines = [l.strip() for l in chunk_end.split('\n') if l.strip()]
for l in lines[:60]:
    print(l[:130])
