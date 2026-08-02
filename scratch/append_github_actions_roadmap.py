import json

# Read existing 100 roadmap items
json_path = "scratch/system_roadmap_100_items.json"
with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

existing_items = data["items"]

# GitHub Actions & DevOps recommendations from user screenshot
github_action_items = [
    {
        "id": 101,
        "category": "GitHub Actions & CI/CD Dağıtımı",
        "title": "Node.js CI/CD Otomasyonu & Test İş Akışı",
        "desc": "Her git push işleminde Node.js bağımlılıklarını, build sürecini ve otomatik testleri çalıştıran GitHub Actions CI iş akışı.",
        "status": "⏳ Eklenme Bekliyor (Yol Haritasında)"
    },
    {
        "id": 102,
        "category": "GitHub Actions & CI/CD Dağıtımı",
        "title": "Webpack & Frontend Otomatik Bundle Derleme İş Akışı",
        "desc": "Frontend React ve JavaScript varlıklarının GitHub Actions üzerinde otomatik Webpack ile minifiye edilip paketlenmesi.",
        "status": "⏳ Eklenme Bekliyor (Yol Haritasında)"
    },
    {
        "id": 103,
        "category": "GitHub Actions & CI/CD Dağıtımı",
        "title": "SLSA OpenSSF Yazılım Tedarik Zinciri Güvenlik Jeneratörü",
        "desc": "Yazılım paketlerinin ve bağımlılıkların güvenliğini onaylayan OpenSSF SLSA güvenlik bildirim jeneratörü entegrasyonu.",
        "status": "⏳ Eklenme Bekliyor (Yol Haritasında)"
    },
    {
        "id": 104,
        "category": "GitHub Actions & CI/CD Dağıtımı",
        "title": "Docker Konteyner İmajı Oluşturma ve Registry Dağıtımı",
        "desc": "Projenin Docker imajının GitHub Actions ile otomatik derlenip GitHub Container Registry (GHCR) deposuna yüklenmesi.",
        "status": "⏳ Eklenme Bekliyor (Yol Haritasında)"
    },
    {
        "id": 105,
        "category": "GitHub Actions & CI/CD Dağıtımı",
        "title": "Python Paket Yönetimi & Anaconda Çoklu Sürüm Matrisi",
        "desc": "Backend Python servislerinin (serve_fast_3g.py) farklı Python sürümlerinde otomatik test edilmesi için Anaconda CI matrisi.",
        "status": "⏳ Eklenme Bekliyor (Yol Haritasında)"
    },
    {
        "id": 106,
        "category": "GitHub Actions & CI/CD Dağıtımı",
        "title": "Node.js & npm Paket Yayınlama Otomasyonu",
        "desc": "Sistem modüllerinin ve istemci kütüphanelerinin npm veya GitHub Packages üzerinde versiyonlanarak otomatik yayınlanması.",
        "status": "⏳ Eklenme Bekliyor (Yol Haritasında)"
    },
    {
        "id": 107,
        "category": "GitHub Actions & CI/CD Dağıtımı",
        "title": "Python PyPI Paket Yayınlama Pipeline'ı",
        "desc": "Sistem yardımcı kütüphanelerinin ve veri işleme araçlarının PyPI deposuna GitHub Actions ile otomatik yüklenmesi.",
        "status": "⏳ Eklenme Bekliyor (Yol Haritasında)"
    },
    {
        "id": 108,
        "category": "GitHub Actions & CI/CD Dağıtımı",
        "title": "Azure Web App Otomatik Dağıtım İş Akışı (Azure CI/CD)",
        "desc": "Node.js ve Python backend servislerinin Microsoft Azure Web Apps sunucularına GitHub Actions ile otomatik dağıtımı.",
        "status": "⏳ Eklenme Bekliyor (Yol Haritasında)"
    },
    {
        "id": 109,
        "category": "GitHub Actions & CI/CD Dağıtımı",
        "title": "Azure Functions Sunucusuz (Serverless) Dağıtım Pipeline'ı",
        "desc": "Arka plan medya dönüştürme ve bildirim servislerinin Azure Functions üzerine GitHub Actions ile aktarılması.",
        "status": "⏳ Eklenme Bekliyor (Yol Haritasında)"
    },
    {
        "id": 110,
        "category": "GitHub Actions & CI/CD Dağıtımı",
        "title": "Amazon ECS & AWS Fargate Konteyner Otomatik Yayınlama",
        "desc": "Docker konteynerlerinin AWS ECS / Fargate bulut altyapısına GitHub Actions aracılığıyla sıfır kesintiyle canlıya alınması.",
        "status": "⏳ Eklenme Bekliyor (Yol Haritasında)"
    },
    {
        "id": 111,
        "category": "GitHub Actions & CI/CD Dağıtımı",
        "title": "Google Cloud GKE (Kubernetes Engine) Otomatik Derleme ve Dağıtım",
        "desc": "Google Cloud üzerindeki Kubernetes kümelerine (GKE) Docker konteynerlerinin GitHub Actions ile otomatik dağıtılması.",
        "status": "⏳ Eklenme Bekliyor (Yol Haritasında)"
    },
    {
        "id": 112,
        "category": "GitHub Actions & CI/CD Dağıtımı",
        "title": "Terraform Infrastructure as Code (IaC) CI/CD Entegrasyonu",
        "desc": "Bulut sunucu ve veritabanı altyapı değişikliklerinin Terraform kodları ile GitHub Actions üzerinde otomatik doğrulanması.",
        "status": "⏳ Eklenme Bekliyor (Yol Haritasında)"
    },
    {
        "id": 113,
        "category": "GitHub Actions & CI/CD Dağıtımı",
        "title": "Alibaba Cloud ACK Kubernetes Otomatik Dağıtım",
        "desc": "Asya bölgesi yedekleme sunucuları için Alibaba Cloud ACK Kubernetes ortamına GitHub Actions otomatik yayınlama.",
        "status": "⏳ Eklenme Bekliyor (Yol Haritasında)"
    },
    {
        "id": 114,
        "category": "GitHub Actions & CI/CD Dağıtımı",
        "title": "Django & Python Web Framework Test Otomasyonu",
        "desc": "Backend API servislerinin Django / Python test suite'i ile her PR ve push işleminde otomatik doğrulama testi.",
        "status": "⏳ Eklenme Bekliyor (Yol Haritasında)"
    },
    {
        "id": 115,
        "category": "GitHub Actions & CI/CD Dağıtımı",
        "title": "Datadog Sentetik İzleme ve Performans Pipeline'ı",
        "desc": "Canlı uygulamanın kullanıcı deneyimini ve tepki sürelerini Datadog Synthetic Monitoring ile GitHub Actions üzerinden sürekli test etme.",
        "status": "⏳ Eklenme Bekliyor (Yol Haritasında)"
    },
    {
        "id": 116,
        "category": "GitHub Actions & CI/CD Dağıtımı",
        "title": "Jekyll Static Site & Docker İmaj Paketleme İş Akışı",
        "desc": "Sistem dokümantasyonunun ve rehber sayfalarının Jekyll Docker container imajı olarak GitHub Actions ile derlenmesi.",
        "status": "⏳ Eklenme Bekliyor (Yol Haritasında)"
    }
]

# Combine items
all_items = existing_items + github_action_items

# Update JSON
with open(json_path, "w", encoding="utf-8") as f:
    json.dump({"total": len(all_items), "items": all_items}, f, ensure_ascii=False, indent=2)

# Update Markdown
md_path = "scratch/system_roadmap_100_items.md"
with open(md_path, "w", encoding="utf-8") as f:
    f.write(f"# 🏰 İrem Düğün Sarayı & Organizasyon Platformu — 116 Maddelik Geliştirme ve Eksiklik Yol Haritası\n\n")
    f.write(f"**Toplam Madde Sayısı:** {len(all_items)} Adet Somut Geliştirme ve CI/CD Kalemi\n")
    f.write(f"**Hedef:** Otonom Yapay Zeka Geliştirme Hattı (`task-2254` ve `architectural_evaluator_agent`) tarafından sırayla işlenmek üzere hazırlanmıştır.\n\n")
    f.write("---\n\n")
    
    current_cat = ""
    for item in all_items:
        if item["category"] != current_cat:
            current_cat = item["category"]
            f.write(f"\n## 📌 {current_cat}\n\n")
        status = item.get("status", "⏳ Eklenme Bekliyor")
        f.write(f"### {item['id']}. {item['title']}\n")
        f.write(f"- **Açıklama:** {item['desc']}\n")
        f.write(f"- **Durum:** {status}\n\n")

print(f"Successfully updated roadmap to {len(all_items)} items in {json_path} and {md_path}")
