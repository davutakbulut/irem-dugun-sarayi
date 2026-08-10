import os

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix UserEditModal & UserProfileComponent password onChange handlers
bad_pattern = "if (errorMessage) setErrorMessage('');"

# Replace line 14045 (UserEditModal)
old_line_14045 = """<div><label className="font-bold block mb-1">Giriş Şifresi:</label><input type="password" value={password} onChange={e => { setPassword(e.target.value); if (errorMessage) setErrorMessage(''); }} placeholder="Şifre giriniz..." required className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 font-bold" /></div>"""
new_line_14045 = """<div><label className="font-bold block mb-1">Giriş Şifresi:</label><input type="password" value={password} onChange={e => setPassword(e.target.value)} placeholder="Şifre giriniz..." required className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 font-bold" /></div>"""

if old_line_14045 in content:
    content = content.replace(old_line_14045, new_line_14045)
    print("1. Fixed UserEditModal password onChange handler.")
else:
    print("WARNING: Could not find old_line_14045 in index.html!")

# Replace line 16936 (UserProfileComponent)
old_line_16936 = """                  onChange={e => { setPassword(e.target.value); if (errorMessage) setErrorMessage(''); }}"""
new_line_16936 = """                  onChange={e => setPassword(e.target.value)}"""

if old_line_16936 in content:
    content = content.replace(old_line_16936, new_line_16936)
    print("2. Fixed UserProfileComponent password onChange handler.")
else:
    print("WARNING: Could not find old_line_16936 in index.html!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('yonetim.html', 'w', encoding='utf-8') as f:
    f.write(content)

os.makedirs('dist', exist_ok=True)
with open('dist/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Synced index.html to yonetim.html and dist/index.html!")
