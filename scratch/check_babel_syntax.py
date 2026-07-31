import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

scripts = re.findall(r'<script type="text/babel">(.*?)</script>', html, re.DOTALL)
if scripts:
    code = scripts[0]
    print('Babel script lines:', len(code.split('\n')))
    print('Backtick count:', code.count('`'), 'Even:', code.count('`') % 2 == 0)
    print('Double quotes count:', code.count('"'))
    print('Single quotes count:', code.count("'"))
