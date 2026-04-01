<template>
  <div class="animate-fade-in">

    <!-- Sarlavha -->
    <div class="mb-7">
      <h2 class="text-2xl lg:text-3xl font-bold text-gray-900 dark:text-white">
        Ro'yxatdan o'tish
      </h2>
      <p class="text-gray-500 dark:text-gray-400 mt-1">
        Bepul hisob yarating
      </p>
    </div>

    <!-- API xato xabari -->
    <AppAlert v-if="apiError" type="error" class="mb-5">
      {{ apiError }}
    </AppAlert>

    <!-- Register forma -->
    <form class="space-y-4" @submit.prevent="handleSubmit">

      <!-- To'liq ism -->
      <AppInput
        v-model="form.full_name"
        label="To'liq ism"
        placeholder="Sardor Raximov"
        type="text"
        autocomplete="name"
        :icon-left="User"
        :error="errors.full_name"
        required
        @blur="validateField('full_name')"
      />

      <!-- Email -->
      <AppInput
        v-model="form.email"
        label="Email"
        placeholder="email@example.com"
        type="email"
        autocomplete="email"
        :icon-left="Mail"
        :error="errors.email"
        required
        @blur="validateField('email')"
      />

      <!-- Telefon -->
      <AppInput
        v-model="form.phone"
        label="Telefon raqami"
        placeholder="+998901234567"
        type="text"
        autocomplete="tel"
        :icon-left="Phone"
        :error="errors.phone"
        hint="Format: +998XXXXXXXXX (O'zbekiston raqami)"
        required
        @blur="validateField('phone')"
      />

      <!-- Parol -->
      <div>
        <AppInput
          v-model="form.password"
          label="Parol"
          placeholder="Kamida 8 ta belgi"
          type="password"
          autocomplete="new-password"
          :icon-left="Lock"
          :error="errors.password"
          required
          @blur="validateField('password')"
        />

        <!-- Parol kuchlilik ko'rsatkichi -->
        <div v-if="form.password" class="mt-2">
          <div class="flex gap-1 mb-1">
            <div
              v-for="n in 4"
              :key="n"
              class="flex-1 h-1 rounded-full transition-all duration-300"
              :class="passwordStrengthBarClass(n)"
            />
          </div>
          <p class="text-xs" :class="passwordStrengthTextClass">
            {{ passwordStrengthLabel }}
          </p>
        </div>
      </div>

      <!-- Parolni tasdiqlash -->
      <AppInput
        v-model="form.confirmPassword"
        label="Parolni tasdiqlang"
        placeholder="Parolni qayta kiriting"
        type="password"
        autocomplete="new-password"
        :icon-left="ShieldCheck"
        :error="errors.confirmPassword"
        required
        @blur="validateField('confirmPassword')"
      />

      <!-- Ro'yxatdan o'tish tugmasi -->
      <AppButton
        type="submit"
        variant="primary"
        size="lg"
        :loading="authStore.loading"
        full-width
        class="w-full mt-2"
      >
        {{ authStore.loading ? 'Ro\'yxatdan o\'tilmoqda...' : 'Ro\'yxatdan o\'tish' }}
      </AppButton>
    </form>

    <!-- Login ga havola -->
    <p class="text-center mt-6 text-sm text-gray-500 dark:text-gray-400">
      Hisobingiz bormi?
      <RouterLink
        to="/login"
        class="text-primary-500 hover:text-primary-600 font-semibold transition-colors"
      >
        Kirish
      </RouterLink>
    </p>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { RouterLink } from 'vue-router'
import { User, Mail, Phone, Lock, ShieldCheck, AlertCircle, X, UserPlus } from 'lucide-vue-next'
import * as yup from 'yup'

import AppInput from '@/components/ui/AppInput.vue'
import AppButton from '@/components/ui/AppButton.vue'
import AppAlert from '@/components/ui/AppAlert.vue'
import { useAuthStore } from '@/stores/auth.js'

const authStore = useAuthStore()

// ─── Forma holati ────────────────────────────────────────────────────────────

const form = reactive({
  full_name:       '',
  email:           '',
  phone:           '',
  password:        '',
  confirmPassword: '',
})

const errors = reactive({
  full_name:       '',
  email:           '',
  phone:           '',
  password:        '',
  confirmPassword: '',
})

const apiError = ref('')

// ─── Yup validatsiya sxemalari ────────────────────────────────────────────────

const schemas = {
  full_name: yup
    .string()
    .required('To\'liq ismni kiriting')
    .min(2, 'Ism kamida 2 ta belgi bo\'lishi kerak')
    .max(255, 'Ism juda uzun'),

  email: yup
    .string()
    .required('Email manzilini kiriting')
    .email('Noto\'g\'ri email format'),

  phone: yup
    .string()
    .required('Telefon raqamini kiriting')
    .matches(
      /^\+998[0-9]{9}$/,
      'Telefon +998XXXXXXXXX formatida bo\'lishi kerak (masalan: +998901234567)'
    ),

  password: yup
    .string()
    .required('Parolni kiriting')
    .min(8, 'Parol kamida 8 ta belgi bo\'lishi kerak')
    .test(
      'has-digit',
      'Parolda kamida bitta raqam bo\'lishi kerak',
      (v) => !v || /[0-9]/.test(v)
    ),

  confirmPassword: yup
    .string()
    .required('Parolni tasdiqlang')
    .test('passwords-match', 'Parollar mos kelmadi', function (value) {
      return value === form.password
    }),
}

// ─── Parol kuchlilik hisobi ───────────────────────────────────────────────────

const passwordStrength = computed(() => {
  const p = form.password
  if (!p) return 0
  let score = 0
  if (p.length >= 8)  score++
  if (p.length >= 12) score++
  if (/[0-9]/.test(p) && /[a-zA-Z]/.test(p)) score++
  if (/[^a-zA-Z0-9]/.test(p)) score++
  return score
})

const strengthConfig = {
  0: { label: '', textClass: '' },
  1: { label: 'Kuchsiz',      textClass: 'text-danger-500' },
  2: { label: 'O\'rtacha',    textClass: 'text-secondary-500' },
  3: { label: 'Kuchli',       textClass: 'text-secondary-400' },
  4: { label: 'Juda kuchli',  textClass: 'text-success-500' },
}

const passwordStrengthLabel     = computed(() => strengthConfig[passwordStrength.value]?.label || '')
const passwordStrengthTextClass = computed(() => strengthConfig[passwordStrength.value]?.textClass || '')

function passwordStrengthBarClass(n) {
  const s = passwordStrength.value
  if (n > s) return 'bg-gray-200 dark:bg-gray-700'
  if (s === 1) return 'bg-danger-400'
  if (s === 2) return 'bg-secondary-400'
  if (s === 3) return 'bg-secondary-400'
  return 'bg-success-400'
}

// ─── Validatsiya ─────────────────────────────────────────────────────────────

async function validateField(field) {
  try {
    await schemas[field].validate(form[field])
    errors[field] = ''
  } catch (err) {
    errors[field] = err.message
  }
}

async function validateAll() {
  let valid = true
  for (const field of Object.keys(schemas)) {
    try {
      await schemas[field].validate(form[field])
      errors[field] = ''
    } catch (err) {
      errors[field] = err.message
      valid = false
    }
  }
  return valid
}

// ─── Forma yuborish ──────────────────────────────────────────────────────────

async function handleSubmit() {
  apiError.value = ''

  const isValid = await validateAll()
  if (!isValid) return

  const result = await authStore.register({
    full_name: form.full_name,
    email:     form.email,
    phone:     form.phone,
    password:  form.password,
  })

  if (!result?.success) {
    apiError.value = result?.error || 'Ro\'yxatdan o\'tish muvaffaqiyatsiz. Qayta urinib ko\'ring.'
  }
}
</script>

<style scoped>
.alert-enter-active, .alert-leave-active {
  transition: all 0.3s ease;
}
.alert-enter-from, .alert-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}
</style>
