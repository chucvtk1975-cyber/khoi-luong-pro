import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('style.css', 'r', encoding='utf-8') as f:
    c = f.read()

# Xoa toan bo media query cu da them (co loi)
old_media = """@media (max-width: 768px) {
  .project-sidebar { width: 220px; }
  .stats-bar { grid-template-columns: repeat(2, 1fr); }
  .dim-grid { grid-template-columns: repeat(2, 1fr); }
  .opening-grid { grid-template-columns: repeat(2, 1fr); }
  .workspace { padding: 16px; }
  /* Mobile modal: full-width, buttons luôn hiện trên đầu */
  .modal-overlay { align-items: flex-start; padding: 0; }
  .modal-card {
    max-width: 100% !important;
    width: 100% !important;
    max-height: 100dvh !important;
    border-radius: 0 !important;
    margin: 0 !important;
  }
  .modal-footer {
    position: sticky;
    top: 0;
    z-index: 10;
  }
  .modal-body { flex: 1; overflow-y: auto; }
}"""

new_media = """@media (max-width: 768px) {
  .project-sidebar { width: 220px; }
  .stats-bar { grid-template-columns: repeat(2, 1fr); }
  .dim-grid { grid-template-columns: repeat(2, 1fr); }
  .opening-grid { grid-template-columns: repeat(2, 1fr); }
  .workspace { padding: 16px; }
  /* Mobile: modal chiếm toàn màn hình, body scroll bên trong */
  .modal-overlay {
    align-items: flex-start !important;
    justify-content: center !important;
    padding: 0 !important;
    overflow-y: auto;
  }
  .modal-card {
    max-width: 100vw !important;
    width: 100vw !important;
    max-height: none !important;
    min-height: 100dvh !important;
    border-radius: 0 !important;
    margin: 0 !important;
  }
  .modal-body {
    overflow-y: visible !important;
    flex: 1;
  }
  .modal-footer {
    position: static !important;
  }
}"""

if old_media in c:
    c = c.replace(old_media, new_media, 1)
    print("✓ Mobile media query rebuilt correctly")
else:
    # Tim va thay the phan nao co the
    idx = c.find('@media (max-width: 768px)')
    if idx >= 0:
        # Tim dong } ket thuc media query
        depth = 0
        i = idx
        while i < len(c):
            if c[i] == '{': depth += 1
            elif c[i] == '}':
                depth -= 1
                if depth == 0:
                    old_block = c[idx:i+1]
                    c = c.replace(old_block, new_media, 1)
                    print(f"✓ Replaced media query at {idx}")
                    break
            i += 1
    else:
        c += "\n\n" + new_media
        print("✓ Added new mobile media query")

# Dam bao .modal-body co overflow-y:auto tren desktop
old_body = """.modal-body {
  padding: 18px 22px;
  overflow-y: auto;
  flex: 1;
}"""
if old_body not in c:
    # Tim va dam bao no dung
    idx_body = c.find('.modal-body {')
    if idx_body >= 0:
        print(f"Current modal-body: {c[idx_body:c.find('}',idx_body)+1]}")

with open('style.css', 'w', encoding='utf-8') as f:
    f.write(c)

print("\n✅ style.css fixed")
