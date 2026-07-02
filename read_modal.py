import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Tim modal-room va lay toan bo noi dung
start = c.find('id="modal-room"')
start = c.rfind('<div', 0, start)  # lui ve div chua no
end = c.find('<!-- ========== APP CHÍNH', start)
chunk = c[start:end]
lines = chunk.split('\n')
real = [l for l in lines if l.strip()]
print(f'Modal room structure ({len(real)} lines):')
print('\n'.join(real[:80]))
