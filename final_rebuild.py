import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

modal_start       = c.find('<div class="modal-overlay" id="modal-room">')
app_start         = c.find('<!-- ========== APP CHÍNH', modal_start)
modal_footer_open = 24112   # <div class="modal-footer">
modal_footer_end  = 24465   # end of </div> closing footer
thiet_bi_start    = 24489   # <!-- THIẾT BỊ NỘI THẤT -->
section_end       = 26640   # end of all section content (after CHỐNG THẤM)

# Tim vi tri CHINH XAC cua wrong close (</div> ngay truoc modal-footer)
# Tim backward tu modal_footer_open
wrong_close_end = c.rfind('</div>', modal_footer_open - 30, modal_footer_open) + 6
wrong_close_start = wrong_close_end - 6
print(f"Wrong close found at: {wrong_close_start} → {wrong_close_end}")
print(f"Context: {repr(c[wrong_close_start-20:wrong_close_end+20])}")

# Lay noi dung section (THIET BI, PHAN NUOC, CHONG THAM)
section_content = c[thiet_bi_start:section_end]
# Trim trailing whitespace nhung giu indent
section_content = section_content.rstrip()

# Footer HTML goc
footer_html = """      <div class="modal-footer">
        <button class="btn-secondary" id="btn-cancel-room">Hủy</button>
        <button class="btn-primary" id="btn-save-room">
          <i data-lucide="plus-circle"></i> <span id="btn-save-room-label">Thêm Phòng</span>
        </button>
      </div>"""

# XAY DUNG HTML MOI:
# 1. Giu tu dau file den truoc wrong close (toan bo noi dung modal-body hien co)
part1 = c[:wrong_close_start]

# 2. Them section content (THIET BI etc.) SAU cac form hien tai (van con trong modal-body)
# 3. Dong modal-body
# 4. Them footer
# 5. Dong modal-card va modal-overlay
new_end = section_content + """
      </div><!-- end modal-body -->
""" + footer_html + """
    </div><!-- end modal-card -->
  </div><!-- end modal-room -->

"""

# 6. Phan con lai cua file (bat dau tu app_start)
part3 = c[app_start:]

# Ghep lai
c_new = part1 + new_end + part3

# VERIFY: dem divs trong modal moi
new_modal_start = c_new.find('<div class="modal-overlay" id="modal-room">')
new_app_start   = c_new.find('<!-- ========== APP CHÍNH', new_modal_start)
modal_chunk = c_new[new_modal_start:new_app_start]

depth = 0
opens = closes = 0
i = 0
while i < len(modal_chunk):
    if modal_chunk[i:i+4] == '<div':
        depth += 1; opens += 1
        i = modal_chunk.find('>', i) + 1
    elif modal_chunk[i:i+6] == '</div>':
        depth -= 1; closes += 1; i += 6
    else:
        i += 1

print(f"\nVerification: opens={opens}, closes={closes}, final_depth={depth}")
if depth == 0:
    print("✅ BALANCED! HTML is correct")
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(c_new)
    print("✅ index.html saved")
else:
    print(f"❌ Still unbalanced (depth={depth}), NOT saving")
    # Debug: show last few div operations
    print("\nLast 10 div operations in new modal:")
    ops = []
    depth2 = 0
    i = 0
    while i < len(modal_chunk):
        if modal_chunk[i:i+4] == '<div':
            depth2 += 1
            end = modal_chunk.find('>', i)
            ops.append((i, depth2, 'OPEN', modal_chunk[i:end+1][:60]))
            i = end + 1
        elif modal_chunk[i:i+6] == '</div>':
            depth2 -= 1
            ops.append((i, depth2, 'CLOSE', '</div>'))
            i += 6
        else:
            i += 1
    for pos, d, t, tag in ops[-10:]:
        print(f"  {pos}: d={d} {t}: {tag}")
