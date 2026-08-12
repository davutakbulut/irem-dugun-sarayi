import os, re

# 1. UPDATE server.js
with open('server.js', 'r', encoding='utf-8') as f:
    server_code = f.read()

# Add Method Override / POST-DELETE middleware if not present
middleware_target = "app.use(express.urlencoded({ extended: true, limit: '50mb' }));"
middleware_addition = """app.use(express.urlencoded({ extended: true, limit: '50mb' }));

// POST Fallback Middleware for DELETE actions (Prevents 403 Forbidden on Plesk / IIS / ModSecurity WAF)
app.use((req, res, next) => {
  if (req.method === 'POST') {
    const overrideMethod = req.headers['x-http-method-override'] || req.headers['x-method-override'];
    if (overrideMethod === 'DELETE') {
      req.method = 'DELETE';
    } else if (req.url.includes('/delete/')) {
      req.url = req.url.replace('/delete/', '/');
      req.method = 'DELETE';
    } else if (req.url.endsWith('-delete')) {
      req.url = req.url.replace(/-delete$/, '');
      req.method = 'DELETE';
    }
  }
  next();
});"""

if "POST Fallback Middleware for DELETE actions" not in server_code and middleware_target in server_code:
    server_code = server_code.replace(middleware_target, middleware_addition)

# Update draft-reservations delete handlers
old_draft_delete = """app.delete('/api/draft-reservations/:id', async (req, res) => {
  const { id } = req.params;
  try {
    memoryStore.draftReservations = (memoryStore.draftReservations || []).filter(d => d.id !== id && d.refKey !== id);
    const activePool = await getPool();
    if (activePool) {
      await activePool.query(
        "DELETE FROM reservations WHERE status = 'DRAFT' AND (id = ? OR notes LIKE ?)",
        [id, `%"refKey":"${id}"%`]
      );
    }
    return res.json({ success: true, deletedId: id });
  } catch(e) {
    console.error('MySQL DELETE /api/draft-reservations error:', e.message);
    return res.status(500).json({ error: e.message });
  }
});"""

new_draft_delete = """const deleteDraftReservationHandler = async (req, res) => {
  const id = req.params.id || req.body?.id || req.body?.refKey;
  if (!id) return res.status(400).json({ error: 'ID required' });
  try {
    memoryStore.draftReservations = (memoryStore.draftReservations || []).filter(d => d.id !== id && d.refKey !== id);
    const activePool = await getPool();
    if (activePool) {
      await activePool.query(
        "DELETE FROM reservations WHERE status = 'DRAFT' AND (id = ? OR notes LIKE ?)",
        [id, `%"refKey":"${id}"%`]
      );
    }
    return res.json({ success: true, deletedId: id });
  } catch(e) {
    console.error('MySQL DELETE /api/draft-reservations error:', e.message);
    return res.status(500).json({ error: e.message });
  }
};

app.delete('/api/draft-reservations/:id', deleteDraftReservationHandler);
app.post('/api/draft-reservations/delete/:id', deleteDraftReservationHandler);
app.post('/api/draft-reservations-delete/:id', deleteDraftReservationHandler);
app.post('/api/draft-reservations-delete', deleteDraftReservationHandler);
app.post('/api/draft-reservations/:id', deleteDraftReservationHandler);"""

if old_draft_delete in server_code:
    server_code = server_code.replace(old_draft_delete, new_draft_delete)

with open('server.js', 'w', encoding='utf-8') as f:
    f.write(server_code)

print("Successfully updated server.js with POST-delete middleware and draft-reservations handlers!")

# 2. UPDATE HTML FILES (index.html, yonetim.html, yonetim/index.html, dist/index.html)
html_files = ['index.html', 'yonetim.html', 'yonetim/index.html', 'dist/index.html']

for h_file in html_files:
    if not os.path.exists(h_file):
        continue
    with open(h_file, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Update fetchWithRetry function to retry 403 / 405 DELETE requests as POST
    old_retry_code = """      return fetch(url, options).then(function(res) {
        if (!res.ok && (res.status === 404 || res.status === 500)) {"""

    new_retry_code = """      options = options || {};
      if (options.method === 'DELETE') {
        options.headers = options.headers || {};
        options.headers['X-HTTP-Method-Override'] = 'DELETE';
      }
      return fetch(url, options).then(function(res) {
        if (!res.ok && options.method === 'DELETE' && (res.status === 403 || res.status === 405 || res.status === 404)) {
          // Retry DELETE action using POST fallback route for Plesk / IIS compatibility
          var postUrl = url.indexOf('/delete/') === -1 ? url.replace('/api/', '/api/').replace(/\/([^/]+)$/, '/delete/$1') : url;
          var postOptions = Object.assign({}, options, {
            method: 'POST',
            headers: Object.assign({}, options.headers || {}, { 'Content-Type': 'application/json', 'X-HTTP-Method-Override': 'DELETE' })
          });
          return fetch(postUrl, postOptions).then(function(pRes) {
            if (pRes.ok) return pRes;
            return res;
          }).catch(function() { return res; });
        }
        if (!res.ok && (res.status === 404 || res.status === 500)) {"""

    if old_retry_code in html_content:
        html_content = html_content.replace(old_retry_code, new_retry_code)

    # Update frontend draft reservation delete fetch calls
    old_call_1 = "if (targetRef) fetchFn(`/api/draft-reservations/${encodeURIComponent(targetRef)}`, { method: 'DELETE' }).catch(() => {});"
    new_call_1 = "if (targetRef) { fetchFn(`/api/draft-reservations/delete/${encodeURIComponent(targetRef)}`, { method: 'POST' }).catch(() => fetchFn(`/api/draft-reservations/${encodeURIComponent(targetRef)}`, { method: 'DELETE' }).catch(() => {})); }"

    old_call_2 = "if (cleanRef) fetchFn(`/api/draft-reservations/${encodeURIComponent(cleanRef)}`, { method: 'DELETE' }).catch(() => {});"
    new_call_2 = "if (cleanRef) { fetchFn(`/api/draft-reservations/delete/${encodeURIComponent(cleanRef)}`, { method: 'POST' }).catch(() => fetchFn(`/api/draft-reservations/${encodeURIComponent(cleanRef)}`, { method: 'DELETE' }).catch(() => {})); }"

    if old_call_1 in html_content:
        html_content = html_content.replace(old_call_1, new_call_1)

    if old_call_2 in html_content:
        html_content = html_content.replace(old_call_2, new_call_2)

    with open(h_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"Successfully updated {h_file}!")

# Update web.config IIS trigger
with open('web.config', 'w', encoding='utf-8') as f:
    f.write("""<?xml version="1.0" encoding="utf-8"?>
<configuration>
  <system.webServer>
    <handlers>
      <add name="iisnode" path="server.js" verb="*" modules="iisnode" />
    </handlers>
    <rewrite>
      <rules>
        <rule name="NodeContent">
          <match url="/*" />
          <action type="Rewrite" url="server.js" />
        </rule>
      </rules>
    </rewrite>
    <httpErrors existingResponse="PassThrough" />
  </system.webServer>
</configuration>
<!-- IIS Restart Trigger: 2026-08-13-v1-post-delete-resilience -->
""")

print("Updated web.config restart trigger!")
