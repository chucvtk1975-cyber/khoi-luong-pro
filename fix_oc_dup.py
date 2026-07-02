import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app.js', 'r', encoding='utf-8') as f:
    c = f.read()

# Van de: khi filter theo phong, cac row khong co data-kr bi return som
# nen boq-other-header khong bi an
# Fix: kiem tra class boq-other-header/item TRUOC khi check !kr

old = "      if (!kr) return; // rows không có data-kr (không nên có)\n"
new = """      // Ẩn project-level OC khi xem từng phòng cụ thể (rows này không có data-kr)
      if (row.classList.contains('boq-other-header') || row.classList.contains('boq-other-item')) {
        row.style.display = 'none';
        return;
      }
      if (!kr) return; // rows không có data-kr (không nên có)
"""

if old in c:
    c = c.replace(old, new, 1)
    print("✓ Fixed: boq-other-header now hidden before !kr return")
else:
    # Tim truoc khi check !kr
    print("String not found exactly, trying alternate...")
    old2 = "      if (!kr) return;"
    idx = c.find(old2, c.find('function filterBOQByRoom'))
    if idx > 0:
        print(f"Found at {idx}: {repr(c[idx:idx+60])}")
        # Lay dong chinh xac
        line_end = c.find('\n', idx)
        exact = c[idx:line_end+1]
        print(f"Exact line: {repr(exact)}")
        c = c.replace(exact, """      // Ẩn project-level OC khi xem từng phòng cụ thể
      if (row.classList.contains('boq-other-header') || row.classList.contains('boq-other-item')) {
        row.style.display = 'none';
        return;
      }
""" + exact, 1)
        print("✓ Fixed via alternate method")
    else:
        print("✗ Could not find !kr check in filterBOQByRoom")

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(c)

print("Done.")
