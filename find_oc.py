import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app.js', 'r', encoding='utf-8') as f:
    c = f.read()

# Tim doan "boq-other-header" va "boq-other-item" - la project-level OC
idx = c.find('boq-other-header')
print('boq-other-header occurrences:')
pos = 0
while True:
    idx = c.find('boq-other-header', pos)
    if idx == -1:
        break
    print(f'  At {idx}: ...{repr(c[idx-50:idx+100])}...')
    pos = idx + 1

print('\n\nSearching for per-room OC header:')
idx2 = c.find('boq-room-oc-hdr')
pos2 = 0
while True:
    idx2 = c.find('boq-room-oc-hdr', pos2)
    if idx2 == -1:
        break
    print(f'  At {idx2}: ...{repr(c[idx2-50:idx2+150])}...')
    pos2 = idx2 + 1

print('\n\nSearching filterBOQByRoom else branch (room != all):')
idx3 = c.find('} else {')
pos3 = c.find('filterBOQByRoom')
# Find else after filterBOQByRoom
chunk = c[pos3:pos3+5000]
else_pos = chunk.find('} else {')
if else_pos > 0:
    print(chunk[else_pos:else_pos+2000])
