import { Link } from 'react-router-dom'
import { useLanguage } from '../context/LanguageContext'
import LanguageSelector from '../components/LanguageSelector'

export default function MainLayout({ children }) {
  const { t } = useLanguage()

  return (
    <div className="min-h-screen flex flex-col bg-neutral-50 text-neutral-900">
      <header className="border-b border-neutral-200 bg-white sticky top-0 z-40 shadow-2xs">
        <div className="max-w-5xl mx-auto px-4 py-3 flex items-center justify-between gap-3">
          <Link to="/" className="flex items-center gap-2">
            <span className="text-2xl font-bold text-orange-600 tracking-tight">{t('appTitle')}</span>
            <span className="text-xs text-neutral-500 hidden md:inline border-l border-neutral-200 pl-2">
              {t('appTagline')}
            </span>
          </Link>
          <div className="flex items-center gap-3">
            <nav className="flex items-center gap-3 text-sm">
              <Link
                to="/vendor"
                className="text-neutral-700 hover:text-orange-600 font-medium px-2 py-1 rounded-md hover:bg-neutral-100 transition"
              >
                {t('navVendorDashboard')}
              </Link>
            </nav>
            <LanguageSelector />
          </div>
        </div>
      </header>

      <main className="flex-1 max-w-5xl w-full mx-auto px-4 py-8">{children}</main>

      <footer className="border-t border-neutral-200 py-6 text-center text-xs text-neutral-500 bg-white space-y-2">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-50 border border-emerald-200 text-emerald-700 text-[11px] font-medium">
          <span className="h-2 w-2 rounded-full bg-emerald-500 animate-pulse" />
          <span>All AI Models & Database Services Operational</span>
        </div>
        <p>{t('footerText')}</p>
        <p className="text-[11px] text-neutral-400">{t('hackathonBadge')}</p>
      </footer>
    </div>
  )
}
