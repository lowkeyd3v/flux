import apiClient from './api'

/**
 * Sales record API calls, nested under a vendor.
 * Mirrors backend/app/api/sales_records.py.
 */

export async function createSalesRecord(vendorId, record) {
  const response = await apiClient.post(`/api/vendors/${vendorId}/sales`, record)
  return response.data
}

export async function bulkCreateSalesRecords(vendorId, records) {
  const response = await apiClient.post(`/api/vendors/${vendorId}/sales/bulk`, { records })
  return response.data
}

export async function listSalesRecords(vendorId) {
  const response = await apiClient.get(`/api/vendors/${vendorId}/sales`)
  return response.data
}

export async function deleteSalesRecord(vendorId, recordId) {
  await apiClient.delete(`/api/vendors/${vendorId}/sales/${recordId}`)
}
