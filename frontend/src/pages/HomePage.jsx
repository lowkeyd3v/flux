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
      </section>

      <HealthStatusCard />

      <section className="grid sm:grid-cols-3 gap-4">
        {[
          { title: 'Demand Forecasting', desc: 'ML-driven predictions for daily sales.' },
          { title: 'Smart Recommendations', desc: 'Actionable, explainable business decisions.' },
          { title: 'Scheme Assistant', desc: 'RAG-grounded answers on government schemes.' },
        ].map((f) => (
          <div
            key={f.title}
            className="rounded-xl border border-neutral-200 bg-white p-5 shadow-sm"
          >
            <h3 className="font-semibold text-neutral-800">{f.title}</h3>
            <p className="text-sm text-neutral-500 mt-1">{f.desc}</p>
            <p className="text-xs text-neutral-400 mt-2 italic">Coming in a later milestone</p>
          </div>
        ))}
      </section>
    </div>
  )
}
