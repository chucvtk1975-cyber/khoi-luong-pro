import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app.js', 'r', encoding='utf-8') as f:
    c = f.read()

# Tim surface label rendering trong vong lap items
# Tim "surfaceLabel" hoac "THIẾT BỊ NỘI THẤT" hoac "surface" group headers
idx = c.find('boq-room-header')
chunk = c[idx:idx+20000]
lines = chunk.split('\n')
real = [l for l in lines if l.strip()]

# In tat ca dong co "surface" de hieu cu phap
surface_lines = []
for i, l in enumerate(real):
    if 'surface' in l.lower() or 'label' in l.lower() or 'group' in l.lower() or 'hdr' in l.lower() or '🪣' in l or '🔧' in l or '🪟' in l:
        surface_lines.append(f'[{i}] {l[:200]}')

print('\n'.join(surface_lines[:100]))
