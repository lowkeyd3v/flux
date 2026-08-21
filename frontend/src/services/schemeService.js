import apiClient from './api'

/**
 * Government scheme RAG & recommendations API calls (Milestone 5).
 * Mirrors backend/app/api/schemes.py.
 */

export async function listSchemes(category = null) {
  const params = category ? { category } : {}
  const response = await apiClient.get('/api/schemes', { params })
  return response.data
}

export async function getSchemeById(schemeId) {
  const response = await apiClient.get(`/api/schemes/${schemeId}`)
  return response.data
}

export async function querySchemes({ query, vendorId = null, topK = 4 }) {
  const response = await apiClient.post('/api/schemes/query', {
    query,
    vendor_id: vendorId,
    top_k: topK,
  })
  return response.data
}

export async function getRecommendedSchemes(vendorId) {
  const response = await apiClient.get(`/api/vendors/${vendorId}/schemes/recommended`)
  return response.data
}
