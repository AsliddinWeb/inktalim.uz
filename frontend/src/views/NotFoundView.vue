<template>
  <!-- 404 — Sahifa topilmadi -->
  <div class="min-h-screen bg-app flex items-center justify-center p-6 transition-theme">
    <div class="text-center max-w-md">
      <!-- Raqam -->
      <div class="relative mb-8">
        <p class="text-9xl font-black text-primary-100 dark:text-primary-900/40 select-none">
          404
        </p>
        <div class="absolute inset-0 flex items-center justify-center">
          <span class="text-6xl">🔍</span>
        </div>
      </div>

      <h1 class="text-2xl font-bold text-app-primary mb-3">
        Sahifa topilmadi
      </h1>
      <p class="text-app-secondary text-sm mb-8 leading-relaxed">
        Siz izlayotgan sahifa mavjud emas yoki o'chirib yuborilgan.
        Bosh sahifaga qaytishingiz mumkin.
      </p>

      <div class="flex flex-col sm:flex-row gap-3 justify-center">
        <AppButton
          variant="primary"
          size="lg"
          :icon-left="Home"
          @click="goHome"
        >
          Bosh sahifaga qaytish
        </AppButton>
        <AppButton
          variant="ghost"
          size="lg"
          :icon-left="ArrowLeft"
          @click="$router.back()"
        >
          Orqaga
        </AppButton>
      </div>
    </div>
  </div>
</template>

<script setup>
import { Home, ArrowLeft } from 'lucide-vue-next'
import { useRouter } from 'vue-router'
import AppButton from '@/components/ui/AppButton.vue'
import { useAuthStore } from '@/stores/auth.js'

const router = useRouter()
const authStore = useAuthStore()

function goHome() {
  if (authStore.isAuthenticated) {
    router.push(authStore.isAdmin ? '/admin' : '/dashboard')
  } else {
    router.push('/login')
  }
}
</script>
