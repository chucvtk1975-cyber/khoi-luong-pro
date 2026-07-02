import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('app.js', 'r', encoding='utf-8') as f:
    c = f.read()

marker = "wsDetail['!cols']"
idx = c.find(marker)
print('found at:', idx)
if idx > 0:
    print(repr(c[idx:idx+500]))

# Cũng tìm wsSum và wsVT cols để biết context
idx2 = c.find("wsSum['!cols']")
print('\nwsSum cols at:', idx2)
if idx2 > 0:
    print(repr(c[idx2:idx2+300]))
