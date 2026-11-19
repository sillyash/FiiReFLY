export const API_URL = import.meta.env.VITE_API_URL.replace(/\/+$/, '')

export const AUTH_ENDPOINTS = {
  login: '/auth/login/',
  token: '/auth/token/',
  logout: '/auth/logout/',
  me: '/auth/me/',
} as const
