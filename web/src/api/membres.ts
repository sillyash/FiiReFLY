import { api } from '@/api/client'

export interface Pole {
  id: number
  nom: string
  couleur: string
  ordre: number
}

export interface Membre {
  id: number
  nom: string
  role: string
  // triés par ordre, le premier = pole principal
  poles: Pole[]
  photo: string | null
  description: string
}

// pas de pagination sur /membres/, on recoit direct la liste
export async function fetchMembres(): Promise<Membre[]> {
  const { data } = await api.get<Membre[]>('/api/membres/')
  return data
}

export function initiales(nom: string): string {
  return nom
    .split(/\s+/)
    .filter(Boolean)
    .slice(0, 2)
    .map((w) => w[0]!.toUpperCase())
    .join('')
}
