import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app.js', 'r', encoding='utf-8') as f:
    c = f.read()

# Tim dong set btn-save-room-label va them dong sync mobile label
old = "document.getElementById('btn-save-room-label').textContent  = isEdit ? 'Lưu Thay Đổi' : 'Thêm Phòng';"
new = """document.getElementById('btn-save-room-label').textContent  = isEdit ? 'Lưu Thay Đổi' : 'Thêm Phòng';
  const mobileLabel = document.getElementById('btn-save-room-label-mobile');
  if (mobileLabel) mobileLabel.textContent = isEdit ? 'Lưu Thay Đổi' : 'Thêm Phòng';"""

if old in c:
    c = c.replace(old, new, 1)
    print("✓ Mobile label sync added")
else:
    print("✗ Not found")

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(c)
print("✅ Done")
