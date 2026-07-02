import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('style.css', 'r', encoding='utf-8') as f:
    c = f.read()

# Them CSS cho mobile-only buttons
# 1. An tren desktop
desktop_css = """
/* Mobile-only action buttons inside modal-body (hidden on desktop) */
.modal-footer-mobile-top {
  display: none;
}"""

# 2. Hien tren mobile, trong media query 768px
# Tim media query hien tai
idx = c.find('@media (max-width: 768px)')
if idx >= 0:
    # Chen vao ben trong media query (truoc dau dong }) cuoi
    depth = 0
    i = idx
    while i < len(c):
        if c[i] == '{': depth += 1
        elif c[i] == '}':
            depth -= 1
            if depth == 0:
                # Chen truoc dau }
                mobile_css = """
  /* Hien nut mobile-only, an nut desktop */
  .modal-footer-mobile-top {
    display: flex;
    justify-content: flex-end;
    gap: 8px;
    padding: 10px 16px;
    border-bottom: 1px solid var(--border-light);
    background: var(--bg-card);
  }
  /* An nut footer goc (dua xuong duoi trong modal) */
  .modal-footer {
    display: none;
  }"""
                c = c[:i] + mobile_css + '\n' + c[i:]
                print("✓ Mobile CSS added inside media query")
                break
        i += 1

# Them desktop CSS (an mobile buttons) truoc media query
c = c[:idx] + desktop_css + '\n\n' + c[idx:]
print("✓ Desktop CSS (hide mobile buttons) added")

with open('style.css', 'w', encoding='utf-8') as f:
    f.write(c)
print("✅ Done")
