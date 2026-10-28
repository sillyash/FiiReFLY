<template>
  <header class="site-header">
    <RouterLink id="branding" to="/">
      <h1>FiiReFLY</h1>
    </RouterLink>

    <div id="navbar">
      <RouterLink to="/" class="nav-link">Accueil</RouterLink>
      <RouterLink to="/soirees" class="nav-link">Soirées</RouterLink>
      <RouterLink to="/livre-dor" class="nav-link">Livre d'or</RouterLink>
    </div>
  </header>
</template>

<script lang="ts">
export default {
  name: 'AppHeader',
}
</script>

<style scoped>
#branding {
  display: flex;
  align-items: center;
  gap: 1rem;
  /* It's a home link, but should look like plain branding. */
  color: inherit;
  text-decoration: none;
}

#branding h1 {
  margin: 0;
}

.site-header {
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  align-items: center;
  padding: 1rem;
  border-bottom: 2px solid var(--color-border);
}

#navbar {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 0.5rem 1rem;
}

.nav-link {
  font-weight: bold;
  font-size: 1.2rem;
  color: var(--color-accent);
  text-decoration: underline;
}

.nav-link.router-link-exact-active {
  color: var(--color-text);
  text-decoration: none;
}

@media (max-width: 700px) {
  .site-header {
    grid-template-columns: 1fr;
    justify-items: center;
    gap: 1rem;
  }
}
</style>
