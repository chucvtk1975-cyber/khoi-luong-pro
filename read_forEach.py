import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app.js', 'r', encoding='utf-8') as f:
    c = f.read()

# Doc vung render chi tiet tu ng phong - tim vung co boq-room-header
start = c.find('boq-room-header')
# Tim function chua no
func_start = c.rfind('\n  rooms.forEach', 0, start)
if func_start < 0:
    func_start = c.rfind('\nrooms.forEach', 0, start)
print(f'forEach loop starts at: {func_start}')

chunk = c[func_start:func_start+12000]
lines = chunk.split('\n')
real_lines = [l for l in lines if l.strip()]
print('\n'.join(real_lines[:300]))
