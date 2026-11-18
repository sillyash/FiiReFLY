<script setup lang="ts">
import { useTheme } from '@/composables/useTheme'

const { theme, toggleTheme } = useTheme()
</script>

<template>
  <button
    type="button"
    class="theme-toggle"
    :aria-label="theme === 'day' ? 'Passer en mode nuit' : 'Passer en mode jour'"
    @click="toggleTheme"
  >
    <Transition name="flip" mode="out-in">
      <span
        v-if="theme === 'day'"
        key="sun"
        class="theme-icon material-symbols-outlined"
        aria-hidden="true"
        >light_mode</span
      >
      <span v-else key="moon" class="theme-icon filled material-symbols-outlined" aria-hidden="true"
        >dark_mode</span
      >
    </Transition>
  </button>
</template>

<style scoped>
.theme-toggle {
  flex: none;
  width: 2.75rem;
  height: 2.75rem;
  padding: 0;
  border: 2px solid var(--color-border);
  border-radius: 50%;
  background: var(--color-surface);
  color: var(--color-text);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition:
    background-color var(--theme-transition-duration) ease,
    border-color var(--theme-transition-duration) ease,
    color var(--theme-transition-duration) ease,
    transform 0.15s ease;
}

.theme-toggle:hover {
  border-color: var(--color-accent);
  color: var(--color-accent);
}

.theme-toggle:active {
  transform: scale(0.88);
}

.theme-icon {
  display: block;
  font-size: 22px;
}

/* la lune etait pleine en svg, on garde ca via l'axe FILL */
.filled {
  font-variation-settings: 'FILL' 1;
}

.flip-enter-active,
.flip-leave-active {
  transition:
    transform 0.35s ease,
    opacity 0.35s ease;
}

.flip-enter-from {
  transform: rotate(-120deg) scale(0.4);
  opacity: 0;
}

.flip-leave-to {
  transform: rotate(120deg) scale(0.4);
  opacity: 0;
}
</style>
