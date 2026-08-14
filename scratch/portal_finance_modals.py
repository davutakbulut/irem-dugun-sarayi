import os

html_files = ['index.html', 'yonetim.html', 'yonetim/index.html', 'dist/index.html']

for h_file in html_files:
    if not os.path.exists(h_file):
        continue
    with open(h_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Custom Expense Modal Portal
    old_custom_expense_modal = """          {/* DEDICATED RESERVATION CUSTOM EXPENSE MANAGEMENT MODAL */}
          {customExpenseModalRes && ("""

    new_custom_expense_modal = """          {/* DEDICATED RESERVATION CUSTOM EXPENSE MANAGEMENT MODAL */}
          {customExpenseModalRes && typeof document !== 'undefined' && ReactDOM.createPortal("""

    old_custom_expense_close = """                <div className="pt-3 border-t border-slate-200 dark:border-brand-border flex justify-end">
                  <button
                    type="button"
                    onClick={() => setCustomExpenseModalRes(null)}
                    className="px-5 py-2 bg-slate-100 dark:bg-brand-dark text-slate-700 dark:text-gray-300 rounded-xl font-bold text-xs cursor-pointer"
                  >
                    Kapat
                  </button>
                </div>
              </div>
            </div>
          )}"""

    new_custom_expense_close = """                <div className="pt-3 border-t border-slate-200 dark:border-brand-border flex justify-end">
                  <button
                    type="button"
                    onClick={() => setCustomExpenseModalRes(null)}
                    className="px-5 py-2 bg-slate-100 dark:bg-brand-dark text-slate-700 dark:text-gray-300 rounded-xl font-bold text-xs cursor-pointer"
                  >
                    Kapat
                  </button>
                </div>
              </div>
            </div>,
            document.body
          )}"""

    # 2. General Cashflow Transaction Modal Portal
    old_general_modal = """          {/* GENERAL CASHFLOW TRANSACTION MODAL (GELİR / GİDER SEÇİMLİ) */}
          {isModalOpen && ("""

    new_general_modal = """          {/* GENERAL CASHFLOW TRANSACTION MODAL (GELİR / GİDER SEÇİMLİ) */}
          {isModalOpen && typeof document !== 'undefined' && ReactDOM.createPortal("""

    old_general_modal_close = """                    <button
                      type="submit"
                      className="px-5 py-2 gold-button font-bold text-xs rounded-xl shadow cursor-pointer"
                    >
                      Kaydet & Kasaya Ekle
                    </button>
                  </div>
                </form>
              </div>
            </div>
          )}"""

    new_general_modal_close = """                    <button
                      type="submit"
                      className="px-5 py-2 gold-button font-bold text-xs rounded-xl shadow cursor-pointer"
                    >
                      Kaydet & Kasaya Ekle
                    </button>
                  </div>
                </form>
              </div>
            </div>,
            document.body
          )}"""

    if old_custom_expense_modal in content and old_custom_expense_close in content:
        content = content.replace(old_custom_expense_modal, new_custom_expense_modal)
        content = content.replace(old_custom_expense_close, new_custom_expense_close)
        print(f"Portaled customExpenseModalRes in {h_file}")

    if old_general_modal in content and old_general_modal_close in content:
        content = content.replace(old_general_modal, new_general_modal)
        content = content.replace(old_general_modal_close, new_general_modal_close)
        print(f"Portaled isModalOpen in {h_file}")
    else:
        print(f"old_general_modal not matched in {h_file}")

    # Ensure modal container has fixed inset-0 z-[999999]
    content = content.replace(
        '<div className="fixed inset-0 z-[99999] bg-black/80 backdrop-blur-md flex items-center justify-center p-4 animate-fade-in">',
        '<div className="fixed inset-0 z-[999999] bg-slate-950/80 backdrop-blur-md flex items-center justify-center p-4 sm:p-6 overflow-y-auto animate-fade-in">'
    )

    with open(h_file, 'w', encoding='utf-8') as f:
        f.write(content)

print("All finance modals portaled successfully!")
