<template>
  <PageLayout title="Rallye">
    <div class="rallye-card">
      <img src="/rallye_fun.png" alt="Rally Fun illustration" width="1920" height="1080" />
    </div>
  </PageLayout>
</template>

<script lang="ts">
import PageLayout from '@/components/PageLayout.vue'

export default {
  name: 'RallyeView',
  components: {
    PageLayout,
  },
}
</script>

<style scoped>
.rallye-card {
  max-width: 80rem;
  margin: 0 auto;
}

/* width/height en attributs = ratio reserve, pas de saut au chargement */
.rallye-card img {
  display: block;
  width: 100%;
  height: auto;
  border-radius: 0.75rem;
}

/* telephone : pleine largeur d'ecran, on sort du padding de main / PageLayout */
@media (max-width: 700px) {
  .rallye-card {
    width: 100vw;
    max-width: none;
    margin-left: calc(50% - 50vw);
  }

  .rallye-card img {
    border-radius: 0;
  }
}
</style>
