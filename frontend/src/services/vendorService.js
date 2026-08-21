import apiClient from './api'

/**
 * Vendor profile API calls. Mirrors backend/app/api/vendors.py.
 */

export async function createVendor(vendorData) {
  const response = await apiClient.post('/api/vendors', vendorData)
  return response.data
}

export async function listVendors() {
  const response = await apiClient.get('/api/vendors')
  return response.data
}

export async function getVendor(vendorId) {
  const response = await apiClient.get(`/api/vendors/${vendorId}`)
  return response.data
}

export async function updateVendor(vendorId, updates) {
  const response = await apiClient.patch(`/api/vendors/${vendorId}`, updates)
  return response.data
}

export async function deleteVendor(vendorId) {
  await apiClient.delete(`/api/vendors/${vendorId}`)
}
