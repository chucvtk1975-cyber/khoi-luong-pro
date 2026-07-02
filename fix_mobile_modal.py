import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('style.css', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Them mobile CSS cho modal
old_media = """@media (max-width: 768px) {
  .project-sidebar { width: 220px; }
  .stats-bar { grid-template-columns: repeat(2, 1fr); }
  .dim-grid { grid-template-columns: repeat(2, 1fr); }
  .opening-grid { grid-template-columns: repeat(2, 1fr); }
  .workspace { padding: 16px; }
}"""

new_media = """@media (max-width: 768px) {
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

if old_media in c:
    c = c.replace(old_media, new_media, 1)
    print("✓ Mobile media query updated")
else:
    print("✗ Media query not found, adding at end")
    c += "\n\n" + new_media

# 2. Dam bao modal-overlay co align-items center tren desktop
old_overlay = ".modal-overlay {"
idx = c.find(old_overlay)
if idx > 0:
    block_end = c.find('}', idx)
    block = c[idx:block_end+1]
    print(f"\nCurrent .modal-overlay:\n{block}")

with open('style.css', 'w', encoding='utf-8') as f:
    f.write(c)

print("\n✅ style.css updated with mobile modal fixes")
