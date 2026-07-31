import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

scripts = re.findall(r'<script type="text/babel">(.*?)</script>', html, re.DOTALL)
if scripts:
    code = scripts[0]
    lines = code.split('\n')
    
    for i in range(1034, 2612):
        if 'createPortal' in lines[i]:
            print(f'Line {i+1}: {lines[i]}')

