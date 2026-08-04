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
    <div className="bg-[#F5F2ED] min-h-screen text-[#1A1A1A] py-16 px-4 sm:px-8 max-w-7xl mx-auto space-y-12">
      
      {/* HEADER */}
      <div className="text-center space-y-3 max-w-3xl mx-auto">
        <span className="text-[#C5B37D] font-bold text-xs uppercase tracking-[0.2em]">
          İLETİŞİM & RANDEVU
        </span>
        <h1 className="font-great-vibes text-5xl sm:text-6xl text-[#1A1A1A] font-normal">
          Bizimle İletişime Geçin
        </h1>
        <p className="text-xs sm:text-sm text-[#666666] leading-relaxed">
          Tesisimizi ziyaret etmek, randevu almak veya düğün tarihinizi sorgulatmak için bize ulaşabilirsiniz.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-start">
        
        {/* LEFT CONTACT INFO */}
        <div className="lg:col-span-5 space-y-6">
          <div className="bg-white p-8 rounded-2xl border border-[#E6E1D8] shadow-lg space-y-6">
            <h3 className="font-serif font-bold text-xl text-[#1A1A1A] border-b border-[#E6E1D8] pb-3">
              Tesis Bilgileri
            </h3>

            <div className="space-y-4 text-xs text-[#333333]">
              <div>
                <p className="font-bold text-[#1A1A1A]">Açık Adres:</p>
                <p className="text-[#666666]">Sapanca Göl Caddesi No:10, Sakarya / Türkiye</p>
              </div>

              <div>
                <p className="font-bold text-[#1A1A1A]">Telefon:</p>
                <a href="tel:+905321112233" className="text-[#1A1A1A] font-bold hover:text-[#C5B37D] transition">
                  +90 532 111 2233
                </a>
              </div>

              <div>
                <p className="font-bold text-[#1A1A1A]">E-Posta:</p>
                <p className="text-[#666666]">info@iremdugunsarayi.com</p>
              </div>
            </div>
          </div>

          {/* MAP IFRAME */}
          <div className="h-64 rounded-2xl overflow-hidden border border-[#E6E1D8] shadow-lg">
            <iframe
              title="İrem Düğün Sarayı Harita Konumu"
              src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d12089.444390022204!2d30.27!3d40.69!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x0!2zNDDCsDQxJzI0LjAiTiAzMMKwMTYnMTIuMCJF!5e0!3m2!1str!2str!4v1620000000000!5m2!1str!2str"
              className="w-full h-full border-0"
              loading="lazy"
            />
          </div>
        </div>

        {/* RIGHT CONTACT FORM */}
        <div className="lg:col-span-7 bg-white p-8 sm:p-10 rounded-2xl border border-[#E6E1D8] shadow-xl space-y-6">
          <div className="space-y-1">
            <h3 className="font-serif font-bold text-2xl text-[#1A1A1A]">Mesaj Gönderin</h3>
            <p className="text-xs text-[#666666]">Sorularınızı ve randevu taleplerinizi aşağıdaki formdan iletebilirsiniz.</p>
          </div>

          {submitted ? (
            <div className="bg-[#F5F2ED] border border-[#C5B37D] p-6 rounded-xl text-center space-y-2">
              <div className="text-3xl">✨</div>
              <h4 className="font-serif font-bold text-[#1A1A1A]">Mesajınız Ulaştı!</h4>
              <p className="text-xs text-[#666666]">Ekibimiz en kısa sürede sizinle iletişime geçecektir.</p>
            </div>
          ) : (
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-bold text-[#1A1A1A] mb-1">Adınız Soyadınız *</label>
                  <input
                    type="text"
                    required
                    value={form.name}
                    onChange={e => setForm({ ...form, name: e.target.value })}
                    className="w-full bg-[#F5F2ED] border border-[#E6E1D8] focus:border-[#C5B37D] text-[#1A1A1A] text-xs px-4 py-3 rounded-lg outline-none"
                  />
                </div>

                <div>
                  <label className="block text-xs font-bold text-[#1A1A1A] mb-1">Telefon Numarası *</label>
                  <input
                    type="tel"
                    required
                    value={form.phone}
                    onChange={e => setForm({ ...form, phone: e.target.value })}
                    className="w-full bg-[#F5F2ED] border border-[#E6E1D8] focus:border-[#C5B37D] text-[#1A1A1A] text-xs px-4 py-3 rounded-lg outline-none"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-bold text-[#1A1A1A] mb-1">Konu</label>
                <input
                  type="text"
                  placeholder="Örn: Rezervasyon Randevusu Talebi"
                  value={form.subject}
                  onChange={e => setForm({ ...form, subject: e.target.value })}
                  className="w-full bg-[#F5F2ED] border border-[#E6E1D8] focus:border-[#C5B37D] text-[#1A1A1A] text-xs px-4 py-3 rounded-lg outline-none"
                />
              </div>

              <div>
                <label className="block text-xs font-bold text-[#1A1A1A] mb-1">Mesajınız</label>
                <textarea
                  rows="4"
                  value={form.message}
                  onChange={e => setForm({ ...form, message: e.target.value })}
                  className="w-full bg-[#F5F2ED] border border-[#E6E1D8] focus:border-[#C5B37D] text-[#1A1A1A] text-xs p-4 rounded-lg outline-none"
                  placeholder="Detaylı bilgi veya sormak istediğiniz sorular..."
                />
              </div>

              <button type="submit" className="w-full bg-[#1A1A1A] hover:bg-[#2c2c2c] text-[#F5F2ED] border border-[#C5B37D] font-bold text-xs py-4 rounded-full shadow-lg uppercase tracking-widest">
                MESAJI GÖNDER
              </button>
            </form>
          )}
        </div>

      </div>

    </div>
  );
}
