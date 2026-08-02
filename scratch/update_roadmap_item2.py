import json

with open("scratch/system_roadmap_100_items.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for item in data["items"]:
    if item["id"] == 2:
        item["status"] = "✅ Tamamlandı (v1.5.04)"

with open("scratch/system_roadmap_100_items.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Updated item #2 status in system_roadmap_100_items.json")
