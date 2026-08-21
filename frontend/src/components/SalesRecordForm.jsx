import { useState } from 'react'
import { useLanguage } from '../context/LanguageContext'

const today = () => new Date().toISOString().slice(0, 10)

const INITIAL_FORM = {
  sale_date: today(),
  units_sold: '',
  price: '',
  is_holiday_or_event: false,
  weather_condition: '',
}

export default function SalesRecordForm({ onSubmit, submitting }) {
  const { t } = useLanguage()
  const [form, setForm] = useState(INITIAL_FORM)
  const [formError, setFormError] = useState(null)

  const weatherOptions = [
    { value: '', label: 'Not recorded' },
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
    setFormError(null)

    if (!form.sale_date || !form.units_sold || !form.price) {
      setFormError('Please fill in date, units sold, and price.')
      return
    }

    const payload = {
      sale_date: form.sale_date,
      units_sold: parseFloat(form.units_sold),
      price: parseFloat(form.price),
      is_holiday_or_event: form.is_holiday_or_event,
      weather_condition: form.weather_condition || null,
    }

    try {
      await onSubmit(payload)
      setForm({ ...INITIAL_FORM, sale_date: today() })
    } catch (err) {
      setFormError(
        err?.response?.data?.detail
          ? JSON.stringify(err.response.data.detail)
          : 'Could not save this sales record.'
      )
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-3">
      <div className="grid sm:grid-cols-4 gap-3">
        <label className="block">
          <span className="block text-xs font-medium text-neutral-600 mb-1">{t('dateLabel')}</span>
          <input
            type="date"
            value={form.sale_date}
            onChange={handleChange('sale_date')}
            className="input"
          />
        </label>

        <label className="block">
          <span className="block text-xs font-medium text-neutral-600 mb-1">{t('unitsSoldLabel')}</span>
          <input
            type="number"
            min="0"
            step="0.01"
            value={form.units_sold}
            onChange={handleChange('units_sold')}
            placeholder="e.g. 45"
            className="input"
          />
        </label>

        <label className="block">
          <span className="block text-xs font-medium text-neutral-600 mb-1">{t('sellingPriceLabel')}</span>
          <input
            type="number"
            min="0"
            step="0.01"
            value={form.price}
            onChange={handleChange('price')}
            placeholder="e.g. 10"
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

      <label className="flex items-center gap-2 text-sm text-neutral-600">
        <input
          type="checkbox"
          checked={form.is_holiday_or_event}
          onChange={handleChange('is_holiday_or_event')}
          className="rounded border-neutral-300"
        />
        {t('holidayEventLabel')}
      </label>

      {formError && (
        <p className="text-sm text-red-600 bg-red-50 border border-red-200 rounded-md px-3 py-2">
          {formError}
        </p>
      )}

      <button
        type="submit"
        disabled={submitting}
        className="px-4 py-2 rounded-lg bg-neutral-800 text-white text-sm font-medium hover:bg-neutral-900 disabled:opacity-50 disabled:cursor-not-allowed transition cursor-pointer"
      >
        {submitting ? 'Saving...' : t('btnAddRecord')}
      </button>
    </form>
  )
}
