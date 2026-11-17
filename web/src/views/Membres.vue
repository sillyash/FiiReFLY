<template>
  <PageLayout title="Membres">
    <p v-if="loading">Chargement des lucioles...</p>
    <p v-else-if="error">Impossible de charger les membres, réessaie plus tard.</p>
    <p v-else-if="!membres.length">Personne pour l'instant.</p>

    <template v-else>
      <ul v-if="poles.length" class="legende">
        <li v-for="pole in poles" :key="pole.id">
          <span class="pastille" :style="{ background: pole.couleur }" />
          {{ pole.nom }}
        </li>
      </ul>

      <div class="essaim">
        <MembreLuciole
          v-for="(membre, i) in membres"
          :key="membre.id"
          :membre="membre"
          :index="i"
          @select="selected = $event"
        />
      </div>
    </template>

    <MembreDetail :membre="selected" @close="selected = null" />
  </PageLayout>
</template>

<script lang="ts">
import { fetchMembres, type Membre, type Pole } from '@/api/membres'
import PageLayout from '@/components/PageLayout.vue'
import MembreDetail from '@/components/trombi/MembreDetail.vue'
import MembreLuciole from '@/components/trombi/MembreLuciole.vue'

export default {
  name: 'MembresView',
  components: {
    MembreDetail,
    MembreLuciole,
    PageLayout,
  },
  data() {
    return {
      membres: [] as Membre[],
      selected: null as Membre | null,
      loading: true,
      error: false,
    }
  },
  computed: {
    // tous les poles representés, dans l'ordre des poles
    poles(): Pole[] {
      const seen = new Map<number, Pole>()
      for (const m of this.membres) for (const p of m.poles) seen.set(p.id, p)
      return [...seen.values()].sort((a, b) => a.ordre - b.ordre)
    },
  },
  async mounted() {
    try {
      this.membres = await fetchMembres()
    } catch {
      this.error = true
    } finally {
      this.loading = false
    }
  },
}
</script>

<style scoped>
/* inspire tres fortement de https://www.grabmotion.dev/effects/bubble-swarm */

.legende {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 0.5rem 1.25rem;
  margin: 0 0 1.5rem;
  padding: 0;
  list-style: none;
}

.legende li {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  font-weight: bold;
}

.pastille {
  width: 0.9rem;
  height: 0.9rem;
  border-radius: 50%;
}

.essaim {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 1.5rem 1rem;
  padding: 1rem 0 2rem;
}
</style>
