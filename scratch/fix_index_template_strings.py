with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

old_block = """            ${res.flowPlan && res.flowPlan.length > 0 ? `
              <div style="margin-bottom: 20px;">
                <h4 style="margin: 0 0 8px 0; font-size: 14px; color: #b45309; text-transform: uppercase;">6. ORGANİZASYON & ETKİNLİK AKIŞ PLANLAMASI:</h4>
                <table style="margin-top: 5px;">
                  <thead>
                    <tr>
                      <th style="width: 100px;">Saat</th>
                      <th>Program / Etkinlik Adımı</th>
                    </tr>
                  </thead>
                  <tbody>
                    ${res.flowPlan.map(fp => `
                      <tr>
                        <td style="font-weight: bold; color: #b45309; font-family: monospace;">${fp.time}</td>
                        <td>${fp.title}</td>
                      </tr>
                    `).join('')}
                  </tbody>
                </table>
              </div>
            ` : ''}"""

new_block = """            ${(res.flowPlan && res.flowPlan.length > 0) ? (
              '<div style="margin-bottom: 20px;">' +
                '<h4 style="margin: 0 0 8px 0; font-size: 14px; color: #b45309; text-transform: uppercase;">6. ORGANİZASYON & ETKİNLİK AKIŞ PLANLAMASI:</h4>' +
                '<table style="margin-top: 5px;">' +
                  '<thead>' +
                    '<tr>' +
                      '<th style="width: 100px;">Saat</th>' +
                      '<th>Program / Etkinlik Adımı</th>' +
                    '</tr>' +
                  '</thead>' +
                  '<tbody>' +
                    res.flowPlan.map(function(fp) {
                      return '<tr><td style="font-weight: bold; color: #b45309; font-family: monospace;">' + fp.time + '</td><td>' + fp.title + '</td></tr>';
                    }).join('') +
                  '</tbody>' +
                '</table>' +
              '</div>'
            ) : ''}"""

if old_block in content:
    content = content.replace(old_block, new_block)
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(content)
    print("✅ Fixed handlePrintInvoice template string nesting in index.html!")
else:
    print("⚠️ old_block not found exactly")
