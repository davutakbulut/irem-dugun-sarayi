import sys

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Remove find-skills line from vercelSkillsList
old_item = "          { name: 'find-skills', desc: 'Açık ajan ekosisteminden yeni yetenek arama ve bağlama.' },\n"
if old_item in html:
    html = html.replace(old_item, '')
    print("Removed find-skills from vercelSkillsList successfully!")
else:
    print("Could not find old_item in vercelSkillsList!")

# Update 10 -> 9 in headers and counts
html = html.replace("10 adet Vercel Labs Ajan Yeteneğinin", "9 adet Vercel Labs Ajan Yeteneğinin")
html = html.replace("🚀 10 Vercel Ajan Skills", "🚀 9 Vercel Ajan Skills")
html = html.replace("🚀 10 Adet Vercel Labs Ajan Yeteneği", "🚀 9 Adet Vercel Labs Ajan Yeteneği")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html System Guide page find-skills removal successfully!")
