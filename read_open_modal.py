import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app.js', 'r', encoding='utf-8') as f:
    c = f.read()

# Doc ham openRoomModal va closeRoomModal
start = c.find('function openRoomModal(')
chunk = c[start:start+3000]
lines = chunk.split('\n')
real = [l for l in lines if l.strip()]
print('=== openRoomModal ===')
print('\n'.join(real[:50]))

# Doc phan xu ly modal-room trong event listeners (682210)
start2 = c.find("['modal-project', 'modal-room']")
chunk2 = c[start2:start2+2000]
lines2 = chunk2.split('\n')
real2 = [l for l in lines2 if l.strip()]
print('\n\n=== modal click handler ===')
print('\n'.join(real2[:40]))
