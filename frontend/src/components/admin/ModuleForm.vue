<template>
  <Form :validation-schema="schema" :initial-values="initial" @submit="onSubmit">
    <div class="space-y-4">

      <Field name="title" v-slot="{ field, errors }">
        <AppInput v-bind="field" label="Modul nomi *" placeholder="Masalan: Python asoslari" :error="errors[0]" />
      </Field>

      <Field name="description" v-slot="{ field, errors }">
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5">
            Tavsif (ixtiyoriy)
          </label>
          <textarea
            v-bind="field"
            rows="3"
            placeholder="Modul haqida qisqacha ma'lumot..."
            class="w-full px-3.5 py-2.5 bg-gray-50 dark:bg-gray-900/50 border border-gray-200 dark:border-gray-700 rounded-xl text-sm text-gray-900 dark:text-gray-100 placeholder:text-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500/20 focus:border-primary-500 resize-y transition-all duration-200"
            :class="errors[0] ? 'border-danger-400 dark:border-danger-600' : 'border-gray-200 dark:border-gray-700'"
          />
          <p v-if="errors[0]" class="mt-1 text-xs text-danger-500">{{ errors[0] }}</p>
        </div>
      </Field>

      <Field name="order" v-slot="{ field, errors }">
        <AppInput v-bind="field" type="number" label="Tartib raqami" placeholder="1" :error="errors[0]" />
      </Field>

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

const props = defineProps({
  module: { type: Object, default: null },
  saving: { type: Boolean, default: false },
})

const emit = defineEmits(['submit', 'cancel'])

const isEdit = computed(() => !!props.module?.id)

const initial = computed(() => ({
  title:        props.module?.title        ?? '',
  description:  props.module?.description  ?? '',
  order:        props.module?.order        ?? 1,
  is_published: props.module?.is_published ?? false,
}))

const schema = yup.object({
  title:        yup.string().min(2, 'Kamida 2 ta belgi').required('Modul nomi majburiy'),
  description:  yup.string().nullable(),
  order:        yup.number().integer().min(1).required(),
  is_published: yup.boolean(),
})

function onSubmit(values) {
  emit('submit', {
    ...values,
    order:       Number(values.order),
    description: values.description || null,
  })
}
</script>
