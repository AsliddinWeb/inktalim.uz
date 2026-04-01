<template>
  <div :class="['w-full', wrapperClass]">
    <!-- Label -->
    <label
      v-if="label"
      :for="inputId"
      class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5"
    >
      {{ label }}
      <span v-if="required" class="text-danger-500 ml-0.5">*</span>
    </label>

    <!-- Input wrapper -->
    <div class="relative">
      <!-- Chap ikon -->
      <div
        v-if="iconLeft"
        class="absolute left-3 top-1/2 -translate-y-1/2 flex items-center pointer-events-none text-gray-400"
      >
        <component :is="iconLeft" class="w-4 h-4" />
      </div>

      <!-- Textarea elementi -->
      <textarea
        v-if="type === 'textarea'"
        :id="inputId"
        :value="modelValue"
        :placeholder="placeholder"
        :disabled="disabled"
        :required="required"
        v-bind="$attrs"
        :class="textareaClasses"
        @input="$emit('update:modelValue', $event.target.value)"
        @blur="$emit('blur', $event)"
        @focus="$emit('focus', $event)"
      />

      <!-- Input elementi -->
      <input
        v-else
        :id="inputId"
        :type="currentType"
        :value="modelValue"
        :placeholder="placeholder"
        :disabled="disabled"
        :required="required"
        :autocomplete="autocomplete"
        v-bind="$attrs"
        :class="inputClasses"
        @input="$emit('update:modelValue', $event.target.value)"
        @blur="$emit('blur', $event)"
        @focus="$emit('focus', $event)"
      />

      <!-- O'ng ikon yoki parol toggle -->
      <div
        v-if="type !== 'textarea'"
        class="absolute right-3 top-1/2 -translate-y-1/2 flex items-center gap-1"
      >
        <!-- Parol ko'rsatish/yashirish tugmasi -->
        <button
          v-if="type === 'password'"
          type="button"
          class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors"
          :aria-label="showPassword ? 'Parolni yashirish' : 'Parolni ko\'rsatish'"
          @click="togglePassword"
        >
          <component :is="showPassword ? EyeOff : Eye" class="w-4 h-4" />
        </button>
        <!-- Oddiy o'ng ikon -->
        <component
          v-else-if="iconRight"
          :is="iconRight"
          class="w-4 h-4 text-gray-400 pointer-events-none"
        />
      </div>
    </div>

    <!-- Character count -->
    <p v-if="maxlength && type === 'textarea'" class="text-xs text-gray-400 text-right mt-1">
      {{ String(modelValue || '').length }}/{{ maxlength }}
    </p>

    <!-- Xato xabari -->
    <Transition name="fade-down">
      <p
        v-if="error"
        class="mt-1.5 text-xs text-danger-500 flex items-center gap-1"
      >
        <AlertCircle class="w-3.5 h-3.5 flex-shrink-0" />
        {{ error }}
      </p>
    </Transition>

    <!-- Yordam matni -->
    <p
      v-if="hint && !error"
      class="mt-1.5 text-xs text-gray-400"
    >
      {{ hint }}
    </p>
  </div>
</template>

<script setup>
import { ref, computed, useId } from 'vue'
import { Eye, EyeOff, AlertCircle } from 'lucide-vue-next'

// Emits
defineEmits(['update:modelValue', 'blur', 'focus'])

// Props
const props = defineProps({
  modelValue: {
    type: String,
    default: '',
  },
  label: {
    type: String,
    default: '',
  },
  placeholder: {
    type: String,
    default: '',
  },
  type: {
    type: String,
    default: 'text',
  },
  error: {
    type: String,
    default: '',
  },
  hint: {
    type: String,
    default: '',
  },
  disabled: {
    type: Boolean,
    default: false,
  },
  required: {
    type: Boolean,
    default: false,
  },
  autocomplete: {
    type: String,
    default: 'off',
  },
  maxlength: {
    type: Number,
    default: null,
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
  wrapperClass: {
    type: String,
    default: '',
  },
})

// Noyob ID — label va input bog'lanishi uchun
const inputId = computed(() => `input-${Math.random().toString(36).slice(2, 9)}`)

// Parol ko'rinishi holati
const showPassword = ref(false)

// Joriy input turi (parol toggle uchun)
const currentType = computed(() => {
  if (props.type === 'password') {
    return showPassword.value ? 'text' : 'password'
  }
  return props.type
})

function togglePassword() {
  showPassword.value = !showPassword.value
}

// Input klass hisoblash
const inputClasses = computed(() => {
  const base = [
    'w-full h-11 bg-gray-50 dark:bg-gray-900/50',
    'border border-gray-200 dark:border-gray-700',
    'rounded-xl text-sm',
    'text-gray-900 dark:text-gray-100',
    'placeholder:text-gray-400',
    'transition-all duration-200',
    'focus:outline-none focus:ring-2',
    // Chap ikon bo'lsa padding
    props.iconLeft ? 'pl-10' : 'px-4',
    // O'ng ikon yoki parol toggle bo'lsa padding
    (props.iconRight || props.type === 'password') ? 'pr-10' : '',
  ]

  if (props.error) {
    base.push('border-danger-500 focus:ring-danger-500/20 focus:border-danger-500')
  } else {
    base.push('focus:ring-primary-500/20 focus:border-primary-500')
  }

  if (props.disabled) {
    base.push('opacity-60 cursor-not-allowed bg-gray-100 dark:bg-gray-800')
  }

  return base.join(' ')
})

// Textarea klass hisoblash
const textareaClasses = computed(() => {
  const base = [
    'w-full py-3 px-4 bg-gray-50 dark:bg-gray-900/50',
    'border border-gray-200 dark:border-gray-700',
    'rounded-xl text-sm',
    'text-gray-900 dark:text-gray-100',
    'placeholder:text-gray-400',
    'transition-all duration-200',
    'focus:outline-none focus:ring-2',
    'min-h-[88px] resize-y',
  ]

  if (props.error) {
    base.push('border-danger-500 focus:ring-danger-500/20 focus:border-danger-500')
  } else {
    base.push('focus:ring-primary-500/20 focus:border-primary-500')
  }

  if (props.disabled) {
    base.push('opacity-60 cursor-not-allowed bg-gray-100 dark:bg-gray-800')
  }

  return base.join(' ')
})
</script>

<style scoped>
/* Xato xabari animatsiyasi */
.fade-down-enter-active,
.fade-down-leave-active {
  transition: all 0.2s ease;
}
.fade-down-enter-from,
.fade-down-leave-to {
  opacity: 0;
  transform: translateY(-4px);
}
</style>
