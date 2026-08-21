import { Link } from 'react-router-dom'

export default function MainLayout({ children }) {
  return (
    <div className="min-h-screen flex flex-col bg-neutral-50 text-neutral-900">
      <header className="border-b border-neutral-200 bg-white">
        <div className="max-w-5xl mx-auto px-4 py-4 flex items-center justify-between">
          <Link to="/" className="flex items-center gap-2">
            <span className="text-2xl font-bold text-orange-600">FLUX</span>
            <span className="text-sm text-neutral-500 hidden sm:inline">
              Adaptive intelligence for everyday commerce
            </span>
          </Link>
          <nav className="flex items-center gap-4 text-sm">
            <Link to="/vendor" className="text-neutral-600 hover:text-orange-600 font-medium">
              Vendor Dashboard
            </Link>
            <span className="text-neutral-400">OOSC 4.0 &middot; PS5</span>
          </nav>
        </div>
      </header>

      <main className="flex-1 max-w-5xl w-full mx-auto px-4 py-8">{children}</main>

      <footer className="border-t border-neutral-200 py-4 text-center text-xs text-neutral-400">
        FLUX &mdash; AI for Public Good &middot; Built for street vendors and micro-entrepreneurs
      </footer>
    </div>
  )
}
