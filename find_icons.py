import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app.js', 'r', encoding='utf-8') as f:
    c = f.read()

# Tim tat ca cho co ↑↓ hoac U/D trong nut move
searches = ['&#8593;', '&#8595;', '↑', '↓', 
            'btn-move', 'moveBoqRow', 'boq-move-up', 'boq-move-dn',
            '"U"', '"D"', "'U'", "'D'"]

for s in searches:
    idx = c.find(s)
    if idx >= 0:
        line_start = c.rfind('\n', 0, idx) + 1
        line_end = c.find('\n', idx)
        line = c[line_start:line_end].strip()
        print(f'[{idx}] "{s}": {line[:150]}')
    else:
        print(f'NOT FOUND: "{s}"')
