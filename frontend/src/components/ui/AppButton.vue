<template>
  <button
    :type="type"
    :disabled="disabled || loading"
    :class="buttonClasses"
    v-bind="$attrs"
  >
    <!-- Yuklash spinneri -->
    <svg
      v-if="loading"
      class="animate-spin w-4 h-4 flex-shrink-0"
      viewBox="0 0 24 24"
      fill="none"
    >
      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
    </svg>

    <!-- Chap ikon -->
    <component
      v-if="iconLeft && !loading"
      :is="iconLeft"
      class="flex-shrink-0"
      :class="iconSizeClass"
    />

    <!-- Matn -->
    <span v-if="$slots.default && !loading"><slot /></span>

    <!-- O'ng ikon -->
    <component
      v-if="iconRight && !loading"
      :is="iconRight"
      class="flex-shrink-0"
      :class="iconSizeClass"
    />
  </button>
</template>

<script setup>
import { computed } from 'vue'

// Props ta'rifi
const props = defineProps({
  // Tugma varianti
  variant: {
    type: String,
    default: 'primary',
    validator: (v) => ['primary', 'secondary', 'danger', 'ghost', 'outline'].includes(v),
  },
  // Tugma o'lchami
  size: {
    type: String,
    default: 'md',
    validator: (v) => ['sm', 'md', 'lg'].includes(v),
  },
  // Yuklash holati
  loading: {
    type: Boolean,
    default: false,
  },
  // O'chirilgan holat
  disabled: {
    type: Boolean,
    default: false,
  },
  // Kenglikni to'ldirsin
  fullWidth: {
    type: Boolean,
    default: false,
  },
  // Tugma turi
  type: {
    type: String,
    default: 'button',
  },
  // Lucide ikonlar
  iconLeft: {
    type: [Object, Function],
    default: null,
  },
  iconRight: {
    type: [Object, Function],
    default: null,
  },
})

// O'lchamga qarab ikon hajmi
const iconSizeClass = computed(() => ({
  sm: 'w-3.5 h-3.5',
  md: 'w-4 h-4',
  lg: 'w-5 h-5',
}[props.size]))

// Tugma klasslarini hisoblash
const buttonClasses = computed(() => {
  const base = [
    'inline-flex items-center justify-center gap-2',
    'font-medium leading-none',
    'rounded-xl',
    'select-none',
    props.fullWidth ? 'w-full' : '',
    (props.disabled || props.loading) ? 'opacity-50 cursor-not-allowed pointer-events-none' : 'cursor-pointer',
  ]

  // O'lcham klasslari
  const sizes = {
    sm: 'px-4 py-1.5 text-sm',
    md: 'px-6 py-2.5 text-sm',
    lg: 'px-8 py-3 text-base',
  }

  // Variant klasslari
  const variants = {
    primary: [
      'bg-primary-500 text-white',
      'hover:bg-primary-600 active:translate-y-0',
      'transition-all duration-200',
      'shadow-sm hover:shadow-md hover:-translate-y-0.5',
    ].join(' '),
    secondary: [
      'bg-secondary-500/10 text-secondary-600 dark:text-secondary-400',
      'hover:bg-secondary-500/20',
      'transition-all duration-200',
      'rounded-xl font-medium',
    ].join(' '),
    danger: [
      'bg-danger-500 text-white',
      'hover:bg-danger-600 active:translate-y-0',
      'transition-all duration-200',
      'shadow-sm hover:shadow-md hover:-translate-y-0.5',
    ].join(' '),
    ghost: [
      'text-gray-700 dark:text-gray-300',
      'hover:bg-gray-100 dark:hover:bg-gray-800',
      'transition-colors duration-200',
    ].join(' '),
    outline: [
      'bg-transparent border-2 border-primary-500 text-primary-600',
      'hover:bg-primary-50 active:bg-primary-100',
      'dark:text-primary-400 dark:border-primary-400',
      'dark:hover:bg-primary-900/30',
      'transition-all duration-200',
    ].join(' '),
  }

  return [...base, sizes[props.size], variants[props.variant]].filter(Boolean).join(' ')
})
</script>
