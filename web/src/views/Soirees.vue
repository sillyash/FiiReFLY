<template>
  <PageLayout title="Soirées">
    <SoireeDescription
      v-for="soiree in soirees"
      :key="soiree.titre"
      :date-debut="soiree.dateDebut"
      :date-fin="soiree.dateFin"
      :titre="soiree.titre"
      :description="soiree.description"
    />
  </PageLayout>
</template>

<script lang="ts">
import PageLayout from '@/components/PageLayout.vue'
import SoireeDescription from '@/components/SoireeDescription.vue';

const soirees = [
  {
    titre: 'Soirée x Pipale',
    dateDebut: new Date('2026-11-24T'),
    dateFin: new Date('2026-11-25'),
    description: 'Test hdgdgdhsvsh',
  },
  {
    titre: 'Soirée x Sérieuse',
    dateDebut: new Date('2026-11-30'),
    dateFin: new Date('2026-12-01'),
    description: 'Test hdgdgdhsvsh',
  },
  {
    titre: 'Soirée solo',
    dateDebut: new Date('2026-12-02'),
    dateFin: new Date('2026-12-03'),
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
  }
}

</script>
