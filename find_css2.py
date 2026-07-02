import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('style.css', 'r', encoding='utf-8') as f:
    c = f.read()

idx = c.find('modal-footer')
while idx >= 0:
    print(f'--- at {idx}:')
    print(c[max(0,idx-100):idx+400])
    print()
    idx = c.find('modal-footer', idx+1)
