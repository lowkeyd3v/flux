export default function VendorList({ vendors, selectedVendorId, onSelect }) {
  if (vendors.length === 0) {
    return (
      <p className="text-sm text-neutral-500 italic">
        No vendor profiles yet. Create one above to get started.
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
            onClick={() => onSelect(vendor.id)}
            className={`text-left rounded-xl border p-4 transition ${
              isSelected
                ? 'border-orange-500 bg-orange-50 ring-1 ring-orange-300'
                : 'border-neutral-200 bg-white hover:border-neutral-300'
            }`}
          >
            <div className="flex items-center justify-between">
              <h3 className="font-semibold text-neutral-800">{vendor.name}</h3>
              {isSelected && (
                <span className="text-xs font-medium text-orange-600">Selected</span>
              )}
            </div>
            <p className="text-sm text-neutral-500 mt-0.5">
              {vendor.product} &middot; {vendor.location}
            </p>
            <div className="flex gap-4 mt-2 text-xs text-neutral-500">
              <span>₹{vendor.selling_price}/unit</span>
              <span>{vendor.current_inventory} in stock</span>
              <span>₹{vendor.budget} budget</span>
            </div>
          </button>
        )
      })}
    </div>
  )
}
