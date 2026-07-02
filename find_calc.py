import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app.js', 'r', encoding='utf-8') as f:
    c = f.read()

# Tim CALC.room hoac ham tinh toan items
calc_room = c.find('CALC.room')
if calc_room < 0:
    calc_room = c.find("function calcRoom")
    if calc_room < 0:
        calc_room = c.find("items.push")
        
print(f"CALC/items at: {calc_room}")

# Tim noi tao items array
item_push = c.find("items.push")
print(f"First items.push at: {item_push}")

# Hieu structure: tim tat ca surface values duoc su dung
import re
surfaces = set(re.findall(r"surface:\s*['\"]([^'\"]+)['\"]", c))
print(f"\nAll surface values: {sorted(surfaces)}")

# Tim ham tao items cho room (CALC.room)
idx = c.find('CALC = {')
if idx < 0: idx = c.find('const CALC')
if idx < 0: idx = c.find('var CALC')
print(f"\nCALC definition at: {idx}")
if idx > 0:
    chunk = c[idx:idx+200]
    print(chunk[:300])
