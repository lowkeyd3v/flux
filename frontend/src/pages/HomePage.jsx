import { Link } from 'react-router-dom'
import { useLanguage } from '../context/LanguageContext'

export default function HomePage() {
  const { t } = useLanguage()

  const features = [
    {
      title: t('homeFeatureDemandTitle'),
      desc: t('homeFeatureDemandDesc'),
      status: t('statusLive'),
      statusColor: 'text-emerald-700 bg-emerald-50 border-emerald-200',
      link: '/vendor',
      icon: '📈',
    },
    {
      title: t('homeFeatureRecTitle'),
      desc: t('homeFeatureRecDesc'),
      status: t('statusLive'),
      statusColor: 'text-emerald-700 bg-emerald-50 border-emerald-200',
      link: '/vendor',
      icon: '💡',
    },
    {
      title: t('homeFeatureSchemeTitle'),
      desc: t('homeFeatureSchemeDesc'),
      status: t('statusLive'),
      statusColor: 'text-emerald-700 bg-emerald-50 border-emerald-200',
      link: '/vendor',
      icon: '🏛️',
    },
    {
      title: t('homeFeatureVoiceTitle'),
      desc: t('homeFeatureVoiceDesc'),
      status: t('statusLive'),
      statusColor: 'text-emerald-700 bg-emerald-50 border-emerald-200',
      link: '/vendor',
      icon: '🎙️',
    },
  ]

  const workflowSteps = [
    {
      step: '01',
      title: 'Store Profile & Sales',
      desc: 'Set daily inventory, unit price, and budget. Log daily sales records effortlessly.',
      icon: '🛒',
    },
    {
      step: '02',
      title: 'ML Demand Forecast',
      desc: 'Random Forest model predicts expected sales with honest low/high confidence intervals.',
      icon: '📊',
    },
    {
      step: '03',
      title: 'Weather & Stock Advice',
      desc: 'Get exact prep quantities adjusted for live rain/heat and strictly capped by your budget.',
      icon: '🌤️',
    },
    {
      step: '04',
      title: 'Welfare & Credit (RAG)',
      desc: 'Ask in Hindi or English to discover PM SVANidhi, MUDRA, and Vishwakarma grants.',
      icon: '🏛️',
    },
  ]

  return (
    <div className="space-y-10">
      {/* Hero Section */}
      <section className="text-center py-10 px-4 bg-gradient-to-b from-orange-50/50 via-white to-transparent rounded-2xl border border-orange-100 shadow-2xs">
        <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-orange-100/80 border border-orange-200 text-orange-800 text-xs font-semibold mb-4">
          <span>🇮🇳</span>
          <span>Empowering India's 10M+ Street Vendors & Micro-Entrepreneurs</span>
        </div>
        <h1 className="text-4xl sm:text-5xl font-extrabold tracking-tight text-neutral-900">
          {t('homeHeroTitle')} <span className="text-orange-600">FLUX</span>
        </h1>
        <p className="mt-3 text-neutral-600 max-w-2xl mx-auto leading-relaxed text-sm sm:text-base">
          {t('homeHeroDesc')}
        </p>
        <div className="mt-6 flex flex-wrap justify-center gap-3">
          <Link
            to="/vendor"
            className="px-7 py-3 rounded-xl bg-orange-600 text-white font-semibold hover:bg-orange-700 transition shadow-sm hover:shadow flex items-center gap-2"
          >
            <span>{t('homeOpenDashboard')}</span>
          </Link>
        </div>
      </section>

      {/* Feature Grid */}
      <section className="grid sm:grid-cols-2 md:grid-cols-4 gap-4">
        {features.map((f) => (
          <Link
            to={f.link}
            key={f.title}
            className="rounded-xl border border-neutral-200 bg-white p-5 shadow-2xs hover:border-orange-300 hover:shadow-md transition flex flex-col justify-between"
          >
            <div>
              <div className="flex items-center justify-between mb-2">
                <span className="text-2xl">{f.icon}</span>
                <span
                  className={`text-[11px] font-semibold px-2 py-0.5 rounded-full border ${f.statusColor}`}
                >
                  {f.status}
                </span>
              </div>
              <h3 className="font-semibold text-neutral-800 text-base mb-1">{f.title}</h3>
              <p className="text-xs text-neutral-500 leading-relaxed">{f.desc}</p>
            </div>
            <span className="text-xs font-medium text-orange-600 mt-4 flex items-center gap-1">
              {t('homeExploreFeature')}
            </span>
          </Link>
        ))}
      </section>

      {/* How FLUX Works - End-to-End Workflow */}
      <section className="rounded-2xl border border-neutral-200 bg-white p-6 sm:p-8 shadow-2xs">
        <div className="text-center max-w-xl mx-auto mb-8">
          <h2 className="text-xl font-bold text-neutral-900">How FLUX Empowers Street Vendors</h2>
          <p className="text-xs sm:text-sm text-neutral-500 mt-1">
            From morning preparation to government credit access, in 4 simple steps
          </p>
        </div>

        <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-5">
          {workflowSteps.map((step) => (
            <div
              key={step.step}
              className="relative p-4 rounded-xl bg-neutral-50 border border-neutral-200/80 flex flex-col justify-between"
            >
              <div>
                <div className="flex items-center justify-between mb-3">
                  <span className="text-2xl">{step.icon}</span>
                  <span className="text-xs font-mono font-bold text-orange-600 bg-orange-100/80 px-2 py-0.5 rounded">
                    {step.step}
                  </span>
                </div>
                <h3 className="font-semibold text-neutral-800 text-sm mb-1">{step.title}</h3>
                <p className="text-xs text-neutral-500 leading-relaxed">{step.desc}</p>
              </div>
            </div>
          ))}
        </div>

        <div className="mt-8 text-center">
          <Link
            to="/vendor"
            className="inline-flex items-center gap-2 text-sm font-semibold text-orange-600 hover:text-orange-700 hover:underline"
          >
            <span>Launch Vendor Dashboard Demo</span>
            <span>→</span>
          </Link>
        </div>
      </section>
    </div>
  )
}
