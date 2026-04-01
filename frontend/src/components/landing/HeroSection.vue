<template>
  <section
    class="relative min-h-screen flex items-center overflow-hidden pt-16"
    style="background: linear-gradient(160deg, #F0EFFE 0%, #E0E7FF 40%, #F8F7FF 100%)"
  >
    <!-- Dark mode foni -->
    <div
      class="absolute inset-0 hidden dark:block"
      style="background: linear-gradient(160deg, #0F0E17 0%, #0F1A2B 50%, #0D1117 100%)"
    />

    <!-- ─── Dekorativ blur doiralar ──────────────────────────────────────── -->
    <div
      class="absolute top-24 left-8 w-72 h-72 rounded-full opacity-20 dark:opacity-10 pointer-events-none"
      style="background: radial-gradient(circle, #6C63FF, transparent 70%); filter: blur(48px)"
    />
    <div
      class="absolute bottom-16 right-8 w-96 h-96 rounded-full opacity-15 dark:opacity-10 pointer-events-none"
      style="background: radial-gradient(circle, #857EFA, transparent 70%); filter: blur(64px)"
    />
    <div
      class="absolute top-1/2 left-1/3 w-48 h-48 rounded-full opacity-10 dark:opacity-5 pointer-events-none"
      style="background: radial-gradient(circle, #F59E0B, transparent 70%); filter: blur(40px)"
    />

    <div class="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 w-full py-20">
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-12 lg:gap-20 items-center">

        <!-- ─── Chap: matn ────────────────────────────────────────────── -->
        <div class="text-center lg:text-left animate-hero-in">

          <!-- Badge -->
          <div class="inline-flex items-center gap-2 px-4 py-2 rounded-full text-sm font-semibold mb-6
                      bg-primary-100 dark:bg-primary-900/30 text-primary-700 dark:text-primary-400
                      border border-primary-200 dark:border-primary-800">
            🎓 Bepul online ta'lim
          </div>

          <!-- Asosiy sarlavha -->
          <h1 class="text-4xl sm:text-5xl lg:text-6xl font-black leading-tight mb-6">
            <span class="text-gray-900 dark:text-white">Bilimingizni</span><br>
            <span class="text-gray-900 dark:text-white">oshiring,</span><br>
            <span
              class="bg-clip-text text-transparent"
              style="background-image: linear-gradient(135deg, #4840B3 0%, #6C63FF 50%, #857EFA 100%)"
            >
              o'z sur'atingizda
            </span>
          </h1>

          <!-- Tavsif -->
          <p class="text-lg text-gray-600 dark:text-gray-300 leading-relaxed mb-8 max-w-lg mx-auto lg:mx-0">
            EduUz — O'zbek tilidagi bepul kurslar platformasi.
            Istalgan joydan, istalgan vaqtda o'qing.
          </p>

          <!-- CTA tugmalar -->
          <div class="flex flex-col sm:flex-row gap-3 justify-center lg:justify-start mb-10">
            <RouterLink
              to="/register"
              class="flex items-center justify-center gap-2 px-7 py-3.5 text-base font-bold rounded-2xl
                     bg-primary-500 hover:bg-primary-600 text-white transition-all
                     shadow-[0_4px_20px_rgba(108,99,255,0.35)] hover:shadow-[0_6px_28px_rgba(108,99,255,0.5)]
                     hover:-translate-y-0.5"
            >
              <span>Bepul boshlash</span>
              <ArrowRight class="w-5 h-5" />
            </RouterLink>
            <a
              href="#courses"
              class="flex items-center justify-center gap-2 px-7 py-3.5 text-base font-semibold rounded-2xl
                     border border-gray-300 dark:border-gray-600
                     text-gray-700 dark:text-gray-200
                     hover:border-primary-400 dark:hover:border-primary-500
                     hover:text-primary-600 dark:hover:text-primary-400
                     transition-all hover:-translate-y-0.5"
            >
              <BookOpen class="w-5 h-5" />
              Kurslarni ko'rish
            </a>
          </div>

          <!-- Kichik inline statslar -->
          <div class="flex flex-wrap items-center gap-x-6 gap-y-3 justify-center lg:justify-start">
            <div
              v-for="stat in inlineStats"
              :key="stat.label"
              class="flex items-center gap-2 text-sm text-gray-600 dark:text-gray-400"
            >
              <div class="w-5 h-5 rounded-full bg-primary-100 dark:bg-primary-900/40 flex items-center justify-center">
                <component :is="stat.icon" class="w-3 h-3 text-primary-600 dark:text-primary-400" />
              </div>
              <span class="font-medium">{{ stat.label }}</span>
              <span class="text-gray-300 dark:text-gray-700">|</span>
            </div>
          </div>
        </div>

        <!-- ─── O'ng: dekorativ illustration ──────────────────────────── -->
        <div class="hidden lg:flex items-center justify-center animate-hero-in-right">
          <div class="relative w-full max-w-md">

            <!-- Asosiy karta -->
            <div
              class="relative rounded-3xl p-8 shadow-2xl overflow-hidden"
              style="background: linear-gradient(135deg, #1C1A3E 0%, #0F0E17 100%); border: 1px solid rgba(108,99,255,0.3)"
            >
              <!-- Mini dekoratsiya -->
              <div
                class="absolute -top-10 -right-10 w-32 h-32 rounded-full opacity-20"
                style="background: radial-gradient(circle, #6C63FF, transparent)"
              />

              <!-- Platform logo katta -->
              <div class="flex items-center gap-3 mb-6">
                <div class="w-12 h-12 rounded-2xl gradient-primary flex items-center justify-center">
                  <span class="text-white text-xl font-black">E</span>
                </div>
                <div>
                  <p class="text-white font-bold text-lg">EduUz</p>
                  <p class="text-gray-400 text-xs">Online Ta'lim</p>
                </div>
              </div>

              <!-- Kurs progress SVG -->
              <div class="space-y-4 mb-6">
                <div
                  v-for="(item, i) in demoProgress"
                  :key="i"
                  class="bg-white/5 rounded-2xl p-4"
                >
                  <div class="flex items-center justify-between mb-2">
                    <div class="flex items-center gap-2">
                      <div
                        class="w-8 h-8 rounded-xl flex items-center justify-center text-sm"
                        :style="`background: ${item.color}22`"
                      >
                        {{ item.emoji }}
                      </div>
                      <span class="text-white text-sm font-medium">{{ item.title }}</span>
                    </div>
                    <span class="text-xs font-bold" :style="`color: ${item.color}`">
                      {{ item.percent }}%
                    </span>
                  </div>
                  <div class="h-1.5 bg-white/10 rounded-full overflow-hidden">
                    <div
                      class="h-full rounded-full transition-all"
                      :style="`width: ${item.percent}%; background: ${item.color}`"
                    />
                  </div>
                </div>
              </div>

              <!-- Sertifikat mini -->
              <div
                class="flex items-center gap-3 rounded-2xl p-3"
                style="background: rgba(245,158,11,0.1); border: 1px solid rgba(245,158,11,0.2)"
              >
                <div class="w-9 h-9 rounded-xl bg-amber-500/20 flex items-center justify-center flex-shrink-0">
                  <Award class="w-5 h-5 text-amber-400" />
                </div>
                <div>
                  <p class="text-amber-300 text-xs font-semibold">Sertifikat olindi!</p>
                  <p class="text-gray-400 text-xs">Vue.js kursi — EDUUZ-2024-AB3X9</p>
                </div>
              </div>
            </div>

            <!-- Suzuvchi badge — yuqori o'ng -->
            <div
              class="absolute -top-4 -right-4 bg-white dark:bg-gray-800 rounded-2xl px-4 py-2.5 shadow-xl
                     border border-gray-100 dark:border-gray-700 flex items-center gap-2"
            >
              <div class="w-2.5 h-2.5 rounded-full bg-green-400 animate-pulse" />
              <span class="text-sm font-semibold text-gray-700 dark:text-gray-200">500+ o'quvchi</span>
            </div>

            <!-- Suzuvchi badge — pastki chap -->
            <div
              class="absolute -bottom-4 -left-4 bg-white dark:bg-gray-800 rounded-2xl px-4 py-2.5 shadow-xl
                     border border-gray-100 dark:border-gray-700 flex items-center gap-2"
            >
              <span class="text-lg">🏆</span>
              <span class="text-sm font-semibold text-gray-700 dark:text-gray-200">100% Bepul</span>
            </div>
          </div>
        </div>

      </div>
    </div>

    <!-- Pastki to'lqin SVG -->
    <div class="absolute bottom-0 left-0 right-0">
      <svg viewBox="0 0 1440 60" fill="none" xmlns="http://www.w3.org/2000/svg" class="w-full">
        <path
          d="M0 60L48 50C96 40 192 20 288 15C384 10 480 20 576 25C672 30 768 30 864 25C960 20 1056 10 1152 10C1248 10 1344 20 1392 25L1440 30V60H0Z"
          class="fill-gray-50 dark:fill-gray-950"
        />
      </svg>
    </div>
  </section>
</template>

<script setup>
import { RouterLink } from 'vue-router'
import { ArrowRight, BookOpen, Award, CheckCircle, Globe, Star } from 'lucide-vue-next'

const inlineStats = [
  { label: '100% Bepul',    icon: CheckCircle },
  { label: "O'zbek tilida", icon: Globe },
  { label: 'Sertifikat bilan', icon: Star },
]

const demoProgress = [
  { emoji: '🖥️', title: 'Vue.js asoslari',    percent: 100, color: '#14B8A6' },
  { emoji: '⚙️', title: 'Python dasturlash',  percent: 65,  color: '#06B6D4' },
  { emoji: '📱', title: 'Django Framework',   percent: 30,  color: '#F59E0B' },
]
</script>

<style scoped>
@keyframes heroIn {
  from { opacity: 0; transform: translateY(24px); }
  to   { opacity: 1; transform: translateY(0); }
}
@keyframes heroInRight {
  from { opacity: 0; transform: translateX(32px); }
  to   { opacity: 1; transform: translateX(0); }
}
.animate-hero-in {
  animation: heroIn 0.7s ease both;
}
.animate-hero-in-right {
  animation: heroInRight 0.7s 0.15s ease both;
}
</style>
