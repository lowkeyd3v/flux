import { useState } from 'react'
import { useVendors } from '../hooks/useVendors'
import { useSalesRecords } from '../hooks/useSalesRecords'
import VendorProfileForm from '../components/VendorProfileForm'
import VendorList from '../components/VendorList'
import SalesRecordForm from '../components/SalesRecordForm'
import SalesRecordTable from '../components/SalesRecordTable'
import DemandPredictionCard from '../components/DemandPredictionCard'
import RecommendationCard from '../components/RecommendationCard'

export default function VendorPage() {
  const { vendors, status: vendorsStatus, createVendor } = useVendors()
  const [selectedVendorId, setSelectedVendorId] = useState(null)
  const [creatingVendor, setCreatingVendor] = useState(false)
  const [creatingRecord, setCreatingRecord] = useState(false)

  const {
    records,
    status: recordsStatus,
    createRecord,
  } = useSalesRecords(selectedVendorId)

  const selectedVendor = vendors.find((v) => v.id === selectedVendorId) || null

  const handleCreateVendor = async (payload) => {
    setCreatingVendor(true)
    try {
      const created = await createVendor(payload)
      setSelectedVendorId(created.id)
    } finally {
      setCreatingVendor(false)
    }
  }

  const handleCreateRecord = async (payload) => {
    setCreatingRecord(true)
    try {
      await createRecord(payload)
    } finally {
      setCreatingRecord(false)
    }
  }

  return (
    <div className="space-y-8">
      <section>
        <h1 className="text-2xl font-bold text-neutral-900">Vendor Profile</h1>
        <p className="text-sm text-neutral-500 mt-1">
          Create a business profile to start tracking sales and getting AI-powered
          recommendations.
        </p>
      </section>

      <section className="rounded-xl border border-neutral-200 bg-white p-5 shadow-sm">
        <h2 className="font-semibold text-neutral-800 mb-4">New Vendor Profile</h2>
        <VendorProfileForm onSubmit={handleCreateVendor} submitting={creatingVendor} />
      </section>

      <section>
        <h2 className="font-semibold text-neutral-800 mb-3">Your Vendors</h2>
        {vendorsStatus === 'loading' && (
          <p className="text-sm text-neutral-500">Loading vendors...</p>
        )}
        {vendorsStatus === 'error' && (
          <p className="text-sm text-red-600">Could not load vendors. Is the backend running?</p>
        )}
        {vendorsStatus === 'ok' && (
          <VendorList
            vendors={vendors}
            selectedVendorId={selectedVendorId}
            onSelect={setSelectedVendorId}
          />
        )}
      </section>

      {selectedVendor && (
        <section className="rounded-xl border border-neutral-200 bg-white p-5 shadow-sm space-y-4">
          <div>
            <h2 className="font-semibold text-neutral-800">
              Demand Prediction — {selectedVendor.name}
            </h2>
            <p className="text-sm text-neutral-500">
              Get an ML-driven forecast for a specific day, adjusted for weather and
              holidays.
            </p>
          </div>
          <DemandPredictionCard vendor={selectedVendor} />
        </section>
      )}

      {selectedVendor && (
        <section className="rounded-xl border border-neutral-200 bg-white p-5 shadow-sm space-y-4">
          <div>
            <h2 className="font-semibold text-neutral-800">
              Recommendation — {selectedVendor.name}
            </h2>
            <p className="text-sm text-neutral-500">
              How much to prepare, expected revenue, and risk — combining the demand
              forecast with your inventory, budget, and local weather.
            </p>
          </div>
          <RecommendationCard vendor={selectedVendor} />
        </section>
      )}

      {selectedVendor && (
        <section className="rounded-xl border border-neutral-200 bg-white p-5 shadow-sm space-y-5">
          <div>
            <h2 className="font-semibold text-neutral-800">
              Sales History — {selectedVendor.name}
            </h2>
            <p className="text-sm text-neutral-500">
              Log historical daily sales. This data will power demand forecasting.
            </p>
          </div>

          <SalesRecordForm onSubmit={handleCreateRecord} submitting={creatingRecord} />

          {recordsStatus === 'loading' && (
            <p className="text-sm text-neutral-500">Loading sales records...</p>
          )}
          {recordsStatus === 'error' && (
            <p className="text-sm text-red-600">Could not load sales records.</p>
          )}
          {recordsStatus === 'ok' && <SalesRecordTable records={records} />}
        </section>
      )}
    </div>
  )
}
