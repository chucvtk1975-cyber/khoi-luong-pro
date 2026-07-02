# -*- coding: utf-8 -*-
with open("d:/Kho tri thức/du-toan/app.js", "r", encoding="utf-8") as f:
    lines = f.readlines()

with open("d:/Kho tri thức/du-toan/scratch_web_preview_out.txt", "w", encoding="utf-8") as out:
    for idx in range(8609, min(8650, len(lines))):
        out.write(f"{idx+1}: {lines[idx]}")

print("Saved output to scratch_web_preview_out.txt")
