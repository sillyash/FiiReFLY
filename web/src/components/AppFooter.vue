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
  border-top: 2px solid var(--color-border);
}

.site-footer p {
  margin: 0;
}
</style>
