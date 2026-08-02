import os
import sys
import json
import re
import time
import subprocess

# Automatically Auto-Increment System Version in db_system_settings.json on build
try:
    db_path = os.path.join(os.path.dirname(__file__), 'db_system_settings.json')
    if os.path.exists(db_path):
        with open(db_path, 'r', encoding='utf-8') as dbf:
            db_data = json.load(dbf)
        cur_v = db_data.get('systemVersion', 'v1.4.48')
        v_match = re.search(r'v?(\d+)\.(\d+)\.(\d+)', cur_v)
        if v_match:
            major, minor, patch = v_match.groups()
            new_v = f"v{major}.{minor}.{int(patch) + 1}"
            db_data['systemVersion'] = new_v
            db_data['lastUpdated'] = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
            
            # Add automatic changelog entry (reads from scratch/next_changelog.json if available, or env vars)
            changelog_info = {
                "title": os.environ.get('BUILD_CHANGELOG_TITLE', f"Sürüm Güncellemesi ({new_v})"),
                "desc": os.environ.get('BUILD_CHANGELOG_DESC', "Sistem mimarisi, UI/UX düzenlemeleri ve kod optimizasyonları yapıldı.")
            }
            next_cl_path = os.path.join(os.path.dirname(__file__), 'next_changelog.json')
            if os.path.exists(next_cl_path):
                try:
                    with open(next_cl_path, 'r', encoding='utf-8') as ncf:
                        next_cl = json.load(ncf)
                        changelog_info['title'] = next_cl.get('title', changelog_info['title'])
                        changelog_info['desc'] = next_cl.get('desc', changelog_info['desc'])
                    os.remove(next_cl_path)
                except Exception as e:
                    print("next_changelog error:", e)

            history = db_data.get('versionHistory', [])
            history.insert(0, {
                "version": new_v,
                "date": time.strftime('%d Ağustos %Y', time.localtime()),
                "title": changelog_info['title'],
                "desc": changelog_info['desc']
            })
            db_data['versionHistory'] = history[:15] # Keep last 15 entries
            
            with open(db_path, 'w', encoding='utf-8') as dbf:
                json.dump(db_data, dbf, indent=2, ensure_ascii=False)
            print(f"🚀 AUTO-INCREMENTED SYSTEM VERSION IN BACKEND DB: {cur_v} -> {new_v}")
except Exception as e:
    print("Auto-increment warning:", e)

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

scripts = re.findall(r'<script type="text/babel">(.*?)</script>', html, re.DOTALL)
if not scripts:
    print("No Babel script found in index.html")
    exit()

raw_jsx = '\n\n'.join(scripts)

js_code = f"""
if (typeof console === 'undefined') {{ var console = {{ error: function(){{}}, log: function(){{}} }}; }}

{open('scratch/babel.min.js', 'r', encoding='utf-8').read()}

var targetCode = {repr(raw_jsx)};

try {{
    var res = Babel.transform(targetCode, {{ presets: ['react'], compact: true }});
    res.code;
}} catch (err) {{
    "BABEL BUILD ERROR: " + err.message;
}}
"""

with open('scratch/compile_step.js', 'w', encoding='utf-8') as f:
    f.write(js_code)

print("Pre-compiling JSX via Babel standalone...")
res = subprocess.run(['osascript', '-l', 'JavaScript', 'scratch/compile_step.js'], capture_output=True, text=True)

compiled_js = res.stdout.strip() or res.stderr.strip()

if not compiled_js or "BABEL BUILD ERROR" in compiled_js or len(compiled_js) < 100000:
    print("Build failed or returned small output!")
    print("Output len:", len(compiled_js))
    print("Start:", compiled_js[:300])
    exit(1)

print(f"Pre-compilation SUCCESS! Compiled JS length: {len(compiled_js)} bytes")

# Save precompiled js to src/app.compiled.js
with open('src/app.compiled.js', 'w', encoding='utf-8') as f:
    f.write(compiled_js)

# Create index_prod.html
prod_html = html

# Remove babel.min.js script tag
prod_html = prod_html.replace('<script src="https://cdn.jsdelivr.net/npm/@babel/standalone@7.23.2/babel.min.js"></script>', '')

# Replace <script type="text/babel">...</script> with <script src="src/app.compiled.js?v=timestamp" defer></script>
old_tag_pattern = r'<script type="text/babel">.*?</script>'
new_script_tag = '<script src="src/app.compiled.js?v=' + str(int(time.time())) + '" defer></script>'

prod_html = re.sub(old_tag_pattern, new_script_tag, prod_html, flags=re.DOTALL)

with open('index_prod.html', 'w', encoding='utf-8') as f:
    f.write(prod_html)

print("Saved pre-compiled index_prod.html and src/app.compiled.js successfully!")
