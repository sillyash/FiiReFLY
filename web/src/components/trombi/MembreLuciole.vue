<template>
  <button
    type="button"
    class="luciole"
    :style="flight"
    :aria-label="`${membre.nom}${membre.role ? ', ' + membre.role : ''}`"
    @click="$emit('select', membre)"
  >
    <span class="glow" aria-hidden="true" />
    <img v-if="membre.photo" class="photo" :src="membre.photo" alt="" loading="lazy" />
    <span v-else class="photo initiales" aria-hidden="true">{{ initiales(membre.nom) }}</span>
    <span class="nom">{{ membre.nom }}</span>
    <span v-if="membre.role" class="role">{{ membre.role }}</span>
  </button>
</template>

<script lang="ts">
import type { PropType } from 'vue'

import { initiales, type Membre } from '@/api/membres'

export default {
  name: 'MembreLuciole',
  props: {
    membre: {
      type: Object as PropType<Membre>,
      required: true,
    },
    // sert a varier le vol sans Math.random(), comme ça c'est pareil a chaque visite
    index: {
      type: Number,
      default: 0,
    },
  },
  emits: ['select'],
  computed: {
    flight(): Record<string, string> {
      const i = this.index
      return {
        '--glow-color': this.membre.poles[0]?.couleur ?? 'var(--color-accent)',
        '--fly-duration': `${7 + ((i * 37) % 50) / 10}s`,
        '--fly-delay': `-${((i * 13) % 60) / 10}s`,
        '--blink-delay': `-${((i * 7) % 30) / 10}s`,
        '--fly-x': `${((i * 17) % 3) * 4 + 4}px`,
        '--fly-y': `${((i * 11) % 3) * 4 + 6}px`,
      }
    },
  },
  methods: {
    initiales,
  },
}
</script>

<style scoped>
.luciole {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.25rem;
  width: 8.5rem;
  padding: 0.5rem;
  border: none;
  background: none;
  color: var(--color-text);
  font: inherit;
  cursor: pointer;
  animation: fly var(--fly-duration) ease-in-out var(--fly-delay) infinite;
}

/* le halo qui clignote derriere la photo */
.glow {
  position: absolute;
  top: 0;
  left: 50%;
  width: 7.5rem;
  height: 7.5rem;
  border-radius: 50%;
  translate: -50% -0.5rem;
  background: radial-gradient(circle, var(--glow-color) 0%, transparent 70%);
  opacity: 0.55;
  animation: blink 2.8s ease-in-out var(--blink-delay) infinite;
  pointer-events: none;
}

.photo {
  position: relative;
  width: 6rem;
  height: 6rem;
  border-radius: 50%;
  border: 3px solid var(--glow-color);
  box-shadow:
    0 0 12px var(--glow-color),
    0 0 28px color-mix(in srgb, var(--glow-color) 60%, transparent);
  object-fit: cover;
  background: var(--color-surface);
  transition: transform 0.2s ease;
}

.initiales {
  display: grid;
  place-items: center;
  font-size: 1.8rem;
  font-weight: bold;
  color: var(--glow-color);
}

.nom {
  position: relative;
  margin-top: 0.4rem;
  font-weight: bold;
}

.role {
  position: relative;
  font-size: 0.9rem;
  opacity: 0.8;
}

.luciole:hover .photo,
.luciole:focus-visible .photo {
  transform: scale(1.08);
}

.luciole:focus-visible {
  outline: 2px dashed var(--color-accent);
  outline-offset: 2px;
  border-radius: 1rem;
}

@keyframes fly {
  0%,
  100% {
    transform: translate(0, 0);
  }
  25% {
    transform: translate(var(--fly-x), calc(var(--fly-y) * -1));
  }
  50% {
    transform: translate(calc(var(--fly-x) * -0.5), calc(var(--fly-y) * -0.4));
  }
  75% {
    transform: translate(calc(var(--fly-x) * -1), calc(var(--fly-y) * -0.8));
  }
}

@keyframes blink {
  0%,
  100% {
    opacity: 0.35;
  }
  50% {
    opacity: 0.9;
  }
}

/* pas d'anim pour ceux qui veulent pas */
@media (prefers-reduced-motion: reduce) {
  .luciole,
  .glow {
    animation: none;
  }
}
</style>
