<template>
  <Transition name="alert">
    <div v-if="visible" :class="alertClasses" role="alert">
      <!-- Ikon -->
      <component :is="iconComponent" class="size-5 flex-shrink-0 mt-0.5" />

      <!-- Matn -->
      <div class="flex-1">
        <p v-if="title" class="font-semibold text-sm">{{ title }}</p>
        <div class="text-sm" :class="title ? 'mt-0.5' : ''">
          <slot />
        </div>
      </div>

      <!-- Yopish tugmasi -->
      <button
        v-if="dismissible"
        type="button"
        class="ml-auto -mt-0.5 w-6 h-6 rounded-lg hover:bg-black/10 dark:hover:bg-white/10 flex items-center justify-center transition-colors flex-shrink-0"
        aria-label="Yopish"
        @click="visible = false"
      >
        <X class="size-3.5" />
      </button>
    </div>
  </Transition>
</template>

<script setup>
import { ref, computed } from 'vue'
import {
  CheckCircle,
  AlertCircle,
  AlertTriangle,
  Info,
  X,
} from 'lucide-vue-next'

const props = defineProps({
  type: {
    type: String,
    default: 'info',
    validator: (v) => ['success', 'error', 'warning', 'info'].includes(v),
  },
  dismissible: {
    type: Boolean,
    default: false,
  },
  title: {
    type: String,
    default: '',
  },
})

const visible = ref(true)

// Turga qarab ikon
const iconComponent = computed(() => ({
  success: CheckCircle,
  error:   AlertCircle,
  warning: AlertTriangle,
  info:    Info,
}[props.type]))

// Turga qarab rang klasslari
const typeClasses = {
  success: 'bg-success-50 dark:bg-success-900/20 border-success-200 dark:border-success-800/30 text-success-800 dark:text-success-300',
  error:   'bg-danger-50 dark:bg-danger-900/20 border-danger-200 dark:border-danger-800/30 text-danger-800 dark:text-danger-300',
  warning: 'bg-secondary-50 dark:bg-secondary-900/20 border-secondary-200 dark:border-secondary-800/30 text-secondary-700 dark:text-secondary-300',
  info:    'bg-primary-50 dark:bg-primary-900/20 border-primary-200 dark:border-primary-800/30 text-primary-800 dark:text-primary-300',
}

const alertClasses = computed(() => [
  'rounded-xl p-4 border flex items-start gap-3',
  typeClasses[props.type],
])
</script>

<style scoped>
.alert-enter-active, .alert-leave-active {
  transition: all 0.3s ease;
}
.alert-enter-from, .alert-leave-to {
  opacity: 0;
  transform: translateY(-6px);
}
</style>
