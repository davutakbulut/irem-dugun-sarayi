import subprocess
import json
import urllib.request
import ssl
import os
import re

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
    print("ERROR: GitHub token not found!")
    exit(1)

def run_query(query, variables=None):
    payload = {"query": query}
    if variables:
        payload["variables"] = variables
    req = urllib.request.Request("https://api.github.com/graphql", data=json.dumps(payload).encode('utf-8'))
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Content-Type", "application/json")
    req.add_header("User-Agent", "Antigravity-AI")
    context = ssl._create_unverified_context()
    with urllib.request.urlopen(req, context=context) as resp:
        return json.loads(resp.read().decode('utf-8'))

project_id = "PVT_kwHOAsupAs4BfH1c"
status_field_id = "PVTSSF_lAHOAsupAs4BfH1czhZdAUM"

status_options = {
    "Backlog": "f75ad846",
    "In progress": "47fc9ee4",
    "Done": "98236657"
}

# Fetch all items on Project #2
fetch_query = """
query($projectId: ID!) {
  node(id: $projectId) {
    ... on ProjectV2 {
      items(first: 100) {
        nodes {
          id
          fieldValueByName(name: "Status") {
            ... on ProjectV2ItemFieldSingleSelectValue {
              name
              optionId
            }
          }
          content {
            ... on DraftIssue {
              id
              title
            }
          }
        }
      }
    }
  }
}
"""

res = run_query(fetch_query, {"projectId": project_id})
items = res["data"]["node"]["items"]["nodes"]

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

done_items = []
in_progress_items = []
backlog_items = []
fixed_count = 0

for it in items:
    content = it.get("content", {})
    title = content.get("title", "")
    item_id = it["id"]
    current_status = it.get("fieldValueByName", {}) or {}
    current_opt = current_status.get("optionId", "")
    current_name = current_status.get("name", "Unknown")

    # Extract item number
    match = re.search(r"Madde #(\d+)", title)
    if match:
        item_num = int(match.group(1))
    else:
        continue

    # Determine target status option
    if item_num <= 7:
        target_opt = status_options["Done"]
        target_name = "Done"
        done_items.append(f"Madde #{item_num}")
    elif item_num == 8:
        target_opt = status_options["In progress"]
        target_name = "In progress"
        in_progress_items.append(f"Madde #{item_num}")
    else:
        target_opt = status_options["Backlog"]
        target_name = "Backlog"
        backlog_items.append(f"Madde #{item_num}")

    # Fix status if mismatched
    if current_opt != target_opt:
        try:
            run_query(set_status_mutation, {
                "projectId": project_id,
                "itemId": item_id,
                "fieldId": status_field_id,
                "singleSelectOptionId": target_opt
            })
            fixed_count += 1
            print(f"FIXED Madde #{item_num}: Moved from {current_name} -> {target_name}")
        except Exception as e:
            print(f"Error fixing Madde #{item_num}: {e}")

print("=" * 60)
print(f"KANBAN COLUMN AUDIT COMPLETE!")
print(f"Total Fixed / Moved Cards: {fixed_count}")
print(f"🟢 DONE Column ({len(done_items)} items): {', '.join(done_items)}")
print(f"🟡 IN PROGRESS Column ({len(in_progress_items)} items): {', '.join(in_progress_items)}")
print(f"📋 BACKLOG Column ({len(backlog_items)} items): Madde #9 to #{max([int(x.split('#')[1]) for x in backlog_items] or [9])}")
print("=" * 60)
