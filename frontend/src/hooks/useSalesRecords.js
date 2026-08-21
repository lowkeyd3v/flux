import { useCallback, useEffect, useState } from 'react'
import {
  listSalesRecords,
  createSalesRecord as createSalesRecordApi,
} from '../services/salesService'

/**
 * Fetches sales records for a given vendor and exposes a createRecord
 * action that refreshes the list on success. Returns an idle state when
 * no vendorId is provided.
 */
export function useSalesRecords(vendorId) {
  const [records, setRecords] = useState([])
  const [status, setStatus] = useState('idle') // 'idle' | 'loading' | 'ok' | 'error'
  const [error, setError] = useState(null)

  const refetch = useCallback(async () => {
    if (!vendorId) {
      setRecords([])
      setStatus('idle')
      return
    }
    setStatus('loading')
    setError(null)
    try {
      const data = await listSalesRecords(vendorId)
      setRecords(data)
      setStatus('ok')
    } catch (err) {
      setError(err)
      setStatus('error')
    }
  }, [vendorId])

  useEffect(() => {
    refetch()
  }, [refetch])

  const createRecord = useCallback(
    async (recordData) => {
      const created = await createSalesRecordApi(vendorId, recordData)
      await refetch()
      return created
    },
    [vendorId, refetch]
  )

  return { records, status, error, refetch, createRecord }
}
