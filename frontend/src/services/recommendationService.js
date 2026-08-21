import apiClient from './api'

/**
 * Recommendation API calls. Mirrors backend/app/api/recommendations.py.
 */
export async function getRecommendation(vendorId, payload) {
  const response = await apiClient.post(`/api/vendors/${vendorId}/recommend`, payload)
  return response.data
}
