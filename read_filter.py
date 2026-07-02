import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app.js', 'r', encoding='utf-8') as f:
    c = f.read()

# Xem toan bo filterBOQByRoom function
start = c.find('function filterBOQByRoom(roomId)')
end = c.find('\nfunction ', start + 100)
print(f'Function from {start} to {end}')
print(c[start:end])
