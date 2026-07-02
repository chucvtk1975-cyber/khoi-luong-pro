import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

modal_start = c.find('<div class="modal-overlay" id="modal-room">')
modal_end = c.find('<!-- ========== APP CHÍNH', modal_start)
chunk = c[modal_start:modal_end]

depth = 0
pos_results = []
i = 0
while i < len(chunk):
    if chunk[i:i+4] == '<div':
        end = chunk.find('>', i)
        tag = chunk[i:end+1]
        depth += 1
        pos_results.append((modal_start+i, depth, 'OPEN', tag[:80]))
        i = end + 1
    elif chunk[i:i+6] == '</div>':
        depth -= 1
        pos_results.append((modal_start+i, depth, 'CLOSE', chunk[i:i+6]))
        i += 6
    else:
        i += 1

print(f"Total: {len(pos_results)}, Final depth: {depth}")
print("\n=== LAST 20 entries ===")
for pos, d, t, tag in pos_results[-20:]:
    # Them context
    ctx = c[pos-30:pos+40].replace('\n','↵').replace('\r','')
    print(f"  pos={pos}, d={d:+2d}, {t}: {ctx[:80]}")
