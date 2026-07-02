# -*- coding: utf-8 -*-
with open("d:/Kho tri thức/du-toan/app.js", "r", encoding="utf-8") as f:
    lines = f.readlines()

with open("d:/Kho tri thức/du-toan/scratch_woodwork_usage_out.txt", "w", encoding="utf-8") as out:
    out.write("--- Range 6720 to 6770 ---\n")
    for idx in range(6719, min(6770, len(lines))):
        out.write(f"{idx+1}: {lines[idx]}")

    out.write("\n\n--- Range 8570 to 8610 ---\n")
    for idx in range(8569, min(8610, len(lines))):
        out.write(f"{idx+1}: {lines[idx]}")

print("Saved output to scratch_woodwork_usage_out.txt")
