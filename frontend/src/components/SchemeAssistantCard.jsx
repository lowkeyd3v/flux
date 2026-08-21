import { useState } from 'react'
import { querySchemes, getSchemeById } from '../services/schemeService'
import { useLanguage } from '../context/LanguageContext'
import SchemeDetailModal from './SchemeDetailModal'
import VoiceButton from './VoiceButton'
import SpeakerButton from './SpeakerButton'

const SAMPLE_QUERIES = {
  en: [
    'How do I get a ₹10,000 working capital loan under PM SVANidhi?',
    'What is the difference between Shishu and Kishore MUDRA loans?',
    'What benefits does PM Vishwakarma offer for artisans & craftsmen?',
    'What documents are needed for street vendors to apply for loans?',
    'How to get accident insurance cover through e-Shram portal?',
  ],
  hi: [
    'पीएम स्वनिधि के तहत ₹10,000 का वर्किंग कैपिटल लोन कैसे मिलेगा?',
    'मुद्रा योजना में शिशु और किशोर लोन में क्या अंतर है?',
    'पीएम विश्वकर्मा योजना में कारीगरों को क्या लाभ मिलते हैं?',
    'स्ट्रीट वेंडर्स को लोन के लिए कौन से दस्तावेज चाहिए?',
    'ई-श्रम पोर्टल से दुर्घटना बीमा का लाभ कैसे लें?',
  ],
  hinglish: [
    'PM SVANidhi me ₹10,000 ka working capital loan kaise milega?',
    'MUDRA Shishu aur Kishore loans me kya difference hai?',
    'PM Vishwakarma scheme me artisans ko kya benefits milte hain?',
    'Street vendors ko loan ke liye kaunse documents chahiye?',
    'e-Shram card se accident insurance kaise claim karein?',
  ],
}

export default function SchemeAssistantCard({ vendor = null }) {
  const { language, t } = useLanguage()
  const [query, setQuery] = useState('')
  const [result, setResult] = useState(null)
  const [status, setStatus] = useState('idle') // 'idle' | 'loading' | 'ok' | 'error'
  const [error, setError] = useState(null)
  const [showSources, setShowSources] = useState(false)
  const [activeSchemeDetail, setActiveSchemeDetail] = useState(null)
  const [loadingSchemeId, setLoadingSchemeId] = useState(null)

  const activeSampleQueries = SAMPLE_QUERIES[language] || SAMPLE_QUERIES.en

  const handleAsk = async (textToAsk = null) => {
    const q = typeof textToAsk === 'string' ? textToAsk : query
    if (!q.trim()) return

    setStatus('loading')
    setError(null)
    try {
      const data = await querySchemes({
        query: q,
        vendorId: vendor?.id || null,
        topK: 4,
      })
      setResult(data)
      setStatus('ok')
    } catch (err) {
      setError(
        err?.response?.data?.detail ||
          'Could not retrieve scheme information. Please try again.'
      )
      setStatus('error')
    }
  }

  const handleVoiceTranscript = (transcript) => {
    if (transcript) {
      setQuery(transcript)
      handleAsk(transcript)
    }
  }

  const handleOpenDetail = async (schemeId) => {
    setLoadingSchemeId(schemeId)
    try {
      const fullScheme = await getSchemeById(schemeId)
      setActiveSchemeDetail(fullScheme)
    } catch (err) {
      console.error('Failed to load scheme details', err)
    } finally {
      setLoadingSchemeId(null)
    }
  }

  return (
    <div className="space-y-4">
      {/* Sample Query Chips */}
      <div className="flex flex-wrap gap-2 items-center">
        <span className="text-xs font-semibold text-neutral-500 uppercase tracking-wider">
          {t('suggestedQuestions')}
        </span>
        {activeSampleQueries.map((sample, idx) => (
          <button
            key={idx}
            type="button"
            onClick={() => {
              setQuery(sample)
              handleAsk(sample)
            }}
            className="text-xs rounded-full bg-neutral-100 px-3 py-1 text-neutral-700 hover:bg-orange-100 hover:text-orange-800 transition text-left cursor-pointer"
          >
            {sample}
          </button>
        ))}
      </div>

      {/* Search Input Form with Voice Button */}
      <form
        onSubmit={(e) => {
          e.preventDefault()
          handleAsk()
        }}
        className="flex gap-2 items-center"
      >
        <div className="relative flex-1">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder={t('assistantInputPlaceholder')}
            className="input w-full pr-10"
          />
          {query && (
            <button
              type="button"
              onClick={() => setQuery('')}
              className="absolute right-3 top-1/2 -translate-y-1/2 text-neutral-400 hover:text-neutral-600 text-sm"
              title="Clear input"
            >
              ✕
            </button>
          )}
        </div>

        <VoiceButton onTranscript={handleVoiceTranscript} />

        <button
          type="submit"
          disabled={status === 'loading' || !query.trim()}
          className="px-5 py-2.5 rounded-lg bg-orange-600 text-white text-sm font-medium hover:bg-orange-700 disabled:opacity-50 transition shrink-0 flex items-center gap-2 cursor-pointer"
        >
          {status === 'loading' ? (
            <>
              <span className="animate-spin text-xs">⏳</span>
              <span>{t('btnAsking')}</span>
            </>
          ) : (
            <>
              <span>{t('btnAsk')}</span>
              <span>↗</span>
            </>
          )}
        </button>
      </form>

      {/* Error state */}
      {status === 'error' && (
        <p className="text-sm text-red-600 bg-red-50 border border-red-200 rounded-md px-3 py-2">
          {error}
        </p>
      )}

      {/* Answer Result Display */}
      {status === 'ok' && result && (
        <div className="rounded-xl border border-orange-200 bg-white p-5 shadow-sm space-y-4">
          <div className="flex items-center justify-between border-b border-neutral-100 pb-3 flex-wrap gap-2">
            <div className="flex items-center gap-2">
              <span className="inline-flex items-center justify-center w-6 h-6 rounded-full bg-orange-100 text-orange-700 text-xs font-bold">
                AI
              </span>
              <span className="text-xs font-semibold text-neutral-700">
                {t('schemeAssistantTitle')}
              </span>
            </div>
            <div className="flex items-center gap-2">
              <SpeakerButton text={result.answer} />
              <span className="text-xs text-neutral-400">
                {result.sources.length} sources
              </span>
            </div>
          </div>

          {/* Formatted Answer */}
          <div className="prose prose-sm text-neutral-800 whitespace-pre-line leading-relaxed text-sm bg-neutral-50/70 p-4 rounded-lg border border-neutral-200/70">
            {result.answer}
          </div>

          {/* Matched Scheme Badges */}
          {result.matched_schemes?.length > 0 && (
            <div className="pt-2 border-t border-neutral-100">
              <span className="block text-xs font-semibold text-neutral-500 uppercase tracking-wider mb-2">
                Referenced Official Schemes:
              </span>
              <div className="flex flex-wrap gap-2">
                {result.matched_schemes.map((s) => (
                  <button
                    key={s.id}
                    type="button"
                    onClick={() => handleOpenDetail(s.id)}
                    disabled={loadingSchemeId === s.id}
                    className="inline-flex items-center gap-1.5 rounded-lg border border-orange-200 bg-orange-50/80 px-3 py-1.5 text-xs font-medium text-orange-900 hover:bg-orange-100 transition cursor-pointer"
                  >
                    <span>🏛️</span>
                    <span>{s.name}</span>
                    <span className="text-orange-600 text-xs">ℹ️</span>
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Source Grounding & Transparency Accordion */}
          {result.sources?.length > 0 && (
            <div className="pt-2">
              <button
                type="button"
                onClick={() => setShowSources(!showSources)}
                className="text-xs font-medium text-neutral-600 hover:text-neutral-900 flex items-center gap-1.5 transition cursor-pointer"
              >
                <span>{showSources ? '▼ Hide' : '▶ View'} {t('sourceCitationsTitle', { count: result.sources.length })}</span>
              </button>

              {showSources && (
                <div className="mt-3 space-y-2 rounded-lg bg-neutral-50 p-3 border border-neutral-200">
                  {result.sources.map((src, idx) => (
                    <div key={idx} className="text-xs border-b border-neutral-200/60 pb-2 last:border-b-0 last:pb-0">
                      <div className="flex items-center justify-between font-medium text-neutral-700 mb-1">
                        <span>
                          [{idx + 1}] {src.source} — <span className="text-neutral-500">{src.section}</span>
                        </span>
                        <span className="text-orange-600 bg-orange-100/70 px-1.5 py-0.5 rounded text-[10px]">
                          Score: {Math.round(src.score * 100)}%
                        </span>
                      </div>
                      <p className="text-neutral-600 text-[11px] leading-relaxed line-clamp-3">
                        {src.content}
                      </p>
                      {src.official_url && (
                        <a
                          href={src.official_url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="inline-block mt-1 text-[11px] text-orange-600 hover:underline"
                        >
                          {t('officialPortal')} ({src.official_url}) ↗
                        </a>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* Follow-up question pills */}
          {result.suggested_followups?.length > 0 && (
            <div className="pt-3 border-t border-neutral-100">
              <span className="block text-xs font-semibold text-neutral-500 uppercase tracking-wider mb-1.5">
                {t('suggestedFollowUpsTitle')}
              </span>
              <div className="flex flex-wrap gap-1.5">
                {result.suggested_followups.map((item, idx) => (
                  <button
                    key={idx}
                    type="button"
                    onClick={() => {
                      setQuery(item)
                      handleAsk(item)
                    }}
                    className="text-xs rounded-md bg-neutral-100 px-2.5 py-1 text-neutral-700 hover:bg-orange-100 hover:text-orange-800 transition cursor-pointer"
                  >
                    💬 {item}
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Scheme Full Detail Modal */}
      {activeSchemeDetail && (
        <SchemeDetailModal
          scheme={activeSchemeDetail}
          onClose={() => setActiveSchemeDetail(null)}
        />
      )}
    </div>
  )
}
