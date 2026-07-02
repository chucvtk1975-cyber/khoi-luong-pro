import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

modal_start = c.find('<div class="modal-overlay" id="modal-room">')
modal_end_approx = c.find('<!-- ========== APP CHÍNH', modal_start)
chunk = c[modal_start:modal_end_approx]

# Phan tich cau truc div theo tung the thuc su
# Quet tu trai sang phai, tim <div va </div>
depth = 0
depth_map = []  # (pos_in_chunk, depth_after, tag)
i = 0
while i < len(chunk):
    if chunk[i:i+4] == '<div':
        end = chunk.find('>', i)
        tag = chunk[i:end+1]
        depth += 1
        depth_map.append((i, depth, 'OPEN', tag[:60]))
        i = end + 1
    elif chunk[i:i+6] == '</div>':
        depth -= 1
        depth_map.append((i, depth, 'CLOSE', '</div>'))
        i += 6
    else:
        i += 1

print(f"Total divs: {len(depth_map)}, Final depth: {depth}")
print("\n=== Structure ===")
for pos, d, t, tag in depth_map[:80]:
    line_content = ''
    # Tim noi dung gan day (comment hoac text)
    nearby = chunk[max(0,pos-100):pos]
    for kw in ['modal-footer', 'modal-body', 'modal-header', 'modal-card', 'modal-overlay',
                'THIẾT BỊ', 'modal-footer-mobile']:
        if kw in tag or kw in chunk[pos:pos+100]:
            line_content = f' ← {kw}'
            break
    indent = '  ' * d
    print(f"{pos:6d} | d={d:2d} | {t:5s} | {indent}{tag[:50]}{line_content}")
