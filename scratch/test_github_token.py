import subprocess
import json
import urllib.request
import os

# Try loading from ~/.env if exists
env_path = os.path.expanduser("~/.env")
token = None

if os.path.exists(env_path):
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("GITHUB_TOKEN="):
                token = line.strip().split("=", 1)[1].strip('"\'')

# If token not in .env, try getting token from git credential helper (osxkeychain)
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
        print("Credential helper error:", e)

if not token:
    print("NO_TOKEN_FOUND")
    exit(1)

# Test GraphQL API to query User Projects (v2) for davutakbulut
graphql_query = {
    "query": """
    query {
      user(login: "davutakbulut") {
        projectsV2(first: 5) {
          nodes {
            id
            title
            number
            url
          }
        }
      }
    }
    """
}

req = urllib.request.Request("https://api.github.com/graphql", data=json.dumps(graphql_query).encode('utf-8'))
req.add_header("Authorization", f"Bearer {token}")
req.add_header("Content-Type", "application/json")
req.add_header("User-Agent", "Antigravity-AI")

try:
    with urllib.request.urlopen(req) as resp:
        res_data = json.loads(resp.read().decode('utf-8'))
        print("API_SUCCESS:", json.dumps(res_data, indent=2, ensure_ascii=False))
except Exception as e:
    print("API_ERROR:", e)
