import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

modal_start = c.find('id="modal-room"')

# 1. Tim chinh xac footer block (chi div modal-footer, khong lay modal-card close)
footer_div_start = c.find('<div class="modal-footer">', modal_start)
# Tim </div> dong footer
footer_div_end = c.find('</div>', footer_div_start) + 6  # dong </div> cua modal-footer

footer_block = c[footer_div_start:footer_div_end]
print("=== Footer block ===")
print('\n'.join([l for l in footer_block.split('\n') if l.strip()]))

# 2. Tim vi tri sau modal-header de chen vao
# Tim </div> dong modal-header
header_close = c.find('</div>', c.find('<div class="modal-header">', modal_start)) + 6
print(f"\nInserting after char {header_close}")
print(f"Context: {repr(c[header_close-10:header_close+30])}")

# 3. Xay dung HTML moi:
# - Xoa footer khoi vi tri cu (sau modal-body)
# - Them vao sau modal-header

# Xoa footer cu (bao gom newline truoc no)
# Tim whitespace/newline truoc footer_div_start
pre_footer = footer_div_start
while pre_footer > 0 and c[pre_footer-1] in ' \t\r\n':
    pre_footer -= 1
pre_footer += 1  # giu lai 1 newline

c_new = c[:pre_footer] + c[footer_div_end:]

# Sau khi xoa, tim lai header_close (vi tri thay doi)
# Offset: footer da bi xoa o footer_div_start, header_close < footer_div_start nen khong anh huong
new_modal_start = c_new.find('id="modal-room"')
new_header_close = c_new.find('</div>', c_new.find('<div class="modal-header">', new_modal_start)) + 6

# Chen footer moi vao sau header
footer_with_mobile_style = '\n      ' + footer_block.strip() + '\n'
c_new = c_new[:new_header_close] + footer_with_mobile_style + c_new[new_header_close:]

# Verify
verify_idx = c_new.find('id="modal-room"')
verify_chunk = c_new[verify_idx:verify_idx+3000]
lines = verify_chunk.split('\n')
print("\n=== Result structure ===")
print('\n'.join([l for l in lines if l.strip()][:30]))

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(c_new)

print("\n✅ modal-footer moved to top (after modal-header)")
