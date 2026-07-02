import openpyxl, sys
sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('FILE MẪU.xlsx')
ws = list(wb)[0]
print('Sheet:', ws.title)
print('Merges:', [str(m) for m in ws.merged_cells.ranges])

for r in [1,2,3,5,6,7,9,10,11,30,31,32,33,34,35]:
    for c in range(1, 11):
        cell = ws.cell(row=r, column=c)
        try:
            bg = str(cell.fill.fgColor.rgb)
        except:
            bg = 'err'
        try:
            fc = str(cell.font.color.rgb) if cell.font and cell.font.color else None
        except:
            fc = None
        v = repr(cell.value)[:40] if cell.value else '-'
        bold = bool(cell.font.bold) if cell.font else False
        fs = cell.font.size if cell.font else None
        ha = cell.alignment.horizontal if cell.alignment else None
        print(f'R{r}C{c}({cell.coordinate}): v={v} bg={bg} fc={fc} bold={bold} size={fs} ha={ha}')
    print('---')
