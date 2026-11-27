<template>
  <PageLayout title="Programme">
    <ol class="programme">
      <li>
        <h2>Végétalisation des repas</h2>
        <p>
          Nous proposons que la totalité des repas faits par le BdE soient des repas végétariens,
          avec une option vegan systématiquement.
        </p>
        <AppCard tag="aside">
          <p>
            Cela prend en compte les repas lors de soirées où le repas est préparé par le BdE, à
            l'intégration et potentiellement jusqu'au WEI. Cela permet de respecter les animaux ou
            diminuer le bilan carbone des évènements du BdE entre autres.
          </p>
        </AppCard>
      </li>

      <li>
        <h2>Engagement social et associatif</h2>
        <p>
          Tout au long de notre mandat, nous prévoyons de travailler avec des associations
          caritatives. Cela peut être par exemple une collecte de fonds ou une collecte de matériel.
          On a également prévu d'organiser des cleanwalks dans Evry.
        </p>
        <AppCard tag="aside">
          <p>Les associations que nous souhaitons contacter sont :</p>
          <ul>
            <li>
              Fiert'Essonne : une association LGBTQIAP+ basée à Évry-Courcouronnes qui lutte contre
              les discriminations et défend l'égalité des droits.
            </li>
            <li>
              S.O.S Racisme : une association dont le but est la lutte contre le racisme,
              l'antisémitisme et plus généralement toutes les formes de discrimination.
            </li>
          </ul>
        </AppCard>
      </li>

      <li>
        <h2>Mise en valeur de la vie associative</h2>
        <p>
          Nous avons observé qu'il y a une décroissance inquiétante de personnes actives dans la vie
          associative. Nous avons réfléchi à plusieurs solutions pour répondre à ce problème.
        </p>
        <ol>
          <li>
            <h3>Réduire la densité de soirées pendant la période de l'intégration</h3>
            <p>
              Nous pensons que réduire la densité de soirées pourrait permettre à plus d'iien·ne de
              venir à de plus grosses soirées pendant la période de l'intégration
            </p>
            <AppCard tag="aside">
              <p>
                Cette période de l'année est dense, et nous pensons qu'avoir des soirées tous les
                soirs peut être contre-productif. C'est pourquoi nous souhaitons diminuer légèrement
                la quantité de soirée pour privilégier les soirées avec le plus de clubs ou
                associations, et un budget plus important. Cela pourrait permettre aux iiens·ne·s
                d'être plus présent·e·s dans les soirées et ainsi mieux s'intégrer dans la vie
                associative.
              </p>
            </AppCard>
          </li>
          <li>
            <h3>Revaloriser la vie associative auprès de l'administration</h3>
            <p>
              Pour résoudre ce problème, on a prévu de négocier un accord avec l'administration
              concernant une revalorisation de la vie associative, que ce ne soit plus quelque chose
              d'adjacent à l'école mais qui soit directement intégré à la vie de l'école.
            </p>
            <AppCard tag="aside">
              <p>
                Par exemple des absences justifiées lors des périodes intenses (intégration,
                campagne, organisation pré-évènements, …) ou des évènements en collaboration avec
                l'administration. Cela pourrait se faire avec un document pré-rempli, prévoyant des
                absences à l'avance, de manière formelle, en partenariat avec la vie scolaire de
                l'école, qui devra être validée par le BdE.
              </p>
            </AppCard>
          </li>
          <li>
            <h3>
              Proposer un vrai statut pour les pipales et autoriser les 3As à pouvoir lister en tant
              que membres actifs.
            </h3>
            <p>
              Cela permettrait de créer des pipales plus facilement, et ainsi avoir une pré-campagne
              et une campagne plus active, et intéresser plus d'élèves dans la vie associative.
            </p>
            <AppCard tag="aside">
              <p>
                Ce statut existe selon le règlement du CBDE, l'idée ici est de l'inclure au sein des
                statuts, car c'est le quota de membres actifs par promotion qui peut être difficile
                à compléter. Nous avons également prévu une aide financière pour les pipales, car
                cela peut être un frein.
              </p>
            </AppCard>
          </li>
        </ol>
      </li>

      <li>
        <h2>Ecriture d'un règlement intérieur</h2>
        <p>
          Il n'existe pas de règlement intérieur actuellement, cela servirait à statuer sur les
          détails non prévus par les actuels statuts modifiés sous TIIMELESS comme l'utilisation de
          matériel du BdE ou les sanctions au niveau de l'AEIIE.
        </p>
      </li>

      <li>
        <h2>Relance du comité de prévention</h2>
        <p>
          En plus du comité Anti-HVSS, externe au BdE, il existait avant un comité de prévention. On
          s'engage à le remettre sur pied, toujours indépendamment du BdE.
        </p>
        <AppCard tag="aside">
          <p>
            Ce comité de prévention a pour but de mettre en œuvre des projets de sensibilisation et
            de prévention dans les domaines de la santé mentale et des addictions.
          </p>
        </AppCard>
      </li>
      <li>
        <h2>Continuité de projets en cours</h2>
        <p>
          Nous poursuivrons les projets déjà commencés lors des précédents mandats, comme la cuisine
          collective au sein de l'école ou le changement de banque.
        </p>
        <AppCard tag="aside">
          <p>
            Aussi, nous avons prévu de faire une relance de ResIIE, pour l'aide aux logements des
            étudiants.
          </p>
        </AppCard>
      </li>
    </ol>
  </PageLayout>
</template>

<script lang="ts">
import AppCard from '@/components/AppCard.vue'
import PageLayout from '@/components/PageLayout.vue'

export default {
  name: 'ProgrammeView',
  components: {
    PageLayout,
    AppCard,
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

@media (max-width: 700px) {
  .programme {
    padding: 0.5rem;
  }

  .programme > li::marker {
    font-size: 1.15rem;
  }

  h2 {
    font-size: 1.15rem;
  }

  li {
    padding-left: 0;
  }

  ul,
  ol {
    padding-left: 1rem;
  }
}
</style>
