import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

modal_start = c.find('<div class="modal-overlay" id="modal-room">')
modal_end = c.find('<!-- ========== APP CHÍNH', modal_start)
chunk = c[modal_start:modal_end]

# Tim vi tri </div> "mo coi" - nam giua /modal-header va modal-body
# Sau khi dong modal-header (depth ve 2), neu gap </div> ngay la orphan

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

# Tim khoang giua header close va modal-body open
header_close_idx = None
body_open_idx = None
for j, (pos, d, t, tag) in enumerate(pos_results):
    if t == 'CLOSE' and d == 2 and header_close_idx is None:
        # Day la dong header
        header_close_idx = j
        print(f"Header closes at: pos={pos}, depth={d}")
    if 'modal-body' in tag and t == 'OPEN':
        body_open_idx = j
        print(f"modal-body opens at: pos={pos}, depth={d}")
        break

# Tim bat ky CLOSE gi giua header_close va body_open
print("\n=== Between header-close and modal-body ===")
for j in range(header_close_idx, body_open_idx+1):
    pos, d, t, tag = pos_results[j]
    print(f"  j={j}: pos={pos}, d={d}, {t}: {tag[:60]}")
    
# Tim vi tri tuyet doi cua orphan </div>
# (se la CLOSE o depth 1 - nghia la dong modal-card bi dong qua som)
for j in range(header_close_idx, body_open_idx+1):
    pos, d, t, tag = pos_results[j]
    if t == 'CLOSE' and d == 1:
        print(f"\n🔴 ORPHAN </div> at absolute pos={pos}, depth becomes {d}")
        print(f"   Context: {repr(c[pos-50:pos+20])}")
