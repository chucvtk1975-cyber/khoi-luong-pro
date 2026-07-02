import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('app.js', 'r', encoding='utf-8') as f:
    c = f.read()

changes = 0

# 1. Them subRomIdx sau dong "const roman = romanNums[idx]..."
old1 = "const roman = romanNums[idx] || (idx + 1);"
new1 = "const roman = romanNums[idx] || (idx + 1);\n    let subRomIdx = 1; // sub-section Roman counter"
if old1 in c:
    c = c.replace(old1, new1, 1)
    print("✓ 1. subRomIdx added")
    changes += 1
else:
    print("✗ 1. romanNums line not found")

# 2. elecHeader - thay noi dung
old2 = "⚡ THIẾT BỊ ĐIỆN</td></tr>`;"
new2 = "${romanNums[subRomIdx++] || subRomIdx}. ⚡ THIẾT BỊ ĐIỆN</td></tr>`;"
if old2 in c:
    c = c.replace(old2, new2, 1)
    print("✓ 2. Roman added to elecHeader")
    changes += 1
else:
    print("✗ 2. elecHeader label not found")
    # debug
    idx = c.find('THIẾT BỊ ĐIỆN')
    if idx > 0:
        print(f"   THIẾT BỊ ĐIỆN found at {idx}: {repr(c[idx-30:idx+60])}")

# 3. noteHeader
old3 = "📝 CHI TIẾT TỪ GHI CHÚ</td></tr>`;"
new3 = "${romanNums[subRomIdx++] || subRomIdx}. 📝 CHI TIẾT TỪ GHI CHÚ</td></tr>`;"
if old3 in c:
    c = c.replace(old3, new3, 1)
    print("✓ 3. Roman added to noteHeader")
    changes += 1
else:
    print("✗ 3. noteHeader not found")
    idx3 = c.find('CHI TIẾT TỪ GHI CHÚ')
    if idx3 > 0:
        print(f"   found at {idx3}: {repr(c[idx3-30:idx3+60])}")

# 4. subHeader custom IN HOA - them subRom truoc html +=
# Tim "stt = 1; // reset STT" trong custom section
old4 = "stt = 1; // reset STT"
new4 = "stt = 1; // reset STT\n            const subRom = romanNums[subRomIdx++] || subRomIdx;"
if old4 in c:
    c = c.replace(old4, new4, 1)
    print("✓ 4. subRom declared for custom subHeader")
    changes += 1
else:
    print("✗ 4. 'reset STT' not found")

# 5. OC header - da duoc add o patch truoc (kiem tra)
if "${romanNums[subRomIdx] || (subRomIdx+1)}. 💰 CHI PHÍ KHÁC" in c:
    # Fix: phai tang subRomIdx sau khi dung
    old5 = "${romanNums[subRomIdx] || (subRomIdx+1)}. 💰 CHI PHÍ KHÁC — ${room.name}"
    new5 = "${romanNums[subRomIdx++] || subRomIdx}. 💰 CHI PHÍ KHÁC — ${room.name}"
    c = c.replace(old5, new5, 1)
    print("✓ 5. OC header Roman fixed (added ++)")
    changes += 1
else:
    print("? 5. OC header check - already correct or different format")

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(c)

print(f"\n✅ Done! {changes} changes applied.")
