import sys

with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

start_idx = -1
end_idx = -1

for i, line in enumerate(lines):
    if '{/* PAGE HEADER */}' in line:
        start_idx = i
    if start_idx != -1 and '← Rezervasyon Listesine Dön' in line:
        end_idx = i + 2
        break

if start_idx != -1 and end_idx != -1:
    new_header_lines = [
        "          {/* PAGE HEADER (STRICTLY CONTAINER BOUNDED WITH NO OVERFLOW) */}\n",
        "          <div className=\"glass-panel p-4 sm:p-6 rounded-3xl border border-slate-200 dark:border-brand-border flex flex-col md:flex-row justify-between items-start md:items-center gap-4 shadow-sm overflow-hidden w-full max-w-full\">\n",
        "            <div className=\"flex flex-col items-start gap-2 min-w-0 flex-1 max-w-full\">\n",
        "              \n",
        "              {/* BADGES ROW WITH FLEX-WRAP TO PREVENT HORIZONTAL OVERFLOW */}\n",
        "              <div className=\"flex flex-wrap items-center gap-2 max-w-full\">\n",
        "                <span className=\"inline-flex items-center space-x-1.5 bg-slate-100 dark:bg-brand-dark text-slate-800 dark:text-gray-200 text-xs font-bold px-3 py-1 rounded-full border border-slate-200 dark:border-brand-border shrink-0\">\n",
        "                  <svg className=\"w-3.5 h-3.5 text-slate-600 dark:text-gray-400 inline\" fill=\"none\" stroke=\"currentColor\" viewBox=\"0 0 24 24\"><path strokeLinecap=\"round\" strokeLinejoin=\"round\" strokeWidth=\"2\" d=\"M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z\"></path></svg>\n",
        "                  <span>Rezervasyon Oluşturma & Kiralama</span>\n",
        "                </span>\n",
        "\n",
        "                {/* DRAFT REF KEY BADGE WITH CLICK TO COPY */}\n",
        "                <button\n",
        "                  type=\"button\"\n",
        "                  onClick={() => {\n",
        "                    if (activeRefKey && navigator.clipboard) {\n",
        "                      navigator.clipboard.writeText(activeRefKey);\n",
        "                      if (showToast) showToast('Sözleşme referans kodu kopyalandı! 🔑', 'success');\n",
        "                    }\n",
        "                  }}\n",
        "                  className=\"px-2.5 py-1 rounded-lg bg-amber-500/10 hover:bg-amber-500/20 text-amber-700 dark:text-gold-400 border border-amber-500/30 text-xs font-mono font-bold inline-flex items-center space-x-1 shrink-0 cursor-pointer transition\"\n",
        "                  title=\"Referans kodunu kopyalamak için tıklayın\"\n",
        "                >\n",
        "                  <span>🔑 Ref:</span>\n",
        "                  <span className=\"tracking-wider\">{activeRefKey}</span>\n",
        "                  <span className=\"text-[10px] text-amber-500\">📋</span>\n",
        "                </button>\n",
        "\n",
        "                {lastSavedTime ? (\n",
        "                  <span className=\"px-2.5 py-1 rounded-lg bg-emerald-500/10 text-emerald-700 dark:text-emerald-300 border border-emerald-500/30 text-xs font-bold inline-flex items-center space-x-1 shrink-0\">\n",
        "                    <span>💾 Taslak Kaydedildi</span>\n",
        "                    <span className=\"text-[10px] font-mono\">({lastSavedTime})</span>\n",
        "                  </span>\n",
        "                ) : (\n",
        "                  <span className=\"px-2.5 py-1 rounded-lg bg-slate-100 dark:bg-brand-dark text-slate-500 text-xs font-semibold inline-flex items-center space-x-1 shrink-0\">\n",
        "                    <span>⏱️ Canlı Otomatik Kayıt</span>\n",
        "                  </span>\n",
        "                )}\n",
        "              </div>\n",
        "\n",
        "              <h2 className=\"text-xl sm:text-2xl font-heading font-extrabold gold-gradient-text mt-0.5 break-words max-w-full\">\n",
        "                Hayalinizdeki Düğünü Birlikte Planlayalım!\n",
        "              </h2>\n",
        "              <p className=\"text-[11px] sm:text-xs text-slate-500 dark:text-gray-400 leading-relaxed break-words max-w-2xl\">\n",
        "                Salon kiralama, hizmet adetleri, müşteri üyelik kaydı, fatura ve etkinlik akışını tek ekranda yönetin.\n",
        "              </p>\n",
        "            </div>\n",
        "\n",
        "            <div className=\"flex flex-col sm:flex-row items-center gap-2 w-full md:w-auto shrink-0\">\n",
        "              <button\n",
        "                type=\"button\"\n",
        "                onClick={onCancel}\n",
        "                className=\"w-full sm:w-auto px-4 py-2.5 bg-slate-100 dark:bg-brand-card hover:bg-slate-200 dark:hover:bg-slate-800 text-slate-700 dark:text-gray-300 rounded-xl text-xs font-bold transition text-center whitespace-nowrap cursor-pointer shadow-xs border border-slate-200 dark:border-brand-border\"\n",
        "              >\n",
        "                ← Rezervasyon Listesine Dön\n",
        "              </button>\n",
        "            </div>\n",
        "          </div>\n"
    ]
    lines[start_idx:end_idx] = new_header_lines
    with open('index.html', 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print(f"Successfully replaced lines {start_idx+1} to {end_idx} in index.html!")
else:
    print("Failed to locate target header indices!")
