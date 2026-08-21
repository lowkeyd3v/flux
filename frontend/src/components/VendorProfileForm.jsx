import { useState } from 'react'

const INITIAL_FORM = {
  name: '',
  product: '',
  location: '',
  selling_price: '',
  current_inventory: '',
  budget: '',
}

/**
 * Form for creating a new vendor business profile.
 * Calls onSubmit(payload) with numeric fields coerced from strings.
 */
export default function VendorProfileForm({ onSubmit, submitting }) {
  const [form, setForm] = useState(INITIAL_FORM)
  const [formError, setFormError] = useState(null)

  const handleChange = (field) => (e) => {
    setForm((prev) => ({ ...prev, [field]: e.target.value }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setFormError(null)

    if (!form.name || !form.product || !form.location || !form.selling_price) {
      setFormError('Please fill in all required fields.')
      return
    }

    const payload = {
      name: form.name.trim(),
      product: form.product.trim(),
      location: form.location.trim(),
      selling_price: parseFloat(form.selling_price),
      current_inventory: form.current_inventory ? parseFloat(form.current_inventory) : 0,
      budget: form.budget ? parseFloat(form.budget) : 0,
    }

    try {
      await onSubmit(payload)
      setForm(INITIAL_FORM)
    } catch (err) {
      setFormError(
        err?.response?.data?.detail
          ? JSON.stringify(err.response.data.detail)
          : 'Something went wrong creating the vendor profile.'
      )
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="grid sm:grid-cols-2 gap-4">
        <Field label="Vendor Name *">
          <input
            type="text"
            value={form.name}
            onChange={handleChange('name')}
            placeholder="e.g. Ramesh Kumar"
            className="input"
          />
        </Field>

        <Field label="Product *">
          <input
            type="text"
            value={form.product}
            onChange={handleChange('product')}
            placeholder="e.g. Samosa"
            className="input"
          />
        </Field>

        <Field label="Location *">
          <input
            type="text"
            value={form.location}
            onChange={handleChange('location')}
            placeholder="e.g. Prayagraj"
            className="input"
          />
        </Field>

        <Field label="Selling Price (₹) *">
          <input
            type="number"
            min="0"
            step="0.01"
            value={form.selling_price}
            onChange={handleChange('selling_price')}
            placeholder="e.g. 10"
            className="input"
          />
        </Field>

        <Field label="Current Inventory (units)">
          <input
            type="number"
            min="0"
            step="0.01"
            value={form.current_inventory}
            onChange={handleChange('current_inventory')}
            placeholder="e.g. 50"
            className="input"
          />
        </Field>

        <Field label="Budget (₹)">
          <input
            type="number"
            min="0"
            step="0.01"
            value={form.budget}
            onChange={handleChange('budget')}
            placeholder="e.g. 2000"
            className="input"
          />
        </Field>
      </div>

      {formError && (
        <p className="text-sm text-red-600 bg-red-50 border border-red-200 rounded-md px-3 py-2">
          {formError}
        </p>
      )}

      <button
        type="submit"
        disabled={submitting}
        className="w-full sm:w-auto px-5 py-2.5 rounded-lg bg-orange-600 text-white font-medium hover:bg-orange-700 disabled:opacity-50 disabled:cursor-not-allowed transition"
      >
        {submitting ? 'Creating...' : 'Create Vendor Profile'}
      </button>
    </form>
  )
}

function Field({ label, children }) {
  return (
    <label className="block">
      <span className="block text-sm font-medium text-neutral-700 mb-1">{label}</span>
      {children}
    </label>
  )
}
