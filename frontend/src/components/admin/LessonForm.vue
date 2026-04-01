<template>
  <Form :validation-schema="schema" :initial-values="initial" @submit="onSubmit">
    <div class="space-y-4">

      <Field name="title" v-slot="{ field, errors }">
        <AppInput v-bind="field" label="Dars nomi *" placeholder="Masalan: O'zgaruvchilar va ma'lumot turlari" :error="errors[0]" />
      </Field>

      <Field name="video_url" v-slot="{ field, errors }">
        <AppInput v-bind="field" label="Video URL (YouTube yoki boshqa)" placeholder="https://youtube.com/watch?v=..." :error="errors[0]" />
      </Field>

      <Field name="content" v-slot="{ field, errors }">
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5">
            Dars matni (HTML/Markdown)
          </label>
          <textarea
            v-bind="field"
            rows="6"
            placeholder="Dars bo'yicha qo'shimcha matn, kodlar, izohlar..."
            class="w-full px-3.5 py-2.5 bg-gray-50 dark:bg-gray-900/50 border rounded-xl text-sm text-gray-900 dark:text-gray-100 placeholder:text-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500/20 focus:border-primary-500 resize-y font-mono transition-all duration-200"
            :class="errors[0] ? 'border-danger-400 dark:border-danger-600' : 'border-gray-200 dark:border-gray-700'"
          />
          <p v-if="errors[0]" class="mt-1 text-xs text-danger-500">{{ errors[0] }}</p>
        </div>
      </Field>

      <Field v-if="modules && modules.length" name="module_id" v-slot="{ field, errors }">
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5">Modul</label>
          <select
            v-bind="field"
            class="w-full px-3.5 py-2.5 bg-gray-50 dark:bg-gray-900/50 border border-gray-200 dark:border-gray-700 rounded-xl text-sm text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-primary-500/20 focus:border-primary-500 transition-all duration-200"
          >
            <option value="">— Modulga bog'lamaslik —</option>
            <option v-for="mod in modules" :key="mod.id" :value="mod.id">
              {{ mod.order }}. {{ mod.title }}
            </option>
          </select>
          <p v-if="errors[0]" class="mt-1 text-xs text-danger-500">{{ errors[0] }}</p>
        </div>
      </Field>

      <div class="grid grid-cols-2 gap-3">
        <Field name="duration_minutes" v-slot="{ field, errors }">
          <AppInput v-bind="field" type="number" label="Davomiyligi (daq)" placeholder="15" :error="errors[0]" />
        </Field>
        <Field name="order" v-slot="{ field, errors }">
          <AppInput v-bind="field" type="number" label="Tartib raqami" placeholder="1" :error="errors[0]" />
        </Field>
      </div>

      <Field name="is_published" v-slot="{ field }">
        <label class="flex items-center gap-3 cursor-pointer select-none">
          <div class="relative">
            <input type="checkbox" v-bind="field" :checked="field.value" class="sr-only peer" />
            <div class="w-10 h-5 bg-gray-300 dark:bg-gray-600 peer-checked:bg-primary-500 rounded-full transition-colors" />
            <div class="absolute top-0.5 left-0.5 w-4 h-4 bg-white rounded-full shadow transition-transform peer-checked:translate-x-5" />
          </div>
          <span class="text-sm font-medium text-gray-700 dark:text-gray-300">Nashr qilish</span>
        </label>
      </Field>

      <div class="flex gap-3 pt-2">
        <button
          type="submit"
          :disabled="saving"
          class="flex-1 inline-flex items-center justify-center gap-2 px-5 py-2.5 rounded-xl bg-primary-500 hover:bg-primary-600 text-white text-sm font-semibold shadow-sm hover:shadow-md hover:-translate-y-0.5 active:translate-y-0 transition-all duration-200 disabled:opacity-60 disabled:cursor-not-allowed disabled:transform-none"
        >
          <svg v-if="saving" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
          </svg>
          {{ isEdit ? 'Saqlash' : 'Qo\'shish' }}
        </button>
        <button
          type="button"
          class="px-4 py-2.5 rounded-xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-surface text-gray-700 dark:text-gray-300 text-sm font-medium hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors"
          @click="$emit('cancel')"
        >
          Bekor
        </button>
      </div>

    </div>
  </Form>
</template>

<script setup>
import { computed } from 'vue'
import { Form, Field } from 'vee-validate'
import * as yup from 'yup'
import AppInput from '@/components/ui/AppInput.vue'
import AppButton from '@/components/ui/AppButton.vue'

const props = defineProps({
  lesson:   { type: Object, default: null },
  saving:   { type: Boolean, default: false },
  moduleId: { type: String, default: null },
  modules:  { type: Array, default: () => [] },
})

const emit = defineEmits(['submit', 'cancel'])

const isEdit = computed(() => !!props.lesson?.id)

const initial = computed(() => ({
  title:            props.lesson?.title            ?? '',
  video_url:        props.lesson?.video_url        ?? '',
  content:          props.lesson?.content          ?? '',
  duration_minutes: props.lesson?.duration_minutes ?? 10,
  order:            props.lesson?.order            ?? 1,
  is_published:     props.lesson?.is_published     ?? false,
  module_id:        props.lesson?.module_id        ?? props.moduleId ?? '',
}))

const schema = yup.object({
  title:            yup.string().min(3, 'Kamida 3 ta belgi').required('Dars nomi majburiy'),
  video_url:        yup.string().url('To\'g\'ri URL kiriting').nullable().transform(v => v || null),
  content:          yup.string().nullable(),
  duration_minutes: yup.number().integer().min(1).required(),
  order:            yup.number().integer().min(1).required(),
  is_published:     yup.boolean(),
  module_id:        yup.string().nullable(),
})

function onSubmit(values) {
  emit('submit', {
    ...values,
    order:            Number(values.order),
    duration_minutes: Number(values.duration_minutes),
    video_url:        values.video_url  || null,
    content:          values.content    || null,
    module_id:        values.module_id  || null,
  })
}
</script>
