import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app.js', 'r', encoding='utf-8') as f:
    c = f.read()

# Xac nhan fix da duoc ap dung
start = c.find('function filterBOQByRoom')
chunk = c[start:start+15000]

# Tim phan xu ly row trong forEach
idx = chunk.find('const kr = row.dataset.kr')
print("=== Code around !kr check ===")
print(chunk[idx:idx+800])
