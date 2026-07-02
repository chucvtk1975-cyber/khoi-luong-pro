import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app.js', 'r', encoding='utf-8') as f:
    c = f.read()

# Tim DOMContentLoaded cuoi cung (main app init)
# va them JS fix TRUOC khi no chay
dce_pos = c.find("DOMContentLoaded', () => { init(); initMediaListeners(); });")
if dce_pos < 0:
    dce_pos = c.find("DOMContentLoaded")
    while True:
        next_pos = c.find("DOMContentLoaded", dce_pos + 1)
        if next_pos < 0: break
        dce_pos = next_pos
    
print(f"Last DOMContentLoaded at: {dce_pos}")
print(c[dce_pos:dce_pos+100])

# JS FIX se them ngay TRUOC DOMContentLoaded
fix_js = """// ============ DOM STRUCTURE FIX ============
// Fix: neu browser da auto-correct modal-footer ra ngoai modal-card
// thi di chuyen no vao dung cho truoc khi bat ky gi xay ra
(function fixModalLayout() {
  var overlay = document.getElementById('modal-room');
  if (!overlay) return;
  var card = overlay.querySelector('.modal-room-card');
  var footer = overlay.querySelector('.modal-footer');
  if (card && footer && footer.parentElement !== card) {
    // Footer bi parse ngoai card → move vao cuoi card
    card.appendChild(footer);
    console.log('[FIX] modal-footer moved into modal-card');
  }
  // Dam bao modal-overlay la flex container cho dung 1 con (modal-card)
  // Xoa tat ca direct children cua overlay khong phai modal-card
  if (card && overlay) {
    Array.from(overlay.children).forEach(function(child) {
      if (child !== card) {
        // Child bi lenh: co the la footer hoac gi do khac
        card.appendChild(child);
        console.log('[FIX] extra child moved into modal-card:', child.className);
      }
    });
  }
})();

"""

# Tim dong "document.addEventListener('DOMContentLoaded'"
target = "document.addEventListener('DOMContentLoaded'"
idx = c.rfind(target)  # Tim tu cuoi len dau (last occurrence)
print(f"\nTarget found at: {idx}")
print(c[idx:idx+80])

# Chen fix_js NGAY TRUOC target
c_new = c[:idx] + fix_js + c[idx:]

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(c_new)

print("\n✅ JS DOM fix added to app.js")
