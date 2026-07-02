import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app.js', 'r', encoding='utf-8') as f:
    c = f.read()

# Tim filterBOQByRoom
idx = c.find('filterBOQByRoom')
print('filterBOQByRoom at:', idx)
if idx > 0:
    # In 3000 chars xung quanh
    start = max(0, idx - 100)
    print(c[start:start+3000])
