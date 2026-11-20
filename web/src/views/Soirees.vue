<template>
  <PageLayout title="Soirées">
    <SoireeDescription
      v-for="soiree in soirees"
      :key="soiree.titre"
      :date="soiree.date"
      :titre="soiree.titre"
      :description="soiree.description"
      :heure-fin="soiree.heureFin"
    />
  </PageLayout>
</template>

<script lang="ts">
import PageLayout from '@/components/PageLayout.vue'
import SoireeDescription from '@/components/SoireeDescription.vue'

const soirees = [
  {
    titre: 'FiiReFLY x MÉDiiÉVALe',
    date: '2026-11-23',
    heureFin: 1,
    description: 'Forêt de Brocéliande + After',
  },
  {
    titre: 'FiiReFLY x MIIragE',
    date: '2026-11-25',
    heureFin: 2,
    description: 'Le labyrinthe des illusions',
  },
  {
    titre: 'FiiReFLY',
    date: '2026-12-01',
    heureFin: 2,
    description: 'La nuit des lucioles',
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
