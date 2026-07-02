import sys, re
sys.stdout.reconfigure(encoding='utf-8')
with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Tim link css
links = re.findall(r'href="([^"]+\.css)"', c)
print('CSS files:', links)

# Tim tat ca style blocks
styles = re.findall(r'<style[^>]*>(.*?)</style>', c, re.DOTALL)
print(f'Style blocks: {len(styles)}')
for i, s in enumerate(styles):
    if 'modal-footer' in s:
        idx = s.find('modal-footer')
        print(f'Block {i}: modal-footer CSS:')
        print(s[max(0,idx-100):idx+400])
