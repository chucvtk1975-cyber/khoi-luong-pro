import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

modal_start = c.find('id="modal-room"')

# === BUOC 1: Xoa modal-footer hien tai (nam truoc modal-body)
# Tim modal-footer trong modal-room
footer_start = c.find('<div class="modal-footer">', modal_start)
footer_end = c.find('</div>', footer_start) + 6  # dong modal-footer
footer_html = c[footer_start:footer_end]

# Verify: chi chua buttons, khong chua modal-body
print("=== Footer HTML to move ===")
print('\n'.join([l for l in footer_html.split('\n') if l.strip()]))

# Kiem tra footer_end khong can vao modal-body
after = c[footer_end:footer_end+100].strip()
print(f"\nAfter footer: {repr(after[:80])}")
