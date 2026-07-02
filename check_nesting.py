import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Kiem tra: nut co nam NGOAI modal-card khong?
start = c.find('modal-overlay" id="modal-room"')
start = c.rfind('<div', 0, start+10)
chunk = c[start:start+2500]
lines = [l.strip() for l in chunk.split('\n') if l.strip()]

depth = 0
for l in lines[:50]:
    if l.startswith('<div'): depth += 1
    elif l.startswith('</div>'): depth -= 1
    print(f"{'  '*depth}{l[:110]}")
    if l.startswith('</div>'): pass
