// Vue ilovasini ishga tushirish — Pinia, Router, global komponentlar
import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router/index.js'

// Asosiy CSS (Tailwind + CSS o'zgaruvchilar)
import './assets/main.css'

// Ilovani yaratish
const app = createApp(App)

// Pinia state management
app.use(createPinia())

// Vue Router
app.use(router)

// Ilovani DOM ga ulash
app.mount('#app')
