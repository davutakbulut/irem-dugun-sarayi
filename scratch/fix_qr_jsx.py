with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_qr_grid = """                  {[...Array(25)].map((_, i) => (
                    <div key={i} className={`rounded-xs ${i % 2 === 0 ? 'bg-white' : 'bg-amber-500'}`} />
                  ))}"""

new_qr_grid = """                  {Array.from({ length: 25 }).map((_, i) => (
                    <div key={i} className={i % 2 === 0 ? 'rounded-xs bg-white' : 'rounded-xs bg-amber-500'} />
                  ))}"""

if old_qr_grid in html:
    html = html.replace(old_qr_grid, new_qr_grid)
    print('Fixed JSX template literal in PDF QR Grid!')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
