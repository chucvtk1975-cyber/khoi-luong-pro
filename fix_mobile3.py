import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('style.css', 'r', encoding='utf-8') as f:
    c = f.read()

# Tim va thay the toan bo media query 768px
idx = c.find('@media (max-width: 768px)')
if idx >= 0:
    depth = 0
    i = idx
    while i < len(c):
        if c[i] == '{': depth += 1
        elif c[i] == '}':
            depth -= 1
            if depth == 0:
                old_block = c[idx:i+1]
                break
        i += 1
    
    print("=== Replacing media query ===")
    print(old_block[:200])
    
    new_block = """@media (max-width: 768px) {
  .project-sidebar { width: 220px; }
  .stats-bar { grid-template-columns: repeat(2, 1fr); }
  .dim-grid { grid-template-columns: repeat(2, 1fr); }
  .opening-grid { grid-template-columns: repeat(2, 1fr); }
  .workspace { padding: 16px; }

  /* === MOBILE MODAL FIX ===
     Overlay trở thành trang scroll thẳng đứng (block)
     Modal-card chiếm toàn màn hình theo chiều dài tự nhiên
     Footer (buttons) nằm ở đầu HTML → luôn thấy ngay khi mở modal
  */
  .modal-overlay.open {
    display: block !important;
    overflow-y: auto !important;
    padding: 0 !important;
    -webkit-overflow-scrolling: touch;
  }
  .modal-card {
    display: block !important;
    max-width: 100vw !important;
    width: 100vw !important;
    max-height: none !important;
    border-radius: 0 !important;
    min-height: 100dvh;
    box-sizing: border-box;
  }
  /* modal-body không cần overflow riêng - overlay đã scroll */
  .modal-body {
    overflow-y: visible !important;
    flex: none !important;
  }
  /* modal-footer: block thường, nằm đúng vị trí trong HTML (sau header) */
  .modal-footer {
    position: static !important;
    border-radius: 0;
  }
}"""
    
    c = c.replace(old_block, new_block, 1)
    print("✓ Media query replaced")
else:
    print("✗ Not found")

with open('style.css', 'w', encoding='utf-8') as f:
    f.write(c)
print("✅ Done")
