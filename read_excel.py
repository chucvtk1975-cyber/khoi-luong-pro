import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app.js', 'r', encoding='utf-8') as f:
    c = f.read()

# Doc ham exportExcel - 12000 ky tu
idx = c.find('function exportExcel()')
chunk = c[idx:idx+12000]
lines = [l.strip() for l in chunk.split('\n') if l.strip()]

print("=== exportExcel function ===")
for l in lines[:150]:
    print(l[:130])
