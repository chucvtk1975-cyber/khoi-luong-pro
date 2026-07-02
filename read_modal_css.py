import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('style.css', 'r', encoding='utf-8') as f:
    c = f.read()

for kw in ['modal-card', 'modal-overlay', 'modal-room-card', 'modal-body', 'modal-header', 'modal-footer', 'max-height', 'overflow']:
    idx = c.find(kw)
    while idx >= 0:
        line_start = c.rfind('\n', 0, idx)+1
        # lay 10 dong
        end = idx
        for _ in range(12):
            end = c.find('\n', end+1)
            if end < 0: break
        block = c[line_start:end]
        if '{' in block or ':' in block:
            print(f'=== {kw} at {idx} ===')
            print('\n'.join([l for l in block.split('\n') if l.strip()][:10]))
            print()
        idx = c.find(kw, idx+1)
