import { useLanguage } from '../context/LanguageContext'

export default function VendorList({ vendors, selectedVendorId, onSelect }) {
  const { t } = useLanguage()

  if (vendors.length === 0) {
    return (
      <p className="text-sm text-neutral-500 italic">
        {t('noVendorsYet')}
      </p>
    )
  }

  return (
    <div className="grid sm:grid-cols-2 gap-3">
      {vendors.map((vendor) => {
        const isSelected = vendor.id === selectedVendorId
        return (
          <button
            key={vendor.id}
            type="button"
            onClick={() => onSelect(vendor.id)}
            className={`text-left rounded-xl border p-4 transition cursor-pointer ${
              isSelected
                ? 'border-orange-500 bg-orange-50 ring-1 ring-orange-300'
                : 'border-neutral-200 bg-white hover:border-neutral-300'
            }`}
          >
            <div className="flex items-center justify-between">
              <h3 className="font-semibold text-neutral-800">{vendor.name}</h3>
              {isSelected && (
                <span className="text-xs font-semibold text-orange-600 bg-orange-100/80 px-2 py-0.5 rounded-full border border-orange-200">
                  {t('btnSelected')}
                </span>
              )}
            </div>
            <p className="text-sm text-neutral-500 mt-0.5">
              {vendor.product} &middot; {vendor.location}
            </p>
            <div className="flex flex-wrap gap-x-4 gap-y-1 mt-2 text-xs text-neutral-600 font-medium">
              <span>{t('unitPrice', { price: vendor.selling_price })}</span>
              <span>{t('inStock', { qty: vendor.current_inventory })}</span>
              <span>{t('budgetAmount', { amount: vendor.budget })}</span>
            </div>
          </button>
        )
      })}
    </div>
  )
}
