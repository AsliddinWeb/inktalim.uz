// Vite konfiguratsiyasi — Vue3 + Tailwind uchun
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath, URL } from 'node:url'

export default defineConfig({
  plugins: [vue()],

  // @ alias — src papkasiga qisqa yo'l
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },

  // Dev server sozlamalari
  server: {
    host: '0.0.0.0',
    port: 5173,
    // Backend API ga proxy (Docker ichida)
    proxy: {
      '/api': {
        target: 'http://backend:8000',
        changeOrigin: true,
      },
    },
  },
})
