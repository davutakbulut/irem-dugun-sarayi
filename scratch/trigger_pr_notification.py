import subprocess
import json
import urllib.request
import os
import datetime

now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# 1. Create a test branch and commit
branch_name = f"test/notification-pr-{datetime.datetime.now().strftime('%H%M%S')}"

try:
    subprocess.run(["git", "checkout", "-b", branch_name], check=True, cwd=os.getcwd())
    
    # Touch board file
    md_path = "scratch/GITHUB_PROJECTS_BOARD.md"
    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()

    import re
    content = re.sub(
        r'<!-- 📲 FRESH MOBILE NOTIFICATION TEST #2: .*? -->',
        f'<!-- 📲 LIVE PULL REQUEST MOBILE NOTIFICATION TEST: {now_str} for @davutakbulut -->',
        content
    )
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(content)

    subprocess.run(["git", "add", "scratch/GITHUB_PROJECTS_BOARD.md"], check=True, cwd=os.getcwd())
    subprocess.run(["git", "commit", "-m", f"test(pr): @davutakbulut için Canlı Pull Request Mobil Bildirim Testi #{now_str}"], check=True, cwd=os.getcwd())
    subprocess.run(["git", "push", "origin", branch_name], check=True, cwd=os.getcwd())
    
    # Switch back to main
    subprocess.run(["git", "checkout", "main"], check=True, cwd=os.getcwd())
    print("Test branch pushed:", branch_name)
except Exception as e:
    print("Git branch error:", e)

# 2. Create Pull Request via REST API
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
    url = "https://api.github.com/repos/davutakbulut/irem-dugun-sarayi/pulls"
    payload = {
        "title": f"🚨 PULL REQUEST MOBİL PUSH BİLDİRİMİ TESTİ — @davutakbulut ({now_str})",
        "body": f"""## 🚀 Canlı Pull Request Mobil Push Bildirimi Testi

Sayın @davutakbulut,

Telefonunuzdaki **GitHub Mobile** uygulamasının kilit ekranı (Lock-screen) push bildirimini %100 zorunlu tetiklemek amacıyla resmi **Pull Request** açılmıştır.

- **Tarih:** {now_str}
- **Atanan Reviewer:** @davutakbulut
- **Dal:** {branch_name} ➔ main
""",
        "head": branch_name,
        "base": "main"
    }
    req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), method='POST')
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Content-Type", "application/json")
    req.add_header("User-Agent", "Antigravity-AI")
    try:
        with urllib.request.urlopen(req) as resp:
            res_data = json.loads(resp.read().decode('utf-8'))
            pr_url = res_data.get("html_url")
            print("PR_CREATED_SUCCESS:", pr_url)
            
            # Request review from @davutakbulut
            pr_number = res_data.get("number")
            review_url = f"https://api.github.com/repos/davutakbulut/irem-dugun-sarayi/pulls/{pr_number}/requested_reviewers"
            rev_payload = {"reviewers": ["davutakbulut"]}
            req_rev = urllib.request.Request(review_url, data=json.dumps(rev_payload).encode('utf-8'), method='POST')
            req_rev.add_header("Authorization", f"Bearer {token}")
            req_rev.add_header("Content-Type", "application/json")
            req_rev.add_header("User-Agent", "Antigravity-AI")
            with urllib.request.urlopen(req_rev) as r_resp:
                print("REVIEW_REQUESTED_SUCCESS!")
    except Exception as e:
        print("PR_ERROR:", e)

print("PR Notification Test Script Complete!")
