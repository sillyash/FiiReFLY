<template>
  <PageLayout title="Extras">
    <section>
      <AppCard tag="div">
        <a href="https://baitolo3.itch.io/fiirefly" target="_blank">
          <h2>Jeu vidéo</h2>
        </a>
      </AppCard>
    </section>
  </PageLayout>
</template>

<script lang="ts">
import AppCard from '@/components/AppCard.vue'
import PageLayout from '@/components/PageLayout.vue'

export default {
  name: 'PartenariatsView',
  components: {
    AppCard,
    PageLayout,
  },
}
</script>

<style scoped></style>
