<template>
  <PageLayout title="Programme">
    <ol class="programme">
      <li>
        <h2>Végétalisation des repas</h2>
        <p>
          Nous proposons que la totalité des repas faits par le BdE soient des repas végétariens,
          avec une option vegan systématiquement. Cela prend en compte les repas lors de soirées, à
          l'intégration et potentiellement jusqu'au WEI.
        </p>
      </li>

      <li>
        <h2>Engagement social et associatif</h2>
        <p>
          Tout au long de notre mandat, nous prévoyons de travailler avec d'autres associations.
          Cela peut être une collecte de fonds ou une collecte de matériel. On a également prévu
          d'organiser des cleanwalks dans Evry.
        </p>
      </li>

      <li>
        <h2>Continuité de projets en cours</h2>
        <p>
          Nous poursuivrons les projets déjà commencés lors des précédents mandats, comme la cuisine
          collective au sein de l'école et le changement de banque. Nous avons aussi prévu de faire
          une relance de ResIIE, pour l'aide au logement des étudiants.
        </p>
      </li>

      <li>
        <h2>Mise en valeur de la vie associative</h2>
        <p>
          Nous avons observé qu'il y a une décroissance inquiétante du nombre de personnes actives
          dans la vie associative. Nous avons réfléchi à plusieurs solutions pour répondre à ce
          problème.
        </p>
        <ol>
          <li>
            <h3>Réduire la densité de soirées pendant la période de l'intégration</h3>
            <p>
              Cette période est très dense. Nous pensons que réduire la densité de soirées pourrait
              permettre à des gens de venir proportionnellement à plus de grosses soirées, et donc
              de s'intégrer dans la vie associative plus facilement, avec un plus grand public.
            </p>
          </li>
          <li>
            <h3>Revaloriser la vie associative auprès de l'administration</h3>
            <p>
              Nous avons prévu de négocier avec l'administration une revalorisation de la vie
              associative, pour que ce ne soit plus quelque chose d'à côté de l'école mais qui soit
              directement intégré à la vie de l'école. Par exemple des absences justifiées lors des
              périodes intenses (intégration, campagne, organisation pré-évènements…) ou des
              évènements en collaboration avec l'administration.
            </p>
          </li>
          <li>
            <h3>
              Proposer un vrai statut pour les pipales et autoriser les 3A à lister en tant que
              membres actifs
            </h3>
            <p>
              Cela permettrait de créer des pipales plus facilement, et ainsi d'avoir une
              pré-campagne et une campagne plus actives, et d'intéresser plus d'élèves à la vie
              associative. Nous avons prévu une aide financière pour les pipales, car cela a été un
              frein pour les précédentes.
            </p>
          </li>
        </ol>
      </li>

      <li>
        <h2>Écriture d'un règlement intérieur</h2>
        <p>
          Il n'existe pas de règlement intérieur actuellement. Il servirait à statuer sur les
          détails non prévus par les statuts actuels (modifiés sous TIIMELESS), comme l'utilisation
          du matériel du BdE ou les sanctions au niveau de l'AEIIE.
        </p>
      </li>

      <li>
        <h2>Relance du comité de prévention</h2>
        <p>
          En plus du comité anti-HVSS, externe au BdE, il existait avant un comité de prévention. On
          s'engage à le remettre sur pied, toujours indépendamment du BdE, pour pouvoir continuer la
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

.programme ol > li::marker {
  font-weight: bold;
}
</style>
