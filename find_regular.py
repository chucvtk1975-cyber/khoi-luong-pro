import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app.js', 'r', encoding='utf-8') as f:
    c = f.read()

# Tim "--- Regular items ---" va doc 1500 ky tu tiep theo
idx = c.find('// --- Regular items ---')
print(f"Regular items at: {idx}")
chunk = c[idx:idx+2000]
lines = [l.strip() for l in chunk.split('\n') if l.strip()]
for l in lines[:40]:
    print(l[:130])
    
# Tim "let subRomIdx"
idx2 = c.find('let subRomIdx')
print(f"\n\nsubRomIdx at: {idx2}")
print(repr(c[idx2:idx2+60]))
