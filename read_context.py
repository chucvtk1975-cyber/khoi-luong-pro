import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app.js', 'r', encoding='utf-8') as f:
    c = f.read()

# Tim tat ca cac khu vuc xung quanh boq-room-header
idx = c.find('boq-room-header')
# In 5000 chars truoc va sau
chunk = c[idx-2000:idx+6000]
lines = chunk.split('\n')
real_lines = [l for l in lines if l.strip()]
print('\n'.join(real_lines[:250]))
