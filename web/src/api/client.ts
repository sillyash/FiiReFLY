import axios from 'axios'

import { API_URL } from '@/config'

const TOKEN_KEY = 'fiirefly-token'

// localStorage peut etre bloque (navigation privee, cookies desactives) -> pas connecte
export function getToken(): string | null {
  try {
    return localStorage.getItem(TOKEN_KEY)
  } catch {
    return null
  }
}

export function setToken(token: string | null) {
  try {
    if (token) localStorage.setItem(TOKEN_KEY, token)
    else localStorage.removeItem(TOKEN_KEY)
  } catch {
    // tant pis, on reste deconnecte au prochain chargement
  }
}

/** Le front est sur un autre site que l'API : auth par token, pas de cookie. */
export const api = axios.create({
  baseURL: API_URL,
})

api.interceptors.request.use((config) => {
  const token = getToken()
  if (token) {
    config.headers.set('Authorization', `Token ${token}`)
  }
  return config
})

// token perime / supprime : l'API repond 401 meme sur les GET publics,
// on l'oublie et on rejoue la requete sans
api.interceptors.response.use(undefined, (error) => {
  const config = error.config
  if (
    axios.isAxiosError(error) &&
    error.response?.status === 401 &&
    config?.headers.has('Authorization')
  ) {
    setToken(null)
    config.headers.delete('Authorization')
    return api.request(config)
  }
  return Promise.reject(error)
})
