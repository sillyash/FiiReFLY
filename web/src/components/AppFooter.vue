<template>
  <footer class="site-footer">
    <p>© {{ new Date().getFullYear() }} FiiReFLY</p>
  </footer>
</template>

<script lang="ts">
export default {
  name: 'AppFooter',
}
</script>

<style scoped>
.site-footer {
  padding: 1rem;
  text-align: center;
  background-color: var(--color-surface);
  transition: background-color var(--theme-transition-duration) ease;
}

.site-footer p {
  margin: 0;
}
</style>
