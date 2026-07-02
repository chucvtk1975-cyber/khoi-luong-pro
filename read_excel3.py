import openpyxl, sys, json
sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('FILE MẪU.xlsx')
ws = list(wb)[0]

out = {
    'sheet': ws.title,
    'merges': [str(m) for m in ws.merged_cells.ranges],
    'col_widths': {},
    'header_bg': {}
}

for col_letter, col_dim in ws.column_dimensions.items():
    if col_dim.width:
        out['col_widths'][col_letter] = round(col_dim.width, 2)

# Đọc màu bg các row header (9, 10, 11) và title (1,2,3)
for r in [1, 2, 3, 9, 10, 11, 12, 27, 28, 29, 30]:
    out['header_bg'][str(r)] = {}
    for c in range(1, 11):
        cell = ws.cell(row=r, column=c)
        try:
            fg = cell.fill.fgColor
            if fg.type == 'rgb':
                bg = str(fg.rgb)
            elif fg.type == 'theme':
                bg = 'theme:' + str(fg.theme) + ':' + str(fg.tint)
            else:
                bg = 'none'
        except Exception as e:
            bg = str(e)[:30]
        
        try:
            font_color = str(cell.font.color.rgb) if cell.font and cell.font.color and cell.font.color.type == 'rgb' else None
        except:
            font_color = None

        out['header_bg'][str(r)][str(c)] = {
            'v': str(cell.value)[:30] if cell.value else None,
            'bg': bg,
            'bold': bool(cell.font.bold) if cell.font else False,
            'size': cell.font.size if cell.font else None,
            'fn': cell.font.name if cell.font else None,
            'fc': font_color,
            'ha': cell.alignment.horizontal if cell.alignment else None
        }

with open('colors_out.json', 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

print('Merges:', out['merges'])
print('Col widths:', out['col_widths'])
for r, cols in out['header_bg'].items():
    print(f'\n-- Row {r} --')
    for c, info in cols.items():
        if info['v'] or info['bg'] not in ('none', '00000000', '00FFFFFF'):
            print(f"  C{c}: v={info['v']} bg={info['bg']} bold={info['bold']} size={info['size']} fn={info['fn']} ha={info['ha']}")
