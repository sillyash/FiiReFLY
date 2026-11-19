import { defineStore } from 'pinia'
import { computed, ref } from 'vue'

import { api, getToken, setToken } from '@/api/client'
import { API_URL, AUTH_ENDPOINTS } from '@/config'

export interface User {
  id: number
  username: string
  name: string
}

interface MeResponse {
  user: User | null
}

interface TokenResponse {
  token: string
  user: User
}

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const loaded = ref(false)
  const isLoggedIn = computed(() => user.value !== null)

  async function fetchMe() {
    try {
      // pas de token = pas connecte, inutile de demander a l'API
      user.value = getToken() ? (await api.get<MeResponse>(AUTH_ENDPOINTS.me)).data.user : null
    } catch {
      user.value = null
    } finally {
      loaded.value = true
    }
  }

  /** Retour du login Arise : echange le code court contre un token. */
  async function exchange(code: string) {
    try {
      const { data } = await api.post<TokenResponse>(AUTH_ENDPOINTS.token, { code })
      setToken(data.token)
      user.value = data.user
    } catch {
      user.value = null
    } finally {
      loaded.value = true
    }
  }

  /** Arise Connect login, coming back to `next` (a frontend route) afterwards. */
  function loginUrl(next = '/') {
    return `${API_URL}${AUTH_ENDPOINTS.login}?next=${encodeURIComponent(next)}`
  }

  async function logout() {
    try {
      await api.post(AUTH_ENDPOINTS.logout)
    } finally {
      setToken(null)
      user.value = null
    }
  }

  return { user, loaded, isLoggedIn, fetchMe, exchange, loginUrl, logout }
})
