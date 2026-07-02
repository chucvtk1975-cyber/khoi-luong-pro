#!/usr/bin/env python3
# fix_nostt.py
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

FILE = r"d:\Kho tri thức\du-toan\app.js"

OLD = "const noStt     = ['perimeter','window','ceilPerim','elec','elecManual','elecHeader','noteHeader'].includes(item.surface);"
NEW = "const noStt     = ['perimeter','window','ceilPerim','elec','elecManual','elecHeader','noteHeader','noteItem'].includes(item.surface);"

with open(FILE, 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

count = content.count(OLD)
print(f"Found OLD string: {count} times")

if count == 0:
    print("NOT FOUND! Trying partial match...")
    partial = "['perimeter','window','ceilPerim','elec','elecManual','elecHeader','noteHeader'].includes(item.surface)"
    c2 = content.count(partial)
    print(f"  Partial match: {c2} times")
    if c2 > 0:
        idx = content.find(partial)
        line_no = content[:idx].count('\n') + 1
        print(f"  At line: ~{line_no}")
        print(f"  Context: {repr(content[idx-50:idx+len(partial)+10])}")
elif count == 1:
    new_content = content.replace(OLD, NEW, 1)
    with open(FILE, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("SUCCESS: Fixed noteItem noStt in renderBOQ!")
    print(f"  OLD: {OLD}")
    print(f"  NEW: {NEW}")
else:
    print(f"WARNING: {count} matches found - manual check needed")
