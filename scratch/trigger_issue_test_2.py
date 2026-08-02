import subprocess
import json
import urllib.request
import os
import datetime

now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# 1. Update GITHUB_PROJECTS_BOARD.md
md_path = "scratch/GITHUB_PROJECTS_BOARD.md"
with open(md_path, "r", encoding="utf-8") as f:
    content = f.read()

import re
content = re.sub(
    r'<!-- 📲 REBOOTED PHONE NOTIFICATION TEST: .*? -->',
    f'<!-- 📲 FRESH MOBILE NOTIFICATION TEST #2: {now_str} for @davutakbulut -->',
    content
)

with open(md_path, "w", encoding="utf-8") as f:
    f.write(content)

# 2. Create Issue #2 via REST API
token = None
env_path = os.path.expanduser("~/.env")
if os.path.exists(env_path):
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("GITHUB_TOKEN="):
                token = line.strip().split("=", 1)[1].strip('"\'')

if not token:
    try:
        proc = subprocess.Popen(
            ["git", "credential", "fill"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        out, _ = proc.communicate("protocol=https\nhost=github.com\n\n")
        for line in out.splitlines():
            if line.startswith("password="):
                token = line.split("=", 1)[1].strip()
    except Exception as e:
        pass

if token:
    url = "https://api.github.com/repos/davutakbulut/irem-dugun-sarayi/issues"
    payload = {
        "title": f"🔔 YENİ MOBİL PUSH BİLDİRİMİ #{now_str} — @davutakbulut",
        "body": f"""## 📲 Anlık GitHub Mobil Push Bildirimi Testi #{now_str}

Sayın @davutakbulut,

Telefonunuza doğrudan yüksek öncelikli Kilit Ekranı (Lock-Screen) push bildirimi düşmesi amacıyla **GitHub Issue #2** kartı oluşturulmuş ve hesabınıza atanmıştır.

- **Tarih/Saat:** {now_str}
- **Atanan Kullanıcı:** @davutakbulut
- **Proje Panosu:** https://github.com/users/davutakbulut/projects/2
""",
        "assignees": ["davutakbulut"],
        "labels": ["mobile-notification-test"]
    }
    req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), method='POST')
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Content-Type", "application/json")
    req.add_header("User-Agent", "Antigravity-AI")
    try:
        with urllib.request.urlopen(req) as resp:
            res_data = json.loads(resp.read().decode('utf-8'))
            print("ISSUE_2_CREATED:", res_data.get("html_url"))
    except Exception as e:
        print("ISSUE_2_ERROR:", e)

print("Fresh notification test 2 completed!")
