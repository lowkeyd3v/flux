import apiClient from './api'

/**
 * Demand prediction API calls. Mirrors backend/app/api/predictions.py.
 */
export async function predictDemand(vendorId, payload) {
  const response = await apiClient.post(`/api/vendors/${vendorId}/predict`, payload)
  return response.data
}
