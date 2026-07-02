import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app.js', 'r', encoding='utf-8') as f:
    c = f.read()

excel_start = c.find('function exportExcel()')

# Doc phan surface labels (emoji) - xung quanh vi tri +27000
chunk = c[excel_start + 27000 : excel_start + 35000]
lines = [l.strip() for l in chunk.split('\n') if l.strip()]
print("=== Surface labels area (excel +27000 to +35000) ===")
for l in lines[:100]:
    print(l[:130])
