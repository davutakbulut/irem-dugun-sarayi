import json

# Read 116 roadmap items
json_path = "scratch/system_roadmap_100_items.json"
with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

items = data["items"]

todo_items = [i for i in items if "Tamamlandı" not in i.get("status", "")]
done_items = [i for i in items if "Tamamlandı" in i.get("status", "")]

board_md_path = "scratch/GITHUB_PROJECTS_BOARD.md"
with open(board_md_path, "w", encoding="utf-8") as f:
    f.write("# 📊 İrem Düğün Sarayı — GitHub Projects Live Kanban Board\n\n")
    f.write("Bu pano, otonom yapay zeka geliştirme hattı (`task-2254`) tarafından anlık olarak güncellenir.\n\n")
    f.write("---\n\n")
    
    f.write("## ✅ DONE (TAMAMLANAN YAPAY ZEKA GELİŞTİRMELERİ)\n\n")
    for item in done_items:
        f.write(f"- [x] **Madde #{item['id']}: {item['title']}** — Status: `{item.get('status')}`\n")
        f.write(f"  > *Açıklama:* {item['desc']}\n\n")
        
    f.write("\n## 🔄 IN PROGRESS (AKTİF GELİŞTİRİLEN VE TEST EDİLEN)\n\n")
    f.write("- [ ] **Madde #3: Sürüm & Değişiklik İkazı** — *Sıradaki Otomatik Yapay Zeka Görevi*\n\n")

    f.write("\n## 📋 TO DO (BEKLEYEN YOL HARİTASI MADDELERİ - TOTAL: " + str(len(todo_items)) + ")\n\n")
    for item in todo_items[:15]:  # Preview next 15 items
        f.write(f"- [ ] **Madde #{item['id']}: {item['title']}** ({item['category']})\n")
        f.write(f"  > {item['desc']}\n\n")
        
    if len(todo_items) > 15:
        f.write(f"\n*... ve {len(todo_items) - 15} adet diğer bekleyen yol haritası maddesi `system_roadmap_100_items.json` içerisinde kayıtlıdır.*\n")

print(f"Generated GitHub Projects Board in {board_md_path}")
