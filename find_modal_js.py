import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app.js', 'r', encoding='utf-8') as f:
    c = f.read()

# Tim tat ca JS lien quan den modal-room va modal-footer
searches = ['modal-footer', 'modal-room', 'btn-save-room', 'btn-cancel-room',
            'modal-room-card', 'openRoomModal', 'showRoomModal']

for s in searches:
    pos = 0
    while True:
        idx = c.find(s, pos)
        if idx < 0: break
        line_s = c.rfind('\n', 0, idx)+1
        line_e = c.find('\n', idx)
        line = c[line_s:line_e].strip()
        print(f'[{idx}] {s}: {line[:120]}')
        pos = idx + 1
