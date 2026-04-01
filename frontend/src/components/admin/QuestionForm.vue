<template>
  <form class="space-y-4" @submit.prevent="onSubmit">

    <!-- Question text -->
    <div>
      <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5">
        Savol matni *
      </label>
      <textarea
        v-model="form.text"
        rows="3"
        required
        maxlength="2000"
        placeholder="Savol yozing..."
        class="w-full px-3.5 py-2.5 bg-gray-50 dark:bg-gray-900/50 border border-gray-200 dark:border-gray-700 rounded-xl text-sm text-gray-900 dark:text-gray-100 placeholder:text-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500/20 focus:border-primary-500 resize-none transition-all duration-200"
      />
    </div>

    <!-- Choices -->
    <div>
      <div class="flex items-center justify-between mb-2">
        <label class="text-sm font-medium text-gray-700 dark:text-gray-300">
          Javob variantlari *
        </label>
        <button
          v-if="form.choices.length < 6"
          type="button"
          class="text-xs text-primary-600 dark:text-primary-400 hover:text-primary-700 dark:hover:text-primary-300 font-medium transition-colors"
          @click="addChoice"
        >
          + Variant qo'shish
        </button>
      </div>

      <div class="space-y-2">
        <div v-for="(choice, index) in form.choices" :key="index" class="flex items-center gap-2">
          <!-- Correct radio -->
          <button
            type="button"
            class="flex-shrink-0 w-5 h-5 rounded-full border-2 transition-all flex items-center justify-center"
            :class="choice.is_correct
              ? 'border-primary-500 bg-primary-500'
              : 'border-gray-300 dark:border-gray-600 hover:border-primary-400'"
            :title="choice.is_correct ? 'To\'g\'ri javob' : 'To\'g\'ri deb belgilash'"
            @click="setCorrect(index)"
          >
            <div v-if="choice.is_correct" class="w-2 h-2 rounded-full bg-white" />
          </button>

          <!-- Choice text -->
          <input
            v-model="choice.text"
            type="text"
            required
            maxlength="1000"
            :placeholder="`${index + 1}-variant`"
            class="flex-1 h-9 px-3 text-sm bg-gray-50 dark:bg-gray-900/50 border border-gray-200 dark:border-gray-700 rounded-lg text-gray-900 dark:text-gray-100 placeholder:text-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500/20 focus:border-primary-500 transition-all duration-200"
          />

          <!-- Remove -->
          <button
            v-if="form.choices.length > 2"
            type="button"
            class="flex-shrink-0 p-1 text-gray-400 hover:text-danger-500 transition-colors"
            @click="removeChoice(index)"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>
      </div>

      <p v-if="!hasCorrect" class="text-xs text-secondary-600 dark:text-secondary-400 mt-1.5">
        Kamida bitta to'g'ri javobni belgilang (to'la doira)
      </p>
    </div>

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
        :disabled="loading || !form.text.trim() || !hasCorrect"
        class="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-primary-500 hover:bg-primary-600 text-white text-sm font-semibold shadow-sm hover:shadow-md hover:-translate-y-0.5 active:translate-y-0 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
      >
        <svg v-if="loading" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
        </svg>
        {{ loading ? 'Saqlanmoqda...' : (question ? 'Yangilash' : 'Qo\'shish') }}
      </button>
    </div>
  </form>
</template>

<script setup>
import { computed, reactive, watch } from 'vue'

const props = defineProps({
  question: { type: Object, default: null },
  loading: { type: Boolean, default: false },
})

const emit = defineEmits(['submit', 'cancel'])

const form = reactive({
  text: '',
  choices: [
    { text: '', is_correct: false, order: 0 },
    { text: '', is_correct: false, order: 1 },
    { text: '', is_correct: false, order: 2 },
    { text: '', is_correct: false, order: 3 },
  ],
})

const hasCorrect = computed(() => form.choices.some((c) => c.is_correct))

watch(
  () => props.question,
  (q) => {
    if (q) {
      form.text = q.text ?? ''
      form.choices =
        q.choices?.length
          ? q.choices.map((c, i) => ({ text: c.text, is_correct: c.is_correct, order: i }))
          : [
              { text: '', is_correct: false, order: 0 },
              { text: '', is_correct: false, order: 1 },
              { text: '', is_correct: false, order: 2 },
              { text: '', is_correct: false, order: 3 },
            ]
    } else {
      form.text = ''
      form.choices = [
        { text: '', is_correct: false, order: 0 },
        { text: '', is_correct: false, order: 1 },
        { text: '', is_correct: false, order: 2 },
        { text: '', is_correct: false, order: 3 },
      ]
    }
  },
  { immediate: true },
)

function setCorrect(index) {
  form.choices.forEach((c, i) => (c.is_correct = i === index))
}

function addChoice() {
  if (form.choices.length < 6) {
    form.choices.push({ text: '', is_correct: false, order: form.choices.length })
  }
}

function removeChoice(index) {
  form.choices.splice(index, 1)
  // Agar o'chirilgan to'g'ri bo'lsa, birinchini to'g'ri qilamiz
  if (!form.choices.some((c) => c.is_correct) && form.choices.length) {
    form.choices[0].is_correct = true
  }
  // order ni qayta tartiblash
  form.choices.forEach((c, i) => (c.order = i))
}

function onSubmit() {
  emit('submit', {
    text: form.text.trim(),
    order: props.question?.order ?? 0,
    choices: form.choices
      .filter((c) => c.text.trim())
      .map((c, i) => ({ text: c.text.trim(), is_correct: c.is_correct, order: i })),
  })
}
</script>
