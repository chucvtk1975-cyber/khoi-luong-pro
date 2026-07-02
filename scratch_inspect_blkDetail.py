# -*- coding: utf-8 -*-
with open("d:/Kho tri thức/du-toan/app.js", "r", encoding="utf-8") as f:
    content = f.read()

import re
matches = re.finditer(r"function\s+blkDetail\b", content)
for m in matches:
    start = m.start()
    line_no = content[:start].count("\n") + 1
    print(f"blkDetail defined at line: {line_no}")
    
# Let's also print lines 6760-6780 of app.js to be absolutely sure of index mappings
with open("d:/Kho tri thức/du-toan/scratch_inspect_blkDetail_out.txt", "w", encoding="utf-8") as out:
    lines = content.splitlines()
    for idx in range(6750, min(6790, len(lines))):
        out.write(f"{idx+1}: {lines[idx]}\n")
