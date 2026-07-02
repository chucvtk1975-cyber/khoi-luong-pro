import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('style.css', 'r', encoding='utf-8') as f:
    c = f.read()

# Tim .modal-card CSS block
idx = c.find('.modal-card {')
block_end = c.find('}', idx) + 1
old_card_css = c[idx:block_end]
print("=== Current .modal-card ===")
print(old_card_css)

# Tim .modal-room-card
idx2 = c.find('.modal-room-card {')
if idx2 > 0:
    block2_end = c.find('}', idx2) + 1
    old_room_css = c[idx2:block2_end]
    print("=== Current .modal-room-card ===")
    print(old_room_css)

# Tim @media mobile section
idx3 = c.find('@media (max-width:')
if idx3 > 0:
    print(f"\n=== Mobile media query at {idx3} ===")
    print(c[idx3:idx3+300])
