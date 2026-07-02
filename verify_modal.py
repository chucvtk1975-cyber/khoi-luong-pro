import sys
sys.stdout.reconfigure(encoding='utf-8')

# Check 1: Verify HTML structure of modal-room
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

modal_start = html.find('id="modal-room"')
chunk = html[modal_start:modal_start+1500]
lines = [l for l in chunk.split('\n') if l.strip()]
print("=== modal-room HTML structure ===")
print('\n'.join(lines[:25]))

# Check 2: Mobile media query for modal
with open('style.css', 'r', encoding='utf-8') as f:
    css = f.read()

idx = css.find('@media')
while idx >= 0:
    block = css[idx:idx+800]
    if 'modal' in block or '480' in block or '768' in block or '600' in block:
        print(f'\n=== Media query at {idx} ===')
        lines2 = [l for l in block.split('\n') if l.strip()]
        print('\n'.join(lines2[:20]))
    idx = css.find('@media', idx+1)
