import { createApp } from 'vue'
import { createPinia } from 'pinia'

import '@/assets/main.css'
import App from '@/App.vue'
import router from '@/router'
import { useAuthStore } from '@/stores/auth'

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')

// apres la 1ere navigation : si c'est un retour de login (#/connexion), le token est deja la
router.isReady().then(() => useAuthStore().fetchMe())
