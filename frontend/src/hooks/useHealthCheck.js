import { useEffect, useState, useCallback } from 'react'
import { getHealthStatus } from '../services/healthService'

/**
 * Fetches backend health status once on mount.
 * Returns { status, data, error, refetch } so components can
 * display connectivity state and manually retry.
 */
export function useHealthCheck() {
  const [status, setStatus] = useState('loading') // 'loading' | 'ok' | 'error'
  const [data, setData] = useState(null)
  const [error, setError] = useState(null)

  const check = useCallback(async () => {
    setStatus('loading')
    setError(null)
    try {
      const result = await getHealthStatus()
      setData(result)
      setStatus('ok')
    } catch (err) {
      setError(err)
      setStatus('error')
    }
  }, [])

  useEffect(() => {
    check()
  }, [check])

  return { status, data, error, refetch: check }
}
