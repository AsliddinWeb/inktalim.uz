<template>
  <form class="space-y-4" @submit.prevent="onSubmit">

    <!-- Title -->
    <div>
      <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5">
        Quiz sarlavhasi *
      </label>
      <input
        v-model="form.title"
        type="text"
        required
        maxlength="500"
        placeholder="Masalan: 1-dars testi"
        class="w-full h-11 px-3.5 bg-gray-50 dark:bg-gray-900/50 border border-gray-200 dark:border-gray-700 rounded-xl text-sm text-gray-900 dark:text-gray-100 placeholder:text-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500/20 focus:border-primary-500 transition-all duration-200"
      />
    </div>

    <!-- Description -->
    <div>
      <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5">
        Tavsif (ixtiyoriy)
      </label>
      <textarea
        v-model="form.description"
        rows="2"
        placeholder="Quiz haqida qisqacha ma'lumot..."
        class="w-full px-3.5 py-2.5 bg-gray-50 dark:bg-gray-900/50 border border-gray-200 dark:border-gray-700 rounded-xl text-sm text-gray-900 dark:text-gray-100 placeholder:text-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500/20 focus:border-primary-500 resize-none transition-all duration-200"
      />
    </div>

    <!-- Pass percent -->
    <div>
      <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5">
        O'tish foizi: <span class="text-primary-600 dark:text-primary-400 font-bold">{{ form.pass_percent }}%</span>
      </label>
      <input
        v-model.number="form.pass_percent"
        type="range"
        min="0"
        max="100"
        step="5"
        class="w-full accent-primary-500"
      />
      <div class="flex justify-between text-xs text-gray-400 mt-1">
        <span>0%</span><span>50%</span><span>100%</span>
      </div>
    </div>

    <!-- is_active toggle -->
    <label class="flex items-center gap-3 cursor-pointer select-none">
      <div
        class="relative w-10 h-5 rounded-full transition-colors"
        :class="form.is_active ? 'bg-primary-500' : 'bg-gray-300 dark:bg-gray-600'"
        @click="form.is_active = !form.is_active"
      >
        <div
          class="absolute top-0.5 left-0.5 w-4 h-4 rounded-full bg-white shadow transition-transform"
          :class="form.is_active ? 'translate-x-5' : 'translate-x-0'"
        />
      </div>
      <span class="text-sm text-gray-700 dark:text-gray-300">Faol (studentlarga ko'rinadi)</span>
    </label>

    <!-- Buttons -->
    <div class="flex justify-end gap-3 pt-2">
      <button
        type="button"
        class="px-4 py-2.5 rounded-xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-surface text-gray-700 dark:text-gray-300 text-sm font-medium hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors"
        @click="$emit('cancel')"
      >
        Bekor qilish
      </button>
      <button
        type="submit"
        :disabled="loading || !form.title.trim()"
        class="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-primary-500 hover:bg-primary-600 text-white text-sm font-semibold shadow-sm hover:shadow-md hover:-translate-y-0.5 active:translate-y-0 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
      >
        <svg v-if="loading" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
        </svg>
        {{ loading ? 'Saqlanmoqda...' : (quiz ? 'Yangilash' : 'Yaratish') }}
      </button>
    </div>
  </form>
</template>

<script setup>
import { reactive, watch } from 'vue'

const props = defineProps({
  quiz: { type: Object, default: null },
  lessonId: { type: String, default: null },
  loading: { type: Boolean, default: false },
})

const emit = defineEmits(['submit', 'cancel'])

const form = reactive({
  title: '',
  description: '',
  pass_percent: 60,
  is_active: true,
})

// Tahrirlash rejimida mavjud ma'lumotlar bilan to'ldirish
watch(
  () => props.quiz,
  (quiz) => {
    if (quiz) {
      form.title = quiz.title ?? ''
      form.description = quiz.description ?? ''
      form.pass_percent = quiz.pass_percent ?? 60
      form.is_active = quiz.is_active ?? true
    } else {
      form.title = ''
      form.description = ''
      form.pass_percent = 60
      form.is_active = true
    }
  },
  { immediate: true },
)

function onSubmit() {
  const payload = {
    title: form.title.trim(),
    description: form.description.trim() || null,
    pass_percent: form.pass_percent,
    is_active: form.is_active,
  }
  if (!props.quiz && props.lessonId) {
    payload.lesson_id = props.lessonId
  }
  emit('submit', payload)
}
</script>
