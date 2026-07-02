import sys
sys.stdout.reconfigure(encoding='utf-8')

lesson = """

---

## BÀI HỌC: Modal Footer Bug (2026-06-21)

### Vấn đề
Nút "Hủy" / "Thêm Phòng" của modal-room bị hiển thị RA NGOÀI modal-card, sang phải màn hình.

### Root cause
1. Script `move_footer.py` đã lấy footer_block bằng `c.find('</div>', footer_start) + 6` — chỉ tìm closing tag ĐẦU TIÊN.
2. Nhưng `</div>` đầu tiên sau `<div class="modal-footer">` KHÔNG phải là close của footer mà là close của modal-card (do file có nhiều `\r\n` xen kẽ làm lệch parse).
3. Kết quả: đã move footer + modal-card closing tag ra khỏi vị trí gốc → HTML mất cân bằng.
4. Browser auto-corrected → đưa `modal-footer` thành SIBLING của `modal-card` trong flex overlay → hiển thị sang phải.

### Tại sao Python count 89/89 vẫn không fix được
- Python count `'<div'` và `'</div>'` trong chuỗi raw — không bị ảnh hưởng bởi browser parsing rules.
- Tuy nhiên browser có thể parse HTML KHÁC với Python count (do element nesting rules, auto-close behaviors, v.v.).
- File có `\r\n` sau mỗi ký tự (encoding corruption) khiến browser dễ parse sai hơn.

### Fix cuối cùng hoạt động
**JavaScript runtime DOM fix** — chạy ngay khi script load:
```javascript
(function fixModalLayout() {
  var overlay = document.getElementById('modal-room');
  var card = overlay.querySelector('.modal-room-card');
  var footer = overlay.querySelector('.modal-footer');
  if (card && footer && footer.parentElement !== card) {
    card.appendChild(footer);  // kéo về đúng chỗ
  }
  // Dọn bất kỳ thứ gì bị parse ra ngoài card
  Array.from(overlay.children).forEach(function(child) {
    if (child !== card) card.appendChild(child);
  });
})();
```

### Mobile top-buttons
Thêm `<div class="modal-footer-mobile-top">` TRONG modal-body (ngay đầu form):
- Desktop: ẩn bằng CSS `display: none`
- Mobile (≤768px): hiện bằng CSS `display: flex`
→ User luôn thấy nút ngay khi mở modal, không cần scroll xuống cuối.

### Bài học rút ra
1. **Không dùng position hardcode** khi đã modify file nhiều lần — vị trí thay đổi sau mỗi lần save.
2. **File có encoding corruption** (`\r\n` xen kẽ ký tự): luôn dùng Python utf-8 để đọc/ghi, nhưng kết quả count DIV có thể khác với browser parsing.
3. **JS DOM fix > HTML manipulation** khi HTML phức tạp và bị corrupt — JavaScript chạy SAU khi browser đã parse, nên nó luôn thắng.
4. **Luôn deploy bằng zip mới** trước khi test trên mobile — mobile dùng Netlify URL, không phải file local.
"""

with open('LEARN.md', 'r', encoding='utf-8') as f:
    existing = f.read()

with open('LEARN.md', 'w', encoding='utf-8') as f:
    f.write(existing + lesson)

print("✅ LEARN.md updated")
