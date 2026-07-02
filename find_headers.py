import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app.js', 'r', encoding='utf-8') as f:
    c = f.read()

# Tim cac doan render section header lon: room-header, surface header
searches = [
    'boq-room-header',
    'boq-surface-hdr',
    'boq-surface-header',
    'CHI PHÍ KHÁC',
    'boq-room-oc-hdr',
    'boq-other-header',
    'renderBOQ',
    'renderRoom',
    'surfaceLabel',
]

for s in searches:
    idx = c.find(s)
    if idx >= 0:
        print(f'\n=== "{s}" at {idx} ===')
        print(c[idx-80:idx+200])
    else:
        print(f'\n=== "{s}" NOT FOUND ===')
