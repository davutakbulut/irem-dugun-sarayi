import React from 'react';
import { ThemeIcon } from './ThemeIcon';

/**
 * PageErrorBoundary provides fault-isolation per page / component.
 * If one page or modal encounters a runtime error,
 * only that page displays a fallback UI, preventing the rest of the application
 * (navigation, header, sidebar, and other pages) from crashing.
 */
export class PageErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null, errorInfo: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error(`React ErrorBoundary caught an exception [${this.props.pageName || 'Unknown Page'}]:`, error, errorInfo);
    this.setState({ errorInfo });
  }

  handleReset = () => {
    this.setState({ hasError: false, error: null, errorInfo: null });
    if (this.props.onReset) {
      this.props.onReset();
    }
  };

  render() {
    if (this.state.hasError) {
      return (
        <div className="p-8 max-w-xl mx-auto my-12 glass-panel rounded-3xl border border-red-500/40 shadow-2xl text-center space-y-4 animate-fade-in">
          <div className="w-20 h-20 mx-auto rounded-3xl bg-red-500/10 border border-red-500/30 flex items-center justify-center text-red-500 shadow-inner">
            <ThemeIcon icon="alert" fallbackEmoji="⚠️" className="w-10 h-10 shrink-0" />
          </div>
          <span className="bg-red-500/10 text-red-500 font-extrabold text-xs px-3.5 py-1 rounded-full border border-red-500/30 uppercase tracking-wider inline-block">
            Bileşen / Sayfa Yükleme Uyarısı
          </span>
          <h3 className="text-xl font-heading font-extrabold text-slate-800 dark:text-gray-100">
            {this.props.fallbackTitle || (this.props.pageName ? `${this.props.pageName} Geçici Bir Hata Oluştu` : "Bu Bölümde Beklenmeyen Bir İşlem Oluştu")}
          </h3>
          <p className="text-xs text-slate-500 dark:text-gray-400 max-w-md mx-auto leading-relaxed">
            Sisteminizin diğer tüm bölümleri, navigasyon menünüz ve üst kontrol barınız kesintisiz çalışmaya devam etmektedir. Sol menüden başka bir sayfaya geçebilir veya bu bölümü yenileyebilirsiniz.
          </p>
          {this.state.error && (
            <div className="bg-slate-950/80 text-red-400 font-mono text-[10px] p-3 rounded-xl text-left overflow-x-auto border border-red-500/20 max-h-28 custom-scrollbar">
              {this.state.error.toString()}
            </div>
          )}
          <div className="pt-2 flex flex-col sm:flex-row justify-center gap-3">
            <button
              type="button"
              onClick={this.handleReset}
              className="gold-button font-bold text-xs py-2.5 px-6 rounded-xl shadow-lg inline-flex items-center justify-center space-x-1.5"
            >
              <ThemeIcon icon="refresh" fallbackEmoji="🔄" className="w-3.5 h-3.5 shrink-0" />
              <span>Yeniden Dene & Bölümü Kurtar</span>
            </button>
            {this.props.onNavigateHome && (
              <button
                type="button"
                onClick={() => {
                  this.handleReset();
                  this.props.onNavigateHome('dashboard');
                }}
                className="px-5 py-2.5 bg-slate-200 dark:bg-slate-800 hover:bg-slate-300 dark:hover:bg-slate-700 text-slate-800 dark:text-gray-200 font-semibold rounded-xl text-xs transition-all flex items-center justify-center space-x-1.5"
              >
                <span>🏠 Anasayfaya Dön</span>
              </button>
            )}
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

export default PageErrorBoundary;
