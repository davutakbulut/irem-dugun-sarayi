import subprocess
import json
import urllib.request
import ssl
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
    context = ssl._create_unverified_context()
    with urllib.request.urlopen(req, context=context) as resp:
        return json.loads(resp.read().decode('utf-8'))

project_id = "PVT_kwHOAsupAs4BfH1c"

query = """
query($projectId: ID!) {
  node(id: $projectId) {
    ... on ProjectV2 {
      items(first: 100) {
        nodes {
          id
          content {
            ... on DraftIssue {
              id
              title
              body
            }
          }
        }
      }
    }
  }
}
"""

res = run_query(query, {"projectId": project_id})
items = res["data"]["node"]["items"]["nodes"]
print(f"Found {len(items)} items on Project #2 board:")
for item in items[:5]:
    c = item.get("content", {})
    print("Item ID:", item["id"], "| Draft ID:", c.get("id"), "| Title:", c.get("title"))
