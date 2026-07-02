import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

modal_start  = c.find('<div class="modal-overlay" id="modal-room">')
app_start    = c.find('<!-- ========== APP CHÍNH', modal_start)

modal_footer_open = 24112   # vi tri <div class="modal-footer">
modal_footer_end  = 24465   # vi tri sau </div> dong footer
thiet_bi_start    = 24489   # vi tri <!-- THIẾT BỊ NỘI THẤT -->

# 1. Tim va lay noi dung THIET BI / PHAN NUOC / CHONG THAM
#    Tu thiet_bi_start den truoc dong "<!-- end modal-body -->" hoac den cuoi
content_after_footer = c[thiet_bi_start:app_start]
# Tim ket thuc noi dung chinh (truoc 3 dong </div> cuoi cung)
# Tim "<!-- end modal-body -->" neu co
end_marker = content_after_footer.find('<!-- end modal-body -->')
if end_marker > 0:
    # Lay tu thiet_bi_start den truoc end_marker
    # Tim </div> truoc end_marker (day la dong close cuoi cung cua noi dung)
    last_close = content_after_footer.rfind('</div>', 0, end_marker)
    body_content_end = thiet_bi_start + last_close + 6
    print(f"Found end-modal-body marker, content ends at {body_content_end}")
else:
    # Khong co marker, lay het roi trim 3 dong </div> cuoi
    # Tim 3 dong </div> cuoi cung cua modal
    # Doi sach: tim vi tri cua cac dong </div> cuoi
    chunk = c[thiet_bi_start:app_start]
    # Tim vi tri cua 3 </div> cuoi cung
    closes = []
    idx = 0
    while True:
        idx = chunk.find('</div>', idx)
        if idx < 0: break
        closes.append(thiet_bi_start + idx)
        idx += 1
    print(f"Found {len(closes)} </div> tags after THIẾT BỊ")
    # 3 cuoi: closes[-3], closes[-2], closes[-1]
    # closes[-1] = orphan
    # closes[-2] = close modal-overlay
    # closes[-3] = close modal-card
    # closes[-4] = close modal-body (that's what we want to find)
    # Nhung truoc day da co "close modal-body" sai nen co them the
    # Thu lay tu thiet_bi_start den closes[-3] (close modal-card)
    body_content_end = closes[-3] if len(closes) >= 3 else closes[-1]
    print(f"Using content end at: {body_content_end}")

section_content = c[thiet_bi_start:body_content_end].rstrip()
print(f"Section content length: {len(section_content)}")
print("First 200:", repr(section_content[:200]))
print("Last 200:", repr(section_content[-200:]))

# 2. Tim noi dung modal-footer goc de tai su dung
footer_html = c[modal_footer_open:modal_footer_end].strip()
print(f"\nFooter HTML ({len(footer_html)} chars):")
print('\n'.join([l for l in footer_html.split('\n') if l.strip()]))

# 3. Tim vi tri cua nut mobile-top da insert truoc do
mobile_top_start = c.find('<div class="modal-footer-mobile-top">', 
                           c.find('<div class="modal-body">', modal_start))
print(f"\nmobile-top at: {mobile_top_start}")
