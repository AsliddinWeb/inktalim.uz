<template>
  <section id="stats" class="py-16 bg-gray-50 dark:bg-gray-900/50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">

      <div class="grid grid-cols-2 lg:grid-cols-4 gap-6">
        <div
          v-for="(stat, i) in stats"
          :key="stat.label"
          ref="statRefs"
          :data-index="i"
          class="bg-white dark:bg-gray-900 rounded-2xl p-6 text-center
                 border border-gray-100 dark:border-gray-800
                 shadow-sm hover:shadow-md transition-shadow stat-card"
        >
          <!-- Ikoni -->
          <div
            class="w-12 h-12 rounded-2xl flex items-center justify-center mx-auto mb-4"
            :class="stat.bgClass"
          >
            <span class="text-2xl">{{ stat.emoji }}</span>
          </div>

          <!-- Raqam -->
          <p
            class="text-3xl sm:text-4xl font-black mb-1"
            :class="stat.valueClass"
          >
            {{ stat.animated ? displayValues[i] : stat.value }}
          </p>

          <!-- Tavsif -->
          <p class="text-sm font-medium text-gray-500 dark:text-gray-400">
            {{ stat.label }}
          </p>
        </div>
      </div>

    </div>
  </section>
</template>

<script setup>
import { ref, reactive, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  coursesCount: { type: Number, default: 0 },
})

const stats = [
  {
    emoji:      '📚',
    value:      null,      // API dan
    label:      'Kurslar',
    animated:   true,
    bgClass:    'bg-primary-50 dark:bg-primary-900/20',
    valueClass: 'text-primary-600 dark:text-primary-400',
  },
  {
    emoji:      '👨‍🎓',
    value:      '500+',
    label:      "O'quvchilar",
    animated:   false,
    bgClass:    'bg-blue-50 dark:bg-blue-900/20',
    valueClass: 'text-blue-600 dark:text-blue-400',
  },
  {
    emoji:      '🏆',
    value:      '200+',
    label:      'Sertifikatlar',
    animated:   false,
    bgClass:    'bg-amber-50 dark:bg-amber-900/20',
    valueClass: 'text-amber-500 dark:text-amber-400',
  },
  {
    emoji:      '⭐',
    value:      '100%',
    label:      'Bepul kurslar',
    animated:   false,
    bgClass:    'bg-green-50 dark:bg-green-900/20',
    valueClass: 'text-green-600 dark:text-green-400',
  },
]

// Count-up animatsiya uchun display qiymatlar
const displayValues = reactive(stats.map(() => '0'))

// Intersection Observer — element ko'ringanda animatsiya boshlansin
const statRefs = ref([])
let observer = null
const animated = ref(false)

function countUp(from, to, duration, index) {
  const start = performance.now()
  function step(now) {
    const elapsed = now - start
    const progress = Math.min(elapsed / duration, 1)
    // easeOutCubic
    const eased = 1 - Math.pow(1 - progress, 3)
    displayValues[index] = Math.round(from + (to - from) * eased).toString()
    if (progress < 1) requestAnimationFrame(step)
  }
  requestAnimationFrame(step)
}

function startAnimations() {
  if (animated.value) return
  animated.value = true
  const target = props.coursesCount || 0
  countUp(0, target, 1200, 0)
}

onMounted(() => {
  observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          startAnimations()
          observer?.disconnect()
        }
      })
    },
    { threshold: 0.3 },
  )

  // Birinchi statni kuzat
  const el = document.querySelector('#stats')
  if (el) observer.observe(el)
})

onUnmounted(() => observer?.disconnect())
</script>

<style scoped>
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(20px); }
  to   { opacity: 1; transform: translateY(0); }
}
.stat-card {
  animation: fadeInUp 0.5s ease both;
}
.stat-card:nth-child(1) { animation-delay: 0.05s; }
.stat-card:nth-child(2) { animation-delay: 0.12s; }
.stat-card:nth-child(3) { animation-delay: 0.19s; }
.stat-card:nth-child(4) { animation-delay: 0.26s; }
</style>
