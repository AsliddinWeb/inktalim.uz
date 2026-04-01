<template>
  <div class="flex h-screen overflow-hidden bg-gray-50 dark:bg-gray-950">

    <!-- Mobil Overlay -->
    <Transition name="fade">
      <div
        v-if="sidebarOpen"
        class="fixed inset-0 bg-black/50 z-20 lg:hidden"
        @click="sidebarOpen = false"
      />
    </Transition>

    <!-- ─── Sidebar ─────────────────────────────────────────────────────── -->
    <aside
      class="fixed top-0 left-0 h-full w-60 z-30 flex flex-col
             bg-white dark:bg-gray-900
             border-r border-gray-200 dark:border-gray-800
             transition-transform duration-300 ease-in-out
             lg:translate-x-0 lg:static lg:z-auto"
      :class="sidebarOpen ? 'translate-x-0' : '-translate-x-full'"
    >
      <!-- Logo -->
      <div class="flex items-center gap-3 px-5 h-16 border-b border-gray-200 dark:border-gray-800 flex-shrink-0">
        <RouterLink to="/dashboard" class="flex items-center gap-3 flex-1 min-w-0">
          <div
            class="w-8 h-8 rounded-xl flex items-center justify-center flex-shrink-0"
            style="background: linear-gradient(135deg, #4840B3, #6C63FF, #857EFA)"
          >
            <span class="text-white font-black text-sm leading-none">E</span>
          </div>
          <span
            class="text-base font-black bg-clip-text text-transparent"
            style="background-image: linear-gradient(135deg, #4840B3, #6C63FF, #857EFA); -webkit-background-clip: text;"
          >
            EduUz
          </span>
        </RouterLink>
      </div>

      <!-- Nav -->
      <nav class="flex-1 overflow-y-auto px-3 py-4 space-y-0.5">
        <RouterLink
          v-for="item in navItems"
          :key="item.name"
          :to="item.to"
          class="flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium
                 text-gray-600 dark:text-gray-400
                 hover:bg-gray-100 dark:hover:bg-gray-800
                 hover:text-gray-900 dark:hover:text-white
                 transition-colors duration-150"
          active-class="!bg-primary-50 dark:!bg-primary-900/20 !text-primary-700 dark:!text-primary-400"
          @click="sidebarOpen = false"
        >
          <component :is="item.icon" class="w-5 h-5 flex-shrink-0" />
          <span>{{ item.label }}</span>
        </RouterLink>
      </nav>

      <!-- Bottom -->
      <div class="flex-shrink-0 border-t border-gray-200 dark:border-gray-800 p-3 space-y-1">
        <div class="flex items-center gap-3 px-3 py-2.5 rounded-xl bg-gray-50 dark:bg-gray-800">
          <AppAvatar size="sm" :name="authStore.user?.full_name" />
          <div class="flex-1 min-w-0">
            <p class="text-sm font-semibold text-gray-900 dark:text-white truncate">
              {{ authStore.user?.full_name }}
            </p>
            <p class="text-xs text-gray-400">O'quvchi</p>
          </div>
        </div>
        <button
          class="flex items-center gap-3 w-full px-3 py-2.5 rounded-xl text-sm
                 text-gray-500 dark:text-gray-400
                 hover:bg-red-50 dark:hover:bg-red-900/20
                 hover:text-red-500 dark:hover:text-red-400
                 transition-colors"
          @click="handleLogout"
        >
          <LogOut class="w-4 h-4 flex-shrink-0" />
          <span>Chiqish</span>
        </button>
      </div>
    </aside>

    <!-- ─── Main ─────────────────────────────────────────────────────────── -->
    <div class="flex-1 flex flex-col min-w-0 overflow-hidden">

      <!-- Header -->
      <header
        class="h-16 flex items-center gap-3 px-4 sm:px-6 flex-shrink-0 sticky top-0 z-10
               bg-white/80 dark:bg-gray-900/80 backdrop-blur-md
               border-b border-gray-200 dark:border-gray-800"
      >
        <button
          class="lg:hidden p-2 rounded-lg text-gray-500
                 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
          aria-label="Menyu"
          @click="sidebarOpen = true"
        >
          <Menu class="w-5 h-5" />
        </button>

        <h1 class="flex-1 text-sm font-semibold text-gray-900 dark:text-white truncate">
          {{ currentPageTitle }}
        </h1>

        <div class="flex items-center gap-2">
          <ThemeToggle />

          <!-- User dropdown -->
          <div class="relative" ref="dropdownRef">
            <button
              class="flex items-center gap-2 pl-1 pr-2 py-1 rounded-xl
                     hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
              @click="dropdownOpen = !dropdownOpen"
            >
              <AppAvatar size="sm" :name="authStore.user?.full_name" />
              <ChevronDown
                class="w-3.5 h-3.5 text-gray-400 transition-transform duration-200"
                :class="dropdownOpen ? 'rotate-180' : ''"
              />
            </button>

            <!-- Dropdown menu -->
            <Transition name="dropdown">
              <div
                v-if="dropdownOpen"
                class="absolute right-0 top-full mt-2 w-56 rounded-2xl
                       bg-white dark:bg-gray-900
                       border border-gray-200 dark:border-gray-800
                       shadow-xl shadow-black/10
                       py-1.5 z-50"
              >
                <!-- User info -->
                <div class="px-4 py-3 border-b border-gray-100 dark:border-gray-800">
                  <p class="text-sm font-semibold text-gray-900 dark:text-white truncate">
                    {{ authStore.user?.full_name }}
                  </p>
                  <p class="text-xs text-gray-400 truncate mt-0.5">
                    {{ authStore.user?.email }}
                  </p>
                </div>

                <!-- Links -->
                <div class="py-1">
                  <RouterLink
                    v-for="item in dropdownLinks"
                    :key="item.to"
                    :to="item.to"
                    class="flex items-center gap-3 px-4 py-2 text-sm text-gray-700 dark:text-gray-300
                           hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors"
                    @click="dropdownOpen = false"
                  >
                    <component :is="item.icon" class="w-4 h-4 text-gray-400 flex-shrink-0" />
                    {{ item.label }}
                  </RouterLink>
                </div>

                <!-- Logout -->
                <div class="border-t border-gray-100 dark:border-gray-800 pt-1 mt-1">
                  <button
                    class="flex items-center gap-3 w-full px-4 py-2 text-sm text-red-500
                           hover:bg-red-50 dark:hover:bg-red-900/20 transition-colors"
                    @click="handleLogout"
                  >
                    <LogOut class="w-4 h-4 flex-shrink-0" />
                    Chiqish
                  </button>
                </div>
              </div>
            </Transition>
          </div>
        </div>
      </header>

      <!-- Content -->
      <main class="flex-1 overflow-y-auto">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 lg:py-8">
          <RouterView />
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { RouterLink, RouterView, useRoute, useRouter } from 'vue-router'
import {
  Award,
  LayoutDashboard,
  BookOpen,
  TrendingUp,
  User,
  LogOut,
  Menu,
  ChevronDown,
} from 'lucide-vue-next'
import ThemeToggle from '@/components/ui/ThemeToggle.vue'
import AppAvatar from '@/components/ui/AppAvatar.vue'
import { useAuthStore } from '@/stores/auth.js'

const authStore = useAuthStore()
const route = useRoute()
const router = useRouter()

const sidebarOpen = ref(false)
const dropdownOpen = ref(false)
const dropdownRef  = ref(null)

const userInitial = computed(() =>
  authStore.user?.full_name?.charAt(0)?.toUpperCase() || 'U'
)

const pageTitles = {
  StudentDashboard:    'Bosh sahifa',
  StudentCourses:      'Kurslar',
  lesson:              'Dars',
  quiz:                'Test',
  StudentProgress:     'Mening progressim',
  StudentProfile:      'Profilim',
  StudentCertificates: 'Sertifikatlarim',
  StudentCertificate:  'Sertifikat',
}
const currentPageTitle = computed(() =>
  pageTitles[route.name] || 'EduUz'
)

const navItems = [
  { name: 'StudentDashboard',    to: '/dashboard',               label: 'Bosh sahifa',     icon: LayoutDashboard },
  { name: 'StudentCourses',      to: '/dashboard/courses',       label: 'Kurslar',         icon: BookOpen },
  { name: 'StudentProgress',     to: '/dashboard/progress',      label: 'Progressim',      icon: TrendingUp },
  { name: 'StudentCertificates', to: '/dashboard/certificates',  label: 'Sertifikatlarim', icon: Award },
  { name: 'StudentProfile',      to: '/dashboard/profile',       label: 'Profilim',        icon: User },
]

const dropdownLinks = [
  { to: '/dashboard/profile',      label: 'Profilim',        icon: User },
  { to: '/dashboard/progress',     label: 'Progressim',      icon: TrendingUp },
  { to: '/dashboard/certificates', label: 'Sertifikatlarim', icon: Award },
]

function onClickOutside(e) {
  if (dropdownRef.value && !dropdownRef.value.contains(e.target)) {
    dropdownOpen.value = false
  }
}
onMounted(() => document.addEventListener('mousedown', onClickOutside))
onUnmounted(() => document.removeEventListener('mousedown', onClickOutside))

async function handleLogout() {
  dropdownOpen.value = false
  await authStore.logout()
}
</script>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity 0.25s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

.dropdown-enter-active { transition: all 0.15s ease; }
.dropdown-leave-active { transition: all 0.1s ease; }
.dropdown-enter-from, .dropdown-leave-to { opacity: 0; transform: translateY(-6px) scale(0.97); }
</style>
