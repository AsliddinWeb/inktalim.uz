<template>
  <div class="rounded-2xl border border-gray-100 dark:border-gray-800 bg-white dark:bg-surface p-5 flex items-center gap-4">
    <div
      class="flex-shrink-0 w-12 h-12 rounded-2xl flex items-center justify-center"
      :class="iconBg"
    >
      <component :is="icon" class="w-6 h-6" :class="iconColor" />
    </div>
    <div class="min-w-0">
      <p class="text-sm text-gray-500 dark:text-gray-400 truncate">{{ label }}</p>
      <p class="text-2xl font-bold text-gray-900 dark:text-white leading-tight">
        <span v-if="loading" class="inline-block w-12 h-6 bg-gray-200 dark:bg-gray-700 rounded animate-pulse" />
        <template v-else>{{ value }}</template>
      </p>
      <p v-if="sub" class="text-xs text-gray-500 dark:text-gray-400 mt-0.5 truncate">{{ sub }}</p>
    </div>
  </div>
</template>

<script setup>
import AppCard from '@/components/ui/AppCard.vue'

defineProps({
  icon: { type: Object, required: true },   // Lucide component
  label: { type: String, required: true },
  value: { type: [String, Number], default: 0 },
  sub: { type: String, default: '' },
  loading: { type: Boolean, default: false },
  iconBg: { type: String, default: 'bg-primary/10' },
  iconColor: { type: String, default: 'text-primary' },
})
</script>
