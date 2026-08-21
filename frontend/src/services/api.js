import axios from 'axios'

// Base URL comes from Vite env config (see .env.example).
// In production with Nginx reverse proxy, relative '/api' or full URL can be used.
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 15000,
})

// Request Interceptor: Attach timestamp and client Request-ID
apiClient.interceptors.request.use((config) => {
  config.metadata = { startTime: new Date().getTime() }
  // Generate random request id if none exists
  if (!config.headers['X-Request-ID']) {
    config.headers['X-Request-ID'] = 'req-' + Math.random().toString(36).substring(2, 11)
  }
  return config
})

// Response Interceptor: Record duration and log in development
apiClient.interceptors.response.use(
  (response) => {
    if (response.config.metadata) {
      const duration = new Date().getTime() - response.config.metadata.startTime
      if (import.meta.env.DEV) {
        console.debug(
          `[FLUX API] ${response.config.method?.toUpperCase()} ${response.config.url} took ${duration}ms [${response.status}]`
        )
      }
    }
    return response
  },
  (error) => {
    if (error.config?.metadata) {
      const duration = new Date().getTime() - error.config.metadata.startTime
      console.warn(
        `[FLUX API Error] ${error.config.method?.toUpperCase()} ${error.config.url} failed after ${duration}ms:`,
        error.message
      )
    }
    return Promise.reject(error)
  }
)

export default apiClient
