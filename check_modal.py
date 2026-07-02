import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Tim vi tri modal-room
modal_ov_start = c.find('<div class="modal-overlay" id="modal-room">')
modal_ov_end = c.find('<!-- ========== APP CHÍNH', modal_ov_start)
print(f"Modal overlay: {modal_ov_start} → {modal_ov_end}")

# In cau truc hien tai (chi cac dong co noi dung)
chunk = c[modal_ov_start:modal_ov_end]
lines = [l for l in chunk.split('\n') if l.strip()]
print("\n=== CURRENT STRUCTURE ===")
for i, l in enumerate(lines[:50]):
    print(f"{i:3}: {l[:120]}")
