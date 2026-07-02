import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Tim chinh xac modal-footer cua modal-room
# No nam giua </div> (ket thuc modal-body) va </div> (ket thuc modal-card)
# Tim modal-footer
footer_start = c.find('<div class="modal-footer">', c.find('id="modal-room"'))
footer_end = c.find('</div>', footer_start)
footer_end = c.find('</div>', footer_end + 1)  # close modal-footer itself
footer_html = c[footer_start:footer_end + 6]  # +6 de lay </div>

print("=== Current footer HTML ===")
lines = footer_html.split('\n')
print('\n'.join([l for l in lines if l.strip()][:20]))

print(f"\nfooter_start={footer_start}, footer_end+6={footer_end+6}")
print(f"Chars: {len(footer_html)}")
