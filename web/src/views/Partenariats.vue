<template>
  <PageLayout title="Partenariats">
    <section class="partenaires">
      <article class="part-card">
        <img class="part-logo" src="/chopstix_logo.jpg" alt="Logo Chopstix" height="70" width="70" />
        <div class="part-content">
          <h2>Chopstix</h2>
          <p>
            -10% sur tout le menu avec le code <strong>CHOPSTIXBDE</strong> à rentrer
            sur l'application mobile Chopstix
          </p>
          <a
            class="part-lien"
            href="https://chopstixnoodles.fr/chopstix-app/"
            target="_blank"
            rel="noopener noreferrer"
          >
            Application
          </a>
        </div>
      </article>
    </section>
  </PageLayout>
</template>

<script lang="ts">
import PageLayout from '@/components/PageLayout.vue'

export default {
  name: 'PartenariatsView',
  components: {
    PageLayout,
  },
}
</script>

<style scoped>
.partenaires {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  max-width: 34rem;
  margin: 0 auto 2rem;
}

/* meme style que .description de l'accueil */
.part-card {
  display: flex;
  align-items: center;
  gap: 1.25rem;
  padding: 1.25rem;
  border-radius: 0.75rem;
  background: var(--color-surface);
  color: var(--color-text);
}

.part-logo {
  flex-shrink: 0;
  width: 70px;
  height: 70px;
  object-fit: cover;
  border-radius: 0.5rem;
}

.part-content h2 {
  margin: 0 0 0.35rem;
  font-size: 1.25rem;
}

.part-content p {
  margin: 0;
}

/* bouton pilule, version simple des raccourcis de l'accueil */
.part-lien {
  display: inline-block;
  margin-top: 0.75rem;
  padding: 0.4rem 1rem;
  border-radius: 999px;
  background: var(--color-accent);
  color: var(--color-surface);
  font-weight: bold;
  text-decoration: none;
}

</style>
