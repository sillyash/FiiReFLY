<template>
  <dialog ref="dialog" class="detail" @close="$emit('close')" @click="onBackdrop">
    <div v-if="membre" class="detail-body" :style="{ '--glow-color': couleur }">
      <button type="button" class="close" aria-label="Fermer" @click="close">✕</button>
      <img v-if="membre.photo" class="photo" :src="membre.photo" alt="" />
      <span v-else class="photo initiales" aria-hidden="true">{{ initiales(membre.nom) }}</span>
      <h2>{{ membre.nom }}</h2>
      <p v-if="membre.role" class="role">{{ membre.role }}</p>
      <span v-if="membre.pole" class="pole">{{ membre.pole.nom }}</span>
      <p v-if="membre.description" class="description">{{ membre.description }}</p>
    </div>
  </dialog>
</template>

<script lang="ts">
import type { PropType } from 'vue'

import { initiales, type Membre } from '@/api/membres'

export default {
  name: 'MembreDetail',
  props: {
    membre: {
      type: Object as PropType<Membre | null>,
      default: null,
    },
  },
  emits: ['close'],
  computed: {
    couleur(): string {
      return this.membre?.pole?.couleur ?? 'var(--color-accent)'
    },
  },
  watch: {
    membre(value: Membre | null) {
      const dialog = this.$refs.dialog as HTMLDialogElement
      if (value && !dialog.open) dialog.showModal()
      else if (!value && dialog.open) dialog.close()
    },
  },
  methods: {
    initiales,
    close() {
      ;(this.$refs.dialog as HTMLDialogElement).close()
    },
    // clic en dehors de la carte = fermer
    onBackdrop(event: MouseEvent) {
      if (event.target === this.$refs.dialog) this.close()
    },
  },
}
</script>

<style scoped>
.detail {
  width: min(28rem, calc(100vw - 2rem));
  padding: 0;
  border: 2px solid var(--color-border);
  border-radius: 1.5rem;
  background: var(--color-surface);
  color: var(--color-text);
}

.detail::backdrop {
  background: rgb(0 0 0 / 0.5);
  backdrop-filter: blur(2px);
}

.detail-body {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 2rem 1.5rem 1.5rem;
  text-align: center;
}

.close {
  position: absolute;
  top: 0.75rem;
  right: 0.75rem;
  border: none;
  background: none;
  color: var(--color-text);
  font-size: 1.2rem;
  cursor: pointer;
}

.photo {
  width: 12rem;
  height: 12rem;
  border-radius: 50%;
  border: 4px solid var(--glow-color);
  box-shadow: 0 0 30px var(--glow-color);
  object-fit: cover;
}

.initiales {
  display: grid;
  place-items: center;
  font-size: 3rem;
  font-weight: bold;
  color: var(--glow-color);
}

h2 {
  margin: 1rem 0 0.25rem;
}

.role {
  margin: 0;
  font-weight: bold;
}

.pole {
  margin-top: 0.5rem;
  padding: 0.15rem 0.7rem;
  border-radius: 999px;
  background: var(--glow-color);
  color: #fff;
  font-size: 0.9rem;
  font-weight: bold;
}

.description {
  white-space: pre-line;
}
</style>
