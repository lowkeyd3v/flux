import { useState } from 'react'
import { getRecommendation } from '../services/recommendationService'
import { useLanguage } from '../context/LanguageContext'
import SpeakerButton from './SpeakerButton'

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

const RISK_STYLES = {
  low: 'border-green-200 bg-green-50 text-green-700 font-semibold',
  medium: 'border-amber-200 bg-amber-50 text-amber-700 font-semibold',
  high: 'border-red-200 bg-red-50 text-red-700 font-semibold',
}

export default function RecommendationCard({ vendor }) {
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

  const speechText = result
    ? `${result.explanation} Expected revenue is ${result.expected_revenue} rupees.`
    : ''

  const getRiskLabel = (level) => {
    if (level === 'low') return t('riskLow')
    if (level === 'medium') return t('riskMedium')
    if (level === 'high') return t('riskHigh')
    return `${level} risk`
  }

  return (
    <div className="space-y-4">
      <form onSubmit={handleSubmit} className="space-y-3">
        <div className="grid sm:grid-cols-3 gap-3 items-end">
          <label className="block">
            <span className="block text-xs font-medium text-neutral-600 mb-1">{t('targetDateLabel')}</span>
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
            {t('holidayEventLabel')}
          </label>

          <button
            type="submit"
            disabled={status === 'loading'}
            className="px-4 py-2 rounded-lg bg-orange-600 text-white text-sm font-medium hover:bg-orange-700 disabled:opacity-50 transition cursor-pointer"
          >
            {status === 'loading' ? t('btnGettingRecommendation') : t('btnGetRecommendation')}
          </button>
        </div>

        <label className="flex items-center gap-2 text-sm text-neutral-600">
          <input
            type="checkbox"
            checked={form.manual_weather}
            onChange={handleChange('manual_weather')}
            className="rounded border-neutral-300"
          />
          {t('manualWeatherCheckbox')}
        </label>

        {form.manual_weather && (
          <div className="grid sm:grid-cols-2 gap-3">
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
          </div>
        )}
      </form>

      {status === 'error' && (
        <p className="text-sm text-red-600 bg-red-50 border border-red-200 rounded-md px-3 py-2">
          {error}
        </p>
      )}

      {status === 'ok' && result && (
        <div className="rounded-xl border border-orange-200 bg-orange-50/80 p-5 space-y-3">
          <div className="flex items-center justify-between flex-wrap gap-2">
            <div className="flex items-baseline gap-2">
              <span className="text-3xl font-bold text-orange-700">
                {result.recommended_preparation_qty}
              </span>
              <span className="text-sm font-semibold text-neutral-800">
                {t('prepUnits', { qty: '' })}
              </span>
            </div>
            <div className="flex items-center gap-2">
              <SpeakerButton text={speechText} />
              <span
                className={`text-xs px-2.5 py-1 rounded-full border ${RISK_STYLES[result.risk_level] ?? ''}`}
              >
                {getRiskLabel(result.risk_level)}
              </span>
            </div>
          </div>

          <p className="text-sm text-neutral-800 leading-relaxed font-medium bg-white/70 p-3 rounded-lg border border-orange-100">
            {result.explanation}
          </p>

          <div className="grid sm:grid-cols-3 gap-3 text-sm text-neutral-700 pt-1">
            <div className="bg-white/60 p-2.5 rounded-md border border-orange-100">
              <span className="block text-xs text-neutral-500 font-medium">{t('expectedRevenueTitle')}</span>
              <span className="font-semibold text-neutral-900">₹{result.expected_revenue}</span>
            </div>
            <div className="bg-white/60 p-2.5 rounded-md border border-orange-100">
              <span className="block text-xs text-neutral-500 font-medium">{t('estSurplusShortageTitle')}</span>
              <span className="font-semibold text-neutral-900">
                {result.estimated_surplus_or_shortage > 0 ? '+' : ''}
                {result.estimated_surplus_or_shortage} units
              </span>
            </div>
            <div className="bg-white/60 p-2.5 rounded-md border border-orange-100">
              <span className="block text-xs text-neutral-500 font-medium">Weather Context</span>
              <span className="text-xs text-neutral-800">
                {result.weather.condition ?? 'Default'}
                {result.weather.temperature_celsius != null
                  ? ` · ${result.weather.temperature_celsius}°C`
                  : ''}
                {' '}
                <span className="text-neutral-500 font-mono text-[11px]">({result.weather.source})</span>
              </span>
            </div>
          </div>

          <p className="text-xs text-neutral-400">{t('modelVersion', { version: result.model_version })}</p>
        </div>
      )}
    </div>
  )
}
