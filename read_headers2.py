import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app.js', 'r', encoding='utf-8') as f:
    c = f.read()

# Tim tat ca cac loai header ben trong forEach phong
idx = c.find('boq-room-header')
chunk = c[idx:idx+15000]
lines = chunk.split('\n')
real_lines = [l for l in lines if l.strip()]

# Chỉ in các dong co class boq- hoac innerHTML
key_lines = []
for l in real_lines:
    if any(x in l for x in ['boq-', 'Header', 'header', 'THIẾT BỊ', 'CHI PHÍ', 'surface', 'stt =', 'roman', 'subRoman', 'data-kr', 'html +=']):
        key_lines.append(l[:200])

print('\n'.join(key_lines[:200]))
