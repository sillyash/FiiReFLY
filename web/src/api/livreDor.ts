import axios from 'axios'

import { api } from '@/api/client'

export interface LivreDorEntry {
  id: number
  nom: string
  message: string
  created_at: string
  updated_at: string
}

// son propre message, on sait aussi s'il est masqué par la modo
export type MonEntry = LivreDorEntry & { is_visible: boolean }

export interface Page<T> {
  count: number
  next: string | null
  previous: string | null
  results: T[]
}

// paginé (20/page) contrairement a /membres/
export async function fetchLivreDor(page = 1): Promise<Page<LivreDorEntry>> {
  const { data } = await api.get<Page<LivreDorEntry>>('/api/livre-dor/', { params: { page } })
  return data
}

// connecté uniquement, le nom est mis par l'API. Throttle 429, 400 si deja signé
export async function postLivreDor(message: string): Promise<MonEntry> {
  const { data } = await api.post<MonEntry>('/api/livre-dor/', { message })
  return data
}

// null si pas encore signé (404)
export async function fetchMonLivreDor(): Promise<MonEntry | null> {
  try {
    const { data } = await api.get<MonEntry>('/api/livre-dor/moi/')
    return data
  } catch (e) {
    if (axios.isAxiosError(e) && e.response?.status === 404) return null
    throw e
  }
}

// meme throttle
export async function patchLivreDor(message: string): Promise<MonEntry> {
  const { data } = await api.patch<MonEntry>('/api/livre-dor/moi/', { message })
  return data
}

export async function deleteLivreDor(): Promise<void> {
  await api.delete('/api/livre-dor/moi/')
}
