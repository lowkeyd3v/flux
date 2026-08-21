export default function SalesRecordTable({ records }) {
  if (records.length === 0) {
    return (
      <p className="text-sm text-neutral-500 italic">
        No sales records yet for this vendor.
      </p>
    )
  }

  return (
    <div className="overflow-x-auto rounded-lg border border-neutral-200">
      <table className="w-full text-sm">
        <thead className="bg-neutral-50 text-neutral-500 text-left">
          <tr>
            <th className="px-3 py-2 font-medium">Date</th>
            <th className="px-3 py-2 font-medium">Units Sold</th>
            <th className="px-3 py-2 font-medium">Price</th>
            <th className="px-3 py-2 font-medium">Weather</th>
            <th className="px-3 py-2 font-medium">Holiday/Event</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-neutral-100">
          {records.map((r) => (
            <tr key={r.id}>
              <td className="px-3 py-2 text-neutral-700">{r.sale_date}</td>
              <td className="px-3 py-2 text-neutral-700">{r.units_sold}</td>
              <td className="px-3 py-2 text-neutral-700">₹{r.price}</td>
              <td className="px-3 py-2 text-neutral-500">
                {r.weather_condition || '—'}
              </td>
              <td className="px-3 py-2 text-neutral-500">
                {r.is_holiday_or_event ? 'Yes' : 'No'}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
