<template>
  <article class="ticket" :class="{ 'is-past': isPast, 'menu-open': menuOpen }">
    <div class="ticket-stub">
      <span class="stub-month">{{ month }}</span>
      <span class="stub-day">{{ day }}</span>
      <span class="stub-weekday">{{ weekday }}</span>
      <span class="stub-time">{{ displayTime }}</span>
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
        <span class="calendar-label">Ajouter à l'agenda</span>
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

<script lang="ts">
import { defineComponent } from 'vue'
import type { TZDate } from '@date-fns/tz'
import {
  PARIS_TIME_ZONE,
  atParisTime,
  dayOfMonth,
  shortMonthFr,
  shortWeekdayFr,
  utcStamp,
} from '@/utils/datetime'

// Toutes les soirées : 19h 1h
const START_HOUR = 19
const END_HOUR = 1

let nextId = 0

// ICS sinon c broken
const escapeIcs = (text: string) => text.replace(/[\\;,]/g, '\\$&').replace(/\n/g, '\\n')

export default defineComponent({
  name: 'SoireeDescription',

  props: {
    /** format AAAA-MM-JJ. */
    date: { type: String, required: true },
    titre: { type: String, required: true },
    description: { type: String, default: '' },
  },

  data() {
    return {
      menuOpen: false,
      menuId: `calendar-menu-${nextId++}`,
      displayTime: `${START_HOUR}h-${END_HOUR}h`,
    }
  },

  computed: {
    start(): TZDate {
      return atParisTime(this.date, 0, START_HOUR)
    },
    end(): TZDate {
      return atParisTime(this.date, 1, END_HOUR)
    },
    month(): string {
      return shortMonthFr(this.start)
    },
    day(): string {
      return dayOfMonth(this.start)
    },
    weekday(): string {
      return shortWeekdayFr(this.start)
    },
    isPast(): boolean {
      return this.end.getTime() <= Date.now()
    },
    googleCalendarUrl(): string {
      const params = new URLSearchParams({
        action: 'TEMPLATE',
        text: this.titre,
        dates: `${utcStamp(this.start)}/${utcStamp(this.end)}`,
        details: this.description,
        ctz: PARIS_TIME_ZONE,
      })
      return `https://calendar.google.com/calendar/render?${params}`
    },
  },

  mounted() {
    document.addEventListener('pointerdown', this.onDocumentPointerDown)
  },

  beforeUnmount() {
    document.removeEventListener('pointerdown', this.onDocumentPointerDown)
  },

  methods: {
    toggleMenu() {
      if (this.menuOpen) return this.closeMenu()
      this.menuOpen = true
      this.$nextTick(() => {
        const menu = this.$refs.calendarMenu as HTMLElement | undefined
        menu?.querySelector<HTMLElement>('[role="menuitem"]')?.focus()
      })
    },

    closeMenu() {
      if (!this.menuOpen) return
      this.menuOpen = false
      ;(this.$refs.calendarToggle as HTMLElement | undefined)?.focus()
    },

    isInsideCalendar(node: EventTarget | null) {
      return (this.$refs.calendar as HTMLElement | undefined)?.contains(node as Node) ?? false
    },

    onDocumentPointerDown(event: PointerEvent) {
      if (!this.isInsideCalendar(event.target)) this.menuOpen = false
    },

    onCalendarFocusOut(event: FocusEvent) {
      if (event.relatedTarget && !this.isInsideCalendar(event.relatedTarget)) this.menuOpen = false
    },

    downloadIcs() {
      const ics = [
        'BEGIN:VCALENDAR',
        'VERSION:2.0',
        'PRODID:-//FiiReFLY//Soirées//FR',
        'BEGIN:VEVENT',
        `UID:soiree-${this.date}@fiirefly`,
        `DTSTAMP:${utcStamp(new Date())}`,
        `DTSTART:${utcStamp(this.start)}`,
        `DTEND:${utcStamp(this.end)}`,
        `SUMMARY:${escapeIcs(this.titre)}`,
        ...(this.description ? [`DESCRIPTION:${escapeIcs(this.description)}`] : []),
        'END:VEVENT',
        'END:VCALENDAR',
      ].join('\r\n')

      const link = document.createElement('a')
      link.href = URL.createObjectURL(new Blob([ics], { type: 'text/calendar;charset=utf-8' }))
      link.download = `fiirefly-${this.date}.ics`
      link.click()
      URL.revokeObjectURL(link.href)

      this.closeMenu()
    },
  },
})
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

.is-past {
  filter: grayscale(1);
  opacity: 0.6;
}

@media (max-width: 480px) {
  .ticket-stub {
    flex-basis: 4.5rem;
  }

  .stub-month,
  .stub-weekday {
    font-size: 1.1rem;
  }

  .stub-day {
    font-size: 2.5rem;
  }

  .stub-time {
    font-size: 0.9rem;
  }

  .event-title {
    font-size: 1.5rem;
  }

  .notes {
    font-size: 1.1rem;
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
