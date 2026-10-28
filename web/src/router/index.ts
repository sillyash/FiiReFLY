import { createRouter, createWebHashHistory } from 'vue-router'

import Home from '@/views/Home.vue'
import Soirees from '@/views/Soirees.vue'
import LivreDor from '@/views/LivreDor.vue'

const router = createRouter({
  history: createWebHashHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'home', component: Home },
    { path: '/soirees', name: 'soirees', component: Soirees },
    { path: '/livre-dor', name: 'livre-dor', component: LivreDor },
  ],
})

export default router
