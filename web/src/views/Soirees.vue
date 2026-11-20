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
    description: 'Featuring de légende',
  },
  {
    titre: 'FiiReFLY solo',
    date: '2026-12-02',
    description: "Vous êtes pas prêt⋅e⋅s pour l'after",
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
