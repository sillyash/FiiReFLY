<template>
  <PageLayout title="Programme">
    <ol class="programme">
      <li>
        <h2>Végétalisation des repas</h2>
        <p>
          Tous les repas faits par le BdE seront au minimum végétariens, avec une option vegan. Ça
          compte les repas de soirées, de l'intégration et potentiellement jusqu'au WEI.
        </p>
      </li>

      <li>
        <h2>Engagement social et associatif</h2>
        <p>
          Tout au long du mandat, on bosse avec d'autres associations : collectes de fonds,
          collectes de matériel. On organise aussi des cleanwalks.
        </p>
      </li>

      <li>
        <h2>Continuité des projets en cours</h2>
        <p>
          On poursuit les projets lancés lors des mandats précédents : la cuisine collective à
          l'école, le changement de banque et une relance de ResIIE.
        </p>
      </li>

      <li>
        <h2>Mise en valeur de la vie associative</h2>
        <p>
          On observe une baisse inquiétante du nombre de personnes actives dans la vie associative.
          Nos solutions :
        </p>
        <ul>
          <li>
            Réduire la densité de soirées pendant l'intégration, pour que chacun·e puisse venir à
            plus de soirées (en proportion).
          </li>
          <li>
            Revaloriser la vie associative auprès de l'administration, en négociant par exemple des
            absences justifiées lors des périodes intenses (intégration, campagne, préparation
            d'évènements…).
          </li>
          <li>
            Proposer un vrai statut pour les pipales et autoriser les 3A à lister en tant que
            membres actifs.
          </li>
        </ul>
      </li>

      <li>
        <h2>Écriture d'un règlement intérieur</h2>
        <p>
          Pour trancher les détails non prévus par les statuts actuels (modifiés sous TIIMELESS),
          comme les sanctions au niveau de l'AEIIE.
        </p>
      </li>

      <li>
        <h2>Relance du comité de prévention</h2>
        <p>
          À côté du comité anti-HVSS, externe au BdE, il existait un comité de prévention. On
          s'engage à le remettre sur pied, toujours indépendamment du CA, pour continuer la
          sensibilisation.
        </p>
      </li>
    </ol>
  </PageLayout>
</template>

<script lang="ts">
import PageLayout from '@/components/PageLayout.vue'

export default {
  name: 'ProgrammeView',
  components: {
    PageLayout,
  },
}
</script>

<style scoped>
.programme {
  max-width: 50rem;
  margin: 0 auto;
  line-height: 1.5;
}

.programme > li::marker {
  font-size: 1.5rem;
  font-weight: bold;
}
</style>
