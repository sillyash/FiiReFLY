<template>
  <PageLayout title="Soirées">
    <SoireeDescription
      v-for="soiree in soirees"
      :key="soiree.titre"
      :date="soiree.date"
      :titre="soiree.titre"
      :description="soiree.description"
    />
  </PageLayout>
</template>

<script lang="ts">
import PageLayout from '@/components/PageLayout.vue'
import SoireeDescription from '@/components/SoireeDescription.vue'

// Toutes les soirées ont lieu de 19h à 1h (heure de Paris) : seule la date est à renseigner.
const soirees = [
  {
    titre: 'Soirée x Pipale',
    date: '2026-11-24',
    description: 'Test hdgdgdhsvsh',
  },
  {
    titre: 'Soirée x Sérieuse',
    date: '2026-11-30',
    description: 'Test hdgdgdhsvsh',
  },
  {
    titre: 'Soirée solo',
    date: '2026-12-02',
    description: 'Test hdgdgdhsvsh',
  },
]

export default {
  name: 'SoireesView',
  components: {
    PageLayout,
    SoireeDescription,
  },

  data() {
    return {
      soirees: soirees,
    }
  },
}
</script>
