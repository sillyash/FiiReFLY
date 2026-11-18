<template>
  <PageLayout title="Livre d'or">
    <template v-if="auth.loaded">
      <form v-if="auth.isLoggedIn" class="carte formulaire" novalidate @submit.prevent="envoyer">
        <h2>Signer le livre d'or ✎</h2>

        <label for="livre-dor-message">Ton message</label>
        <textarea
          id="livre-dor-message"
          v-model="nouveau"
          :maxlength="messageMax"
          rows="4"
          placeholder="Laisse un petit mot ♡"
          :aria-invalid="Boolean(fieldError)"
        />
        <p class="compteur">{{ nouveau.length }}/{{ messageMax }}</p>
        <p v-if="fieldError" class="erreur">{{ fieldError }}</p>

        <div class="pied">
          <p v-if="sendError" class="erreur" role="alert">{{ sendError }}</p>
          <p v-else-if="merci" role="status">Merci ♡</p>
          <button type="submit" :disabled="!peutEnvoyer">
            {{ sending ? 'Envoi...' : 'Signer !' }}
          </button>
        </div>
      </form>
      <p v-else class="carte connexion">
        <a :href="auth.loginUrl($route.fullPath)">Connecte-toi</a> pour signer le livre d'or ✎
      </p>
    </template>

    <p v-if="loading" class="statut">Chargement du livre d'or...</p>

    <div v-else-if="error" class="statut">
      <p>Impossible de charger le livre d'or :(</p>
      <button type="button" @click="charger">Réessayer</button>
    </div>

    <template v-else>
      <article v-for="entry in entries" :key="entry.id" class="note">
        <p class="message">{{ entry.message }}</p>
        <p class="signature">
          - <span class="nom">{{ entry.nom }}</span> ·
          <time :datetime="entry.created_at">{{ formatDate(entry.created_at) }}</time>
        </p>
      </article>
      <p v-if="!entries.length" class="statut">Personne n'a encore signé, sois le·la premier·e ♡</p>

      <div v-if="hasNext" class="statut">
        <p v-if="loadMoreError">Impossible d'en charger plus :(</p>
        <button type="button" :disabled="loadingMore" @click="chargerPlus">
          {{ loadingMore ? 'Chargement...' : loadMoreError ? 'Réessayer' : 'Voir plus ↓' }}
        </button>
      </div>
    </template>
  </PageLayout>
</template>

<script lang="ts">
import axios from 'axios'

import { fetchLivreDor, postLivreDor, type LivreDorEntry } from '@/api/livreDor'
import PageLayout from '@/components/PageLayout.vue'
import { useAuthStore } from '@/stores/auth'

// meme limite que LivreDorEntry.message dans api/core/models.py
const MESSAGE_MAX = 1000

export default {
  name: 'LivreDorView',
  components: {
    PageLayout,
  },
  data() {
    return {
      entries: [] as LivreDorEntry[],
      page: 1,
      hasNext: false,
      loading: true,
      error: false,
      loadingMore: false,
      loadMoreError: false,
      nouveau: '',
      sending: false,
      sendError: '',
      fieldError: '',
      merci: false,
      messageMax: MESSAGE_MAX,
    }
  },
  computed: {
    auth() {
      return useAuthStore()
    },
    peutEnvoyer(): boolean {
      return !this.sending && this.nouveau.trim() !== ''
    },
  },
  mounted() {
    this.charger()
  },
  methods: {
    formatDate(iso: string): string {
      return new Date(iso).toLocaleDateString('fr-FR', {
        day: 'numeric',
        month: 'short',
        year: 'numeric',
      })
    },
    async charger() {
      this.loading = true
      this.error = false
      try {
        const page = await fetchLivreDor()
        this.entries = page.results
        this.page = 1
        this.hasNext = page.next !== null
      } catch (e) {
        console.error(e)
        this.error = true
      } finally {
        this.loading = false
      }
    },
    async chargerPlus() {
      if (!this.hasNext || this.loadingMore) return
      this.loadingMore = true
      this.loadMoreError = false
      try {
        const page = await fetchLivreDor(this.page + 1)
        // un message posté entre temps decale les pages, donc on vire les doublons
        const ids = new Set(this.entries.map((e) => e.id))
        this.entries.push(...page.results.filter((e) => !ids.has(e.id)))
        this.page += 1
        this.hasNext = page.next !== null
      } catch (e) {
        console.error(e)
        this.loadMoreError = true
      } finally {
        this.loadingMore = false
      }
    },
    async envoyer() {
      if (!this.peutEnvoyer) return
      this.sending = true
      this.merci = false
      this.sendError = ''
      this.fieldError = ''
      try {
        const entry = await postLivreDor(this.nouveau.trim())
        // le plus recent en premier donc on le met en haut
        this.entries.unshift(entry)
        this.nouveau = ''
        this.merci = true
      } catch (e) {
        console.error(e)
        const res = axios.isAxiosError(e) ? e.response : undefined
        const msgErrors = res?.status === 400 ? res.data?.message : undefined
        if (msgErrors) {
          // DRF renvoie { message: ["..."] }
          this.fieldError = Array.isArray(msgErrors) ? msgErrors.join(' ') : String(msgErrors)
        } else if (res?.status === 429) {
          this.sendError = 'Doucement ♡ trop de messages, réessaie plus tard.'
        } else if (res?.status === 401 || res?.status === 403) {
          this.sendError = 'Ta session a expiré, reconnecte-toi.'
        } else {
          this.sendError = "L'envoi a échoué :( on réessaie ?"
        }
      } finally {
        this.sending = false
      }
    },
  },
}
</script>

<style scoped>
.carte {
  max-width: 30rem;
  margin: 1.5rem auto 3rem;
  padding: 1rem 1.25rem;
  background: var(--color-surface);
  border: 3px solid var(--color-border);
  box-shadow: 6px 6px 0 var(--color-accent);
  transition:
    background-color var(--theme-transition-duration) ease,
    border-color var(--theme-transition-duration) ease;
}

.formulaire {
  display: flex;
  flex-direction: column;
}

.connexion {
  text-align: center;
}

h2 {
  margin: 0 0 0.5rem;
}

label {
  margin-top: 0.5rem;
}

textarea {
  box-sizing: border-box;
  width: 100%;
  font: inherit;
  padding: 0.25rem 0.5rem;
  color: var(--color-text);
  background: var(--color-bg);
  border: 2px solid var(--color-border);
  border-radius: 0;
  resize: vertical;
  transition:
    background-color var(--theme-transition-duration) ease,
    border-color var(--theme-transition-duration) ease;
}

textarea:focus-visible {
  outline: 3px dashed var(--color-accent);
  outline-offset: 2px;
}

[aria-invalid='true'] {
  border-color: var(--color-accent);
}

.compteur {
  margin: 0.1rem 0 0;
  text-align: right;
  font-size: 0.85em;
  opacity: 0.7;
}

.erreur {
  margin: 0.25rem 0 0;
  color: var(--color-accent);
}

.pied {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-end;
  align-items: center;
  gap: 0.5rem 1rem;
  margin-top: 0.75rem;
}

.pied p {
  margin: 0;
}

button {
  font: inherit;
  padding: 0.1rem 0.8rem;
  color: var(--color-text);
  background: var(--color-surface);
  border: 2px solid var(--color-border);
  cursor: pointer;
  transition:
    background-color 0.15s ease,
    color 0.15s ease;
}

button:hover:not(:disabled),
button:focus-visible {
  background: var(--color-text);
  color: var(--color-surface);
}

button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.statut {
  text-align: center;
  opacity: 0.8;
}

.statut p {
  margin: 0 0 0.5rem;
}

.note {
  position: relative;
  max-width: 30rem;
  margin: 2rem auto;
  padding: 1.25rem 1.25rem 0.75rem;
  background: var(--color-surface);
  border: 3px solid var(--color-border);
  box-shadow: 5px 5px 0 var(--color-border);
  transform: rotate(0.6deg);
  transition:
    transform 0.2s ease,
    background-color var(--theme-transition-duration) ease,
    border-color var(--theme-transition-duration) ease;
}

/* on alterne l'inclinaison, comme des mots scotchés a la main */
.note:nth-of-type(even) {
  transform: rotate(-0.6deg);
}

.note:hover {
  transform: rotate(0deg);
}

/* le bout de scotch */
.note::before {
  content: '';
  position: absolute;
  top: -0.8rem;
  left: 50%;
  width: 5rem;
  height: 1.4rem;
  background: var(--color-accent);
  opacity: 0.75;
  transform: translateX(-50%) rotate(-3deg);
}

.message {
  margin: 0;
  white-space: pre-line;
  overflow-wrap: anywhere;
}

.signature {
  margin: 0.75rem 0 0;
  text-align: right;
  font-size: 0.9em;
  opacity: 0.8;
}

.nom {
  color: var(--color-accent);
}

@media (prefers-reduced-motion: reduce) {
  .note,
  .note:nth-of-type(even),
  .note:hover {
    transform: none;
    transition: none;
  }
}
</style>
