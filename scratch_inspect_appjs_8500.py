# -*- coding: utf-8 -*-
with open("d:/Kho tri thức/du-toan/app.js", "r", encoding="utf-8") as f:
    lines = f.readlines()

with open("d:/Kho tri thức/du-toan/scratch_inspect_appjs_8500.txt", "w", encoding="utf-8") as out:
    for idx in range(8499, min(8650, len(lines))):
        out.write(f"{idx+1}: {lines[idx]}")

print("Saved output to scratch_inspect_appjs_8500.txt")
