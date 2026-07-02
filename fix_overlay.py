import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('style.css', 'r', encoding='utf-8') as f:
    c = f.read()

# Xoa dong bi duplicate
bad_line = ".modal-overlay { align-items: flex-start; padding: 0; }"
if bad_line in c:
    # Xoa dong nay va newline lien quan
    c = c.replace('\n' + bad_line, '', 1)
    print("✓ Removed orphaned .modal-overlay override")
elif bad_line.strip() in c:
    c = c.replace(bad_line, '', 1)
    print("✓ Removed (no newline)")
else:
    print("? Not found, searching manually...")
    idx = c.find('modal-overlay { align-items')
    if idx > 0:
        line_start = c.rfind('\n', 0, idx)
        line_end = c.find('\n', idx)
        print(f"Found: {repr(c[line_start:line_end])}")
        c = c[:line_start] + c[line_end:]
        print("✓ Removed")

with open('style.css', 'w', encoding='utf-8') as f:
    f.write(c)

print("✅ Done")
