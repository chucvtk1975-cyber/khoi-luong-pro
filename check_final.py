import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Tim va in phan cuoi modal
app = c.find('<!-- ========== APP CHÍNH')
print("=== Last 600 chars before APP CHÍNH ===")
chunk = c[app-600:app]
# In theo tung dong (bo cac dong trong)
lines = [l for l in chunk.split('\n') if l.strip()]
for l in lines:
    print(l[:120])

# Dem div trong toan modal
modal_start = c.find('<div class="modal-overlay" id="modal-room">')
modal_end = c.find('<!-- ========== APP CHÍNH', modal_start)
modal_chunk = c[modal_start:modal_end]
opens  = modal_chunk.count('<div')
closes = modal_chunk.count('</div>')
print(f"\nModal divs: opens={opens}, closes={closes}, net={opens-closes}")

# Kiem tra footer nam o dau
fi = c.find('<div class="modal-footer">', modal_start)
# Tim the mo cua cua it nhat 1 the bao ngoai footer
pre = c[fi-200:fi]
print(f"\n=== 200 chars before modal-footer ===")
print(repr(pre))
