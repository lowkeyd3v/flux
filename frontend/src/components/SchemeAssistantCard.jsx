import { useState } from 'react'
import { querySchemes, getSchemeById } from '../services/schemeService'
import SchemeDetailModal from './SchemeDetailModal'

const SAMPLE_QUERIES = [
  'How do I get a ₹10,000 working capital loan under PM SVANidhi?',
  'What is the difference between Shishu and Kishore MUDRA loans?',
  'What benefits does PM Vishwakarma offer for artisans & craftsmen?',
  'What documents are needed for street vendors to apply for loans?',
  'How to get accident insurance cover through e-Shram portal?',
]

export default function SchemeAssistantCard({ vendor = null }) {
  const [query, setQuery] = useState('')
  const [result, setResult] = useState(null)
  const [status, setStatus] = useState('idle') // 'idle' | 'loading' | 'ok' | 'error'
  const [error, setError] = useState(null)
  const [showSources, setShowSources] = useState(false)
  const [activeSchemeDetail, setActiveSchemeDetail] = useState(null)
  const [loadingSchemeId, setLoadingSchemeId] = useState(null)

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
          Suggested:
        </span>
        {SAMPLE_QUERIES.map((sample, idx) => (
          <button
            key={idx}
            type="button"
            onClick={() => {
              setQuery(sample)
              handleAsk(sample)
            }}
            className="text-xs rounded-full bg-neutral-100 px-3 py-1 text-neutral-700 hover:bg-orange-100 hover:text-orange-800 transition text-left"
          >
            {sample}
          </button>
        ))}
      </div>

      {/* Search Input Form */}
      <form
        onSubmit={(e) => {
          e.preventDefault()
          handleAsk()
        }}
        className="flex gap-2"
      >
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ask anything about loans, subsidies, eligibility, or government schemes..."
          className="input flex-1"
        />
        <button
          type="submit"
          disabled={status === 'loading' || !query.trim()}
          className="px-5 py-2 rounded-lg bg-orange-600 text-white text-sm font-medium hover:bg-orange-700 disabled:opacity-50 transition shrink-0 flex items-center gap-2"
        >
          {status === 'loading' ? (
            <>
              <span className="animate-spin text-xs">⏳</span>
              <span>Searching...</span>
            </>
          ) : (
            <>
              <span>Ask FLUX</span>
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
          <div className="flex items-center justify-between border-b border-neutral-100 pb-3">
            <div className="flex items-center gap-2">
              <span className="inline-flex items-center justify-center w-6 h-6 rounded-full bg-orange-100 text-orange-700 text-xs font-bold">
                AI
              </span>
              <span className="text-xs font-medium text-neutral-500">
                Grounded Scheme Assistant
              </span>
            </div>
            <span className="text-xs text-neutral-400">
              {result.sources.length} document chunk{result.sources.length === 1 ? '' : 's'} referenced
            </span>
          </div>

          {/* Formatted Answer */}
          <div className="prose prose-sm text-neutral-800 whitespace-pre-line leading-relaxed text-sm">
            {result.answer}
          </div>

          {/* Matched Scheme Badges */}
          {result.matched_schemes?.length > 0 && (
            <div className="pt-3 border-t border-neutral-100">
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
                    className="inline-flex items-center gap-1.5 rounded-lg border border-orange-200 bg-orange-50/70 px-3 py-1.5 text-xs font-medium text-orange-900 hover:bg-orange-100 transition"
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
                className="text-xs font-medium text-neutral-500 hover:text-neutral-800 flex items-center gap-1.5 transition"
              >
                <span>{showSources ? '▼ Hide' : '▶ View'} Source Document Citations & Match Scores</span>
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
                          Official Portal ({src.official_url}) ↗
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
                Suggested Follow-up Questions:
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
                    className="text-xs rounded-md bg-neutral-100 px-2.5 py-1 text-neutral-600 hover:bg-orange-100 hover:text-orange-800 transition"
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
