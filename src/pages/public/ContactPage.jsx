import React, { useState } from 'react';

export default function ContactPage() {
  const [form, setForm] = useState({ name: '', phone: '', email: '', subject: '', message: '' });
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    setSubmitted(true);
    setTimeout(() => {
      setSubmitted(false);
      setForm({ name: '', phone: '', email: '', subject: '', message: '' });
    }, 4000);
  };

  return (
    <div className="max-w-7xl mx-auto px-6 sm:px-12 py-12 space-y-12">
      
      {/* HEADER */}
      <div className="text-center space-y-4 max-w-3xl mx-auto">
        <span className="text-amber-500 font-extrabold text-xs uppercase tracking-widest">
          📞 İletişim & Yol Tarifi
        </span>
        <h1 className="text-4xl sm:text-5xl font-heading font-extrabold text-white">
          Bizimle İletişime Geçin
        </h1>
        <p className="text-xs sm:text-sm text-slate-300 leading-relaxed">
          Tesisimizi ziyaret etmek, randevu almak veya düğün tarihinizi sorgulatmak için bize ulaşabilirsiniz.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-start">
        
        {/* LEFT CONTACT INFO */}
        <div className="lg:col-span-5 space-y-6">
          <div className="bg-slate-900/90 p-8 rounded-3xl border border-slate-800 space-y-6">
            <h3 className="text-xl font-heading font-extrabold text-white border-b border-amber-500/30 pb-3">
              Tesis Bilgileri
            </h3>

            <div className="space-y-4 text-xs">
              <div className="flex items-start space-x-3">
                <span className="text-xl text-amber-400">📍</span>
                <div>
                  <div className="font-bold text-white">Açık Adres</div>
                  <div className="text-slate-300">Sapanca Göl Caddesi No:42, Sakarya / Türkiye</div>
                </div>
              </div>

              <div className="flex items-center space-x-3">
                <span className="text-xl text-amber-400">📞</span>
                <div>
                  <div className="font-bold text-white">Telefon (Santral)</div>
                  <a href="tel:+902645820000" className="text-amber-400 font-bold hover:underline">
                    +90 (264) 582 00 00
                  </a>
                </div>
              </div>

              <div className="flex items-center space-x-3">
                <span className="text-xl text-emerald-400">💬</span>
                <div>
                  <div className="font-bold text-white">WhatsApp Canlı Destek</div>
                  <a href="https://wa.me/905320000000" target="_blank" rel="noreferrer" className="text-emerald-400 font-bold hover:underline">
                    +90 (532) 000 00 00
                  </a>
                </div>
              </div>

              <div className="flex items-center space-x-3">
                <span className="text-xl text-amber-400">✉️</span>
                <div>
                  <div className="font-bold text-white">E-posta Adresi</div>
                  <div className="text-slate-300">info@iremdugunsarayi.com</div>
                </div>
              </div>
            </div>
          </div>

          {/* MAP IFRAME */}
          <div className="h-64 rounded-3xl overflow-hidden border border-amber-500/30 shadow-xl">
            <iframe
              title="İrem Düğün Sarayı Harita Konumu"
              src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d12089.444390022204!2d30.27!3d40.69!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x0!2zNDDCsDQxJzI0LjAiTiAzMMKwMTYnMTIuMCJF!5e0!3m2!1str!2str!4v1620000000000!5m2!1str!2str"
              className="w-full h-full border-0"
              loading="lazy"
            />
          </div>
        </div>

        {/* RIGHT CONTACT FORM */}
        <div className="lg:col-span-7 bg-slate-900/90 p-8 sm:p-10 rounded-3xl border-2 border-amber-500/30 shadow-2xl space-y-6">
          <div className="space-y-1">
            <h3 className="text-2xl font-heading font-extrabold text-white">Mesaj Gönderin</h3>
            <p className="text-xs text-slate-400">Sorularınızı ve randevu taleplerinizi aşağıdaki formdan iletebilirsiniz.</p>
          </div>

          {submitted ? (
            <div className="bg-emerald-500/10 border border-emerald-500/40 p-6 rounded-2xl text-center space-y-2">
              <div className="text-3xl">✅</div>
              <h4 className="font-bold text-emerald-400">Mesajınız Ulaştı!</h4>
              <p className="text-xs text-slate-300">Ekibimiz en kısa sürede sizinle iletişime geçecektir.</p>
            </div>
          ) : (
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-[11px] font-bold text-slate-300 mb-1">Adınız Soyadınız *</label>
                  <input
                    type="text"
                    required
                    value={form.name}
                    onChange={e => setForm({ ...form, name: e.target.value })}
                    className="w-full bg-slate-950 border border-slate-800 focus:border-amber-500 text-white text-xs px-4 py-3 rounded-xl outline-none"
                  />
                </div>

                <div>
                  <label className="block text-[11px] font-bold text-slate-300 mb-1">Telefon Numarası *</label>
                  <input
                    type="tel"
                    required
                    value={form.phone}
                    onChange={e => setForm({ ...form, phone: e.target.value })}
                    className="w-full bg-slate-950 border border-slate-800 focus:border-amber-500 text-white text-xs px-4 py-3 rounded-xl outline-none"
                  />
                </div>
              </div>

              <div>
                <label className="block text-[11px] font-bold text-slate-300 mb-1">Konu</label>
                <input
                  type="text"
                  placeholder="Örn: Rezervasyon Randevusu Talebi"
                  value={form.subject}
                  onChange={e => setForm({ ...form, subject: e.target.value })}
                  className="w-full bg-slate-950 border border-slate-800 focus:border-amber-500 text-white text-xs px-4 py-3 rounded-xl outline-none"
                />
              </div>

              <div>
                <label className="block text-[11px] font-bold text-slate-300 mb-1">Mesajınız</label>
                <textarea
                  rows="4"
                  value={form.message}
                  onChange={e => setForm({ ...form, message: e.target.value })}
                  className="w-full bg-slate-950 border border-slate-800 focus:border-amber-500 text-white text-xs p-4 rounded-xl outline-none"
                  placeholder="Detaylı bilgi veya sormak istediğiniz sorular..."
                />
              </div>

              <button type="submit" className="w-full gold-button font-extrabold text-sm py-4 rounded-xl shadow-xl">
                Mesajı Gönder →
              </button>
            </form>
          )}
        </div>

      </div>

    </div>
  );
}
