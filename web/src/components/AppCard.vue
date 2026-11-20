<template>
  <component :is="tag" class="card">
    <slot />
  </component>
</template>

<script lang="ts">
export default {
  name: 'AppCard',
  props: {
    tag: { type: String, default: 'div' },
  },
}
</script>

<style scoped>
.card {
  padding: 1.25rem;
  border-radius: 0.75rem;
  background: var(--color-surface);
  color: var(--color-text);
}
</style>
