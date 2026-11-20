import { createRouter, createWebHashHistory } from 'vue-router'

import Home from '@/views/Home.vue'
import Soirees from '@/views/Soirees.vue'
import LivreDor from '@/views/LivreDor.vue'
import Membres from '@/views/Membres.vue'
import Programme from '@/views/Programme.vue'
import Partenariats from '@/views/Partenariats.vue'
import Rallye from '@/views/Rallye.vue'
import { useAuthStore } from '@/stores/auth'

// meme regle que safe_next cote API : un chemin du front, jamais un autre host
function safeNext(value: unknown): string {
  return typeof value === 'string' && value.startsWith('/') && !value.startsWith('//') ? value : '/'
}

const router = createRouter({
  history: createWebHashHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'home', component: Home },
    { path: '/programme', name: 'programme', component: Programme },
    { path: '/soirees', name: 'soirees', component: Soirees },
    { path: '/livre-dor', name: 'livre-dor', component: LivreDor },
    { path: '/membres', name: 'membres', component: Membres },
    { path: '/partenariats', name: 'partenariats', component: Partenariats },
    { path: '/rallye', name: 'rallye', component: Rallye },
    // retour du login Arise (#/connexion?code=...&next=...), jamais affichee
    {
      path: '/connexion',
      name: 'connexion',
      component: Home,
      beforeEnter: async (to) => {
        if (typeof to.query.code === 'string') {
          await useAuthStore().exchange(to.query.code)
        }
        return { path: safeNext(to.query.next), replace: true }
      },
    },
  ],
})

export default router
