import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app.js', 'r', encoding='utf-8') as f:
    c = f.read()

# Tim toan bo vung renderBOQ / renderBoqTable
renderBOQ_start = c.find('function renderBOQ(')
print(f"renderBOQ at: {renderBOQ_start}")

# Tim tat ca cac 'surface' va 'header' keywords trong ham nay
chunk = c[renderBOQ_start:renderBOQ_start+30000]
# Tim cac doan phat hien surface de hieu structure
surface_lines = []
for kw in ["'floor'", "'wall'", "'ceiling'", "'door'", "'window'", 
           "'elec'", 'section-header', 'boq-header', 'sub-header',
           'surface ===', 'surface !==', 'group', 'section']:
    idx = 0
    while True:
        found = chunk.find(kw, idx)
        if found < 0: break
        line_s = chunk.rfind('\n', 0, found) + 1
        line_e = chunk.find('\n', found)
        line = chunk[line_s:line_e].strip()
        if line and len(line) < 200:
            surface_lines.append((found, kw, line[:130]))
        idx = found + 1
        if idx > 25000: break

surface_lines.sort(key=lambda x: x[0])
print("\n=== Surface/Section references in renderBOQ ===")
seen = set()
for pos, kw, line in surface_lines:
    if line not in seen:
        seen.add(line)
        print(f"  +{pos:5d} [{kw}]: {line}")
