<template>
  <component
    :is="tag || 'div'"
    :class="cardClasses"
    v-bind="$attrs"
  >
    <!-- Karta sarlavhasi (ixtiyoriy) -->
    <div
      v-if="title || $slots.header"
      class="flex items-center justify-between mb-4"
      :class="{ 'pb-4 border-b border-gray-100 dark:border-gray-800': divider }"
    >
      <h3 v-if="title" class="text-base font-semibold text-gray-900 dark:text-white">
        {{ title }}
      </h3>
      <slot name="header" />
    </div>

    <!-- Asosiy kontent -->
    <slot />

    <!-- Karta footer (ixtiyoriy) -->
    <div
      v-if="$slots.footer"
      class="mt-4 pt-4 border-t border-gray-100 dark:border-gray-800"
    >
      <slot name="footer" />
    </div>
  </component>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  // HTML tag (div, article, section, ...)
  tag: {
    type: String,
    default: 'div',
  },
  // Karta sarlavhasi
  title: {
    type: String,
    default: '',
  },
  // Padding o'lchami
  padding: {
    type: String,
    default: 'md',
    validator: (v) => ['none', 'sm', 'md', 'lg'].includes(v),
  },
  // Hover effekti
  hover: {
    type: Boolean,
    default: false,
  },
  // Glass effect
  glass: {
    type: Boolean,
    default: false,
  },
  // Sarlavha va kontentni ajratuvchi chiziq
  divider: {
    type: Boolean,
    default: false,
  },
  // Chegara
  bordered: {
    type: Boolean,
    default: true,
  },
})

const paddingClasses = {
  none: '',
  sm:   'p-3',
  md:   'p-5',
  lg:   'p-7',
}

const cardClasses = computed(() => [
  'rounded-2xl bg-white dark:bg-surface shadow-sm',
  props.bordered ? 'border border-gray-100 dark:border-gray-800' : '',
  paddingClasses[props.padding],
  props.hover
    ? 'hover:shadow-md hover:-translate-y-1 transition-all duration-300 cursor-pointer'
    : '',
  props.glass
    ? '!bg-white/70 dark:!bg-gray-900/70 backdrop-blur-md border-white/20 dark:border-gray-700/50'
    : '',
])
</script>
