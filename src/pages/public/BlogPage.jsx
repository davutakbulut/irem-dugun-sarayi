import React, { useState } from 'react';

export default function BlogPage() {
  const [selectedPost, setSelectedPost] = useState(null);

  const posts = [
    {
      id: 1,
      title: '2026 Düğün Trendleri: Göl Kenarında Kır Düğünü ve Şık Detaylar',
      category: 'Düğün Trendleri',
      date: '04 Ağustos 2026',
      readTime: '5 dk okuma',
      img: 'https://images.unsplash.com/photo-1519741497674-611481863552?auto=format&fit=crop&w=800&q=80',
      summary: '2026 yılında düğün konseptlerinde en çok öne çıkan doğal pastel tonlar, açık hava organizasyonları ve kişiselleştirilmiş gelin şovları.',
      content: `Düğün hazırlığındaki çiftler için 2026 yılı, doğallık ve lüksün harmanlandığı özel bir dönem. Sapanca Göl kenarında gerçekleştirdiğimiz organizasyonlarda bu sezon en çok tercih edilen trendleri derledik...`,
    },
    {
      id: 2,
      title: 'Düğün Bütçesi Planlarken Dikkat Edilmesi Gereken 10 Altın Kural',
      category: 'Bütçe & Planlama',
      date: '28 Temmuz 2026',
      readTime: '7 dk okuma',
      img: 'https://images.unsplash.com/photo-1544078751-58fee2d8a03b?auto=format&fit=crop&w=800&q=80',
      summary: 'Düğün organizasyonunda sürpriz masraflardan kaçınmak ve bütçenizi en verimli şekilde kullanmak için uzman rehberimiz.',
      content: `Düğün hazırlık süreci heyecanlı olduğu kadar bütçe disiplini gerektiren bir dönemdir. Salon seçiminden menü tercihlerine kadar sürpriz masrafların önüne geçecek ipuçları...`,
    },
    {
      id: 3,
      title: 'Kına Gecesinde Geleneksel ve Modern Şovların Uyumu',
      category: 'Kına Rehberi',
      date: '15 Temmuz 2026',
      readTime: '4 dk okuma',
      img: 'https://images.unsplash.com/photo-1469371670807-013ccf25f16a?auto=format&fit=crop&w=800&q=80',
      summary: 'Kına tahtı seçiminden nedime şovlarına, testi kırma seremonisinden ikram çeşitlerine unutulmaz kına detayları.',
      content: `Geleneksel kına seremonisini modern dans şovlarıyla birleştirmek isteyen gelin adayları için hazırladığımız özel konsept rehberi...`,
    },
  ];

  return (
    <div className="max-w-7xl mx-auto px-6 sm:px-12 py-12 space-y-12">
      
      {/* HEADER */}
      <div className="text-center space-y-4 max-w-3xl mx-auto">
        <span className="text-amber-500 font-extrabold text-xs uppercase tracking-widest">
          📝 Düğün Rehberi & İpuçları
        </span>
        <h1 className="text-4xl sm:text-5xl font-heading font-extrabold text-white">
          Blog & İlham Veren Rehberler
        </h1>
        <p className="text-xs sm:text-sm text-slate-300 leading-relaxed">
          Düğün hazırlık sürecinizi kolaylaştıracak trendler, bütçe ipuçları ve konsept tavsiyeleri.
        </p>
      </div>

      {/* POSTS GRID */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        {posts.map((post) => (
          <article
            key={post.id}
            onClick={() => setSelectedPost(post)}
            className="bg-slate-900/90 rounded-3xl border border-slate-800 hover:border-amber-500/50 overflow-hidden shadow-2xl transition duration-300 cursor-pointer group flex flex-col justify-between"
          >
            <div className="relative h-52 overflow-hidden">
              <img src={post.img} alt={post.title} className="w-full h-full object-cover group-hover:scale-105 transition duration-500" />
              <span className="absolute top-3 left-3 bg-amber-500 text-slate-950 font-black text-[10px] px-2.5 py-1 rounded-full">
                {post.category}
              </span>
            </div>

            <div className="p-6 space-y-3 flex-1 flex flex-col justify-between">
              <div className="space-y-2">
                <div className="flex justify-between items-center text-[10px] text-slate-400 font-medium">
                  <span>{post.date}</span>
                  <span>{post.readTime}</span>
                </div>
                <h3 className="font-heading font-extrabold text-base text-white group-hover:text-amber-400 transition leading-snug">
                  {post.title}
                </h3>
                <p className="text-xs text-slate-300 line-clamp-3">
                  {post.summary}
                </p>
              </div>

              <div className="pt-3 border-t border-slate-800 text-amber-400 font-bold text-xs flex items-center justify-between">
                <span>Devamını Oku</span>
                <span>→</span>
              </div>
            </div>
          </article>
        ))}
      </div>

      {/* READ MODAL */}
      {selectedPost && (
        <div className="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-md flex items-center justify-center p-4">
          <div className="bg-slate-900 text-white p-8 rounded-3xl border border-amber-500/40 max-w-2xl w-full max-h-[80vh] overflow-y-auto space-y-4 shadow-2xl relative">
            <button
              onClick={() => setSelectedPost(null)}
              className="absolute top-4 right-4 text-slate-400 hover:text-white font-bold text-xl"
            >
              ✕
            </button>
            <span className="text-amber-400 text-xs font-bold uppercase">{selectedPost.category}</span>
            <h2 className="text-2xl font-heading font-extrabold">{selectedPost.title}</h2>
            <div className="text-xs text-slate-400">{selectedPost.date} • {selectedPost.readTime}</div>
            <img src={selectedPost.img} alt={selectedPost.title} className="w-full h-64 object-cover rounded-2xl" />
            <p className="text-xs sm:text-sm text-slate-300 leading-relaxed pt-2">
              {selectedPost.content}
            </p>
          </div>
        </div>
      )}

    </div>
  );
}
