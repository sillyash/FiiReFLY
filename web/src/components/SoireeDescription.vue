<template>
  <article class="ticket" :class="{ 'is-past': isPast, 'menu-open': menuOpen }">
    <div class="ticket-stub">
      <span class="stub-month">{{ month }}</span>
      <span class="stub-day">{{ day }}</span>
      <span class="stub-weekday">{{ weekday }}</span>
      <span v-if="displayTime" class="stub-time">{{ displayTime }}</span>
    </div>

    <div class="ticket-body">
      <h2 class="event-title">{{ titre }}</h2>
      <p v-if="description" class="notes">{{ description }}</p>

      <div class="ticket-footer">
        <span v-if="isPast" class="status">On vous attend nombreux</span>
      </div>
    </div>

    <div
      v-if="!isPast"
      ref="calendar"
      class="ticket-calendar"
      @keydown.esc="closeMenu"
      @focusout="onCalendarFocusOut"
    >
      <button
        ref="calendarToggle"
        type="button"
        class="calendar-toggle"
        aria-haspopup="menu"
        :aria-expanded="menuOpen"
        :aria-controls="menuId"
        @click="toggleMenu"
      >
        <span class="calendar-plus" aria-hidden="true">+</span>
        <span class="calendar-label">Ajouter au calendrier</span>
      </button>

      <ul v-if="menuOpen" :id="menuId" ref="calendarMenu" class="calendar-menu" role="menu">
        <li role="none">
          <a
            role="menuitem"
            :href="googleCalendarUrl"
            target="_blank"
            rel="noopener noreferrer"
            @click="closeMenu"
          >
            Google Calendar
          </a>
        </li>
        <li role="none">
          <button type="button" role="menuitem" @click="downloadIcs">.ics (Apple, Outlook)</button>
        </li>
      </ul>
    </div>
  </article>
</template>

<script setup lang="ts">
import { computed, nextTick, onBeforeUnmount, onMounted, ref, useId } from 'vue'

interface Props {
  dateDebut: Date
  dateFin: Date
  titre: string
  description?: string
  time?: string
}

const props = withDefaults(defineProps<Props>(), {
  time: '',
  description: '',
})

const menuOpen = ref(false)
const calendar = ref<HTMLElement | null>(null)
const calendarToggle = ref<HTMLButtonElement | null>(null)
const calendarMenu = ref<HTMLUListElement | null>(null)

const parsedDate = computed(() => localDate(props.dateDebut))
const parsedEndDate = computed(() => localDate(props.dateFin))

const month = computed(() =>
  parsedDate.value.toLocaleDateString(undefined, { month: 'short' }).replace('.', ''),
)
const day = computed(() => String(parsedDate.value.getDate()).padStart(2, '0'))
const weekday = computed(() =>
  parsedDate.value.toLocaleDateString(undefined, { weekday: 'short' }).replace('.', ''),
)
const displayTime = computed(() => {
  if (!props.time) return null
  const [hours = 0, minutes = 0] = props.time.split(':').map(Number)
  const at = new Date(parsedDate.value)
  at.setHours(hours, minutes)
  return at.toLocaleTimeString(undefined, { hour: 'numeric', minute: '2-digit' })
})

const isPast = computed(() => {
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  return parsedDate.value < today
})

const menuId = `calendar-menu-${useId()}`

const calendarEvent = computed(() => {
  const start = new Date(parsedDate.value)
  const end = new Date(parsedDate.value)
  if (props.time) {
    const [hours = 0, minutes = 0] = props.time.split(':').map(Number)
    start.setHours(hours, minutes)
    end.setTime(start.getTime() + 2 * 60 * 60 * 1000)
  } else {
    end.setTime(parsedEndDate.value.getTime())
  }
  const allDay = !props.time
  return {
    title: props.titre,
    details: props.description,
    start: calendarStamp(start, allDay),
    end: calendarStamp(end, allDay),
    allDay,
  }
})

const googleCalendarUrl = computed(() => {
  const { title, details, start, end } = calendarEvent.value
  const params = new URLSearchParams({
    action: 'TEMPLATE',
    text: title,
    dates: `${start}/${end}`,
    details,
  })
  return `https://calendar.google.com/calendar/render?${params}`
})

function toggleMenu() {
  if (menuOpen.value) {
    closeMenu()
    return
  }
  menuOpen.value = true
  nextTick(() => {
    calendarMenu.value?.querySelector<HTMLElement>('[role="menuitem"]')?.focus()
  })
}

function closeMenu() {
  if (!menuOpen.value) return
  menuOpen.value = false
  calendarToggle.value?.focus()
}

function onDocumentPointerDown(event: PointerEvent) {
  if (menuOpen.value && !calendar.value?.contains(event.target as Node)) {
    menuOpen.value = false
  }
}

function onCalendarFocusOut(event: FocusEvent) {
  const next = event.relatedTarget as Node | null
  if (next && !calendar.value?.contains(next)) {
    menuOpen.value = false
  }
}

function downloadIcs() {
  const { title, details, start, end, allDay } = calendarEvent.value
  const dateValue = allDay ? ';VALUE=DATE' : ''
  const lines = [
    'BEGIN:VCALENDAR',
    'VERSION:2.0',
    'PRODID:-//FiiReFLY//Soirées//FR',
    'BEGIN:VEVENT',
    `UID:${menuId}@fiirefly`,
    `DTSTAMP:${new Date().toISOString().replace(/[-:]|\.\d{3}/g, '')}`,
    `DTSTART${dateValue}:${start}`,
    `DTEND${dateValue}:${end}`,
    `SUMMARY:${escapeIcs(title)}`,
    ...(details ? [`DESCRIPTION:${escapeIcs(details)}`] : []),
    'END:VEVENT',
    'END:VCALENDAR',
  ]

  const blob = new Blob([lines.join('\r\n')], { type: 'text/calendar;charset=utf-8' })
  const link = document.createElement('a')
  link.href = URL.createObjectURL(blob)
  link.download = `fiirefly-${calendarStamp(parsedDate.value, true)}.ics`
  document.body.appendChild(link)
  link.click()
  link.remove()
  setTimeout(() => URL.revokeObjectURL(link.href), 0)

  closeMenu()
}

onMounted(() => document.addEventListener('pointerdown', onDocumentPointerDown))
onBeforeUnmount(() => document.removeEventListener('pointerdown', onDocumentPointerDown))

// Escape text for an iCalendar TEXT value (RFC 5545 §3.3.11).
function escapeIcs(text: string): string {
  return text.replace(/[\\;,]/g, (char) => `\\${char}`).replace(/\n/g, '\\n')
}

function localDate(value: Date): Date {
  const isUtcMidnight =
    value.getUTCHours() === 0 &&
    value.getUTCMinutes() === 0 &&
    value.getUTCSeconds() === 0 &&
    value.getUTCMilliseconds() === 0
  const year = isUtcMidnight ? value.getUTCFullYear() : value.getFullYear()
  const month = isUtcMidnight ? value.getUTCMonth() : value.getMonth()
  const day = isUtcMidnight ? value.getUTCDate() : value.getDate()
  return new Date(year, month, day)
}

// "YYYYMMDD" or "YYYYMMDDTHHMMSS" from the local date fields. No trailing Z: times are
// "floating", so both Google and .ics read them as the fan's local time.
function calendarStamp(date: Date, allDay: boolean): string {
  const pad = (n: number) => String(n).padStart(2, '0')
  const day = `${date.getFullYear()}${pad(date.getMonth() + 1)}${pad(date.getDate())}`
  if (allDay) return day
  return `${day}T${pad(date.getHours())}${pad(date.getMinutes())}${pad(date.getSeconds())}`
}
</script>

<style scoped>
.ticket {
  --notch-size: 0.9rem;

  position: relative;
  display: flex;
  max-width: 34rem;
  margin: 1.5rem auto;
  background: var(--color-surface);
  border: 3px solid var(--color-border);
  box-shadow: 6px 6px 0 var(--color-border);
  transform: rotate(-0.8deg);
  transition:
    transform 0.2s ease,
    box-shadow 0.2s ease,
    background-color var(--theme-transition-duration) ease,
    border-color var(--theme-transition-duration) ease;
}

/* Alternate the tilt so a list of tickets looks hand-pinned to a corkboard. */
.ticket:nth-of-type(even) {
  transform: rotate(0.8deg);
}

.ticket:hover,
.ticket:focus-within {
  transform: rotate(0deg) translate(-2px, -2px);
  box-shadow: 8px 8px 0 var(--color-accent);
}

.ticket-stub {
  position: relative;
  display: flex;
  flex: 0 0 6rem;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-width: 0;
  padding: 1rem 0.5rem;
  background: var(--color-accent);
  color: var(--color-surface);
  border-right: 3px dashed var(--color-border);
  line-height: 1;
  text-transform: uppercase;
}

/* Half-circle "punch holes" where the stub would tear off. */
.ticket-stub::before,
.ticket-stub::after {
  content: '';
  position: absolute;
  right: calc(var(--notch-size) / -2 - 1.5px);
  width: var(--notch-size);
  height: var(--notch-size);
  background: var(--color-bg);
  border: 3px solid var(--color-border);
  border-radius: 50%;
  transition: background-color var(--theme-transition-duration) ease;
}

.ticket-stub::before {
  top: calc(var(--notch-size) / -2 - 3px);
}

.ticket-stub::after {
  bottom: calc(var(--notch-size) / -2 - 3px);
}

.stub-month,
.stub-weekday {
  font-size: 1.4rem;
  letter-spacing: 0.1em;
}

.stub-day {
  font-size: 3.5rem;
}

.stub-time {
  margin-top: 0.5rem;
  font-size: 1.1rem;
  letter-spacing: 0.05em;
}

.ticket-body {
  position: relative;
  flex: 1;
  padding: 0.75rem 1.25rem;
  min-width: 0;
}

.event-title {
  margin: 0;
  font-size: 2rem;
  line-height: 1.1;
  overflow-wrap: anywhere;
}

.notes {
  margin: 0.5rem 0 0;
  overflow-wrap: anywhere;
  font-style: italic;
  font-size: 1.25rem;
}

.ticket-footer {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-end;
  align-items: center;
  gap: 0.5rem 1rem;
  margin-top: 0.75rem;
}

.info-link {
  color: var(--color-text);
}

.status {
  opacity: 0.75;
}

/* Right-hand stub, torn off along a dashed line like the date stub on the left. */
.ticket-calendar {
  position: relative;
  display: flex;
  flex: 0 0 7rem;
  width: 7rem;
  border-left: 3px dashed var(--color-border);
}

.calendar-toggle {
  display: flex;
  flex: 1;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.25rem;
  min-width: 0;
  padding: 1rem 0.5rem;
  font: inherit;
  line-height: 1;
  text-transform: uppercase;
  color: var(--color-text);
  background: transparent;
  border: none;
  cursor: pointer;
  transition:
    background-color 0.15s ease,
    color 0.15s ease;
}

.calendar-toggle:hover,
.calendar-toggle:focus-visible,
.calendar-toggle[aria-expanded='true'] {
  background: var(--color-text);
  color: var(--color-surface);
}

.ticket-calendar::before,
.ticket-calendar::after {
  content: '';
  position: absolute;
  z-index: 1;
  left: calc(var(--notch-size) / -2 - 1.5px);
  width: var(--notch-size);
  height: var(--notch-size);
  background: var(--color-bg);
  border: 3px solid var(--color-border);
  border-radius: 50%;
  transition: background-color var(--theme-transition-duration) ease;
}

.ticket-calendar::before {
  top: calc(var(--notch-size) / -2 - 3px);
}

.ticket-calendar::after {
  bottom: calc(var(--notch-size) / -2 - 3px);
}

/* Each ticket's tilt transform makes its own stacking context: lift the open one so the
   menu isn't covered by the next ticket. */
.ticket.menu-open {
  z-index: 2;
}

.calendar-menu {
  position: absolute;
  top: calc(100% + 3px);
  right: -3px;
  z-index: 2;
  min-width: 13rem;
  margin: 0;
  padding: 0;
  list-style: none;
  background: var(--color-surface);
  border: 3px solid var(--color-border);
  box-shadow: 6px 6px 0 var(--color-border);
}

.calendar-menu [role='menuitem'] {
  display: block;
  width: 100%;
  padding: 0.4rem 0.75rem;
  font: inherit;
  text-align: left;
  text-decoration: none;
  color: var(--color-text);
  background: transparent;
  border: none;
  cursor: pointer;
  transition:
    background-color 0.15s ease,
    color 0.15s ease;
}

.calendar-menu li + li {
  border-top: 2px dashed var(--color-border);
}

.calendar-menu [role='menuitem']:hover,
.calendar-menu [role='menuitem']:focus-visible {
  background: var(--color-text);
  color: var(--color-surface);
}

.calendar-plus {
  font-size: 3rem;
}

.calendar-label {
  max-width: 100%;
  font-size: 1rem;
  letter-spacing: 0.05em;
  line-height: 1.2;
  overflow-wrap: anywhere;
  text-align: center;
  white-space: normal;
}

.stamp {
  position: absolute;
  top: 50%;
  right: 1rem;
  padding: 0.1rem 0.5rem;
  border: 3px double var(--color-accent);
  color: var(--color-accent);
  font-size: 2rem;
  letter-spacing: 0.1em;
  transform: translateY(-50%) rotate(-14deg);
  opacity: 0.85;
  pointer-events: none;
}

.is-past {
  filter: grayscale(1);
  opacity: 0.6;
}

@media (max-width: 480px) {
  .ticket-stub {
    flex-basis: 4.5rem;
  }

  .stub-day {
    font-size: 2.5rem;
  }

  /* Not enough room for a third column: the calendar stub tears off the bottom instead. */
  .ticket {
    flex-wrap: wrap;
  }

  .ticket-calendar {
    flex: 1 0 100%;
    width: auto;
    border-left: none;
    border-top: 3px dashed var(--color-border);
  }

  .calendar-toggle {
    flex-direction: row;
    gap: 0.5rem;
    padding: 0.4rem;
  }

  .calendar-label {
    flex: 1;
    text-align: left;
  }

  .ticket-calendar::before,
  .ticket-calendar::after {
    top: calc(var(--notch-size) / -2 - 1.5px);
    bottom: auto;
  }

  .ticket-calendar::before {
    left: calc(var(--notch-size) / -2 - 3px);
  }

  .ticket-calendar::after {
    left: auto;
    right: calc(var(--notch-size) / -2 - 3px);
  }

  .calendar-plus {
    font-size: 1.75rem;
  }
}

@media (prefers-reduced-motion: reduce) {
  .ticket,
  .ticket:nth-of-type(even),
  .ticket:hover,
  .ticket:focus-within {
    transform: none;
    transition: none;
  }
}
</style>
