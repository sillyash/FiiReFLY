<template>
  <PageLayout title="Livre d'or">
    <template v-if="auth.loaded">
      <form v-if="auth.isLoggedIn" class="formulaire" @submit.prevent="envoyer">
        <textarea
          v-model="nouveau"
          maxlength="1000"
          rows="4"
          required
          placeholder="Laisse un petit mot..."
        />
        <p v-if="sendError" class="erreur">{{ sendError }}</p>
        <button type="submit" :disabled="sending || !nouveau.trim()">Envoyer</button>
      </form>
      <p v-else class="formulaire">
        <a :href="auth.loginUrl($route.fullPath)">Connecte-toi</a> pour laisser un message.
      </p>
    </template>

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
import axios from 'axios'

import { fetchLivreDor, postLivreDor, type LivreDorEntry } from '@/api/livreDor'
import PageLayout from '@/components/PageLayout.vue'
import { useAuthStore } from '@/stores/auth'

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
      nouveau: '',
      sending: false,
      sendError: '',
    }
  },
  computed: {
    auth() {
      return useAuthStore()
    },
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
    async envoyer() {
      const message = this.nouveau.trim()
      if (!message || this.sending) return
      this.sending = true
      this.sendError = ''
      try {
        const entry = await postLivreDor(message)
        this.entries.unshift(entry)
        this.nouveau = ''
      } catch (e) {
        const status = axios.isAxiosError(e) ? e.response?.status : undefined
        if (status === 429) {
          this.sendError = 'Doucement, trop de messages, réessaie plus tard.'
        } else if (status === 401 || status === 403) {
          this.sendError = 'Ta session a expiré, reconnecte-toi.'
        } else {
          this.sendError = "Impossible d'envoyer le message."
        }
      } finally {
        this.sending = false
      }
    },
  },
}
</script>

<style scoped>
.formulaire {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 0.5rem;
  margin: 0 0 2rem;
}

.formulaire textarea {
  box-sizing: border-box;
  width: 100%;
  font: inherit;
  resize: vertical;
}

.erreur {
  margin: 0;
  color: #c0392b;
}

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
