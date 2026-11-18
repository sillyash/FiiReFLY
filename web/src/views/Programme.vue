<template>
  <PageLayout title="Programme">
    <div class="fiirefly">
      <ol class="programme">
        <li>
          <h2 class="titre">Végétalisation des repas</h2>
          <div class="carte">
            <p>
              Tous les repas faits par le BdE seront au minimum végétariens, avec une option vegan.
              Ça compte les repas de soirées, de l'intégration et potentiellement jusqu'au WEI.
            </p>
          </div>
        </li>

        <li>
          <h2 class="titre">Engagement social et associatif</h2>
          <div class="carte">
            <p>
              Tout au long du mandat, on bosse avec d'autres associations : collectes de fonds,
              collectes de matériel. On organise aussi des cleanwalks.
            </p>
          </div>
        </li>

        <li>
          <h2 class="titre">Continuité des projets en cours</h2>
          <div class="carte">
            <p>
              On poursuit les projets lancés lors des mandats précédents : la cuisine collective à
              l'école, le changement de banque et une relance de ResIIE.
            </p>
          </div>
        </li>

        <li>
          <h2 class="titre">Mise en valeur de la vie associative</h2>
          <div class="carte">
            <p>
              On observe une baisse inquiétante du nombre de personnes actives dans la vie
              associative. Nos solutions :
            </p>
            <ul>
              <li>
                Réduire la densité de soirées pendant l'intégration, pour que chacun·e puisse venir
                à plus de soirées (en proportion).
              </li>
              <li>
                Revaloriser la vie associative auprès de l'administration, en négociant par exemple
                des absences justifiées lors des périodes intenses (intégration, campagne,
                préparation d'évènements…).
              </li>
              <li>
                Proposer un vrai statut pour les pipales et autoriser les 3A à lister en tant que
                membres actifs.
              </li>
            </ul>
          </div>
        </li>

        <li>
          <h2 class="titre">Écriture d'un règlement intérieur</h2>
          <div class="carte">
            <p>
              Pour trancher les détails non prévus par les statuts actuels (modifiés sous
              TIIMELESS), comme les sanctions au niveau de l'AEIIE.
            </p>
          </div>
        </li>

        <li>
          <h2 class="titre">Relance du comité de prévention</h2>
          <div class="carte">
            <p>
              À côté du comité anti-HVSS, externe au BdE, il existait un comité de prévention. On
              s'engage à le remettre sur pied, toujours indépendamment du CA, pour continuer la
              sensibilisation.
            </p>
          </div>
        </li>
      </ol>
    </div>
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

<!-- Police du thème (non scoped : un @import doit être en tête de feuille) -->
<style>
@import url('https://cdn.jsdelivr.net/npm/@fontsource/marcellus-sc@5.3.0/index.css');
</style>

<style scoped>
/* Couleurs reprises des mails FiiReFLY */
.fiirefly {
  --rose: #cb6c89;
  --vert: #27351b;

  font-family: 'Marcellus SC', 'Garamond', serif;
  color: var(--rose);
  background: var(--vert) /* url('/img/main-bg.png')*/;
  padding: 2rem 1rem;
}

.programme {
  list-style: none;
  max-width: 900px;
  margin: 0 auto;
  padding: 0;
  counter-reset: point;
}

.programme > li {
  counter-increment: point;
  text-align: center;
  margin-bottom: 3rem;
}

/* Titre sur le bandeau décoratif (comme les h1 du mail) */
.fiirefly .titre {
  display: inline-block;
  width: 100%;
  max-width: 900px;
  height: 100px;
  line-height: 125px;
  margin: 50px 0 35px;
  padding: 0;
  font-size: 2.25rem;
  font-weight: bold;
  background-image: url('/img/large-header-bg.png') !important;
  background-position: center !important;
  background-size: 100% 100% !important;
  background-repeat: no-repeat !important;
  background-color: transparent !important;
}

/* Bandeaux plus courts pour les titres courts */
.fiirefly .titre.small {
  max-width: 450px;
  background-image: url('/img/small-header-bg.png') !important;
}

.fiirefly .titre.medium {
  max-width: 675px;
  background-image: url('/img/medium-header-bg.png') !important;
}

.titre::before {
  content: counter(point) '. ';
}

/* Cadre de contenu : milieu répété + bords haut et bas */
.carte {
  position: relative;
  padding: 0.5rem 65px;
  text-align: justify;
  font-size: 1.15rem;
  line-height: 1.5;
  background: url('/img/content-mid-bg.png') center top / 100% 50px repeat-y;
}

.carte::before,
.carte::after {
  content: '';
  position: absolute;
  left: 0;
  right: 0;
  height: 25px;
  background-size: 100% 25px;
  background-repeat: no-repeat;
}

.carte::before {
  top: -25px;
  background-image: url('/img/content-top-bg.png');
}

.carte::after {
  bottom: -25px;
  background-image: url('/img/content-bot-bg.png');
}

.carte p {
  margin: 0.5rem 0;
}

.carte ul {
  text-align: left;
  padding-left: 1.5rem;
}

/* Téléphone */
@media (max-width: 600px) {
  .fiirefly .titre {
    font-size: 1.4rem;
    line-height: 110px;
  }

  .carte {
    padding: 0.5rem 1.5rem;
  }
}
</style>
