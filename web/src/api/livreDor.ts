import { api } from '@/api/client'

export interface LivreDorEntry {
  id: number
  nom: string
  message: string
  created_at: string
}

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
