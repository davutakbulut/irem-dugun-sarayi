import re

# Read a page file, e.g. DashboardPage.jsx
with open("src/pages/DashboardPage.jsx", "r", encoding="utf-8") as f:
    code = f.read()

print("DashboardPage lines:", len(code.splitlines()))
print("DashboardPage has import statements:", "import " in code)
print("DashboardPage has export statements:", "export " in code)
