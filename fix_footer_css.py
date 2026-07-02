import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('style.css', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Doi border-top thanh border-bottom trong .modal-footer
old_footer_css = """.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
  padding: 14px 22px 18px;
  border-top: 1px solid var(--border-light);
  flex-shrink: 0;
}"""

new_footer_css = """.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
  padding: 10px 22px;
  border-bottom: 1px solid var(--border-light);
  flex-shrink: 0;
  background: var(--bg-card);
}"""

if old_footer_css in c:
    c = c.replace(old_footer_css, new_footer_css, 1)
    print("✓ .modal-footer CSS updated (border-top → border-bottom)")
else:
    # Try finding just border-top
    old2 = "border-top: 1px solid var(--border-light);"
    if old2 in c:
        c = c.replace(old2, "border-bottom: 1px solid var(--border-light);", 1)
        print("✓ border-top → border-bottom (via alternate)")
    else:
        print("✗ Not found")

with open('style.css', 'w', encoding='utf-8') as f:
    f.write(c)

print("✅ style.css updated")
