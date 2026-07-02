import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app.js', 'r', encoding='utf-8') as f:
    c = f.read()

# Doc ham updateOtherCost
start = c.find('function updateOtherCost(')
chunk = c[start:start+3000]
lines = chunk.split('\n')
real = [l for l in lines if l.strip()]
print('=== updateOtherCost ===')
print('\n'.join(real[:60]))

# So sanh cac OC_TEMPLATE / OC_PR / OC_T dinh nghia o cac noi
print('\n\n=== All OC_TEMPLATE / OC_PR / OC_T definitions ===')
for marker in ['OC_TEMPLATE', 'OC_PR', 'OC_T']:
    pos = 0
    while True:
        idx = c.find(marker, pos)
        if idx < 0:
            break
        line_start = c.rfind('\n', 0, idx) + 1
        line_end = c.find('\n', idx)
        line = c[line_start:line_end].strip()
        if '=' in line or ':' in line:
            print(f'[{idx}] {marker}: {line[:150]}')
        pos = idx + 1
