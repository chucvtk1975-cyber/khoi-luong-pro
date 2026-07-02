import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app.js', 'r', encoding='utf-8') as f:
    c = f.read()

# Tim surface header rendering
searches = ['surfaceHdr', 'surface-hdr', 'PHÒNG SIÊU ÂM', 'NỘI THẤT', 'VỆ SINH', 
            'boq-group-header', 'boq-grp', 'groupHeader', 'sectionHdr',
            'KÍCH THƯỚC BỀ MẶT', 'BỀ MẶT', '💰 CHI PHÍ KHÁC —']

for s in searches:
    idx = c.find(s)
    if idx >= 0:
        print(f'\n=== "{s}" at {idx} ===')
        chunk = c[idx:idx+300]
        lines = chunk.split('\n')
        print('\n'.join([l for l in lines if l.strip()][:10]))

# Tim phan oc header cua phong
idx2 = c.find('boq-room-oc-hdr')
chunk2 = c[idx2:idx2+1500]
print('\n\n=== boq-room-oc-hdr rendering ===')
lines2 = chunk2.split('\n')
print('\n'.join([l for l in lines2 if l.strip()][:30]))
