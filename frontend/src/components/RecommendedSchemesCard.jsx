import { useState, useEffect } from 'react'
import { getRecommendedSchemes, getSchemeById } from '../services/schemeService'
import { useLanguage } from '../context/LanguageContext'
import SchemeDetailModal from './SchemeDetailModal'

export default function RecommendedSchemesCard({ vendor }) {
  const { t } = useLanguage()
  const [recommendations, setRecommendations] = useState([])
  const [status, setStatus] = useState('idle') // 'idle' | 'loading' | 'ok' | 'error'
  const [error, setError] = useState(null)
  const [selectedScheme, setSelectedScheme] = useState(null)

  useEffect(() => {
    if (!vendor?.id) return

    let isMounted = true
    const fetchRecommendations = async () => {
      setStatus('loading')
      setError(null)
      try {
        const data = await getRecommendedSchemes(vendor.id)
        if (isMounted) {
          setRecommendations(data.recommendations || [])
          setStatus('ok')
        }
      } catch (err) {
        if (isMounted) {
          setError('Could not load personalized scheme recommendations.')
          setStatus('error')
        }
      }
    }

    fetchRecommendations()
    return () => {
      isMounted = false
    }
  }, [vendor?.id])

  const handleOpenDetail = async (schemeId) => {
    try {
      const full = await getSchemeById(schemeId)
      setSelectedScheme(full)
    } catch (err) {
      console.error('Failed to load scheme details', err)
    }
  }

  return (
    <div className="space-y-4">
      {status === 'loading' && (
        <p className="text-sm text-neutral-500">Matching government schemes for {vendor.name}...</p>
      )}

      {status === 'error' && (
        <p className="text-sm text-red-600 bg-red-50 border border-red-200 rounded-md px-3 py-2">
          {error}
        </p>
      )}

      {status === 'ok' && recommendations.length === 0 && (
        <p className="text-sm text-neutral-500">No specific scheme matches found.</p>
      )}

      {status === 'ok' && recommendations.length > 0 && (
        <div className="grid sm:grid-cols-2 gap-4">
          {recommendations.map((rec, idx) => {
            const scheme = rec.scheme
            return (
              <div
                key={idx}
                className="flex flex-col justify-between rounded-xl border border-neutral-200 bg-white p-4 shadow-sm hover:border-orange-200 transition"
              >
                <div className="space-y-2.5">
                  <div className="flex items-start justify-between gap-2">
                    <span className="inline-block rounded-full bg-orange-100 px-2 py-0.5 text-[11px] font-semibold text-orange-800">
                      {scheme.category}
                    </span>
                    <span className="text-xs font-semibold text-neutral-900 bg-neutral-100 px-2 py-0.5 rounded">
                      {scheme.max_benefit.split('(')[0].trim()}
                    </span>
                  </div>

                  <h3 className="font-semibold text-neutral-900 text-sm">{scheme.name}</h3>

                  <div className="bg-amber-50/70 p-2.5 rounded-lg border border-amber-100 text-xs text-amber-900">
                    <span className="font-semibold">{t('matchReasonLabel')}</span> {rec.match_reason}
                  </div>

                  <p className="text-xs text-neutral-600 leading-relaxed">
                    {scheme.short_description}
                  </p>
                </div>

                <div className="pt-4 mt-3 border-t border-neutral-100 flex items-center justify-between gap-2">
                  <button
                    type="button"
                    onClick={() => handleOpenDetail(scheme.id)}
                    className="text-xs font-medium text-neutral-700 hover:text-orange-600 transition cursor-pointer"
                  >
                    {t('btnViewSchemeDetails')}
                  </button>

                  {scheme.official_url && (
                    <a
                      href={scheme.official_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center gap-1 px-3 py-1.5 rounded-lg bg-orange-600 text-white text-xs font-medium hover:bg-orange-700 transition shrink-0"
                    >
                      Apply ↗
                    </a>
                  )}
                </div>
              </div>
            )
          })}
        </div>
      )}

      {selectedScheme && (
        <SchemeDetailModal
          scheme={selectedScheme}
          onClose={() => setSelectedScheme(null)}
        />
      )}
    </div>
  )
}
