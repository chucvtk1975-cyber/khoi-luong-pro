import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app.js', 'r', encoding='utf-8') as f:
    c = f.read()

# Doc tung OC_TEMPLATE definition
positions = [233552, 303073, 521550, 601717, 644033, 663144]

for pos in positions:
    # Tim bat dau "const OC_TEMPLATE" hoac "const OC_T"
    actual_pos = c.find('const OC_T', pos - 20)
    if actual_pos < 0 or abs(actual_pos - pos) > 50:
        actual_pos = pos
    
    chunk = c[actual_pos:actual_pos+800]
    lines = chunk.split('\n')
    real = [l for l in lines if l.strip()]
    print(f'\n{"="*60}')
    print(f'=== OC definition at ~{pos} ===')
    print('\n'.join(real[:20]))
