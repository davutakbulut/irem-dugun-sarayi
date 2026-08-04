import React, { useState } from 'react';

export default function CustomerRegisterPage({ navigateTo }) {
  const [form, setForm] = useState({ brideName: '', groomName: '', phone: '', email: '', targetDate: '' });
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    setSubmitted(true);
  };

  return (
    <div className="max-w-md mx-auto px-6 py-16">
      <div className="bg-slate-900/95 backdrop-blur-2xl p-8 rounded-3xl border-2 border-amber-500/30 shadow-2xl space-y-6 text-white">
        
        <div className="text-center space-y-2">
          <div className="w-12 h-12 rounded-2xl bg-amber-500/20 text-amber-400 flex items-center justify-center text-2xl mx-auto border border-amber-500/40">
            💍
          </div>
          <h2 className="text-2xl font-heading font-extrabold">Çift Ön Kayıt Başvurusu</h2>
          <p className="text-xs text-slate-400">
            Düğün tarihiniz için salon opsiyonu kapatın ve müşteri portalınızı aktifleştirin.
          </p>
        </div>

        {submitted ? (
          <div className="bg-emerald-500/10 border border-emerald-500/40 p-6 rounded-2xl text-center space-y-3">
            <div className="text-3xl">✅</div>
            <h3 className="font-bold text-emerald-400">Başvurunuz Kaydedildi!</h3>
            <p className="text-xs text-slate-300">
              Opsiyon yetkilimiz sizinle iletişime geçip müşteri portalı giriş şifrenizi aktifleştirecektir.
            </p>
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-[11px] font-bold text-slate-300 mb-1">Gelin Adı *</label>
                <input
                  type="text"
                  required
                  value={form.brideName}
                  onChange={(e) => setForm({ ...form, brideName: e.target.value })}
                  className="w-full bg-slate-950 border border-slate-800 focus:border-amber-500 text-white text-xs px-3 py-3 rounded-xl outline-none"
                />
              </div>

              <div>
                <label className="block text-[11px] font-bold text-slate-300 mb-1">Damat Adı *</label>
                <input
                  type="text"
                  required
                  value={form.groomName}
                  onChange={(e) => setForm({ ...form, groomName: e.target.value })}
                  className="w-full bg-slate-950 border border-slate-800 focus:border-amber-500 text-white text-xs px-3 py-3 rounded-xl outline-none"
                />
              </div>
            </div>

            <div>
              <label className="block text-[11px] font-bold text-slate-300 mb-1">Telefon Numarası *</label>
              <input
                type="tel"
                required
                placeholder="0532 000 00 00"
                value={form.phone}
                onChange={(e) => setForm({ ...form, phone: e.target.value })}
                className="w-full bg-slate-950 border border-slate-800 focus:border-amber-500 text-white text-xs px-4 py-3 rounded-xl outline-none"
              />
            </div>

            <div>
              <label className="block text-[11px] font-bold text-slate-300 mb-1">Hedef Düğün Tarihi</label>
              <input
                type="date"
                value={form.targetDate}
                onChange={(e) => setForm({ ...form, targetDate: e.target.value })}
                className="w-full bg-slate-950 border border-slate-800 focus:border-amber-500 text-white text-xs px-4 py-3 rounded-xl outline-none"
              />
            </div>

            <button type="submit" className="w-full gold-button font-extrabold text-xs py-3.5 rounded-xl shadow-xl">
              Ön Kayıt Başvurusunu Tamamla →
            </button>

            <div className="pt-2 text-center text-xs text-slate-400">
              Zaten sözleşmeniz var mı?{' '}
              <button
                type="button"
                onClick={() => navigateTo && navigateTo('/musteri-giris')}
                className="text-amber-400 font-bold hover:underline"
              >
                VIP Portala Giriş Yapın
              </button>
            </div>
          </form>
        )}

      </div>
    </div>
  );
}
