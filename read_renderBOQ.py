import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app.js', 'r', encoding='utf-8') as f:
    c = f.read()

# Doc vung render BOQ - tu renderBOQ function
start = c.find('function renderBOQ(')
if start < 0:
    start = c.find('renderBOQ = function')
print(f'renderBOQ starts at: {start}')

# Doc 8000 chars
chunk = c[start:start+8000]
# Loc chi cac dong co noi dung thuc (khong phai dong trong)
lines = chunk.split('\n')
real_lines = [l for l in lines if l.strip()]
print('\n'.join(real_lines[:200]))
