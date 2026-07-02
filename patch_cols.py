import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app.js', 'r', encoding='utf-8') as f:
    c = f.read()

# Fix wsDetail cols: tìm và thay wch:5 (STT) và wch:36 (HANG MUC)
# theo đúng file mẫu: A=6.33, B=35
old1 = "{ wch: 5  },  // STT\n"
new1 = "{ wch: 6.33 },  // STT (A) - theo file mẫu\n"
if old1 in c:
    c = c.replace(old1, new1, 1)
    print("✓ STT width updated to 6.33")
else:
    print("✗ STT not found exactly")

old2 = "{ wch: 36 },  // HẠNG MỤC\n"
new2 = "{ wch: 35.0 },  // HẠNG MỤC (B) - theo file mẫu\n"
if old2 in c:
    c = c.replace(old2, new2, 1)
    print("✓ HANG MUC width updated to 35.0")
else:
    print("✗ HANG MUC not found - trying alternate")
    old2b = "{ wch: 36 },  // H"
    idx = c.find(old2b)
    print("  alt find:", idx)

# Tìm ĐƠN GIÁ / THÀNH TIỀN / ĐỊNH MỨC cuối wsDetail
old3 = "{ wch: 12 },  // ĐƠN GIÁ\n"
new3 = "{ wch: 13.41 },  // ĐƠN GIÁ (I) - theo file mẫu\n"
if old3 in c:
    c = c.replace(old3, new3, 1)
    print("✓ ĐƠN GIÁ width updated to 13.41")

old4 = "{ wch: 14 },  // THÀNH TIỀN\n"
new4 = "{ wch: 12.75 },  // THÀNH TIỀN (J) - theo file mẫu\n"
if old4 in c:
    c = c.replace(old4, new4, 1)
    print("✓ THÀNH TIỀN width updated to 12.75")

# Thêm sumColWidths theo file mẫu: A=6.33, B=35, rooms default, I=13.41, J=12.75
old5 = "const sumColWidths = [{ wch:5 }, { wch:32 }, { wch:6 }];\n"
new5 = "const sumColWidths = [{ wch:6.33 }, { wch:35.0 }, { wch:6 }];\n"
if old5 in c:
    c = c.replace(old5, new5, 1)
    print("✓ sumColWidths A,B updated")
else:
    # Try another variant
    old5b = "const sumColWidths = [{ wch:7 }, { wch:45 }, { wch:8 }];\n"
    if old5b in c:
        c = c.replace(old5b, "const sumColWidths = [{ wch:6.33 }, { wch:35.0 }, { wch:6 }];\n", 1)
        print("✓ sumColWidths v2 A,B updated")

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(c)

print("✅ col widths patch done")
