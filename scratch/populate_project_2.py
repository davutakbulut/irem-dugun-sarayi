import subprocess
import json
import urllib.request
import os

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

project_id = "PVT_kwHOAsupAs4BfH1c"  # Project #2: Rezervasyon Sistemi - v1
status_field_id = "PVTSSF_lAHOAsupAs4BfH1czhZdAUM"

STATUS_MAP = {
    "backlog": "f75ad846",
    "ready": "61e4505c",
    "in_progress": "47fc9ee4",
    "in_review": "df73e18b",
    "done": "98236657"
}

with open("scratch/system_roadmap_100_items.json", "r", encoding="utf-8") as f:
    roadmap = json.load(f)["items"]

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

count_success = 0

for item in roadmap[:30]:
    status = "backlog"
    if item["id"] in [1, 2]:
        status = "done"
    elif item["id"] == 3:
        status = "in_progress"

    title = f"Madde #{item['id']}: {item['title']}"
    
    try:
        res = run_query(add_item_mutation, {"projectId": project_id, "title": title})
        item_id = res["data"]["addProjectV2DraftIssue"]["projectItem"]["id"]
        
        opt_id = STATUS_MAP[status]
        run_query(set_status_mutation, {
            "projectId": project_id,
            "itemId": item_id,
            "fieldId": status_field_id,
            "singleSelectOptionId": opt_id
        })
        count_success += 1
        print(f"Added Item #{item['id']} to Project #2 (Rezervasyon Sistemi - v1) as [{status.upper()}]")
    except Exception as e:
        print(f"Error adding Item #{item['id']}:", e)

print(f"Successfully populated {count_success} items directly to Project #2 (Rezervasyon Sistemi - v1)!")
