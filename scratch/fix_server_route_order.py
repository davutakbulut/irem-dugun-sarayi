with open('server.js', 'r', encoding='utf-8') as f:
    code = f.read()

# Extract the catch-all middleware and app.listen
catchall = """app.use((req, res) => {
  if (req.path.startsWith('/api/')) {
    return res.status(404).json({ error: 'API Uç Noktası Bulunamadı' });
  }
  res.sendFile('index.html', { root: __dirname });
});"""

# Remove catchall from its current location
code = code.replace(catchall, '')

# Place catchall right before app.listen
pos = code.find("app.listen(")
if pos != -1:
    code = code[:pos] + "\n" + catchall + "\n\n" + code[pos:]

with open('server.js', 'w', encoding='utf-8') as f:
    f.write(code)

print("Fixed server.js route order successfully!")
