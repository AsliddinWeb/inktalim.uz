<template>
  <header
    class="fixed top-0 left-0 right-0 z-50 transition-all duration-300"
    :class="scrolled
      ? 'bg-white/80 dark:bg-gray-950/85 backdrop-blur-md border-b border-gray-200/60 dark:border-gray-800/60 shadow-sm'
      : 'bg-transparent'"
  >
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-16">

        <!-- ─── Logo ────────────────────────────────────────────────────── -->
        <RouterLink to="/" class="flex items-center gap-2.5 flex-shrink-0">
          <div class="w-8 h-8 rounded-xl gradient-primary flex items-center justify-center">
            <span class="text-white text-sm font-black">I</span>
          </div>
          <span
            class="text-xl font-black bg-clip-text text-transparent"
            style="background-image: linear-gradient(135deg, #4840B3, #6C63FF, #857EFA)"
          >
            InkTalim.Uz
          </span>
        </RouterLink>

        <!-- ─── Desktop navigatsiya ─────────────────────────────────────── -->
        <nav class="hidden md:flex items-center gap-1">
          <a
            v-for="link in anchorLinks"
            :key="link.href"
            :href="link.href"
            class="px-4 py-2 text-sm font-medium rounded-xl transition-colors"
            :class="scrolled
              ? 'text-gray-600 dark:text-gray-300 hover:text-primary-600 dark:hover:text-primary-400 hover:bg-primary-50 dark:hover:bg-primary-900/20'
              : 'text-gray-700 dark:text-gray-200 hover:text-primary-600 dark:hover:text-primary-400'"
          >
            {{ link.label }}
          </a>
        </nav>

        <!-- ─── O'ng qism ─────────────────────────────────────────────── -->
        <div class="flex items-center gap-2">
          <FontSizeToggle />
          <ThemeToggle />

          <!-- Login bo'lgan user -->
          <template v-if="isAuthenticated">
            <RouterLink
              :to="isAdmin ? '/admin' : '/dashboard'"
              class="hidden sm:flex items-center gap-1.5 px-4 py-2 text-sm font-semibold rounded-xl
                     bg-primary-500 hover:bg-primary-600 text-white transition-colors"
            >
              <LayoutDashboard class="w-4 h-4" />
              Kabinetga o'tish
            </RouterLink>
          </template>

          <!-- Mehmon -->
          <template v-else>
            <RouterLink
              to="/login"
              class="hidden sm:block px-4 py-2 text-sm font-medium rounded-xl transition-colors"
              :class="scrolled
                ? 'text-gray-700 dark:text-gray-300 hover:text-primary-600 dark:hover:text-primary-400 hover:bg-primary-50 dark:hover:bg-primary-900/20'
                : 'text-gray-700 dark:text-gray-200 hover:text-primary-600 dark:hover:text-primary-400'"
            >
              Kirish
            </RouterLink>
            <RouterLink
              to="/register"
              class="hidden sm:block px-4 py-2 text-sm font-semibold rounded-xl
                     bg-primary-500 hover:bg-primary-600 text-white transition-colors shadow-sm"
            >
              Ro'yxatdan o'tish
            </RouterLink>
          </template>

          <!-- Mobil hamburger -->
          <button
            class="md:hidden p-2 rounded-xl transition-colors"
            :class="scrolled
              ? 'text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800'
              : 'text-gray-700 dark:text-gray-200 hover:bg-white/20'"
            @click="mobileOpen = !mobileOpen"
            aria-label="Menyu"
          >
            <X v-if="mobileOpen" class="w-5 h-5" />
            <Menu v-else class="w-5 h-5" />
          </button>
        </div>
      </div>
    </div>

    <!-- ─── Mobil drawer ────────────────────────────────────────────────── -->
    <Transition name="mobile-menu">
      <div
        v-if="mobileOpen"
        class="md:hidden bg-white dark:bg-gray-950 border-t border-gray-200 dark:border-gray-800 px-4 py-4 space-y-1"
      >
        <a
          v-for="link in anchorLinks"
          :key="link.href"
          :href="link.href"
          class="flex items-center gap-2 px-3 py-2.5 text-sm font-medium rounded-xl
                 text-gray-700 dark:text-gray-200 hover:bg-primary-50 dark:hover:bg-primary-900/20
                 hover:text-primary-600 dark:hover:text-primary-400 transition-colors"
          @click="mobileOpen = false"
        >
          {{ link.label }}
        </a>

        <div class="border-t border-gray-200 dark:border-gray-800 pt-3 mt-2 space-y-1">
          <template v-if="isAuthenticated">
            <RouterLink
              :to="isAdmin ? '/admin' : '/dashboard'"
              class="flex items-center gap-2 px-3 py-2.5 text-sm font-semibold rounded-xl
                     bg-primary-500 text-white"
              @click="mobileOpen = false"
            >
              <LayoutDashboard class="w-4 h-4" />
              Kabinetga o'tish
            </RouterLink>
          </template>
          <template v-else>
            <RouterLink
              to="/login"
              class="flex px-3 py-2.5 text-sm font-medium rounded-xl
                     text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-800"
              @click="mobileOpen = false"
            >
              Kirish
            </RouterLink>
            <RouterLink
              to="/register"
              class="flex px-3 py-2.5 text-sm font-semibold rounded-xl
                     bg-primary-500 text-white text-center justify-center"
              @click="mobileOpen = false"
            >
              Ro'yxatdan o'tish
            </RouterLink>
          </template>
        </div>
      </div>
    </Transition>
  </header>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { RouterLink } from 'vue-router'
import { Menu, X, LayoutDashboard } from 'lucide-vue-next'
import ThemeToggle from '@/components/ui/ThemeToggle.vue'
import FontSizeToggle from '@/components/ui/FontSizeToggle.vue'

const scrolled    = ref(false)
const mobileOpen  = ref(false)

// Auth holati — localStorage dan
const isAuthenticated = computed(() => !!localStorage.getItem('edu-access-token'))
const isAdmin = computed(() => {
  const raw = localStorage.getItem('edu-user')
  return raw ? JSON.parse(raw)?.is_admin === true : false
})

const anchorLinks = [
  { href: '#courses',      label: 'Kurslar' },
  { href: '#afzalliklar',  label: 'Afzalliklar' },
  { href: '#haqimizda',    label: 'Haqimizda' },
]

function onScroll() {
  scrolled.value = window.scrollY > 20
}

onMounted(() => window.addEventListener('scroll', onScroll, { passive: true }))
onUnmounted(() => window.removeEventListener('scroll', onScroll))
</script>

<style scoped>
.mobile-menu-enter-active,
.mobile-menu-leave-active {
  transition: all 0.22s ease;
  overflow: hidden;
}
.mobile-menu-enter-from,
.mobile-menu-leave-to {
  opacity: 0;
  max-height: 0;
}
.mobile-menu-enter-to,
.mobile-menu-leave-from {
  opacity: 1;
  max-height: 400px;
}
</style>
