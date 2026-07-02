import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app.js', 'r', encoding='utf-8') as f:
    c = f.read()

# Tim tat ca cho co vatRate
pos = 0
results = []
while True:
    idx = c.find('vatRate', pos)
    if idx < 0:
        break
    line_start = c.rfind('\n', 0, idx) + 1
    line_end = c.find('\n', idx)
    line = c[line_start:line_end].strip()
    results.append((idx, line[:180]))
    pos = idx + 1

print(f'Total "vatRate" occurrences: {len(results)}\n')
for char_pos, line in results:
    print(f'  [{char_pos}] {line}')
