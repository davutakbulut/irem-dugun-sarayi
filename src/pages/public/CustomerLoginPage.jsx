import React, { useState } from 'react';

export default function CustomerLoginPage({ navigateTo }) {
  const [contractCode, setContractCode] = useState('');
  const [phone, setPhone] = useState('');
  const [isLogged, setIsLogged] = useState(false);

  const handleLogin = (e) => {
    e.preventDefault();
    setIsLogged(true);

    const customerUser = {
      id: 'cust-session-' + Date.now(),
      name: contractCode ? `Çift Portalı (${contractCode.toUpperCase()})` : 'Zeynep & Burak Yılmaz',
      email: 'musteri@iremdugunsarayi.com',
      phone: phone || '+90 532 000 00 00',
      role: 'musteri',
      contractCode: contractCode || 'IRM-2026-8492',
      avatar: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80'
    };

    try {
      localStorage.setItem('irem_session_user', JSON.stringify(customerUser));
      localStorage.setItem('irem_active_role', 'musteri');
    } catch(err) {}

    setTimeout(() => {
      if (typeof window !== 'undefined') {
        window.location.href = '/yonetim';
      }
    }, 1500);
  };

  return (
    <div className="max-w-md mx-auto px-6 py-16">
      <div className="bg-slate-900/95 backdrop-blur-2xl p-8 rounded-3xl border-2 border-amber-500/30 shadow-2xl space-y-6 text-white">
        
        <div className="text-center space-y-2">
          <div className="w-12 h-12 rounded-2xl bg-amber-500/20 text-amber-400 flex items-center justify-center text-2xl mx-auto border border-amber-500/40">
            🔑
          </div>
          <h2 className="text-2xl font-heading font-extrabold">Anlaşmalı Müşteri VIP Portalı</h2>
          <p className="text-xs text-slate-400">
            Sözleşme numaranız ve kayıtlı telefon numaranız ile kendi düğün organizasyon panelinize bağlanın.
          </p>
        </div>

        {isLogged ? (
          <div className="bg-emerald-500/10 border border-emerald-500/40 p-6 rounded-2xl text-center space-y-3">
            <div className="text-3xl">🎉</div>
            <h3 className="font-bold text-emerald-400">Hoş Geldiniz!</h3>
            <p className="text-xs text-slate-300">
              Düğün takviminiz, seçtiğiniz ikram menüsü ve kalan ödeme takibiniz yükleniyor...
            </p>
          </div>
        ) : (
          <form onSubmit={handleLogin} className="space-y-4">
            <div>
              <label className="block text-[11px] font-bold text-slate-300 mb-1">
                Sözleşme / Rezervasyon Kodu *
              </label>
              <input
                type="text"
                required
                placeholder="Örn: IRM-2026-8492"
                value={contractCode}
                onChange={(e) => setContractCode(e.target.value)}
                className="w-full bg-slate-950 border border-slate-800 focus:border-amber-500 text-white text-xs px-4 py-3 rounded-xl outline-none"
              />
            </div>

            <div>
              <label className="block text-[11px] font-bold text-slate-300 mb-1">
                Kayıtlı Telefon Numarası *
              </label>
              <input
                type="tel"
                required
                placeholder="0532 000 00 00"
                value={phone}
                onChange={(e) => setPhone(e.target.value)}
                className="w-full bg-slate-950 border border-slate-800 focus:border-amber-500 text-white text-xs px-4 py-3 rounded-xl outline-none"
              />
            </div>

            <button type="submit" className="w-full gold-button font-extrabold text-xs py-3.5 rounded-xl shadow-xl">
              VIP Portala Giriş Yap →
            </button>

            <div className="pt-2 text-center text-xs text-slate-400">
              Henüz sözleşmeniz yok mu?{' '}
              <button
                type="button"
                onClick={() => navigateTo && navigateTo('/musteri-kayit')}
                className="text-amber-400 font-bold hover:underline"
              >
                Yeni Çift Başvurusu Yapın
              </button>
            </div>
          </form>
        )}

      </div>
    </div>
  );
}
