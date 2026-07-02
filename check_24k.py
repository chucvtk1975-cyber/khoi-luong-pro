import sys
sys.stdout.reconfigure(encoding='utf-8')

# Tim va in noi dung thuc su xung quanh vi tri 24000-24600 trong file hien tai
with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

chunk = c[23800:24700]
lines = [l for l in chunk.split('\n') if l.strip()]
print("=== Content around pos 24000-24700 ===")
for l in lines:
    print(l[:120])
