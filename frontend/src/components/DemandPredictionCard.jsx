import { useState } from 'react'
import { predictDemand } from '../services/predictionService'
import { useLanguage } from '../context/LanguageContext'

const tomorrow = () => {
  const d = new Date()
  d.setDate(d.getDate() + 1)
  return d.toISOString().slice(0, 10)
}

const INITIAL_FORM = {
  target_date: tomorrow(),
  temperature_celsius: '',
  weather_condition: '',
  is_holiday_or_event: false,
}

export default function DemandPredictionCard({ vendor }) {
  const { t } = useLanguage()
  const [form, setForm] = useState(INITIAL_FORM)
  const [result, setResult] = useState(null)
  const [status, setStatus] = useState('idle') // 'idle' | 'loading' | 'ok' | 'error'
  const [error, setError] = useState(null)

  const weatherOptions = [
    { value: '', label: 'Default' },
    { value: 'clear', label: t('weatherClear') },
    { value: 'cloudy', label: t('weatherCloudy') },
    { value: 'rain', label: t('weatherRain') },
    { value: 'extreme_heat', label: t('weatherExtremeHeat') },
  ]

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
        temperature_celsius: form.temperature_celsius
          ? parseFloat(form.temperature_celsius)
          : null,
        weather_condition: form.weather_condition || null,
        is_holiday_or_event: form.is_holiday_or_event,
      }
      const data = await predictDemand(vendor.id, payload)
      setResult(data)
      setStatus('ok')
    } catch (err) {
      setError(
        err?.response?.status === 503
          ? 'The demand model has not been trained yet on the server.'
          : 'Could not get a prediction. Please try again.'
      )
      setStatus('error')
    }
  }

  const expectedRevenue = result
    ? (result.predicted_demand_point * vendor.selling_price).toFixed(0)
    : null

  return (
    <div className="space-y-4">
      <form onSubmit={handleSubmit} className="grid sm:grid-cols-4 gap-3 items-end">
        <label className="block">
          <span className="block text-xs font-medium text-neutral-600 mb-1">{t('targetDateLabel')}</span>
          <input
            type="date"
            value={form.target_date}
            onChange={handleChange('target_date')}
            className="input"
          />
        </label>

        <label className="block">
          <span className="block text-xs font-medium text-neutral-600 mb-1">
            {t('tempCelsiusLabel')}
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
          <span className="block text-xs font-medium text-neutral-600 mb-1">{t('weatherConditionLabel')}</span>
          <select
            value={form.weather_condition}
            onChange={handleChange('weather_condition')}
            className="input"
          >
            {weatherOptions.map((opt) => (
              <option key={opt.value} value={opt.value}>
                {opt.label}
              </option>
            ))}
          </select>
        </label>

        <button
          type="submit"
          disabled={status === 'loading'}
          className="px-4 py-2 rounded-lg bg-orange-600 text-white text-sm font-medium hover:bg-orange-700 disabled:opacity-50 transition cursor-pointer"
        >
          {status === 'loading' ? t('btnPredicting') : t('btnPredict')}
        </button>
      </form>

      <label className="flex items-center gap-2 text-sm text-neutral-600">
        <input
          type="checkbox"
          checked={form.is_holiday_or_event}
          onChange={handleChange('is_holiday_or_event')}
          className="rounded border-neutral-300"
        />
        {t('holidayEventLabel')}
      </label>

      {status === 'error' && (
        <p className="text-sm text-red-600 bg-red-50 border border-red-200 rounded-md px-3 py-2">
          {error}
        </p>
      )}

      {status === 'ok' && result && (
        <div className="rounded-xl border border-orange-200 bg-orange-50 p-5 space-y-3">
          <div className="flex items-baseline gap-2">
            <span className="text-3xl font-bold text-orange-700">
              {result.predicted_demand_point}
            </span>
            <span className="text-sm font-medium text-neutral-700">
              {t('expectedUnits', { qty: '' })}
            </span>
          </div>
          <p className="text-sm text-neutral-700">
            {t('predictionRange', {
              low: result.predicted_demand_low,
              high: result.predicted_demand_high,
            })}{' '}
            &middot;{' '}
            <span className="font-medium text-orange-800">
              {t('confidenceScore', { score: (result.confidence * 100).toFixed(0) })}
            </span>
          </p>
          <p className="text-sm text-neutral-700">
            {t('expectedRevenueTitle')}: <strong>₹{expectedRevenue}</strong> (@ ₹{vendor.selling_price}/unit)
          </p>
          <p className="text-xs text-neutral-400">{t('modelVersion', { version: result.model_version })}</p>
        </div>
      )}
    </div>
  )
}
