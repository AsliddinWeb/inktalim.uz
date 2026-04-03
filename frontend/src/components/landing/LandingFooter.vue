<template>
  <footer
    id="haqimizda"
    class="py-14"
    style="background: #1E1B4B"
  >
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">

      <!-- ─── Asosiy qator ────────────────────────────────────────────── -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-10 mb-10">

        <!-- Chap: Logo va tavsif -->
        <div class="lg:col-span-2">
          <div class="flex items-center gap-2.5 mb-4">
            <div class="w-9 h-9 rounded-xl gradient-primary flex items-center justify-center">
              <span class="text-white font-black text-sm">I</span>
            </div>
            <span class="text-xl font-black text-white">InkTalim.Uz</span>
          </div>
          <p class="text-sm text-gray-400 leading-relaxed max-w-xs mb-5">
            O'zbekistondagi bepul online ta'lim platformasi.
            Zamonaviy texnologiyalarni o'zbek tilida o'rganing.
          </p>
          <!-- Ijtimoiy ikonlar placeholder -->
          <div class="flex gap-3">
            <a
              v-for="social in socials"
              :key="social.label"
              href="#"
              class="w-9 h-9 rounded-xl flex items-center justify-center text-sm
                     bg-white/10 hover:bg-primary-500 text-gray-400 hover:text-white
                     transition-all duration-200"
              :title="social.label"
            >
              <component :is="social.icon" class="w-4 h-4" />
            </a>
          </div>
        </div>

        <!-- Sahifalar -->
        <div>
          <h4 class="text-sm font-bold text-white uppercase tracking-wider mb-4">Sahifalar</h4>
          <ul class="space-y-2.5">
            <li v-for="link in pageLinks" :key="link.label">
              <component
                :is="link.to ? RouterLink : 'a'"
                :to="link.to"
                :href="link.href"
                class="text-sm text-gray-400 hover:text-primary-400 transition-colors"
              >
                {{ link.label }}
              </component>
            </li>
          </ul>
        </div>

        <!-- Platforma -->
        <div>
          <h4 class="text-sm font-bold text-white uppercase tracking-wider mb-4">Platforma</h4>
          <ul class="space-y-2.5">
            <li v-for="link in platformLinks" :key="link.label">
              <a
                :href="link.href"
                class="text-sm text-gray-400 hover:text-primary-400 transition-colors"
              >
                {{ link.label }}
              </a>
            </li>
          </ul>
        </div>

      </div>

      <!-- ─── Pastki chiziq ───────────────────────────────────────────── -->
      <div class="border-t border-white/10 pt-8 flex flex-col sm:flex-row items-center justify-between gap-3">
        <p class="text-xs text-gray-500 text-center sm:text-left">
          © 2026 InkTalim.Uz. Barcha huquqlar himoyalangan.
        </p>
        <p class="text-xs text-gray-600">
          O'zbek tilidagi bepul ta'lim platformasi
        </p>
      </div>

    </div>
  </footer>
</template>

<script setup>
import { RouterLink } from 'vue-router'
import { Twitter, Send, Youtube, Instagram } from 'lucide-vue-next'

const socials = [
  { label: 'Telegram',  icon: Send },
  { label: 'YouTube',   icon: Youtube },
  { label: 'Instagram', icon: Instagram },
  { label: 'Twitter',   icon: Twitter },
]

const pageLinks = [
  { label: 'Kurslar',           href: '#courses' },
  { label: 'Afzalliklar',       href: '#afzalliklar' },
  { label: 'Kirish',            to: '/login' },
  { label: "Ro'yxatdan o'tish", to: '/register' },
]

const platformLinks = [
  { label: 'Biz haqimizda',  href: '#haqimizda' },
  { label: "Bog'lanish",     href: '#haqimizda' },
  { label: 'Maxfiylik siyosati', href: '#' },
  { label: 'Foydalanish shartlari', href: '#' },
]
</script>
