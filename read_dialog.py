import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app.js', 'r', encoding='utf-8') as f:
    c = f.read()

# Tim tat ca vi tri co "openAddItemDialog" - ca call lan khai bao
pos = 0
results = []
while True:
    idx = c.find('openAddItemDialog', pos)
    if idx < 0:
        break
    # Lay 1 dong chua no
    line_start = c.rfind('\n', 0, idx) + 1
    line_end = c.find('\n', idx)
    line = c[line_start:line_end].strip()
    results.append((idx, line[:120]))
    pos = idx + 1

print(f'Total occurrences: {len(results)}\n')
for char_pos, line in results:
    print(f'  [{char_pos}] {line}')

# Doc noi dung ham openAddItemDialog
start = c.find('function openAddItemDialog(')
print(f'\n\n=== FUNCTION BODY (first 3000 chars) at {start} ===')
chunk = c[start:start+3000]
lines = chunk.split('\n')
real = [l for l in lines if l.strip()]
print('\n'.join(real[:60]))
