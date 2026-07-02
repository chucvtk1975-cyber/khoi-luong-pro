# -*- coding: utf-8 -*-
with open("d:/Kho tri thức/du-toan/app.js", "r", encoding="utf-8") as f:
    lines = f.readlines()

for idx, line in enumerate(lines):
    if "blkDetail" in line:
        if "function" in line or "const" in line or "let" in line or "var" in line or "=>" in line:
            print(f"Line {idx+1}: {line.strip()}")
