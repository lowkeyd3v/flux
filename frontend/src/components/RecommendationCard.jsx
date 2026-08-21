import { useState } from 'react'
import { getRecommendation } from '../services/recommendationService'

const tomorrow = () => {
  const d = new Date()
  d.setDate(d.getDate() + 1)
  return d.toISOString().slice(0, 10)
}

const INITIAL_FORM = {
  target_date: tomorrow(),
  is_holiday_or_event: false,
  manual_weather: false,
  temperature_celsius: '',
  weather_condition: '',
}

const WEATHER_OPTIONS = ['', 'clear', 'rain', 'extreme_heat', 'cloudy']

const RISK_STYLES = {
  low: 'border-green-200 bg-green-50 text-green-700',
  medium: 'border-amber-200 bg-amber-50 text-amber-700',
  high: 'border-red-200 bg-red-50 text-red-700',
}

export default function RecommendationCard({ vendor }) {
  const [form, setForm] = useState(INITIAL_FORM)
  const [result, setResult] = useState(null)
  const [status, setStatus] = useState('idle') // 'idle' | 'loading' | 'ok' | 'error'
  const [error, setError] = useState(null)

  const handleChange = (field) => (e) => {
    const value = e.target.type === 'checkbox' ? e.target.checked : e.target.value
    setForm((prev) => ({ ...prev, [field]: value }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setStatus('loading')
    setError(null)
    try {
      const payload = {
        target_date: form.target_date,
        is_holiday_or_event: form.is_holiday_or_event,
        ...(form.manual_weather
          ? {
              temperature_celsius: form.temperature_celsius
                ? parseFloat(form.temperature_celsius)
                : null,
              weather_condition: form.weather_condition || null,
            }
          : {}),
      }
      const data = await getRecommendation(vendor.id, payload)
      setResult(data)
      setStatus('ok')
    } catch (err) {
      setError(
        err?.response?.status === 503
          ? 'The demand model has not been trained yet on the server.'
          : 'Could not get a recommendation. Please try again.'
      )
      setStatus('error')
    }
  }

  return (
    <div className="space-y-4">
      <form onSubmit={handleSubmit} className="space-y-3">
        <div className="grid sm:grid-cols-3 gap-3 items-end">
          <label className="block">
            <span className="block text-xs font-medium text-neutral-600 mb-1">Date</span>
            <input
              type="date"
              value={form.target_date}
              onChange={handleChange('target_date')}
              className="input"
            />
          </label>

          <label className="flex items-center gap-2 text-sm text-neutral-600 sm:pb-2">
            <input
              type="checkbox"
              checked={form.is_holiday_or_event}
              onChange={handleChange('is_holiday_or_event')}
              className="rounded border-neutral-300"
            />
            Holiday or local event
          </label>

          <button
            type="submit"
            disabled={status === 'loading'}
            className="px-4 py-2 rounded-lg bg-orange-600 text-white text-sm font-medium hover:bg-orange-700 disabled:opacity-50 transition"
          >
            {status === 'loading' ? 'Thinking...' : 'Get Recommendation'}
          </button>
        </div>

        <label className="flex items-center gap-2 text-sm text-neutral-600">
          <input
            type="checkbox"
            checked={form.manual_weather}
            onChange={handleChange('manual_weather')}
            className="rounded border-neutral-300"
          />
          Enter weather manually (otherwise we'll try to fetch it for {vendor.location})
        </label>

        {form.manual_weather && (
          <div className="grid sm:grid-cols-2 gap-3">
            <label className="block">
              <span className="block text-xs font-medium text-neutral-600 mb-1">
                Temperature (°C)
              </span>
              <input
                type="number"
                value={form.temperature_celsius}
                onChange={handleChange('temperature_celsius')}
                placeholder="e.g. 30"
                className="input"
              />
            </label>
            <label className="block">
              <span className="block text-xs font-medium text-neutral-600 mb-1">Weather</span>
              <select
                value={form.weather_condition}
                onChange={handleChange('weather_condition')}
                className="input"
              >
                {WEATHER_OPTIONS.map((opt) => (
                  <option key={opt} value={opt}>
                    {opt === '' ? 'Unknown' : opt}
                  </option>
                ))}
              </select>
            </label>
          </div>
        )}
      </form>

      {status === 'error' && (
        <p className="text-sm text-red-600 bg-red-50 border border-red-200 rounded-md px-3 py-2">
          {error}
        </p>
      )}

      {status === 'ok' && result && (
        <div className="rounded-xl border border-orange-200 bg-orange-50 p-5 space-y-3">
          <div className="flex items-baseline justify-between flex-wrap gap-2">
            <div className="flex items-baseline gap-2">
              <span className="text-3xl font-bold text-orange-700">
                {result.recommended_preparation_qty}
              </span>
              <span className="text-sm text-neutral-600">units to prepare</span>
            </div>
            <span
              className={`text-xs font-medium px-2 py-1 rounded-full border capitalize ${RISK_STYLES[result.risk_level] ?? ''}`}
            >
              {result.risk_level} risk
            </span>
          </div>

          <p className="text-sm text-neutral-700">{result.explanation}</p>

          <div className="grid sm:grid-cols-3 gap-3 text-sm text-neutral-600 pt-1">
            <div>
              <span className="block text-xs text-neutral-400">Expected revenue</span>
              ₹{result.expected_revenue}
            </div>
            <div>
              <span className="block text-xs text-neutral-400">Surplus / shortage</span>
              {result.estimated_surplus_or_shortage > 0 ? '+' : ''}
              {result.estimated_surplus_or_shortage} units
            </div>
            <div>
              <span className="block text-xs text-neutral-400">Weather used</span>
              {result.weather.condition ?? 'unknown'}
              {result.weather.temperature_celsius != null
                ? ` · ${result.weather.temperature_celsius}°C`
                : ''}
              {' '}
              <span className="text-xs text-neutral-400">({result.weather.source})</span>
            </div>
          </div>

          <p className="text-xs text-neutral-400">Model: {result.model_version}</p>
        </div>
      )}
    </div>
  )
}
