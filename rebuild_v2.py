import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

modal_start       = c.find('<div class="modal-overlay" id="modal-room">')
app_start         = c.find('<!-- ========== APP CHÍNH', modal_start)
modal_footer_open = 24112   # <div class="modal-footer">
thiet_bi_start    = 24489   # <!-- THIẾT BỊ NỘI THẤT -->
wrong_close_start = 24099   # </div> ky tu sai (dong modal-body som)

# Tim vi tri chinh xac cua </div><!-- end modal-body --> 
# De KHONG bao gom no trong section_content
end_modal_body_tag = c.find('</div><!-- end modal-body -->', thiet_bi_start)
print(f"end-modal-body tag at: {end_modal_body_tag}")
# section_content: chi lay tu THIET BI den TRUOC tag end-modal-body
section_end = end_modal_body_tag  # KHONG bao gom the nay
section_content = c[thiet_bi_start:section_end].rstrip()

print(f"section_content: {thiet_bi_start} → {section_end} ({len(section_content)} chars)")

# Dem div trong section_content
sc_opens  = section_content.count('<div')
sc_closes = section_content.count('</div>')
print(f"  Opens: {sc_opens}, Closes: {sc_closes}, Net: {sc_opens - sc_closes}")

# Footer HTML
footer_html = """      <div class="modal-footer">
        <button class="btn-secondary" id="btn-cancel-room">Hủy</button>
        <button class="btn-primary" id="btn-save-room">
          <i data-lucide="plus-circle"></i> <span id="btn-save-room-label">Thêm Phòng</span>
        </button>
      </div>"""

# Phan truoc wrong close (end at wrong_close_start = 24099)
part1 = c[:wrong_close_start]
p1_opens  = part1.count('<div')
p1_closes = part1.count('</div>')
print(f"\npart1 divs: opens={p1_opens}, closes={p1_closes}, net={p1_opens-p1_closes}")

# Xay dung phan ket thuc moi
new_end = section_content + """
      </div><!-- end modal-body -->
""" + footer_html + """
    </div><!-- end modal-card -->
  </div><!-- end modal-room -->

"""

ne_opens  = new_end.count('<div')
ne_closes = new_end.count('</div>')
print(f"new_end divs: opens={ne_opens}, closes={ne_closes}, net={ne_opens-ne_closes}")

# Ghep lai
part3 = c[app_start:]
c_new = part1 + new_end + part3

# Verify trong modal section
nm_start = c_new.find('<div class="modal-overlay" id="modal-room">')
nm_end   = c_new.find('<!-- ========== APP CHÍNH', nm_start)
modal_only = c_new[nm_start:nm_end]
total_opens  = modal_only.count('<div')
total_closes = modal_only.count('</div>')
net = total_opens - total_closes
print(f"\nFinal modal: opens={total_opens}, closes={total_closes}, net={net}")

if net == 0:
    print("✅ BALANCED!")
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(c_new)
    print("✅ Saved!")
    # Show final structure
    lines = [l for l in modal_only.split('\n') if l.strip()]
    structural = [l for l in lines if '<div' in l or '</div>' in l or 'modal-' in l]
    print("\n=== Final modal structure (key divs) ===")
    for l in structural[:15]:
        print(l[:100])
    print("...")
    for l in structural[-10:]:
        print(l[:100])
else:
    print(f"❌ Still off by {net}")
