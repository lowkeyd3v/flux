import React from 'react'

export default function SchemeDetailModal({ scheme, onClose }) {
  if (!scheme) return null

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4 overflow-y-auto">
      <div className="relative w-full max-w-2xl rounded-2xl bg-white p-6 shadow-xl max-h-[90vh] overflow-y-auto space-y-5">
        <div className="flex items-start justify-between gap-4 border-b border-neutral-100 pb-4">
          <div>
            <span className="inline-block rounded-full bg-orange-100 px-2.5 py-0.5 text-xs font-semibold text-orange-800 mb-1">
              {scheme.category}
            </span>
            <h2 className="text-xl font-bold text-neutral-900">{scheme.name}</h2>
            <p className="text-xs text-neutral-500">{scheme.ministry}</p>
          </div>
          <button
            onClick={onClose}
            className="rounded-lg p-1.5 text-neutral-400 hover:bg-neutral-100 hover:text-neutral-700 transition"
            aria-label="Close"
          >
            ✕
          </button>
        </div>

        <div className="space-y-4 text-sm text-neutral-700">
          <div>
            <h3 className="font-semibold text-neutral-900 mb-1">Overview</h3>
            <p className="text-neutral-600 leading-relaxed">{scheme.short_description}</p>
          </div>

          <div className="grid sm:grid-cols-2 gap-3 bg-orange-50/60 p-3.5 rounded-xl border border-orange-100">
            <div>
              <span className="block text-xs font-medium text-orange-900/70">Maximum Benefit</span>
              <span className="font-semibold text-orange-950">{scheme.max_benefit}</span>
            </div>
            <div>
              <span className="block text-xs font-medium text-orange-900/70">Interest Subsidy / Guarantee</span>
              <span className="font-semibold text-orange-950">{scheme.subsidy_info}</span>
            </div>
          </div>

          {scheme.eligibility && (
            <div>
              <h3 className="font-semibold text-neutral-900 mb-1.5 flex items-center gap-1.5">
                <span>✓</span> Eligibility Criteria
              </h3>
              <ul className="list-disc pl-5 space-y-1 text-neutral-600 text-xs sm:text-sm">
                {scheme.eligibility.map((item, idx) => (
                  <li key={idx}>{item}</li>
                ))}
              </ul>
            </div>
          )}

          {scheme.benefits && (
            <div>
              <h3 className="font-semibold text-neutral-900 mb-1.5 flex items-center gap-1.5">
                <span>🎁</span> Scheme Benefits
              </h3>
              <ul className="list-disc pl-5 space-y-1 text-neutral-600 text-xs sm:text-sm">
                {scheme.benefits.map((item, idx) => (
                  <li key={idx}>{item}</li>
                ))}
              </ul>
            </div>
          )}

          {scheme.documents_required && (
            <div>
              <h3 className="font-semibold text-neutral-900 mb-1.5 flex items-center gap-1.5">
                <span>📄</span> Documents Required
              </h3>
              <ul className="list-disc pl-5 space-y-1 text-neutral-600 text-xs sm:text-sm">
                {scheme.documents_required.map((item, idx) => (
                  <li key={idx}>{item}</li>
                ))}
              </ul>
            </div>
          )}

          {scheme.application_steps && (
            <div>
              <h3 className="font-semibold text-neutral-900 mb-1.5 flex items-center gap-1.5">
                <span>🚀</span> How to Apply
              </h3>
              <div className="space-y-1.5">
                {scheme.application_steps.map((step, idx) => (
                  <p key={idx} className="text-xs sm:text-sm text-neutral-600 bg-neutral-50 p-2 rounded-lg border border-neutral-100">
                    {step}
                  </p>
                ))}
              </div>
            </div>
          )}
        </div>

        <div className="flex items-center justify-between pt-4 border-t border-neutral-100">
          <button
            onClick={onClose}
            className="px-4 py-2 text-sm font-medium text-neutral-600 hover:bg-neutral-100 rounded-lg transition"
          >
            Close
          </button>
          {scheme.official_url && (
            <a
              href={scheme.official_url}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-1.5 px-4 py-2 rounded-lg bg-orange-600 text-white text-sm font-medium hover:bg-orange-700 transition"
            >
              Visit Official Portal ↗
            </a>
          )}
        </div>
      </div>
    </div>
  )
}
