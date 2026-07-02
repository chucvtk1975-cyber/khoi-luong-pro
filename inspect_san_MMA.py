import openpyxl

wb = openpyxl.load_workbook('du-toan/FILE MẪU.xlsx')
ws = wb['sàn MMA']

with open('du-toan/inspect_san_MMA.txt', 'w', encoding='utf-8') as f:
    for r in range(1, 45):
        vals = [ws.cell(row=r, column=c).value for c in range(1, 11)]
        f.write(f"Row {r:02d}: {vals}\n")
