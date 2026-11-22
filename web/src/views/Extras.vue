<template>
  <PageLayout title="Extras">
    <section class="partenaires">
      <AppCard tag="article" class="part-card">
        <img
          class="part-logo"
          src="/jeu_logo.png"
          alt="Logo Jeu Vidéo FiiReFLY"
          height="110"
          width="110"
        />
        <div class="part-content">
          <h2>Jeu vidéo</h2>
          <p>
            Le jeu vidéo de la légendaire liste FiiReFLY ! Rejoignez-nous dans la
            <b>forêt des lucioles</b> et tenter de maxer le bonheur de tous les <b>animaux</b> dans
            ce jeu de puzzle pour grimper dans le classement, et tenter de
            <b>remporter un super lot</b> !
          </p>
          <a
            class="part-lien"
            href="https://baitolo3.itch.io/fiirefly"
            target="_blank"
            rel="noopener noreferrer"
          >
            Jeu
          </a>
        </div>
      </AppCard>
    </section>
  </PageLayout>
</template>

<script lang="ts">
import AppCard from '@/components/AppCard.vue'
import PageLayout from '@/components/PageLayout.vue'

export default {
  name: 'PartenariatsView',
  components: {
    AppCard,
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

.part-card {
  display: flex;
  align-items: center;
  gap: 1.25rem;
}

.part-logo {
  flex-shrink: 0;
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
