import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Tim vi tri <div class="modal-body"> trong modal-room
modal_room_start = c.find('id="modal-room"')
modal_body_start = c.find('<div class="modal-body">', modal_room_start)

# Chen 1 dong nut mobile-only VÀO trong modal-body (ngay sau the mo)
# Tim diem ngay sau <div class="modal-body">
after_modal_body = modal_body_start + len('<div class="modal-body">')

mobile_buttons = """
        <!-- MOBILE ONLY: Nút hành động hiện ở đầu form khi màn hình nhỏ -->
        <div class="modal-footer-mobile-top">
          <button class="btn-secondary" onclick="closeRoomModal()">Hủy</button>
          <button class="btn-primary" onclick="saveRoom()">
            <i data-lucide="plus-circle"></i>
            <span id="btn-save-room-label-mobile">Thêm Phòng</span>
          </button>
        </div>"""

c = c[:after_modal_body] + mobile_buttons + c[after_modal_body:]
print("✓ Mobile-only buttons added inside modal-body")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(c)
print("✅ Done")
