import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app.js', 'r', encoding='utf-8') as f:
    c = f.read()

# Tim tat ca khai bao openAddItemDialog
pos = 0
count = 0
while True:
    idx = c.find('openAddItemDialog', pos)
    if idx < 0:
        break
    # Lay 3 dong truoc va 5 dong sau
    start = c.rfind('\n', 0, idx)
    end_idx = idx
    for _ in range(5):
        end_idx = c.find('\n', end_idx + 1)
        if end_idx < 0:
            break
    snippet = c[start:end_idx]
    lines = [l for l in snippet.split('\n') if l.strip()]
    if 'function' in snippet or '= function' in snippet or '=>' in snippet[:100]:
        count += 1
        print(f'\n=== DECLARATION #{count} at char {idx} ===')
        print('\n'.join(lines[:8]))
    pos = idx + 1

print(f'\nTotal declarations found: {count}')
