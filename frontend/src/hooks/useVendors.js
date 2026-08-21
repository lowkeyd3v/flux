import { useCallback, useEffect, useState } from 'react'
import { listVendors, createVendor as createVendorApi } from '../services/vendorService'

/**
 * Fetches the vendor list and exposes a createVendor action that
 * refreshes the list on success.
 */
export function useVendors() {
  const [vendors, setVendors] = useState([])
  const [status, setStatus] = useState('loading') // 'loading' | 'ok' | 'error'
  const [error, setError] = useState(null)

  const refetch = useCallback(async () => {
    setStatus('loading')
    setError(null)
    try {
      const data = await listVendors()
      setVendors(data)
      setStatus('ok')
    } catch (err) {
      setError(err)
      setStatus('error')
    }
  }, [])

  useEffect(() => {
    refetch()
  }, [refetch])

  const createVendor = useCallback(
    async (vendorData) => {
      const created = await createVendorApi(vendorData)
      await refetch()
      return created
    },
    [refetch]
  )

  return { vendors, status, error, refetch, createVendor }
}
