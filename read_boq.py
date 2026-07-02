import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app.js', 'r', encoding='utf-8') as f:
    c = f.read()

# Doc tiep tu vi tri 205000
chunk = c[205000:210000]
lines = [l.strip() for l in chunk.split('\n') if l.strip()]
print("=== Code 205000-210000 ===")
for l in lines[:80]:
    print(l[:130])
