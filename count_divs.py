import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Tim toan bo modal-room tu dau den cuoi
modal_start = c.find('<div class="modal-overlay" id="modal-room">')
modal_end = c.find('<!-- ========== APP CHÍNH', modal_start)

modal_chunk = c[modal_start:modal_end]
lines = [l for l in modal_chunk.split('\n') if l.strip()]

# Dem div open/close de kiem tra
depth = 0
for i, l in enumerate(lines):
    opens = l.count('<div')
    closes = l.count('</div>')
    depth += opens - closes
    if opens or closes:
        marker = '⚠️' if depth < 0 else ''
        print(f"{depth:+2d} | {marker} {l[:100]}")
