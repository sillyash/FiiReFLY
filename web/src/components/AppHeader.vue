<template>
  <header class="site-header">
    <RouterLink id="branding" to="/">
      <h1>FiiReFLY</h1>
    </RouterLink>

    <div id="navbar">
      <RouterLink to="/" class="nav-link">Accueil</RouterLink>
      <RouterLink to="/programme" class="nav-link">Programme</RouterLink>
      <RouterLink to="/soirees" class="nav-link">Soirées</RouterLink>
      <RouterLink to="/livre-dor" class="nav-link">Livre d'or</RouterLink>
      <RouterLink to="/membres" class="nav-link">Membres</RouterLink>
    </div>

    <div class="toggles">
      <AuthButton />
      <ThemeToggle />
    </div>
  </header>
</template>

<script lang="ts">
import AuthButton from '@/components/AuthButton.vue'
import ThemeToggle from '@/components/ThemeToggle.vue'

export default {
  name: 'AppHeader',
  components: {
    AuthButton,
    ThemeToggle,
  },
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
  background-color: var(--color-surface);
  transition: background-color var(--theme-transition-duration) ease;
}

#navbar {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 0.5rem 1rem;
}

.toggles {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  justify-self: end;
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
