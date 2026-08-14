import os, re

html_files = ['index.html', 'yonetim.html', 'yonetim/index.html', 'dist/index.html']

for h_file in html_files:
    if not os.path.exists(h_file):
        continue
    with open(h_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update categories in handleAddExpense modal
    old_cat_options = """                      <option value="Personel & Sanatçı">Personel & Sanatçı</option>
                      <option value="Dekorasyon & Çiçek">Dekorasyon & Çiçek</option>
                      <option value="Faturalar & Enerji">Faturalar & Enerji</option>
                      <option value="Yiyecek & İçecek">Yiyecek & İçecek</option>
                      <option value="Ekipman & Bakım">Ekipman & Bakım</option>
                      <option value="Genel Harcama">Genel Harcama</option>"""

    new_cat_options = """                      <option value="Faturalar & Enerji">💡 Faturalar & Enerji (Elektrik, Su, Doğalgaz, İnternet)</option>
                      <option value="Yemek & Mutfak & İkram">🍽️ Yemek & Mutfak & İkram</option>
                      <option value="Keyfi & Temsil Ağırlama">☕ Keyfi & Temsil Ağırlama Harcamaları</option>
                      <option value="Personel & Yevmiye">👥 Personel & Yevmiye & Sanatçı</option>
                      <option value="Dekorasyon & Çiçek">🌸 Dekorasyon, Çiçek & Süsleme</option>
                      <option value="Ekipman & Bakım">🔊 Ekipman, Ses, Işık & Bakım Onarım</option>
                      <option value="Ofis & Kırtasiye & Sarf">📑 Ofis, Muhasebe & Sarf Malzeme</option>
                      <option value="Genel Harcama">📦 Diğer Genel İşletme Giderleri</option>"""

    if old_cat_options in content:
        content = content.replace(old_cat_options, new_cat_options)
        print(f"Updated expense categories in modal in {h_file}")

    # 2. Add handleDeleteExpense function inside FinancePageComponent
    old_fn_pos = """        setNewTitle('');
        setNewAmount('');
        setIsModalOpen(false);
      };"""

    new_fn_pos = """        setNewTitle('');
        setNewAmount('');
        setIsModalOpen(false);
      };

      const handleDeleteExpense = (expId) => {
        setExpenses(prev => {
          const updated = prev.filter(e => e.id !== expId);
          try {
            const fetchFn = window.fetchWithRetry || fetch;
            fetchFn(`/api/expenses/${expId}`, {
              method: 'DELETE'
            }).catch(() => {});
          } catch(err) {}
          return updated;
        });
      };"""

    if old_fn_pos in content and "const handleDeleteExpense =" not in content:
        content = content.replace(old_fn_pos, new_fn_pos)
        print(f"Added handleDeleteExpense in {h_file}")

    # 3. Add İşlem / Sil column to Cashflow table
    old_th = """                        <th className="p-3.5 text-right">Tutar</th>
                        <th className="p-3.5 text-center">Durum</th>
                      </tr>"""

    new_th = """                        <th className="p-3.5 text-right">Tutar</th>
                        <th className="p-3.5 text-center">Durum</th>
                        <th className="p-3.5 text-center">İşlem</th>
                      </tr>"""

    if old_th in content:
        content = content.replace(old_th, new_th)
        print(f"Updated table header in {h_file}")

    old_td = """                            <td className="p-3.5 text-center whitespace-nowrap">
                              <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${
                                t.status === 'Ödendi' || t.status === 'Tahsil Edildi' || t.status === 'Tamamlandı'
                                  ? 'bg-emerald-500/10 text-emerald-600 dark:text-emerald-400'
                                  : 'bg-amber-500/10 text-amber-600 dark:text-gold-400'
                              }`}>
                                {t.status}
                              </span>
                            </td>
                          </tr>"""

    new_td = """                            <td className="p-3.5 text-center whitespace-nowrap">
                              <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${
                                t.status === 'Ödendi' || t.status === 'Tahsil Edildi' || t.status === 'Tamamlandı'
                                  ? 'bg-emerald-500/10 text-emerald-600 dark:text-emerald-400'
                                  : 'bg-amber-500/10 text-amber-600 dark:text-gold-400'
                              }`}>
                                {t.status}
                              </span>
                            </td>
                            <td className="p-3.5 text-center whitespace-nowrap">
                              {t.type === 'gider' ? (
                                <button
                                  type="button"
                                  onClick={() => handleDeleteExpense(t.id)}
                                  className="px-2 py-1 bg-red-500/10 hover:bg-red-500 text-red-600 hover:text-white rounded-lg text-[10px] font-bold transition cursor-pointer border border-red-500/20"
                                  title="Bu gider kaydını sil"
                                >
                                  🗑️ Sil
                                </button>
                              ) : (
                                <span className="text-[10px] text-slate-400 font-mono">-</span>
                              )}
                            </td>
                          </tr>"""

    if old_td in content:
        content = content.replace(old_td, new_td)
        print(f"Updated table row with delete button in {h_file}")

    # Colspan 6 to 7
    content = content.replace('colSpan="6"', 'colSpan="7"')

    with open(h_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Processed {h_file} successfully!")

print("General expenses enriched and synchronized across all files!")
