import { Link } from 'react-router-dom'
import HealthStatusCard from '../components/HealthStatusCard'

export default function HomePage() {
  return (
    <div className="space-y-8">
      <section className="text-center py-10">
        <h1 className="text-4xl font-extrabold tracking-tight text-neutral-900">
          Welcome to <span className="text-orange-600">FLUX</span>
        </h1>
        <p className="mt-3 text-neutral-600 max-w-xl mx-auto">
          An AI-powered business intelligence assistant helping Indian street
          vendors and micro-entrepreneurs forecast demand, plan inventory,
          and access government schemes.
        </p>
        <div className="mt-6 flex justify-center gap-3">
          <Link
            to="/vendor"
            className="px-6 py-2.5 rounded-lg bg-orange-600 text-white font-medium hover:bg-orange-700 transition shadow-sm"
          >
            Open Vendor Dashboard & Schemes →
          </Link>
        </div>
      </section>

      <HealthStatusCard />

      <section className="grid sm:grid-cols-3 gap-4">
        {[
          {
            title: 'Demand Forecasting',
            desc: 'ML-driven predictions for daily sales with uncertainty bounds.',
            status: 'Live',
            statusColor: 'text-emerald-700 bg-emerald-50 border-emerald-200',
            link: '/vendor',
          },
          {
            title: 'Smart Recommendations',
            desc: 'Actionable prep quantities, expected revenue, and weather awareness.',
            status: 'Live',
            statusColor: 'text-emerald-700 bg-emerald-50 border-emerald-200',
            link: '/vendor',
          },
          {
            title: 'Scheme Assistant (RAG)',
            desc: 'Grounded answers on PM SVANidhi, MUDRA, Vishwakarma, and subsidies.',
            status: 'Live',
            statusColor: 'text-emerald-700 bg-emerald-50 border-emerald-200',
            link: '/vendor',
          },
        ].map((f) => (
          <Link
            to={f.link}
            key={f.title}
            className="rounded-xl border border-neutral-200 bg-white p-5 shadow-sm hover:border-orange-300 hover:shadow-md transition flex flex-col justify-between"
          >
            <div>
              <div className="flex items-center justify-between mb-2">
                <h3 className="font-semibold text-neutral-800">{f.title}</h3>
                <span
                  className={`text-[11px] font-semibold px-2 py-0.5 rounded-full border ${f.statusColor}`}
                >
                  {f.status}
                </span>
              </div>
              <p className="text-sm text-neutral-500">{f.desc}</p>
            </div>
            <span className="text-xs font-medium text-orange-600 mt-4 flex items-center gap-1">
              Explore feature →
            </span>
          </Link>
        ))}
      </section>
    </div>
  )
}
