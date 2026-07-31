import React, { useState, useEffect, useRef } from 'react';
import { createPortal } from 'react-dom';
import { ThemeIcon } from '../components/ThemeIcon.jsx';

export function MindMapPageComponent({ navigateTo }) {
  const [selectedNode, setSelectedNode] = useState(MIND_MAP_DATA[0]);
  const [searchQuery, setSearchQuery] = useState('');
  const [activeCategoryFilter, setActiveCategoryFilter] = useState('ALL');
  const [viewMode, setViewMode] = useState('topology'); // 'topology' | 'matrix' | 'workflows' | 'rbac'
  const [zoomLevel, setZoomLevel] = useState(1);

  const categories = ['ALL', 'Architecture', 'UI/UX System', 'Pages', 'Security & Management'];

  const filteredNodes = MIND_MAP_DATA.filter(node => {
    const matchesSearch = node.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
                          node.summary.toLowerCase().includes(searchQuery.toLowerCase()) ||
                          node.whichFeatures.some(f => f.toLowerCase().includes(searchQuery.toLowerCase()));
    const matchesCat = activeCategoryFilter === 'ALL' || node.category === activeCategoryFilter;
    return matchesSearch && matchesCat;
  });

  // Check if a node is connected to the selected node
  const isConnectedNode = (nodeId) => {
    if (!selectedNode) return false;
    return selectedNode.id === nodeId || 
           (selectedNode.connectedNodes && selectedNode.connectedNodes.includes(nodeId));
  };

  return (
    <div className="space-y-6 relative animate-fade-in pb-12">
      
      {/* PAGE HEADER & VIEW MODE TABS */}
      <div className="bg-white dark:bg-brand-card p-6 rounded-3xl border border-slate-200 dark:border-brand-border shadow-sm space-y-4">
        <div className="flex flex-col lg:flex-row justify-between items-start lg:items-center gap-4">
          <div className="flex items-center space-x-3">
            <div className="w-12 h-12 rounded-2xl bg-amber-500/20 border border-amber-500/40 text-amber-700 dark:text-gold-400 flex items-center justify-center text-2xl font-bold">
              <ThemeIcon icon="sparkles" fallbackEmoji="🧠" className="w-6 h-6 shrink-0" />
            </div>
            <div>
              <h2 className="text-2xl font-heading font-extrabold gold-gradient-text">
                İnteraktif Sistem Zihin Haritası & Veri Akış Topolojisi
              </h2>
              <p className="text-xs text-slate-500 dark:text-gray-400 font-medium">
                Modül Bağlantıları, State Bağımlılıkları, Uçtan Uca Kullanıcı Akışları & Mimari Kılavuz
              </p>
            </div>
          </div>

          {/* VIEW MODE SWITCHER BUTTONS */}
          <div className="flex flex-wrap items-center gap-2 bg-slate-100 dark:bg-brand-dark p-1.5 rounded-2xl border border-slate-200 dark:border-brand-border w-full lg:w-auto">
            <button
              onClick={() => setViewMode('topology')}
              className={`px-4 py-2 rounded-xl text-xs font-bold transition flex items-center space-x-1.5 ${
                viewMode === 'topology'
                  ? 'gold-button shadow-xs'
                  : 'text-slate-600 dark:text-gray-400 hover:text-amber-500'
              }`}
            >
              <span>🌳 Topoloji & Ağaç</span>
            </button>

            <button
              onClick={() => setViewMode('workflows')}
              className={`px-4 py-2 rounded-xl text-xs font-bold transition flex items-center space-x-1.5 ${
                viewMode === 'workflows'
                  ? 'gold-button shadow-xs'
                  : 'text-slate-600 dark:text-gray-400 hover:text-amber-500'
              }`}
            >
              <span>🔀 Uçtan Uca Akışlar</span>
            </button>

            <button
              onClick={() => setViewMode('matrix')}
              className={`px-4 py-2 rounded-xl text-xs font-bold transition flex items-center space-x-1.5 ${
                viewMode === 'matrix'
                  ? 'gold-button shadow-xs'
                  : 'text-slate-600 dark:text-gray-400 hover:text-amber-500'
              }`}
            >
              <span>🔗 Veri & State Matrisi</span>
            </button>

            <button
              onClick={() => setViewMode('rbac')}
              className={`px-4 py-2 rounded-xl text-xs font-bold transition flex items-center space-x-1.5 ${
                viewMode === 'rbac'
                  ? 'gold-button shadow-xs'
                  : 'text-slate-600 dark:text-gray-400 hover:text-amber-500'
              }`}
            >
              <span>🛡️ Yetki & RBAC</span>
            </button>
          </div>
        </div>

        {/* CONTROLS & FILTERS (Only shown in topology view) */}
        {viewMode === 'topology' && (
          <div className="pt-3 border-t border-slate-100 dark:border-brand-border/60 flex flex-col md:flex-row justify-between items-start md:items-center gap-3">
            {/* CATEGORY BADGES */}
            <div className="flex items-center space-x-2 overflow-x-auto pb-1 custom-scrollbar w-full md:w-auto">
              {categories.map(cat => (
                <button
                  key={cat}
                  onClick={() => setActiveCategoryFilter(cat)}
                  className={`px-3 py-1 rounded-xl text-xs font-bold transition whitespace-nowrap ${
                    activeCategoryFilter === cat
                      ? 'bg-amber-500 text-white shadow-xs'
                      : 'bg-slate-100 dark:bg-brand-dark text-slate-600 dark:text-gray-400 border border-slate-200 dark:border-brand-border hover:border-amber-500'
                  }`}
                >
                  {cat === 'ALL' ? '🌐 Tüm Modüller' : cat}
                </button>
              ))}
            </div>

            {/* SEARCH & ZOOM */}
            <div className="flex items-center space-x-3 w-full md:w-auto">
              <div className="relative flex-1 md:w-56">
                <input
                  type="text"
                  placeholder="Zihin Haritasında Ara..."
                  value={searchQuery}
                  onChange={e => setSearchQuery(e.target.value)}
                  className="w-full pl-8 pr-3 py-1.5 bg-slate-100 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl text-xs font-bold focus:outline-none focus:border-amber-500 text-slate-800 dark:text-white"
                />
                <span className="absolute left-2.5 top-2 text-slate-400 text-xs">
                  <ThemeIcon icon="search" fallbackEmoji="🔍" className="w-3.5 h-3.5 opacity-60" />
                </span>
              </div>

              <div className="flex items-center space-x-1 bg-slate-100 dark:bg-brand-dark p-1 rounded-xl border border-slate-200 dark:border-brand-border">
                <button
                  onClick={() => setZoomLevel(prev => Math.max(0.7, prev - 0.1))}
                  className="px-2 py-0.5 text-xs font-bold hover:bg-amber-500/20 rounded"
                  title="Uzaklaş"
                >
                  -
                </button>
                <span className="text-[10px] font-mono font-bold px-1 text-slate-800 dark:text-white">{Math.round(zoomLevel * 100)}%</span>
                <button
                  onClick={() => setZoomLevel(prev => Math.min(1.3, prev + 0.1))}
                  className="px-2 py-0.5 text-xs font-bold hover:bg-amber-500/20 rounded"
                  title="Yakınlaş"
                >
                  +
                </button>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* VIEW 1: TOPOLOGY & MIND MAP CANVAS */}
      {viewMode === 'topology' && (
        <div className="glass-panel p-6 rounded-3xl border border-slate-200 dark:border-brand-border shadow-sm min-h-[620px] overflow-auto custom-scrollbar relative">
          
          <div
            style={{ transform: `scale(${zoomLevel})`, transformOrigin: 'top left' }}
            className="transition-transform duration-200 space-y-8"
          >
            {/* ROOT NODE (CENTER SYSTEM ROOT) */}
            <div className="flex justify-center">
              <div className="bg-gradient-to-r from-amber-500 via-amber-600 to-yellow-600 text-white p-5 rounded-3xl shadow-xl border-4 border-amber-300 dark:border-amber-400/40 text-center max-w-md">
                <div className="text-3xl mb-1 flex justify-center">
                  <ThemeIcon icon="venue" fallbackEmoji="🏰" className="w-8 h-8 text-white" />
                </div>
                <h3 className="text-lg font-heading font-black tracking-wide">
                  İREM DÜĞÜN SARAYI CORE ECOSYSTEM
                </h3>
                <p className="text-[11px] text-amber-100 font-medium mt-1">
                  Çift Mimarili Dijital Yönetim & Organizasyon Platformu
                </p>
                <div className="mt-2 text-[10px] bg-black/20 py-1 px-3 rounded-full inline-block font-mono">
                  Seçili Modül: <strong className="text-gold-400">{selectedNode?.title}</strong> (Bağlantılı modüller parlar)
                </div>
              </div>
            </div>

            {/* CONNECTOR LINE SVG */}
            <div className="w-full flex justify-center opacity-30">
              <div className="w-0.5 h-8 bg-amber-500"></div>
            </div>

            {/* BRANCH NODES GRID */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {filteredNodes.map(node => {
                const isSelected = selectedNode?.id === node.id;
                const connected = isConnectedNode(node.id);

                return (
                  <div
                    key={node.id}
                    onClick={() => setSelectedNode(node)}
                    className={`p-5 rounded-2xl border-2 transition-all cursor-pointer relative group ${
                      isSelected
                        ? `${node.borderColor} bg-white dark:bg-brand-card shadow-2xl scale-[1.03] ring-4 ring-amber-500/30 z-10`
                        : connected
                        ? 'border-amber-400 dark:border-amber-500/80 bg-amber-50/40 dark:bg-amber-950/20 shadow-md scale-[1.01]'
                        : 'border-slate-200 dark:border-brand-border bg-white dark:bg-brand-card hover:border-amber-500/60 shadow-xs'
                    }`}
                  >
                    {/* TOP BADGES */}
                    <div className="flex justify-between items-center mb-3">
                      <span className={`text-[10px] font-extrabold px-2.5 py-0.5 rounded-full ${node.bgColor} text-amber-700 dark:text-gold-400 border border-amber-500/30 uppercase tracking-wider`}>
                        {node.category}
                      </span>
                      {isSelected ? (
                        <span className="text-[10px] font-bold text-amber-600 bg-amber-100 dark:bg-amber-900/40 px-2 py-0.5 rounded-full animate-pulse">
                          🎯 Aktif Seçim
                        </span>
                      ) : connected ? (
                        <span className="text-[10px] font-bold text-amber-600 dark:text-gold-400 bg-amber-500/10 px-2 py-0.5 rounded-full">
                          🔗 Bağlantılı
                        </span>
                      ) : null}
                    </div>

                    {/* TITLE & SUMMARY */}
                    <div className="flex items-center space-x-2 mb-1">
                      <ThemeIcon icon={node.icon} fallbackEmoji={node.fallbackEmoji} className="w-5 h-5 text-amber-500 shrink-0" />
                      <h4 className="font-heading font-bold text-base text-slate-900 dark:text-white group-hover:text-amber-600 transition">
                        {node.title}
                      </h4>
                    </div>
                    <p className="text-xs text-slate-500 dark:text-gray-400 line-clamp-2 font-medium">
                      {node.summary}
                    </p>

                    {/* STATE DEPENDENCY CHIPS */}
                    <div className="mt-3 pt-2 border-t border-slate-100 dark:border-brand-border/40 flex flex-wrap gap-1">
                      {node.readsState?.map(st => (
                        <span key={st} className="text-[9px] bg-slate-100 dark:bg-brand-dark text-slate-600 dark:text-gray-400 px-1.5 py-0.5 rounded font-mono">
                          👁️ {st}
                        </span>
                      ))}
                      {node.mutatesState?.map(st => (
                        <span key={st} className="text-[9px] bg-emerald-500/10 text-emerald-700 dark:text-emerald-400 px-1.5 py-0.5 rounded font-mono font-bold">
                          ✏️ {st}
                        </span>
                      ))}
                    </div>

                    {/* BOTTOM ACTION INDICATOR */}
                    <div className="mt-3 flex justify-between items-center text-[11px] font-bold text-amber-600 dark:text-gold-400">
                      <span>İncele & Bağlantıları Gör</span>
                      <span>→</span>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      )}

      {/* VIEW 2: END-TO-END WORKFLOW DIAGRAMS */}
      {viewMode === 'workflows' && (
        <div className="space-y-6">
          {E2E_WORKFLOWS.map(flow => (
            <div key={flow.id} className={`bg-white dark:bg-brand-card p-6 rounded-3xl border-2 ${flow.color} shadow-sm space-y-4`}>
              <h3 className="text-lg font-heading font-extrabold text-slate-900 dark:text-white">
                {flow.title}
              </h3>
              
              <div className="grid grid-cols-1 md:grid-cols-5 gap-3 relative">
                {flow.steps.map((step, idx) => (
                  <div key={idx} className="bg-slate-50 dark:bg-brand-dark p-4 rounded-2xl border border-slate-200 dark:border-brand-border relative flex flex-col justify-between">
                    <div>
                      <div className="w-8 h-8 rounded-xl bg-amber-500 text-white font-black text-xs flex items-center justify-center mb-2 shadow-sm">
                        {step.num}
                      </div>
                      <h4 className="font-bold text-xs text-slate-900 dark:text-white mb-1">
                        {step.title}
                      </h4>
                      <p className="text-[11px] text-slate-500 dark:text-gray-400 leading-relaxed">
                        {step.desc}
                      </p>
                    </div>
                    {idx < flow.steps.length - 1 && (
                      <div className="hidden md:block absolute -right-3 top-1/2 -translate-y-1/2 text-amber-500 text-lg font-bold z-10">
                        ➔
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}

      {/* VIEW 3: DATA & STATE DEPENDENCY MATRIX */}
      {viewMode === 'matrix' && (
        <div className="bg-white dark:bg-brand-card p-6 rounded-3xl border border-slate-200 dark:border-brand-border shadow-sm space-y-4">
          <div>
            <h3 className="text-xl font-heading font-extrabold text-slate-900 dark:text-white">
              🔗 Hangi Değer Nereye Bağlı? (State Bağımlılık Matrisi)
            </h3>
            <p className="text-xs text-slate-500 dark:text-gray-400">
              Sistemdeki ana state değişkenleri, nereden beslendikleri, hangi modüllerce okundukları ve güncellendikleri
            </p>
          </div>

          <div className="overflow-x-auto custom-scrollbar">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-100 dark:bg-brand-dark text-slate-700 dark:text-gray-300 font-extrabold uppercase border-b border-slate-200 dark:border-brand-border">
                <tr>
                  <th className="p-3">State Değişkeni</th>
                  <th className="p-3">Açıklama & Depo</th>
                  <th className="p-3 text-blue-600 dark:text-blue-400">Veriyi Okuyan Modüller (Readers)</th>
                  <th className="p-3 text-emerald-600 dark:text-emerald-400">Veriyi Değiştiren Modüller (Mutators)</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 dark:divide-brand-border/40">
                {DATA_FLOW_MATRIX.map(row => (
                  <tr key={row.stateName} className="hover:bg-slate-50 dark:hover:bg-brand-dark/40 transition">
                    <td className="p-3 font-mono font-bold text-amber-600 dark:text-gold-400 whitespace-nowrap">
                      {row.stateName}
                    </td>
                    <td className="p-3">
                      <div className="font-bold text-slate-800 dark:text-white">{row.label}</div>
                      <div className="text-[10px] text-slate-400 font-mono">{row.storage}</div>
                    </td>
                    <td className="p-3">
                      <div className="flex flex-wrap gap-1">
                        {row.readers.map(r => (
                          <span key={r} className="bg-blue-500/10 text-blue-700 dark:text-blue-300 px-2 py-0.5 rounded text-[10px] font-semibold">
                            {r}
                          </span>
                        ))}
                      </div>
                    </td>
                    <td className="p-3">
                      <div className="flex flex-wrap gap-1">
                        {row.mutators.map(m => (
                          <span key={m} className="bg-emerald-500/10 text-emerald-700 dark:text-emerald-300 px-2 py-0.5 rounded text-[10px] font-semibold">
                            {m}
                          </span>
                        ))}
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* VIEW 4: SECURITY & RBAC SCHEME */}
      {viewMode === 'rbac' && (
        <div className="bg-white dark:bg-brand-card p-6 rounded-3xl border border-slate-200 dark:border-brand-border shadow-sm space-y-6">
          <div>
            <h3 className="text-xl font-heading font-extrabold text-slate-900 dark:text-white">
              🛡️ Rol Bazlı Erişim Denetim Şeması (RBAC Hierarchy)
            </h3>
            <p className="text-xs text-slate-500 dark:text-gray-400">
              Kullanıcı rollerinin sistemdeki yetki sınırları ve korunan modüller
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="bg-amber-500/10 border border-amber-500/40 p-5 rounded-2xl space-y-3">
              <span className="text-xs font-black bg-amber-500 text-white px-3 py-1 rounded-full uppercase tracking-wider">
                👑 Süper Admin (SuperAdmin)
              </span>
              <h4 className="font-bold text-sm text-slate-900 dark:text-white">Tam Sistem Yetkisi</h4>
              <p className="text-xs text-slate-600 dark:text-gray-300">
                Tüm sayfaları görüntüleme, rezervasyon ve finansal kayıt silme, rol izin matrisini değiştirme yetkisi.
              </p>
            </div>

            <div className="bg-blue-500/10 border border-blue-500/40 p-5 rounded-2xl space-y-3">
              <span className="text-xs font-black bg-blue-500 text-white px-3 py-1 rounded-full uppercase tracking-wider">
                🛡️ Moderatör (Moderator)
              </span>
              <h4 className="font-bold text-sm text-slate-900 dark:text-white">Operasyonel Yönetim</h4>
              <p className="text-xs text-slate-600 dark:text-gray-300">
                Rezervasyon ve müşteri ekleme/düzenleme yapar. Finans silme ve RBAC ayarları yetkisi kısıtlanabilir.
              </p>
            </div>

            <div className="bg-slate-500/10 border border-slate-500/40 p-5 rounded-2xl space-y-3">
              <span className="text-xs font-black bg-slate-600 text-white px-3 py-1 rounded-full uppercase tracking-wider">
                👤 Resepsiyon / Satışçı
              </span>
              <h4 className="font-bold text-sm text-slate-900 dark:text-white">Sınırlı Veri Girişi</h4>
              <p className="text-xs text-slate-600 dark:text-gray-300">
                Sadece yeni rezervasyon oluşturma ve takvim inceleme yapabilir. Finans ve ayarlar sayfasına erişimi engellenebilir (403).
              </p>
            </div>
          </div>
        </div>
      )}

      {/* INSPECTOR SIDE-SHEET DRAWER FOR SELECTED NODE */}
      {selectedNode && (
        <div className="fixed inset-y-0 right-0 w-full sm:w-[500px] bg-white dark:bg-brand-card border-l border-slate-200 dark:border-brand-border shadow-2xl z-50 flex flex-col animate-slide-in-right">
          {/* DRAWER HEADER */}
          <div className="p-6 border-b border-slate-200 dark:border-brand-border flex justify-between items-start bg-slate-50 dark:bg-brand-dark/50">
            <div>
              <span className="text-[10px] font-extrabold px-2.5 py-0.5 rounded-full bg-amber-500/20 text-amber-700 dark:text-gold-400 border border-amber-500/30 uppercase tracking-wider">
                {selectedNode.category}
              </span>
              <div className="flex items-center space-x-2 mt-2">
                <ThemeIcon icon={selectedNode.icon} fallbackEmoji={selectedNode.fallbackEmoji} className="w-6 h-6 text-amber-500 shrink-0" />
                <h3 className="text-xl font-heading font-extrabold text-slate-900 dark:text-white">
                  {selectedNode.title}
                </h3>
              </div>
            </div>
            <button
              onClick={() => setSelectedNode(null)}
              className="w-8 h-8 rounded-full bg-slate-200 dark:bg-brand-dark text-slate-600 dark:text-gray-300 font-bold hover:bg-red-500 hover:text-white transition flex items-center justify-center text-sm"
            >
              ✕
            </button>
          </div>

          {/* QUICK NAVIGATE ACTION BAR */}
          <div className="p-4 bg-amber-500/10 border-b border-amber-500/20 flex justify-between items-center">
            <span className="text-xs font-bold text-amber-800 dark:text-gold-400">
              Bu modülü canlı sistemde denemek ister misiniz?
            </span>
            <button
              onClick={() => {
                if (navigateTo && selectedNode.relatedRoute) {
                  navigateTo(selectedNode.relatedRoute);
                }
              }}
              className="gold-button font-bold text-xs py-1.5 px-4 rounded-xl shadow-sm flex items-center space-x-1"
            >
              <span>🚀 Sayfaya Git</span>
            </button>
          </div>

          {/* DRAWER BODY CONTENT */}
          <div className="flex-1 overflow-y-auto p-6 space-y-6 custom-scrollbar">
            
            {/* CONNECTED NODES CHIPS */}
            {selectedNode.connectedNodes && selectedNode.connectedNodes.length > 0 && (
              <div className="space-y-2">
                <h4 className="font-bold text-xs text-amber-700 dark:text-gold-400 uppercase tracking-wider">
                  🔗 Doğrudan Etkileşimde Olduğu Modüller
                </h4>
                <div className="flex flex-wrap gap-2">
                  {selectedNode.connectedNodes.map(cId => {
                    const targetNode = MIND_MAP_DATA.find(n => n.id === cId);
                    if (!targetNode) return null;
                    return (
                      <button
                        key={cId}
                        onClick={() => setSelectedNode(targetNode)}
                        className="text-xs bg-amber-500/10 hover:bg-amber-500/20 text-amber-800 dark:text-gold-400 px-3 py-1 rounded-xl border border-amber-500/30 transition flex items-center space-x-1 font-semibold"
                      >
                        <span>• {targetNode.title}</span>
                      </button>
                    );
                  })}
                </div>
              </div>
            )}

            {/* READS & MUTATES STATE */}
            <div className="grid grid-cols-2 gap-3">
              <div className="bg-slate-50 dark:bg-brand-dark p-3 rounded-2xl border border-slate-200 dark:border-brand-border">
                <div className="text-[10px] font-bold text-blue-600 dark:text-blue-400 uppercase mb-1">
                  👁️ Okuduğu State (Reads)
                </div>
                <div className="flex flex-wrap gap-1">
                  {selectedNode.readsState?.map(s => (
                    <span key={s} className="text-[10px] font-mono bg-blue-500/10 text-blue-700 dark:text-blue-300 px-1.5 py-0.5 rounded">
                      {s}
                    </span>
                  )) || <span className="text-xs text-gray-400">Yok</span>}
                </div>
              </div>

              <div className="bg-slate-50 dark:bg-brand-dark p-3 rounded-2xl border border-slate-200 dark:border-brand-border">
                <div className="text-[10px] font-bold text-emerald-600 dark:text-emerald-400 uppercase mb-1">
                  ✏️ Değiştirdiği State (Mutates)
                </div>
                <div className="flex flex-wrap gap-1">
                  {selectedNode.mutatesState?.map(s => (
                    <span key={s} className="text-[10px] font-mono bg-emerald-500/10 text-emerald-700 dark:text-emerald-300 px-1.5 py-0.5 rounded">
                      {s}
                    </span>
                  )) || <span className="text-xs text-gray-400">Yok</span>}
                </div>
              </div>
            </div>

            {/* WHAT IT DOES */}
            <div className="space-y-2">
              <h4 className="font-bold text-xs text-amber-700 dark:text-gold-400 uppercase tracking-wider">
                📌 Modülün Görevi & Amacı
              </h4>
              <p className="text-xs text-slate-700 dark:text-gray-300 leading-relaxed font-medium bg-slate-50 dark:bg-brand-dark p-3 rounded-2xl border border-slate-200 dark:border-brand-border">
                {selectedNode.whatItDoes}
              </p>
            </div>

            {/* FEATURES */}
            <div className="space-y-2">
              <h4 className="font-bold text-xs text-amber-700 dark:text-gold-400 uppercase tracking-wider">
                ✨ İçerdiği Alt Özellikler
              </h4>
              <ul className="space-y-2">
                {selectedNode.whichFeatures.map((feat, idx) => (
                  <li key={idx} className="text-xs text-slate-700 dark:text-gray-300 flex items-start space-x-2 bg-slate-50 dark:bg-brand-dark p-2.5 rounded-xl border border-slate-100 dark:border-brand-border/40 font-medium">
                    <span className="text-amber-500 font-bold">•</span>
                    <span>{feat}</span>
                  </li>
                ))}
              </ul>
            </div>

            {/* RULES */}
            <div className="space-y-2">
              <h4 className="font-bold text-xs text-amber-700 dark:text-gold-400 uppercase tracking-wider">
                🛡️ İş Mantığı & Kritik Kurallar
              </h4>
              <ul className="space-y-2">
                {selectedNode.rulesAndCore.map((rule, idx) => (
                  <li key={idx} className="text-xs text-amber-900 dark:text-amber-200 bg-amber-500/10 p-2.5 rounded-xl border border-amber-500/30 font-medium">
                    {rule}
                  </li>
                ))}
              </ul>
            </div>

            {/* STEP BY STEP FLOW */}
            <div className="space-y-2">
              <h4 className="font-bold text-xs text-amber-700 dark:text-gold-400 uppercase tracking-wider">
                🔄 Adım Adım Kullanım Adımları
              </h4>
              <div className="space-y-2">
                {selectedNode.stepByStepFlow.map((step, idx) => (
                  <div key={idx} className="text-xs text-slate-700 dark:text-gray-300 bg-slate-50 dark:bg-brand-dark p-2.5 rounded-xl border border-slate-200 dark:border-brand-border font-medium">
                    {step}
                  </div>
                ))}
              </div>
            </div>

          </div>

          {/* DRAWER FOOTER */}
          <div className="p-4 border-t border-slate-200 dark:border-brand-border bg-slate-50 dark:bg-brand-dark/50 flex justify-end">
            <button
              onClick={() => setSelectedNode(null)}
              className="px-4 py-2 bg-slate-200 dark:bg-brand-dark text-slate-700 dark:text-gray-300 rounded-xl text-xs font-bold hover:bg-slate-300 transition"
            >
              Kapat
            </button>
          </div>
        </div>
      )}
    </div>
  );
}


// --- PROFILE COMPONENT ---
