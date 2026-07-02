import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app.js', 'r', encoding='utf-8') as f:
    c = f.read()

# Tim tat ca nut move trong BOQ - ca custom lan non-custom
pos = 0
results = []
while True:
    idx = c.find('moveBoqRow', pos)
    if idx < 0:
        break
    line_start = c.rfind('\n', 0, idx) + 1
    line_end = c.find('\n', idx)
    line = c[line_start:line_end].strip()
    results.append((idx, line[:200]))
    pos = idx + 1

print(f'Total moveBoqRow occurrences: {len(results)}\n')
for char_pos, line in results:
    print(f'  [{char_pos}] {line}')

# Tim dong render non-custom item move buttons 
# (khong co ci.id - khong phai custom)
print('\n\n=== Looking for non-custom move buttons ===')
idx = c.find('boq-move-up')
while idx >= 0:
    ctx_start = max(0, idx - 200)
    ctx_end = min(len(c), idx + 300)
    ctx = c[ctx_start:ctx_end]
    lines = [l for l in ctx.split('\n') if l.strip()]
    print(f'\n--- at {idx} ---')
    print('\n'.join(lines[:10]))
    idx = c.find('boq-move-up', idx + 1)
