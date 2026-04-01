<template>
  <span :class="badgeClasses">
    <slot />
  </span>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  variant: {
    type: String,
    default: 'gray',
    validator: (v) => ['primary', 'success', 'warning', 'danger', 'gray'].includes(v),
  },
  size: {
    type: String,
    default: 'sm',
    validator: (v) => ['sm', 'md'].includes(v),
  },
})

const variantClasses = {
  primary: 'bg-primary-100 dark:bg-primary-900/30 text-primary-700 dark:text-primary-400',
  success: 'bg-success-100 dark:bg-success-900/20 text-success-700 dark:text-success-400',
  warning: 'bg-secondary-100 dark:bg-secondary-900/20 text-secondary-700 dark:text-secondary-400',
  danger:  'bg-danger-100 dark:bg-danger-900/20 text-danger-700 dark:text-danger-400',
  gray:    'bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400',
}

const badgeClasses = computed(() => [
  'inline-flex items-center gap-1 rounded-full px-3 py-1 text-xs font-semibold',
  variantClasses[props.variant],
])
</script>
