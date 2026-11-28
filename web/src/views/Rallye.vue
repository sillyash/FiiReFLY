<template>
  <PageLayout title="Rallyes">
    <AppCard class="rallye rallye-bouffe">
      <section>
        <h2>Ral'Hibiscus</h2>
        <ul class="bouffes">
          <AppCard
            v-for="categorie in bouffes"
            :key="categorie.label"
            tag="ul"
            class="bouffe-categorie"
          >
            <h3>{{ categorie.label }}</h3>
            <AppCard v-for="bouffe in categorie.items" :key="bouffe.label" tag="li" class="bouffe">
              <div>
                <p>{{ bouffe.label }}</p>
                <small v-if="bouffe.details">{{ bouffe.details }}</small>
              </div>
              <p class="prix">
                {{ bouffe.prix }}
              </p>
            </AppCard>
          </AppCard>
        </ul>
      </section>
    </AppCard>

    <AppCard class="rallye rallye-fun">
      <section>
        <h2>Ra'libellule</h2>
        <ul class="services">
          <AppCard v-for="service in services" :key="service.label" tag="li" class="service">
            <div>
              <p>{{ service.label }}</p>
              <small v-if="service.details">{{ service.details }}</small>
            </div>
            <p class="prix">
              {{ service.prix }}
              <small v-if="service.duree">/{{ service.duree }}</small>
            </p>
          </AppCard>
        </ul>
      </section>

      <section>
        <h2>Paliers</h2>
        <ol class="paliers">
          <li v-for="palier in paliers" :key="palier.montant">
            <strong>{{ palier.montant }}</strong>
            <span>{{ palier.objectif }}</span>
          </li>
        </ol>
      </section>
    </AppCard>
  </PageLayout>
</template>

<script lang="ts">
import AppCard from '@/components/AppCard.vue'
import PageLayout from '@/components/PageLayout.vue'

const services = [
  { label: 'Nettoyage de votre logis, vaisselle, habits', prix: 'Sur place' },
  { label: 'Achat de vos provisions', prix: '1€' },
  { label: 'Entretien de vos plantes', prix: '1€' },
  { label: "Imitation d'une plante chez la victime de votre choix", prix: '0,5€', duree: '10min' },
  {
    label: 'Fable',
    details: 'Cours de botanique, cours sur les lucioles, histoire magique',
    prix: '1€',
  },
  { label: 'Malédiction...', prix: '1€', duree: '10min' },
  { label: 'Vidéo personnalisée de DIDOU', prix: '1,5€' },
  { label: 'Séance de sport à domicile', prix: '1,5€', duree: '30min' },
  { label: 'Clash de la victime de votre choix (gentil)', prix: '2€' },
  { label: 'Piment sur la place publique', prix: '2€' },
]

const bouffes = [
  {
    label: 'Entrées',
    items: [
      {
        label: 'Chakchouka',
        details: 'Tomates, oignons et poivron à la poêle',
        prix: '1€',
      },
      {
        label: 'Salade des bois',
        details: 'Concombres marinés, carottes rapées et chou blanc',
        prix: '0,5€',
      },
    ],
  },
  {
    label: 'Plats',
    items: [
      {
        label: 'Couscous magique',
        details:
          'Pommes de terre, citrouille, pois chiches, carottes, oignon et semoule, le tout avec une sauce tomate et quelques épices',
        prix: '1€',
      },
      {
        label: 'Riz féérique aux PST',
        details: 'Riz, sauce et protéines de soja texturées',
        prix: '1€',
      },
    ],
  },
  {
    label: 'Desserts',
    items: [
      {
        label: 'Pancake de la forêt',
        details: 'Des pancakes complètement vegans',
        prix: '0,5€',
      },
      {
        label: 'Bissap',
        details: "Jus de fleur d'hibiscus avec de la menthe et du sucre",
        prix: '0,8€',
      },
    ],
  },
]

const paliers = [
  { montant: '100€', objectif: 'Drop V1' },
  { montant: '150€', objectif: 'Jeu vidéo de la liste' },
  { montant: '200€', objectif: 'Didou & Tom files leak' },
  { montant: '250€', objectif: 'Vlog nuit aux Coquibus' },
  { montant: '300€', objectif: 'Cover son & image : Adventure of a Lifetime - Coldplay' },
  { montant: '500€', objectif: '????' },
]

export default {
  name: 'RallyeView',
  components: {
    AppCard,
    PageLayout,
  },
  data() {
    return { services, bouffes, paliers }
  },
}
</script>

<style scoped>
.rallye {
  gap: 2rem;
  max-width: 60rem;
  margin: 0 auto 2rem;
}

.rallye-fun {
  display: grid;
  grid-template-columns: 3fr 2fr;
}

.rallye-bouffe {
  display: grid;
  grid-template-columns: 5fr;
}

h2 {
  margin: 0 0 1rem;
  font-size: 1.5rem;
}

ul,
ol {
  margin: 0;
  padding: 0;
  list-style: none;
}

p {
  margin: 0;
}

.bouffe-categorie {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  padding: 0 0.75rem;
}

.services,
.bouffes {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.rallye .service,
.rallye .bouffe {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  padding: 0.75rem 1rem;
  background: var(--color-bg);
}

.prix {
  flex-shrink: 0;
  color: var(--color-accent);
  font-weight: bold;
  text-align: right;
}

.paliers {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  padding-left: 1.25rem;
  border-left: 3px solid var(--color-accent);
}

.paliers li {
  position: relative;
  display: flex;
  flex-direction: column;
}

.paliers li::before {
  content: '';
  position: absolute;
  top: 0.35rem;
  left: calc(-1.25rem - 3px / 2 - 0.4rem);
  width: 0.8rem;
  height: 0.8rem;
  border-radius: 50%;
  background: var(--color-accent);
}

.paliers strong {
  font-size: 1.2rem;
  color: var(--color-accent);
}

/* telephone : les colonnes se suivent */
@media (max-width: 700px) {
  .rallye {
    grid-template-columns: 1fr;
  }
}
</style>
