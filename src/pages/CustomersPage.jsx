import React, { useState } from 'react';
import { CustomerFormModal } from '../components/Modals';

export function CustomersPage({ customers = [], onAddCustomer, onEditCustomer }) {
  const [searchQuery, setSearchQuery] = useState('');
  const [editingCustomer, setEditingCustomer] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  const filteredCustomers = customers.filter(c => {
    if (!searchQuery.trim()) return true;
    const q = searchQuery.toLowerCase();
    return (c.name || '').toLowerCase().includes(q) ||
      (c.phone || '').includes(q) ||
      (c.email || '').toLowerCase().includes(q);
  });

  return (
    <div className="space-y-6 max-w-7xl mx-auto animate-fade-in">
      {/* MODAL */}
      {isModalOpen && (
        <CustomerFormModal
          customer={editingCustomer}
          onClose={() => { setIsModalOpen(false); setEditingCustomer(null); }}
          onSave={(custObj) => {
            if (editingCustomer) {
              onEditCustomer(custObj);
            } else {
              onAddCustomer(custObj);
            }
            setIsModalOpen(false);
            setEditingCustomer(null);
          }}
        />
      )}

      {/* HEADER */}
      <div className="glass-panel p-6 rounded-3xl border border-slate-200 dark:border-brand-border flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 shadow-sm">
        <div>
          <h2 className="text-xl sm:text-2xl font-heading font-extrabold text-slate-900 dark:text-white">
            👥 Müşteri Rehberi & Otomatik Üye Kartları
          </h2>
          <p className="text-xs text-slate-500 dark:text-gray-400">
            Rezervasyon oluşturan tüm müşteriler otomatik üye olarak sisteme kaydedilir.
          </p>
        </div>

        <button
          onClick={() => { setEditingCustomer(null); setIsModalOpen(true); }}
          className="gold-button font-bold text-xs px-4 py-2.5 rounded-xl shadow flex items-center space-x-1"
        >
          <span>➕ Manuel Müşteri Ekle</span>
        </button>
      </div>

      {/* SEARCH BAR */}
      <div className="glass-panel p-4 rounded-2xl border border-slate-200 dark:border-brand-border text-xs">
        <input
          type="text"
          placeholder="🔍 Ad Soyad, Telefon Numarası veya E-posta ile Müşteri Ara..."
          value={searchQuery}
          onChange={e => setSearchQuery(e.target.value)}
          className="w-full sm:w-96 bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 font-medium text-slate-800 dark:text-gray-200"
        />
      </div>

      {/* CUSTOMERS GRID */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {filteredCustomers.map(c => (
          <div key={c.id} className="glass-panel p-5 rounded-3xl border border-slate-200 dark:border-brand-border space-y-3 shadow-sm flex flex-col justify-between">
            <div className="space-y-2">
              <div className="flex justify-between items-start">
                <div className="w-10 h-10 rounded-2xl bg-amber-500/10 text-amber-600 font-extrabold flex items-center justify-center text-lg shrink-0">
                  👤
                </div>
                <button
                  onClick={() => { setEditingCustomer(c); setIsModalOpen(true); }}
                  className="text-xs font-bold text-amber-700 dark:text-gold-400 hover:underline"
                >
                  Düzenle ✏️
                </button>
              </div>

              <div>
                <h4 className="font-heading font-extrabold text-sm text-slate-900 dark:text-white">
                  {c.name}
                </h4>
                <div className="text-xs text-slate-500 font-mono font-bold mt-0.5">{c.phone}</div>
                <div className="text-xs text-slate-400 mt-0.5">{c.email || 'E-posta Girilmemiş'}</div>
              </div>
            </div>

            <div className="pt-2 border-t border-slate-100 dark:border-brand-border flex justify-between items-center text-xs text-slate-500 font-bold">
              <span>Toplam Rezervasyon:</span>
              <span className="bg-amber-500/10 text-amber-700 dark:text-gold-400 px-2.5 py-0.5 rounded-full font-mono font-extrabold">
                {c.totalBookings || 1} Etkinlik
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
