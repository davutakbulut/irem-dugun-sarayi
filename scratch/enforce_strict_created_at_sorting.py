import os, re

html_files = ['index.html', 'yonetim.html', 'yonetim/index.html', 'dist/index.html']

old_func_block = """      // Helper to extract system creation timestamp
      const extractSystemTimestamp = (item) => {
        if (!item) return 0;
        if (item.recordTimestamp && Number(item.recordTimestamp) > 0) return Number(item.recordTimestamp);
        if (item.created_at) {
          const t = new Date(item.created_at).getTime();
          if (!isNaN(t) && t > 0) return t;
        }
        if (item.createdAt) {
          const t = new Date(item.createdAt).getTime();
          if (!isNaN(t) && t > 0) return t;
        }
        if (typeof item.id === 'string') {
          const match = item.id.match(/\\d{10,13}/);
          if (match) {
            const num = Number(match[0]);
            if (num > 1000000000) return num > 100000000000 ? num : num * 1000;
          }
        }
        if (item.date) {
          const t = new Date(item.date).getTime();
          if (!isNaN(t) && t > 0) return t;
        }
        return 0;
      };"""

new_func_block = """      // Helper to extract system creation timestamp strictly based on created_at / system entry time
      const extractSystemTimestamp = (item) => {
        if (!item) return 0;
        if (item.recordTimestamp && Number(item.recordTimestamp) > 0) return Number(item.recordTimestamp);
        if (item.created_at) {
          const t = new Date(item.created_at).getTime();
          if (!isNaN(t) && t > 0) return t;
        }
        if (item.createdAt) {
          const t = new Date(item.createdAt).getTime();
          if (!isNaN(t) && t > 0) return t;
        }
        if (typeof item.id === 'string') {
          const match = item.id.match(/\\d{10,13}/);
          if (match) {
            const num = Number(match[0]);
            if (num > 1000000000) return num > 100000000000 ? num : num * 1000;
          }
        }
        return 0;
      };"""

for h_file in html_files:
    if not os.path.exists(h_file):
        continue
    with open(h_file, 'r', encoding='utf-8') as f:
        content = f.read()

    if old_func_block in content:
        content = content.replace(old_func_block, new_func_block)
        print(f"Updated extractSystemTimestamp in {h_file}")
    else:
        print(f"old_func_block not found in {h_file}")

    with open(h_file, 'w', encoding='utf-8') as f:
        f.write(content)

print("Enforced strict created_at timestamp sorting across all files!")
