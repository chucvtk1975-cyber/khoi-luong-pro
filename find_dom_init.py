import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app.js', 'r', encoding='utf-8') as f:
    c = f.read()

# Tim doan DOMContentLoaded dau tien
idx = c.find('DOMContentLoaded')
print(f"DOMContentLoaded at: {idx}")
print(c[idx:idx+100])

# Tim vi tri de them dom-fix (truoc khi init bat ky gi)
# Tim dau cua function init chinh hoac cuoi file app.js
idx_end = len(c) - 200
print(f"\nEnd of app.js ({len(c)} bytes):")
print(c[-300:].replace('\r\n', '\n')[:300])
