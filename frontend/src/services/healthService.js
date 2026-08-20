import apiClient from './api'

/**
 * Calls the backend health check endpoint.
 * Used during bootstrap to confirm frontend <-> backend connectivity.
 */
export async function getHealthStatus() {
  const response = await apiClient.get('/api/health')
  return response.data
}
