import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app.js', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. elecHeader label trong renderBOQ (web BOQ preview)
print("=== 1. elecHeader in renderBOQ (web preview) ===")
idx = c.find('boq-elec-header')
while idx > 0:
    line_s = c.rfind('\n', 0, idx) + 1
    line_e = c.find('\n', idx)
    line = c[line_s:line_e].strip()
    if 'exportExcel' not in c[max(0,idx-5000):idx]:  # chi lay trong renderBOQ
        print(f"[{idx}]: {line[:150]}")
    idx = c.find('boq-elec-header', idx+1)

print("\n=== 2. noteHeader in renderBOQ ===")
idx2 = c.find('boq-note-header')
while idx2 > 0 and idx2 < 511317:  # chi truoc exportExcel
    line_s = c.rfind('\n', 0, idx2) + 1
    line_e = c.find('\n', idx2)
    print(f"[{idx2}]: {c[line_s:line_e].strip()[:150]}")
    idx2 = c.find('boq-note-header', idx2+1)

print("\n=== 3. elecHeader in Excel CHI TIẾT sheet ===")
chi_tiet = c.find('BẢNG CHI TIẾT KHỐI LƯỢNG')
idx3 = c.find('elecHeader', chi_tiet)
while idx3 > 0 and idx3 < chi_tiet + 15000:
    line_s = c.rfind('\n', 0, idx3) + 1
    line_e = c.find('\n', idx3)
    print(f"[{idx3}]: {c[line_s:line_e].strip()[:150]}")
    idx3 = c.find('elecHeader', idx3+1)

print("\n=== 4. SURF_GRP in Excel CHI TIẾT ===")
idx4 = c.find('SURF_GRP', chi_tiet)
if idx4 > 0 and idx4 < chi_tiet + 15000:
    print(f"[{idx4}]: FOUND → {c[idx4:idx4+100]}")
else:
    print("NOT FOUND in Excel CHI TIẾT - section headers not added yet!")

print("\n=== 5. Full elecHeader template in renderBOQ ===")
# Tim trong renderBOQ function (179399 → truoc exportExcel 511317)
renderBOQ_start = c.find('function renderBOQ(')
renderBOQ_end = 511317
elec_pos = c.find("'elecHeader'", renderBOQ_start)
while elec_pos > 0 and elec_pos < renderBOQ_end:
    # In 3 dong
    s = c.rfind('\n', 0, elec_pos) + 1
    e = c.find('\n', elec_pos + 200) if c.find('\n', elec_pos + 200) > 0 else elec_pos + 300
    print(f"[{elec_pos}]:", c[s:e].strip()[:200])
    elec_pos = c.find("'elecHeader'", elec_pos+1)
