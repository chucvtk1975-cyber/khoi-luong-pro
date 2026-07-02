import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app.js', 'r', encoding='utf-8') as f:
    c = f.read()

# Tim ket thuc cua calc.items.forEach trong CHI TIET sheet
chi_tiet_pos = c.find('BẢNG CHI TIẾT KHỐI LƯỢNG')
item_forEach = c.find('calc.items.forEach', chi_tiet_pos)

# Doc 12000 ky tu tu dau forEach
chunk = c[item_forEach:item_forEach+12000]

# Tim "})" ket thuc forEach
# Dem do sau ngoac don de tim ket thuc
depth = 0
forEach_end = -1
i = 0
while i < len(chunk):
    if chunk[i] == '(':
        depth += 1
    elif chunk[i] == ')':
        depth -= 1
        if depth == 0:
            forEach_end = i
            break
    i += 1

print(f"forEach ends at chunk pos: {forEach_end}")
print(f"Absolute pos: {item_forEach + forEach_end}")

# In 500 ky tu truoc va sau ket thuc forEach
print("\n=== Code AROUND end of forEach ===")
context = chunk[forEach_end-100:forEach_end+500]
lines = [l.strip() for l in context.split('\n') if l.strip()]
for l in lines[:30]:
    print(l[:130])
