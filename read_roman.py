import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app.js', 'r', encoding='utf-8') as f:
    c = f.read()

# Doc doan code xung quanh vi tri 201495 (romanNums) va 203210 (roman const)
start = 201200
end   = 205000

chunk = c[start:end]
lines = [l.strip() for l in chunk.split('\n') if l.strip()]
print(f"=== Roman numeral code (pos {start}–{end}) ===")
for l in lines[:80]:
    print(l[:120])
