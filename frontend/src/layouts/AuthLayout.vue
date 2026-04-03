<template>
  <!-- Auth layout — Login va Register uchun -->
  <div class="min-h-screen flex transition-theme">

    <!-- ─── Chap panel — gradient, platforma nomi va tavsifi ─────────────── -->
    <!-- Mobilda yashiriladi -->
    <div class="hidden lg:flex lg:w-1/2 relative overflow-hidden flex-col gradient-primary">

      <!-- SVG grid pattern overlay -->
      <div class="absolute inset-0 opacity-10 pointer-events-none" aria-hidden="true">
        <svg width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
              <path d="M 40 0 L 0 0 0 40" fill="none" stroke="white" stroke-width="1"/>
            </pattern>
          </defs>
          <rect width="100%" height="100%" fill="url(#grid)" />
        </svg>
      </div>

      <!-- Kontent: flex-col, justify-between, h-full -->
      <div class="relative z-10 flex flex-col justify-between p-12 h-full text-white">

        <!-- Yuqori: Logo -->
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-xl bg-white/20 flex items-center justify-center flex-shrink-0">
            <span class="text-white font-black text-lg">E</span>
          </div>
          <span class="text-2xl font-bold tracking-tight">InkTalim.Uz</span>
        </div>

        <!-- O'rta: Sarlavha, tavsif, xususiyatlar -->
        <div>
          <h2 class="text-4xl font-bold leading-tight mb-4">
            O'zbek tilidagi bepul online ta'lim
          </h2>
          <p class="text-lg text-white/80 mb-10">
            Istalgan joyda, istalgan vaqtda o'rganing.
          </p>

          <!-- 3 ta xususiyat -->
          <div class="space-y-4">
            <div
              v-for="feature in features"
              :key="feature"
              class="flex items-center gap-3 text-white/90"
            >
              <div class="w-6 h-6 bg-white/20 rounded-full flex items-center justify-center flex-shrink-0 text-sm">
                <Check class="w-3.5 h-3.5" />
              </div>
              <span class="text-base">{{ feature }}</span>
            </div>
          </div>
        </div>

        <!-- Pastki: Testimonial card -->
        <div class="bg-white/10 backdrop-blur-sm rounded-2xl p-5 border border-white/20">
          <div class="mb-3 text-white/60">
            <svg width="24" height="24" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
              <path d="M14.017 21v-7.391c0-5.704 3.731-9.57 8.983-10.609l.995 2.151c-2.432.917-3.995 3.638-3.995 5.849h4v10h-9.983zm-14.017 0v-7.391c0-5.704 3.748-9.57 9-10.609l.996 2.151c-2.433.917-3.996 3.638-3.996 5.849h3.983v10h-9.983z"/>
            </svg>
          </div>
          <p class="text-white/90 italic text-sm leading-relaxed mb-3">
            "Juda qulay platforma!"
          </p>
          <p class="text-white/60 text-sm font-medium">— Aziz, dasturchi</p>
        </div>
      </div>
    </div>

    <!-- ─── O'ng panel — forma ────────────────────────────────────────────── -->
    <div class="w-full lg:w-1/2 flex flex-col bg-app">

      <!-- Yuqori qism — ThemeToggle -->
      <div class="px-6 py-4 flex justify-end">
        <ThemeToggle />
      </div>

      <!-- Forma wrapper — markazda -->
      <main class="flex-1 flex items-center justify-center px-6 py-8">
        <div class="w-full max-w-md">
          <RouterView />
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { RouterView } from 'vue-router'
import { Check } from 'lucide-vue-next'
import ThemeToggle from '@/components/ui/ThemeToggle.vue'

// Platforma xususiyatlari ro'yxati
const features = [
  'Barcha kurslar to\'liq bepul',
  'Sertifikat bilan tasdiqlanadi',
  'O\'zbek tilida, tushunarli',
]
</script>
