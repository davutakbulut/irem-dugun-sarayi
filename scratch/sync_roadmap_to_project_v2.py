import subprocess
import json
import urllib.request
import os

# Fetch token from git credential helper or ~/.env
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

# Query Project V2 details for project number 1 and 2
project_query = """
query {
  user(login: "davutakbulut") {
    projectV2(number: 1) {
      id
      title
      fields(first: 20) {
        nodes {
          ... on ProjectV2SingleSelectField {
            id
            name
            options {
              id
              name
            }
          }
        }
      }
    }
  }
}
"""

res = run_query(project_query)
print("PROJECT_FIELDS:", json.dumps(res, indent=2, ensure_ascii=False))
