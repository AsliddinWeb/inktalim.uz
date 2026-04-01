<template>
  <div class="animate-fade-in">

    <!-- Sarlavha -->
    <div class="mb-8">
      <h2 class="text-2xl lg:text-3xl font-bold text-gray-900 dark:text-white">
        Xush kelibsiz! 👋
      </h2>
      <p class="text-gray-500 dark:text-gray-400 mt-1">
        Hisobingizga kiring
      </p>
    </div>

    <!-- API xato xabari -->
    <AppAlert v-if="apiError" type="error" class="mb-5">
      {{ apiError }}
    </AppAlert>

    <!-- Login forma -->
    <form class="space-y-5" @submit.prevent="handleSubmit">

      <!-- Email yoki telefon -->
      <AppInput
        v-model="form.login"
        label="Email"
        placeholder="example@email.com"
        type="email"
        autocomplete="username"
        :icon-left="Mail"
        :error="errors.login"
        required
        @blur="validateField('login')"
      />

      <!-- Parol -->
      <AppInput
        v-model="form.password"
        label="Parol"
        placeholder="••••••••"
        type="password"
        autocomplete="current-password"
        :icon-left="Lock"
        :error="errors.password"
        required
        @blur="validateField('password')"
      />

      <!-- "Meni eslab qol" + Parolni unutdingiz? -->
      <div class="flex items-center justify-between">
        <label class="flex items-center gap-2 cursor-pointer">
          <input
            v-model="form.rememberMe"
            type="checkbox"
            class="rounded border-gray-300 text-primary-500 focus:ring-primary-500 focus:ring-offset-0"
          />
          <span class="text-sm text-gray-600 dark:text-gray-400">Meni eslab qol</span>
        </label>
        <button
          type="button"
          class="text-sm text-primary-500 hover:text-primary-600 font-medium transition-colors"
        >
          Parolni unutdingiz?
        </button>
      </div>

      <!-- Kirish tugmasi -->
      <AppButton
        type="submit"
        variant="primary"
        size="lg"
        :loading="authStore.loading"
        full-width
        class="w-full mt-1"
      >
        {{ authStore.loading ? 'Kirilmoqda...' : 'Kirish' }}
      </AppButton>
    </form>

    <!-- Register ga havola -->
    <p class="text-center mt-6 text-sm text-gray-500 dark:text-gray-400">
      Hisobingiz yo'qmi?
      <RouterLink
        to="/register"
        class="text-primary-500 hover:text-primary-600 font-semibold transition-colors"
      >
        Ro'yxatdan o'ting
      </RouterLink>
    </p>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { RouterLink } from 'vue-router'
import { Mail, Lock, AlertCircle, X, Check, ArrowRight } from 'lucide-vue-next'
import * as yup from 'yup'

import AppInput from '@/components/ui/AppInput.vue'
import AppButton from '@/components/ui/AppButton.vue'
import AppAlert from '@/components/ui/AppAlert.vue'
import { useAuthStore } from '@/stores/auth.js'

const authStore = useAuthStore()

// ─── Forma holati ────────────────────────────────────────────────────────────

const form = reactive({
  login:      '',
  password:   '',
  rememberMe: false,
})

const errors = reactive({
  login:    '',
  password: '',
})

const apiError = ref('')

// ─── Validatsiya sxemasi (Yup) ───────────────────────────────────────────────

// Email yoki telefon formati tekshiruvi
const loginSchema = yup.string()
  .required('Email yoki telefon raqamini kiriting')
  .test('email-or-phone', 'Email yoki telefon (+998XXXXXXXXX) kiriting', (value) => {
    if (!value) return false
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    const phoneRegex = /^\+998[0-9]{9}$/
    return emailRegex.test(value) || phoneRegex.test(value)
  })

const passwordSchema = yup.string()
  .required('Parolni kiriting')
  .min(6, 'Parol kamida 6 ta belgi bo\'lishi kerak')

// ─── Validatsiya funksiyalari ─────────────────────────────────────────────────

async function validateField(field) {
  try {
    if (field === 'login') {
      await loginSchema.validate(form.login)
      errors.login = ''
    } else if (field === 'password') {
      await passwordSchema.validate(form.password)
      errors.password = ''
    }
  } catch (err) {
    errors[field] = err.message
  }
}

async function validateAll() {
  let valid = true

  try {
    await loginSchema.validate(form.login)
    errors.login = ''
  } catch (err) {
    errors.login = err.message
    valid = false
  }

  try {
    await passwordSchema.validate(form.password)
    errors.password = ''
  } catch (err) {
    errors.password = err.message
    valid = false
  }

  return valid
}

// ─── Forma yuborish ──────────────────────────────────────────────────────────

async function handleSubmit() {
  apiError.value = ''

  // Validatsiya
  const isValid = await validateAll()
  if (!isValid) return

  // Auth store orqali login
  const result = await authStore.login({
    login:    form.login,
    password: form.password,
  })

  if (!result.success) {
    apiError.value = result.error || 'Kirish muvaffaqiyatsiz. Qayta urinib ko\'ring.'
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
