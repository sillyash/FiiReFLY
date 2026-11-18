<template>
  <PageLayout title="Livre d'or">
    <p v-if="loading">Chargement...</p>
    <p v-else-if="error">Impossible de charger le livre d'or, réessaie plus tard.</p>
    <p v-else-if="!entries.length">Aucun message pour l'instant.</p>

    <ul v-else class="messages">
      <li v-for="entry in entries" :key="entry.id">
        <p class="entete">
          <strong>{{ entry.nom }}</strong>
          <span class="date">{{ formatDate(entry.created_at) }}</span>
        </p>
        <p class="message">{{ entry.message }}</p>
      </li>
    </ul>
  </PageLayout>
</template>

<script lang="ts">
import { fetchLivreDor, type LivreDorEntry } from '@/api/livreDor'
import PageLayout from '@/components/PageLayout.vue'

export default {
  name: 'LivreDorView',
  components: {
    PageLayout,
  },
  data() {
    return {
      entries: [] as LivreDorEntry[],
      loading: true,
      error: false,
    }
  },
  async mounted() {
    try {
      // juste la premiere page pour l'instant
      const page = await fetchLivreDor()
      this.entries = page.results
    } catch {
      this.error = true
    } finally {
      this.loading = false
    }
  },
  methods: {
    formatDate(iso: string): string {
      return new Date(iso).toLocaleDateString('fr-FR')
    },
  },
}
</script>

<style scoped>
.messages {
  margin: 0;
  padding: 0;
  list-style: none;
}

.messages li + li {
  margin-top: 1.5rem;
}

.entete {
  display: flex;
  gap: 0.75rem;
  align-items: baseline;
  margin: 0 0 0.25rem;
}

.date {
  font-size: 0.85em;
  opacity: 0.7;
}

.message {
  margin: 0;
  white-space: pre-line;
}
</style>
