import subprocess
import json
import urllib.request
import os

# Fetch token
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

if not token:
    print("NO_TOKEN_FOUND")
    exit(1)

# Create GitHub Issue via REST API
url = "https://api.github.com/repos/davutakbulut/irem-dugun-sarayi/issues"
payload = {
    "title": "📲 ANLIK MOBİL BİLDİRİM TESTİ — @davutakbulut",
    "body": """## 📲 Canlı GitHub Mobil Push Bildirimi Testi

Sayın @davutakbulut,

Bu GitHub Issue kartı, telefonunuzdaki **GitHub Mobile** uygulamasında kilit ekranı (lock-screen) push bildiriminin tetiklenmesi amacıyla otonom sistem tarafından üretilmiştir.

### 🤖 Otonom Sistem Sağlık Raporu:
- **Sistem Sürümü:** v1.5.04
- **Aktif Zamanlayıcı:** 5 Dakikalık Sessiz Hata Tarayıcısı (`task-2466`)
- **1 Saatlik Otonom Cron:** Aktif (`task-2569`)
- **Proje Panosu:** [https://github.com/users/davutakbulut/projects/2](https://github.com/users/davutakbulut/projects/2)
""",
    "assignees": ["davutakbulut"],
    "labels": ["notification-test", "automated"]
}

req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), method='POST')
req.add_header("Authorization", f"Bearer {token}")
req.add_header("Content-Type", "application/json")
req.add_header("User-Agent", "Antigravity-AI")

try:
    with urllib.request.urlopen(req) as resp:
        res_data = json.loads(resp.read().decode('utf-8'))
        print("ISSUE_SUCCESS:", res_data.get("html_url"))
except Exception as e:
    print("ISSUE_ERROR:", e)
