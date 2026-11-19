import { format } from 'date-fns'
import { fr } from 'date-fns/locale'
import { TZDate } from '@date-fns/tz'

export const PARIS_TIME_ZONE = 'Europe/Paris'

/**
 * Date "AAAA-MM-JJ" décalée de `dayOffset` jours, à `hour` heure de Paris.
 * Ex. atParisTime('2026-11-24', 1, 1) → 25 nov. 2026 à 1:00 (Paris).
 */
export function atParisTime(date: string, dayOffset: number, hour: number): TZDate {
  const [year = 0, month = 1, day = 1] = date.split('-').map(Number)
  return TZDate.tz(PARIS_TIME_ZONE, year, month - 1, day + dayOffset, hour)
}

/**
 * Horodatage UTC compact "20261124T180000Z" (Google Calendar, iCalendar).
 * Passe par un Date natif : TZDate#toISOString renvoie l'heure locale avec décalage.
 */
export function utcStamp(date: Date): string {
  return new Date(date.getTime()).toISOString().replace(/[-:]|\.\d{3}/g, '')
}

/** Mois abrégé en français, sans point : "nov", "déc". */
export function shortMonthFr(date: Date): string {
  return format(date, 'MMM', { locale: fr }).replace('.', '')
}

/** Jour de la semaine en 3 lettres en français, sans point : "lun", "mar". */
export function shortWeekdayFr(date: Date): string {
  return format(date, 'EEE', { locale: fr }).replace('.', '')
}

/** Jour du mois sur deux chiffres : "02", "24". */
export function dayOfMonth(date: Date): string {
  return format(date, 'dd')
}
