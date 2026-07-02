import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app.js', 'r', encoding='utf-8') as f:
    c = f.read()

# Tim tat ca doan lien quan Roman numeral
searches = ['roman', 'Roman', 'toRoman', 'I.', 'II.', 'boq-section', 'section-header',
            'boq-group', 'renderBOQ', 'renderRoom', 'section_index']

for s in searches:
    pos = 0
    count = 0
    while True:
        idx = c.find(s, pos)
        if idx < 0 or count > 3: break
        line_s = c.rfind('\n', 0, idx) + 1
        line_e = c.find('\n', idx)
        line = c[line_s:line_e].strip()
        if line:
            print(f"[{idx}] {s}: {line[:120]}")
        pos = idx + 1
        count += 1
