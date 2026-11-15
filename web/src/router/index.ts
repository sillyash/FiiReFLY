import { createRouter, createWebHashHistory } from 'vue-router'

import Home from '@/views/Home.vue'
import Soirees from '@/views/Soirees.vue'
import LivreDor from '@/views/LivreDor.vue'
import Membres from '@/views/Membres.vue'
import Programme from '@/views/Programme.vue'

const router = createRouter({
  history: createWebHashHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'home', component: Home },
    { path: '/programme', name: 'programme', component: Programme },
    { path: '/soirees', name: 'soirees', component: Soirees },
    { path: '/livre-dor', name: 'livre-dor', component: LivreDor },
    { path: '/membres', name: 'membres', component: Membres },
  ],
})

export default router
