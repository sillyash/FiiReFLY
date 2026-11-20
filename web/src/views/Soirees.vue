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
    titre: 'FiiReFLY x MEDiiEVAle',
    date: '2026-11-23',
    description: 'Forêt de Brocéliande + After',
  },
  {
    titre: 'FiiReFLY x MIIragE',
    date: '2026-11-25',
    description: 'Le labyrinthe des illusions',
  },
  {
    titre: 'FiiReFLY solo',
    date: '2026-12-02',
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
