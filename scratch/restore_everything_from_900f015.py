import subprocess

# 1. Fetch exact index.html from commit 900f015
html_900f015 = subprocess.check_output(['git', 'show', '900f015:index.html']).decode('utf-8')

# Fix ProfileComponent missing closing brace in 900f015
old_profile_end = """            <div className="pt-2 flex justify-end">
              <button type="submit" className="gold-button font-bold px-6 py-3 rounded-2xl text-xs shadow-lg hover:scale-105 transition">
                Değişiklikleri Kaydet ✓
              </button>
            </div>
          </form>
        </div>
      );
    // --- 10. GÖRÜNÜM & TEMA AYARLARI (MODULAR SETTINGS PAGE) ---"""

new_profile_end = """            <div className="pt-2 flex justify-end">
              <button type="submit" className="gold-button font-bold px-6 py-3 rounded-2xl text-xs shadow-lg hover:scale-105 transition">
                Değişiklikleri Kaydet ✓
              </button>
            </div>
          </form>
        </div>
      );
    }

    // --- 10. GÖRÜNÜM & TEMA AYARLARI (MODULAR SETTINGS PAGE) ---"""

fixed_html = html_900f015.replace(old_profile_end, new_profile_end)

# Expose window component aliases
alias_code = """
    // Global UMD Page Aliases
    window.DashboardPage = DashboardComponent;
    window.CreateReservationPage = CreateReservationPageComponent;
    window.ReservationsListPage = ReservationsComponent;
    window.VenuesPage = VenuesComponent;
    window.ServicesPage = ServicesComponent;
    window.CampaignsPage = CampaignsComponent;
    window.ReportsPage = ReportsComponent;
    window.CustomersPage = CustomersComponent;
    window.UsersPage = UsersComponent;
    window.SettingsPage = SettingsComponent;

    // Render React Root
"""

fixed_html = fixed_html.replace("    // Render React Root", alias_code)

# Fix handlePrintInvoice template string nesting if needed
old_print = """            ${res.flowPlan && res.flowPlan.length > 0 ? `
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

new_print = """            ${(res.flowPlan && res.flowPlan.length > 0) ? `
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
                    ` + res.flowPlan.map(fp => `
                      <tr>
                        <td style="font-weight: bold; color: #b45309; font-family: monospace;">` + fp.time + `</td>
                        <td>` + fp.title + `</td>
                      </tr>
                    `).join('') + `
                  </tbody>
                </table>
              </div>
            ` : ''}"""

fixed_html = fixed_html.replace(old_print, new_print)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(fixed_html)

print("✅ Restored full index.html from commit 900f015 with fixes!")
