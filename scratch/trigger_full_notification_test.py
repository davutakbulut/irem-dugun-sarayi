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
    r'<!-- 📲 LIVE GITHUB MOBILE NOTIFICATION TEST COMMIT: .*? -->',
    f'<!-- 📲 REBOOTED PHONE NOTIFICATION TEST: {now_str} for @davutakbulut -->',
    content
)

with open(md_path, "w", encoding="utf-8") as f:
    f.write(content)

# 2. Add 3 items to Project #2 mentioning @davutakbulut
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

def run_query(query, variables=None):
    payload = {"query": query}
    if variables:
        payload["variables"] = variables
    req = urllib.request.Request("https://api.github.com/graphql", data=json.dumps(payload).encode('utf-8'))
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Content-Type", "application/json")
    req.add_header("User-Agent", "Antigravity-AI")
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode('utf-8'))

project_id = "PVT_kwHOAsupAs4BfH1c"  # Project #2 (Rezervasyon Sistemi - v1)
status_field_id = "PVTSSF_lAHOAsupAs4BfH1czhZdAUM"

# Add 3 test items mentioning @davutakbulut
test_items = [
    {"title": "🔔 [BİLDİRİM TESTİ #1] Sürükle-Bırak Tarih Güncelleme İkazı - @davutakbulut", "status": "47fc9ee4"}, # In progress
    {"title": "🔔 [BİLDİRİM TESTİ #2] SMS Otomatik İptal ve Bilgilendirme Servisi - @davutakbulut", "status": "f75ad846"}, # Backlog
    {"title": "🔔 [BİLDİRİM TESTİ #3] QR Kodlu Masaya Sipariş Sistemi Entegrasyonu - @davutakbulut", "status": "f75ad846"}  # Backlog
]

add_item_mutation = """
mutation($projectId: ID!, $title: String!) {
  addProjectV2DraftIssue(input: {projectId: $projectId, title: $title}) {
    projectItem {
      id
    }
  }
}
"""

set_status_mutation = """
mutation($projectId: ID!, $itemId: ID!, $fieldId: ID!, $singleSelectOptionId: String!) {
  updateProjectV2ItemFieldValue(
    input: {
      projectId: $projectId
      itemId: $itemId
      fieldId: $fieldId
      value: { singleSelectOptionId: $singleSelectOptionId }
    }
  ) {
    projectV2Item {
      id
    }
  }
}
"""

for item in test_items:
    try:
        res = run_query(add_item_mutation, {"projectId": project_id, "title": item["title"]})
        item_id = res["data"]["addProjectV2DraftIssue"]["projectItem"]["id"]
        run_query(set_status_mutation, {
            "projectId": project_id,
            "itemId": item_id,
            "fieldId": status_field_id,
            "singleSelectOptionId": item["status"]
        })
        print(f"Added Project Card with @davutakbulut mention: {item['title']}")
    except Exception as e:
        print("Error adding project item:", e)

print("Full notification test trigger complete!")
