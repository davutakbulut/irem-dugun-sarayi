import os

format_date_helper = """
    function formatDateForInput(val) {
      if (!val) return '';
      if (typeof val === 'string') {
        if (/^\d{4}-\d{2}-\d{2}$/.test(val)) return val;
        if (val.includes('T')) return val.split('T')[0];
        if (val.includes('.')) {
          const parts = val.split('.');
          if (parts.length === 3) {
            const d = parts[0].padStart(2, '0');
            const m = parts[1].padStart(2, '0');
            const y = parts[2].length === 2 ? '20' + parts[2] : parts[2];
            return `${y}-${m}-${d}`;
          }
        }
      }
      try {
        const dObj = new Date(val);
        if (!isNaN(dObj.getTime())) {
          const y = dObj.getFullYear();
          const m = String(dObj.getMonth() + 1).padStart(2, '0');
          const d = String(dObj.getDate()).padStart(2, '0');
          return `${y}-${m}-${d}`;
        }
      } catch(e) {}
      return String(val).substring(0, 10);
    }
"""

files = ['index.html', 'yonetim.html', 'yonetim/index.html', 'dist/index.html']

for f_path in files:
    if not os.path.exists(f_path):
        continue
    with open(f_path, 'r', encoding='utf-8') as f:
        content = f.read()

    if "function formatDateForInput(" not in content:
        marker = "    function generateDraftRefKey() {"
        marker_idx = content.find(marker)
        if marker_idx != -1:
            content = content[:marker_idx] + format_date_helper + "\n" + content[marker_idx:]
            with open(f_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Successfully added formatDateForInput to {f_path}!")
        else:
            print(f"Marker not found in {f_path}!")
    else:
        print(f"formatDateForInput already exists in {f_path}!")
