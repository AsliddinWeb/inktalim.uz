<template>
  <Teleport to="body">
    <Transition name="modal-fade">
      <div
        v-if="show"
        class="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4"
        role="dialog"
        :aria-modal="show"
        :aria-labelledby="titleId"
        @click.self="$emit('close')"
      >
        <!-- Modal panel -->
        <Transition name="modal-scale" appear>
          <div
            v-if="show"
            class="bg-white dark:bg-surface rounded-2xl shadow-2xl w-full overflow-hidden flex flex-col max-h-[90vh]"
            :class="sizeClass"
            @click.stop
          >
            <!-- Header -->
            <div
              v-if="title"
              class="flex items-center justify-between px-6 py-4 border-b border-gray-100 dark:border-gray-800 flex-shrink-0"
            >
              <h3
                :id="titleId"
                class="text-lg font-semibold text-gray-900 dark:text-white"
              >
                {{ title }}
              </h3>
              <button
                type="button"
                class="w-8 h-8 rounded-xl hover:bg-gray-100 dark:hover:bg-gray-800 flex items-center justify-center transition-colors text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
                aria-label="Yopish"
                @click="$emit('close')"
              >
                <X class="w-4 h-4" />
              </button>
            </div>

            <!-- Body -->
            <div class="px-6 py-5 overflow-y-auto flex-1 max-h-[70vh]">
              <slot />
            </div>

            <!-- Footer (ixtiyoriy) -->
            <div
              v-if="$slots['footer'] || $slots['modal-footer']"
              class="px-6 pb-5 flex-shrink-0 flex items-center justify-end gap-3"
            >
              <slot name="footer" />
              <slot name="modal-footer" />
            </div>
          </div>
        </Transition>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { computed, onMounted, onUnmounted } from 'vue'
import { X } from 'lucide-vue-next'

const props = defineProps({
  show: { type: Boolean, default: false },
  title: { type: String, default: '' },
  size: {
    type: String,
    default: 'md',
    validator: (v) => ['sm', 'md', 'lg', 'xl'].includes(v),
  },
})

defineEmits(['close'])

// Noyob ID — accessibility uchun
const titleId = computed(() => `modal-title-${Math.random().toString(36).slice(2, 7)}`)

const sizeClass = computed(() => ({
  sm: 'max-w-sm',
  md: 'max-w-lg',
  lg: 'max-w-2xl',
  xl: 'max-w-4xl',
}[props.size]))

// ESC tugma bilan yopish
function handleKeydown(e) {
  if (e.key === 'Escape' && props.show) {
    // emit yoki parent dan close
  }
}

onMounted(() => window.addEventListener('keydown', handleKeydown))
onUnmounted(() => window.removeEventListener('keydown', handleKeydown))
</script>

<style scoped>
/* Backdrop fade */
.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.2s ease;
}
.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}

/* Panel scale */
.modal-scale-enter-active,
.modal-scale-leave-active {
  transition: all 0.2s ease;
}
.modal-scale-enter-from,
.modal-scale-leave-to {
  opacity: 0;
  transform: scale(0.95);
}
.modal-scale-enter-to,
.modal-scale-leave-from {
  opacity: 1;
  transform: scale(1);
}
</style>
