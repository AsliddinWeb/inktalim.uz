<template>
  <section id="afzalliklar" class="py-20 bg-gray-50 dark:bg-gray-900/60">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">

      <!-- ─── Sarlavha ────────────────────────────────────────────────── -->
      <div class="text-center mb-14 section-header">
        <span class="inline-block px-4 py-1.5 text-xs font-bold uppercase tracking-widest rounded-full mb-4
                     bg-primary-100 dark:bg-primary-900/30 text-primary-700 dark:text-primary-400
                     border border-primary-200 dark:border-primary-800">
          Afzalliklar
        </span>
        <h2 class="text-3xl sm:text-4xl font-black text-gray-900 dark:text-white mb-4">
          Nega aynan InkTalim.Uz?
        </h2>
        <p class="text-gray-500 dark:text-gray-400 max-w-2xl mx-auto leading-relaxed">
          Biz O'zbekistondagi eng qulay va bepul online ta'lim platformasi bo'lishga intilamiz.
          Mana nima uchun bizni tanash kerak.
        </p>
      </div>

      <!-- ─── Features grid ───────────────────────────────────────────── -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        <div
          v-for="(feature, i) in features"
          :key="feature.title"
          class="group relative bg-white dark:bg-gray-900 rounded-2xl p-6
                 border border-gray-100 dark:border-gray-800
                 hover:border-primary-200 dark:hover:border-primary-700/50
                 hover:shadow-[0_8px_32px_rgba(108,99,255,0.12)]
                 hover:-translate-y-1
                 transition-all duration-300 feature-card"
          :style="`animation-delay: ${i * 0.08}s`"
        >
          <!-- Ikon -->
          <div
            class="w-13 h-13 w-12 h-12 rounded-2xl flex items-center justify-center mb-4
                   transition-transform duration-300 group-hover:scale-110"
            :class="feature.bgClass"
          >
            <component :is="feature.icon" class="w-6 h-6" :class="feature.iconClass" />
          </div>

          <!-- Sarlavha -->
          <h3 class="text-base font-bold text-gray-900 dark:text-white mb-2 group-hover:text-primary-600 dark:group-hover:text-primary-400 transition-colors">
            {{ feature.title }}
          </h3>

          <!-- Tavsif -->
          <p class="text-sm text-gray-500 dark:text-gray-400 leading-relaxed">
            {{ feature.description }}
          </p>

          <!-- Hover dekoratsiya -->
          <div
            class="absolute inset-0 rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none"
            style="background: linear-gradient(135deg, rgba(108,99,255,0.04) 0%, transparent 100%)"
          />
        </div>
      </div>

    </div>
  </section>
</template>

<script setup>
import {
  BadgeDollarSign,
  Globe,
  Monitor,
  Award,
  BarChart3,
  FlaskConical,
} from 'lucide-vue-next'

const features = [
  {
    icon:        BadgeDollarSign,
    title:       'Mutlaqo bepul',
    description: "Barcha kurslar to'liq bepul. Hech qanday yashirin to'lov yoki obuna to'lovi yo'q. Ro'yxatdan o'ting va darhol boshlang.",
    bgClass:     'bg-green-100 dark:bg-green-900/20',
    iconClass:   'text-green-600 dark:text-green-400',
  },
  {
    icon:        Globe,
    title:       "O'zbek tilida",
    description: "Barcha darslar va materiallar ona tilimizda. Murakkab tushunchalar oddiy va tushunarli tarzda tushuntiriladi.",
    bgClass:     'bg-blue-100 dark:bg-blue-900/20',
    iconClass:   'text-blue-600 dark:text-blue-400',
  },
  {
    icon:        Monitor,
    title:       "Har qanday qurilmada",
    description: "Telefon, planshet yoki kompyuter — qurilma muhim emas. Platformamiz barcha ekran o'lchamlariga moslashgan.",
    bgClass:     'bg-primary-100 dark:bg-primary-900/20',
    iconClass:   'text-primary-600 dark:text-primary-400',
  },
  {
    icon:        Award,
    title:       'Rasmiy sertifikat',
    description: "Kursni muvaffaqiyatli tugatganingizdan so'ng rasmiy PDF sertifikat olasiz. Sertifikat istalgan qurilmadan yuklab olinadi.",
    bgClass:     'bg-amber-100 dark:bg-amber-900/20',
    iconClass:   'text-amber-500 dark:text-amber-400',
  },
  {
    icon:        BarChart3,
    title:       "Progress kuzatuvi",
    description: "Shaxsiy kabinetingizda o'z rivojlanishingizni kuzatib boring. Qaysi darslarni tugatganingizni ko'ring.",
    bgClass:     'bg-purple-100 dark:bg-purple-900/20',
    iconClass:   'text-purple-600 dark:text-purple-400',
  },
  {
    icon:        FlaskConical,
    title:       "Bilim tekshiruvi",
    description: "Har bir dars oxirida test orqali bilimingizni mustahkamlang. Natijalar darhol ko'rsatiladi va tarix saqlanadi.",
    bgClass:     'bg-rose-100 dark:bg-rose-900/20',
    iconClass:   'text-rose-600 dark:text-rose-400',
  },
]
</script>

<style scoped>
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(24px); }
  to   { opacity: 1; transform: translateY(0); }
}
.section-header {
  animation: fadeInUp 0.6s ease both;
}
.feature-card {
  animation: fadeInUp 0.55s ease both;
}
</style>
