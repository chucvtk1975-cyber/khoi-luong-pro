import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Tim vi tri chinh xac
modal_start = c.find('<div class="modal-overlay" id="modal-room">')
app_start = c.find('<!-- ========== APP CHÍNH', modal_start)

modal_chunk = c[modal_start:app_start]

# Tim vi tri tuyet doi cua cac element quan trong
modal_body_open = c.find('<div class="modal-body">', modal_start)
print(f"modal-body opens at: {modal_body_open}")

# Tim van ban sau modal-body den het - do co nhieu </div> sai
# Tiep can: tim tat ca noi dung form can giu lai (THIET BI, PHAN NUOC, CHONG THAM)
# va tim vi tri bat dau cua chung

thiet_bi_comment = c.find('<!-- THIẾT BỊ NỘI THẤT -->', modal_start)
phan_nuoc_comment = c.find('<!-- PHẦN NƯỚC -->', modal_start)
chong_tham_comment = c.find('<!-- CHỐNG THẤM -->', modal_start)

print(f"THIẾT BỊ comment at: {thiet_bi_comment}")
print(f"PHẦN NƯỚC comment at: {phan_nuoc_comment}")
print(f"CHỐNG THẤM comment at: {chong_tham_comment}")

# Tim nut footer cu (modal-footer) trong modal
modal_footer_open = c.find('<div class="modal-footer">', modal_start)
modal_footer_end = c.find('</div>', modal_footer_open) + 6
print(f"modal-footer at: {modal_footer_open} → {modal_footer_end}")

# In context vung can giu lai (section titles THIET BI, PHAN NUOC, CHONG THAM)
print("\n=== THIẾT BỊ section start ===")
print(repr(c[thiet_bi_comment:thiet_bi_comment+200]))
