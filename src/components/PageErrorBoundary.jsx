import React from 'react';

/**
 * PageErrorBoundary provides fault-isolation per page.
 * If one page (e.g., CreateReservationPage) encounters a runtime error,
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
    console.error(`PageErrorBoundary caught an error in [${this.props.pageName || 'Unknown Page'}]:`, error, errorInfo);
    this.setState({ errorInfo });
  }

  handleReset = () => {
    this.setState({ hasError: false, error: null, errorInfo: null });
  };

  render() {
    if (this.state.hasError) {
      const pageTitle = this.props.pageName || 'Bu Sayfada';
      return (
        <div className="min-h-[400px] flex items-center justify-center p-6">
          <div className="bg-red-500/10 border border-red-500/30 dark:bg-red-950/30 rounded-3xl p-8 max-w-lg w-full text-center space-y-5 shadow-2xl backdrop-blur-md">
            <div className="w-16 h-16 bg-red-500/20 text-red-500 rounded-full flex items-center justify-center mx-auto text-3xl font-bold animate-pulse">
              ⚠️
            </div>
            
            <div className="space-y-2">
              <h3 className="text-xl font-bold text-slate-800 dark:text-gray-100">
                {pageTitle} Geçici Bir Hata Oluştu
              </h3>
              <p className="text-sm text-slate-600 dark:text-gray-400">
                Bu sayfa yüklenirken bir aksaklık yaşandı. Ancak <strong className="text-amber-600 dark:text-gold-400">sistemin diğer tüm sayfaları kesintisiz çalışmaya devam etmektedir</strong>.
              </p>
            </div>

            {this.state.error && (
              <div className="bg-slate-900/80 text-red-300 p-3 rounded-xl text-xs font-mono text-left overflow-x-auto border border-red-500/20 max-h-32 custom-scrollbar">
                {this.state.error.toString()}
              </div>
            )}

            <div className="flex flex-col sm:flex-row gap-3 justify-center pt-2">
              <button
                onClick={this.handleReset}
                className="px-5 py-2.5 bg-gradient-to-r from-amber-500 to-amber-600 hover:from-amber-600 hover:to-amber-700 text-slate-950 font-bold rounded-xl shadow-lg transition-all text-xs"
              >
                🔄 Sayfayı Yeniden Dene
              </button>
              {this.props.onNavigateHome && (
                <button
                  onClick={() => {
                    this.handleReset();
                    this.props.onNavigateHome('dashboard');
                  }}
                  className="px-5 py-2.5 bg-slate-200 dark:bg-slate-800 hover:bg-slate-300 dark:hover:bg-slate-700 text-slate-800 dark:text-gray-200 font-semibold rounded-xl text-xs transition-all"
                >
                  🏠 Anasayfaya Dön
                </button>
              )}
            </div>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}
