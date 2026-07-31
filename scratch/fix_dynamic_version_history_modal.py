import sys

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace static releases array inside VersionHistoryModalComponent with dynamic releases from backend versionHistory prop
old_modal_releases_code = """      const releases = [
        {
          version: 'v1.5.0 (Yol Haritası)',"""

new_modal_releases_code = """      const dynamicReleases = (versionHistory && versionHistory.length > 0) ? versionHistory.map((item, idx) => ({
        version: item.version,
        tag: idx === 0 ? 'CANLI SON SÜRÜM' : 'SÜRÜM GÜNCELLEMESİ',
        date: item.date,
        title: item.title,
        color: idx === 0 ? 'bg-amber-500 font-extrabold shadow-md' : 'bg-emerald-500',
        changes: [item.desc]
      })) : [];

      const staticReleases = [
        {
          version: 'v1.5.0 (Yol Haritası)',"""

if old_modal_releases_code in html and "const dynamicReleases" not in html:
    html = html.replace(old_modal_releases_code, new_modal_releases_code)
    print("Added dynamicReleases mapping to VersionHistoryModalComponent!")

old_combine_releases = "const releases = ["
new_combine_releases = "const releases = [...dynamicReleases, "

if "const releases = [...dynamicReleases," not in html:
    html = html.replace("const staticReleases = [", "const staticReleases = [", 1)
    # Replace the rendering array
    html = html.replace("const releases = [", "const releases = [...dynamicReleases, ", 1)
    print("Combined dynamicReleases with staticReleases in VersionHistoryModalComponent!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated VersionHistoryModalComponent in index.html successfully!")
