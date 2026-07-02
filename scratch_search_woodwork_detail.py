# -*- coding: utf-8 -*-
with open("d:/Kho tri thức/du-toan/app.js", "r", encoding="utf-8") as f:
    lines = f.readlines()

with open("d:/Kho tri thức/du-toan/scratch_search_woodwork_out.txt", "w", encoding="utf-8") as out:
    for idx, line in enumerate(lines):
        if "noteWoodwork" in line or "notePlumbing" in line or "noteWaterproof" in line:
            out.write(f"Line {idx+1}: {line.strip()}\n")

print("Saved output to scratch_search_woodwork_out.txt")
