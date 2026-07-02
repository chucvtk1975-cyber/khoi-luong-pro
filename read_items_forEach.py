import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app.js', 'r', encoding='utf-8') as f:
    c = f.read()

# Doc tiep phan items.forEach trong CHI TIET sheet
chi_tiet_pos = c.find('BẢNG CHI TIẾT KHỐI LƯỢNG')
# Tim "calc.items.forEach" sau CHI_TIET_POS
item_forEach = c.find('calc.items.forEach', chi_tiet_pos)
print(f"items.forEach at: {item_forEach}")

chunk = c[item_forEach:item_forEach+9000]
lines = [l.strip() for l in chunk.split('\n') if l.strip()]
print("\n=== items.forEach code in CHI TIẾT ===")
for l in lines[:130]:
    print(l[:130])
