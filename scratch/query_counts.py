import urllib.request
import json

req = urllib.request.Request("http://localhost:8001/api/system-settings")
with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read().decode('utf-8'))

users = data.get("users", [])
customers = data.get("customers", [])

print(f"=== DB USERS COUNT: {len(users)} ===")
for i, u in enumerate(users, 1):
    print(f"{i}. Name: {u.get('name')} | Email: {u.get('email')} | Role: {u.get('role')} ({u.get('roleName', '')})")

print(f"\n=== DB CUSTOMERS COUNT: {len(customers)} ===")
for i, c in enumerate(customers, 1):
    print(f"{i}. Name: {c.get('name')} | Email: {c.get('email', '-')} | Phone: {c.get('phone', '-')}")
