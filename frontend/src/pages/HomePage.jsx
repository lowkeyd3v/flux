import { Link } from 'react-router-dom'
import { useLanguage } from '../context/LanguageContext'
import HealthStatusCard from '../components/HealthStatusCard'

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

  return (
    <div className="space-y-8">
      <section className="text-center py-10">
        <h1 className="text-4xl font-extrabold tracking-tight text-neutral-900">
          {t('homeHeroTitle')} <span className="text-orange-600">FLUX</span>
        </h1>
        <p className="mt-3 text-neutral-600 max-w-xl mx-auto leading-relaxed">
          {t('homeHeroDesc')}
        </p>
        <div className="mt-6 flex justify-center gap-3">
          <Link
            to="/vendor"
            className="px-6 py-2.5 rounded-lg bg-orange-600 text-white font-medium hover:bg-orange-700 transition shadow-sm"
          >
            {t('homeOpenDashboard')}
          </Link>
        </div>
      </section>

      <HealthStatusCard />

      <section className="grid sm:grid-cols-2 md:grid-cols-4 gap-4">
        {features.map((f) => (
          <Link
            to={f.link}
            key={f.title}
            className="rounded-xl border border-neutral-200 bg-white p-5 shadow-2xs hover:border-orange-300 hover:shadow-md transition flex flex-col justify-between"
          >
            <div>
              <div className="flex items-center justify-between mb-2">
                <span className="text-xl">{f.icon}</span>
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
    </div>
  )
}
