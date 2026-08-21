import { useState } from 'react'
import { useVendors } from '../hooks/useVendors'
import { useSalesRecords } from '../hooks/useSalesRecords'
import { useLanguage } from '../context/LanguageContext'
import VendorProfileForm from '../components/VendorProfileForm'
import VendorList from '../components/VendorList'
import SalesRecordForm from '../components/SalesRecordForm'
import SalesRecordTable from '../components/SalesRecordTable'
import DemandPredictionCard from '../components/DemandPredictionCard'
import RecommendedSchemesCard from '../components/RecommendedSchemesCard'
import SchemeAssistantCard from '../components/SchemeAssistantCard'
import RecommendationCard from '../components/RecommendationCard'

export default function VendorPage() {
  const { t } = useLanguage()
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
        <h1 className="text-2xl font-bold text-neutral-900">{t('vendorPageTitle')}</h1>
        <p className="text-sm text-neutral-500 mt-1">
          {t('vendorPageSub')}
        </p>
      </section>

      <section className="rounded-xl border border-neutral-200 bg-white p-5 shadow-sm">
        <h2 className="font-semibold text-neutral-800 mb-4">{t('newVendorProfile')}</h2>
        <VendorProfileForm onSubmit={handleCreateVendor} submitting={creatingVendor} />
      </section>

      <section>
        <h2 className="font-semibold text-neutral-800 mb-3">{t('yourVendors')}</h2>
        {vendorsStatus === 'loading' && (
          <p className="text-sm text-neutral-500">{t('loadingVendors')}</p>
        )}
        {vendorsStatus === 'error' && (
          <p className="text-sm text-red-600">{t('errorLoadingVendors')}</p>
        )}
        {vendorsStatus === 'ok' && (
          <VendorList
            vendors={vendors}
            selectedVendorId={selectedVendorId}
            onSelect={setSelectedVendorId}
          />
        )}
      </section>

      {/* Recommended Schemes for Selected Vendor */}
      {selectedVendor && (
        <section className="rounded-xl border border-neutral-200 bg-white p-5 shadow-sm space-y-4">
          <div>
            <div className="flex items-center gap-2">
              <span className="text-lg">🏛️</span>
              <h2 className="font-semibold text-neutral-800">
                {t('recommendedSchemesTitle', { name: selectedVendor.name })}
              </h2>
            </div>
            <p className="text-sm text-neutral-500 mt-0.5">
              {t('recommendedSchemesSub', {
                product: selectedVendor.product,
                location: selectedVendor.location,
              })}
            </p>
          </div>
          <RecommendedSchemesCard vendor={selectedVendor} />
        </section>
      )}

      {/* Scheme RAG Assistant */}
      <section className="rounded-xl border border-neutral-200 bg-white p-5 shadow-sm space-y-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="text-lg">🤖</span>
            <h2 className="font-semibold text-neutral-800">
              {t('schemeAssistantTitle')} {selectedVendor ? `— ${selectedVendor.name}` : ''}
            </h2>
          </div>
          <p className="text-sm text-neutral-500 mt-0.5">
            {t('schemeAssistantSub')}
          </p>
        </div>
        <SchemeAssistantCard vendor={selectedVendor} />
      </section>

      {selectedVendor && (
        <section className="rounded-xl border border-neutral-200 bg-white p-5 shadow-sm space-y-4">
          <div>
            <h2 className="font-semibold text-neutral-800">
              {t('demandPredictionTitle', { name: selectedVendor.name })}
            </h2>
            <p className="text-sm text-neutral-500">
              {t('demandPredictionSub')}
            </p>
          </div>
          <DemandPredictionCard vendor={selectedVendor} />
        </section>
      )}

      {selectedVendor && (
        <section className="rounded-xl border border-neutral-200 bg-white p-5 shadow-sm space-y-4">
          <div>
            <h2 className="font-semibold text-neutral-800">
              {t('recommendationTitle', { name: selectedVendor.name })}
            </h2>
            <p className="text-sm text-neutral-500">
              {t('recommendationSub')}
            </p>
          </div>
          <RecommendationCard vendor={selectedVendor} />
        </section>
      )}

      {selectedVendor && (
        <section className="rounded-xl border border-neutral-200 bg-white p-5 shadow-sm space-y-5">
          <div>
            <h2 className="font-semibold text-neutral-800">
              {t('salesHistoryTitle', { name: selectedVendor.name })}
            </h2>
            <p className="text-sm text-neutral-500">
              {t('salesHistorySub')}
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
