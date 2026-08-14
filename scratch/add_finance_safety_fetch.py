import os

html_files = ['index.html', 'yonetim.html', 'yonetim/index.html', 'dist/index.html']

target = """      // Selected Month for Monthly Cashflow Report
      const [selectedReportMonth, setSelectedReportMonth] = useState('2026-08');

      useEffect(() => {
        setCurrentPage(1);
      }, [filterTab, searchQuery, activeSubTab, selectedReportMonth]);"""

replacement = """      // Selected Month for Monthly Cashflow Report
      const [selectedReportMonth, setSelectedReportMonth] = useState('2026-08');

      useEffect(() => {
        setCurrentPage(1);
      }, [filterTab, searchQuery, activeSubTab, selectedReportMonth]);

      // Direct MariaDB sync on Finance tab mount
      useEffect(() => {
        try {
          const fetchFn = window.fetchWithRetry || fetch;
          fetchFn('/api/expenses')
            .then(res => res.json())
            .then(data => {
              if (Array.isArray(data)) {
                setExpenses(data);
              }
            })
            .catch(() => {});
        } catch(e) {}
      }, []);"""

for h_file in html_files:
    if not os.path.exists(h_file):
        continue
    with open(h_file, 'r', encoding='utf-8') as f:
        content = f.read()

    if target in content:
        content = content.replace(target, replacement)
        with open(h_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Added safety fetch in {h_file}")
    else:
        print(f"target not found in {h_file}")

print("Safety fetch successfully added to all files!")
