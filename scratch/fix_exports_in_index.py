import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace any export function, export const, export default in index.html
html = html.replace('export function ', 'function ')
html = html.replace('export const ', 'const ')
html = html.replace('export default ', '// export default ')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Successfully stripped all 'export' keywords from index.html!")
