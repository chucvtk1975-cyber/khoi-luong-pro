import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app.js', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Doc phan parse note (vi tri 24000-29000 trong app.js)
print("=== Note parsing code (24000-29500) ===")
chunk = c[24000:29500]
lines = [l.strip() for l in chunk.split('\n') if l.strip()]
for l in lines[:80]:
    print(l[:130])

print("\n\n=== noteItem in CALC.room (134000-136000) ===")
chunk2 = c[133000:137000]
lines2 = [l.strip() for l in chunk2.split('\n') if l.strip()]
for l in lines2[:60]:
    print(l[:130])
