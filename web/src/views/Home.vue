<template>
  <ForestBackground class="page-background" />

  <PageLayout title="Accueil">
    <nav class="raccourcis">
      <!-- icones a la main, stroke = currentColor -->
      <RouterLink to="/programme">
        <svg viewBox="0 0 24 24"><path d="M6 3h9l3 3v15H6zM9 10h6M9 14h6M9 18h4" /></svg>
        Lire le programme
      </RouterLink>
      <RouterLink to="/soirees">
        <svg viewBox="0 0 24 24"><path d="M20 14A8 8 0 1 1 10 4a6 6 0 0 0 10 10z" /></svg>
        Voir les soirées
      </RouterLink>
      <RouterLink to="/livre-dor">
        <svg viewBox="0 0 24 24"><path d="M4 20l1-5L16 4l4 4L9 19zM14 6l4 4" /></svg>
        Signer le livre d'or
      </RouterLink>
      <RouterLink to="/membres">
        <svg viewBox="0 0 24 24">
          <circle cx="9" cy="8" r="3" />
          <circle cx="17" cy="9" r="2.5" />
          <path d="M3 20a6 6 0 0 1 12 0M15 15a5 5 0 0 1 6 5" />
        </svg>
        Voir les membres
      </RouterLink>
    </nav>
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

.raccourcis svg {
  width: 1.3em;
  height: 1.3em;
  fill: none;
  stroke: currentColor;
  stroke-width: 2;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.raccourcis a:hover {
  transform: scale(1.05);
}
</style>
