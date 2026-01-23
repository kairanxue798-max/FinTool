/**
 * API Configuration Utility
 * 
 * This utility provides a centralized way to manage API endpoints.
 * In development, it uses the Vite proxy (/api).
 * In production, it uses the VITE_API_URL environment variable.
 */

// Get API base URL from environment variable or use proxy in development
const getApiBaseUrl = (): string => {
  // In production, use environment variable
  if (import.meta.env.VITE_API_URL) {
    return import.meta.env.VITE_API_URL
  }
  
  // In development, use proxy (empty string means same origin)
  return ''
}

export const API_BASE_URL = getApiBaseUrl()

/**
 * Builds a full API URL from a path
 * @param path - API path (e.g., '/api/upload-csv')
 * @returns Full URL or path depending on environment
 */
export const buildApiUrl = (path: string): string => {
  // If path already starts with http, return as-is
  if (path.startsWith('http://') || path.startsWith('https://')) {
    return path
  }
  
  // Ensure path starts with /
  const normalizedPath = path.startsWith('/') ? path : `/${path}`
  
  // If API_BASE_URL is set, use it; otherwise use proxy path
  if (API_BASE_URL) {
    // Remove /api prefix if API_BASE_URL already includes it
    const cleanPath = normalizedPath.startsWith('/api') ? normalizedPath : `/api${normalizedPath}`
    return `${API_BASE_URL}${cleanPath}`
  }
  
  // Development: use proxy path
  return normalizedPath
}

/**
 * Fetch wrapper with automatic API URL building
 */
export const apiFetch = async (
  path: string,
  options?: RequestInit
): Promise<Response> => {
  const url = buildApiUrl(path)
  return fetch(url, options)
}

export default {
  API_BASE_URL,
  buildApiUrl,
  apiFetch,
}

