<template>
  <ForestBackground class="page-background" />

  <PageLayout title="Accueil">
    <section class="about">
      <img class="hero-photo" src="/fiirefly_logo.png" alt="FiiReFLY Logo" />
      <p class="description">
        Merveilleuse forêt peuplée d'animaux et de végétaux enchanteurs, laissez vous porter par
        FiireFly, la liste aux milles lucioles
      </p>
    </section>

    <section class="nav-section">
      <nav class="raccourcis">
        <!-- icones = Material Symbols (voir index.html), color = currentColor -->
        <RouterLink to="/programme">
          <span class="material-symbols-outlined" aria-hidden="true">description</span>
          Lire le programme
        </RouterLink>
        <RouterLink to="/soirees">
          <span class="material-symbols-outlined" aria-hidden="true">dark_mode</span>
          Voir les soirées
        </RouterLink>
        <RouterLink to="/livre-dor">
          <span class="material-symbols-outlined" aria-hidden="true">edit</span>
          Signer le livre d'or
        </RouterLink>
        <RouterLink to="/membres">
          <span class="material-symbols-outlined" aria-hidden="true">group</span>
          Voir les membres
        </RouterLink>
      </nav>
    </section>
  </PageLayout>
</template>

<script lang="ts">
import ForestBackground from '@/components/forest/ForestBackground.vue'
import PageLayout from '@/components/PageLayout.vue'

export default {
  name: 'HomeView',
  components: {
    ForestBackground,
    PageLayout,
  },
}
</script>

<style scoped>
section {
  max-width: 34rem;
  margin: 0 auto;
}

section + section {
  margin-top: 3rem;
}

.description {
  padding: 1.25rem;
  border-radius: 0.75rem;
  background: var(--color-surface);
  color: var(--color-text);
}

.hero-photo {
  /* img = inline par defaut, donc block + margin auto pour centrer */
  display: block;
  width: min(100%, 20rem);
  height: auto;
  margin: 0 auto 1.5rem;
}

.nav-section {
  margin-bottom: 2rem;
}

.page-background {
  position: fixed;
  inset: 0;
  z-index: -1;
}

.raccourcis {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  align-items: center;
  font-size: 1.2rem;
  font-weight: bold;
}

/* boutons pilule, meme largeur pour que ca fasse propre */
.raccourcis a {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.6rem;
  width: 16rem;
  padding: 0.8rem;
  border-radius: 999px;
  background: var(--color-accent);
  color: var(--color-surface);
  text-align: center;
  text-decoration: none;
  transition: transform 0.15s ease;
}

.raccourcis .material-symbols-outlined {
  font-size: 1.3em;
}

.raccourcis a:hover {
  transform: scale(1.05);
}
</style>
