import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('style.css', 'r', encoding='utf-8') as f:
    c = f.read()

# Tim .modal-overlay.active
idx = c.find('modal-overlay.active')
if idx < 0:
    idx = c.find('.active')
    while idx >= 0:
        if 'modal' in c[max(0,idx-30):idx]:
            print(f"modal active at {idx}: {c[idx-30:idx+100]}")
        idx = c.find('.active', idx+1)
