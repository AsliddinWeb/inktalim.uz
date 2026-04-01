<template>
  <div class="space-y-6 max-w-2xl">

    <!-- Header -->
    <div>
      <h1 class="text-2xl font-bold text-gray-900 dark:text-white">Admin Profil</h1>
      <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">Hisob ma'lumotlarini boshqarish</p>
    </div>

    <!-- Avatar card -->
    <div class="rounded-2xl border border-gray-100 dark:border-gray-800 bg-white dark:bg-surface p-6">
      <div class="flex items-center gap-4">
        <div class="flex flex-col items-center gap-1.5">
          <AppAvatar
            :url="user?.avatar_url"
            :name="user?.full_name || user?.email"
            size="xl"
            :editable="true"
            @updated="onAvatarUpdated"
          />
          <p class="text-xs text-gray-400">Rasmni o'zgartirish</p>
        </div>
        <div>
          <p class="text-lg font-semibold text-gray-900 dark:text-white">{{ user?.full_name || 'Admin' }}</p>
          <p class="text-sm text-gray-500 dark:text-gray-400">{{ user?.email }}</p>
          <span class="mt-2 inline-flex items-center rounded-full px-3 py-1 text-xs font-semibold bg-secondary-100 dark:bg-secondary-900/20 text-secondary-700 dark:text-secondary-400">
            Admin
          </span>
        </div>
      </div>
      <div v-if="avatarError" class="mt-3 flex items-center gap-3 rounded-xl border border-danger-200 dark:border-danger-800/30 bg-danger-50 dark:bg-danger-900/10 px-4 py-3">
        <p class="text-sm font-medium text-danger-600 dark:text-danger-400">{{ avatarError }}</p>
        <button type="button" class="ml-auto text-danger-400 hover:text-danger-600" @click="avatarError = ''">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
          </svg>
        </button>
      </div>
    </div>

    <!-- Profile form -->
    <div class="rounded-2xl border border-gray-100 dark:border-gray-800 bg-white dark:bg-surface p-6">
      <h2 class="font-semibold text-gray-900 dark:text-white mb-4">Ma'lumotlarni tahrirlash</h2>

      <div v-if="profileSuccess" class="flex items-center gap-3 rounded-xl border border-success-200 dark:border-success-800/30 bg-success-50 dark:bg-success-900/10 px-4 py-3 mb-4">
        <p class="text-sm font-medium text-success-700 dark:text-success-400">{{ profileSuccess }}</p>
        <button type="button" class="ml-auto text-success-400" @click="profileSuccess = ''">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
          </svg>
        </button>
      </div>
      <div v-if="profileError" class="rounded-xl border border-danger-200 dark:border-danger-800/30 bg-danger-50 dark:bg-danger-900/10 px-4 py-3 mb-4">
        <p class="text-sm font-medium text-danger-600 dark:text-danger-400">{{ profileError }}</p>
      </div>

      <Form :validation-schema="profileSchema" :initial-values="profileInitial" @submit="onProfileSubmit">
        <div class="space-y-4">
          <Field name="full_name" v-slot="{ field, errors }">
            <AppInput v-bind="field" label="To'liq ism" placeholder="Ism Familiya" :error="errors[0]" />
          </Field>
          <Field name="phone" v-slot="{ field, errors }">
            <AppInput v-bind="field" label="Telefon" placeholder="+998901234567" hint="Format: +998XXXXXXXXX" :error="errors[0]" />
          </Field>
          <button
            type="submit"
            :disabled="savingProfile"
            class="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-primary-500 hover:bg-primary-600 text-white text-sm font-semibold shadow-sm hover:shadow-md hover:-translate-y-0.5 active:translate-y-0 transition-all duration-200 disabled:opacity-60 disabled:cursor-not-allowed disabled:transform-none"
          >
            <svg v-if="savingProfile" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
            </svg>
            Saqlash
          </button>
        </div>
      </Form>
    </div>

    <!-- Password form -->
    <div class="rounded-2xl border border-gray-100 dark:border-gray-800 bg-white dark:bg-surface p-6">
      <h2 class="font-semibold text-gray-900 dark:text-white mb-4">Parolni o'zgartirish</h2>

      <div v-if="passwordSuccess" class="flex items-center gap-3 rounded-xl border border-success-200 dark:border-success-800/30 bg-success-50 dark:bg-success-900/10 px-4 py-3 mb-4">
        <p class="text-sm font-medium text-success-700 dark:text-success-400">{{ passwordSuccess }}</p>
        <button type="button" class="ml-auto text-success-400" @click="passwordSuccess = ''">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
          </svg>
        </button>
      </div>
      <div v-if="passwordError" class="rounded-xl border border-danger-200 dark:border-danger-800/30 bg-danger-50 dark:bg-danger-900/10 px-4 py-3 mb-4">
        <p class="text-sm font-medium text-danger-600 dark:text-danger-400">{{ passwordError }}</p>
      </div>

      <Form :validation-schema="passwordSchema" @submit="onPasswordSubmit">
        <div class="space-y-4">
          <Field name="old_password" v-slot="{ field, errors }">
            <AppInput v-bind="field" type="password" label="Joriy parol" :error="errors[0]" />
          </Field>
          <Field name="new_password" v-slot="{ field, errors }">
            <AppInput v-bind="field" type="password" label="Yangi parol" :error="errors[0]" />
          </Field>
          <Field name="confirm_password" v-slot="{ field, errors }">
            <AppInput v-bind="field" type="password" label="Yangi parolni tasdiqlang" :error="errors[0]" />
          </Field>
          <button
            type="submit"
            :disabled="savingPassword"
            class="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-surface text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-800 text-sm font-semibold transition-all duration-200 disabled:opacity-60 disabled:cursor-not-allowed"
          >
            <svg v-if="savingPassword" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
            </svg>
            Parolni o'zgartirish
          </button>
        </div>
      </Form>
    </div>

    <!-- Logout -->
    <div class="rounded-2xl border border-gray-100 dark:border-gray-800 bg-white dark:bg-surface p-6">
      <div class="flex items-center justify-between">
        <div>
          <p class="font-medium text-gray-900 dark:text-white">Tizimdan chiqish</p>
          <p class="text-sm text-gray-500 dark:text-gray-400">Barcha qurilmalardan chiqiladi</p>
        </div>
        <button
          type="button"
          class="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-danger-50 dark:bg-danger-900/20 text-danger-600 dark:text-danger-400 hover:bg-danger-500 hover:text-white dark:hover:bg-danger-500 dark:hover:text-white border border-danger-200 dark:border-danger-800 hover:border-transparent text-sm font-semibold transition-all duration-200"
          @click="handleLogout"
        >
          <LogOut class="w-4 h-4" />
          Chiqish
        </button>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { Form, Field } from 'vee-validate'
import * as yup from 'yup'
import { LogOut } from 'lucide-vue-next'
import { useAuthStore } from '@/stores/auth.js'
import { storeToRefs } from 'pinia'
import api from '@/api/axios.js'
import AppCard   from '@/components/ui/AppCard.vue'
import AppInput  from '@/components/ui/AppInput.vue'
import AppButton from '@/components/ui/AppButton.vue'
import AppBadge  from '@/components/ui/AppBadge.vue'
import AppAlert  from '@/components/ui/AppAlert.vue'
import AppAvatar from '@/components/ui/AppAvatar.vue'

const router    = useRouter()
const authStore = useAuthStore()
const { user }  = storeToRefs(authStore)

// ─── Avatar ────────────────────────────────────────────────────────────────

const avatarError = ref('')

async function onAvatarUpdated() {
  try {
    await authStore.fetchMe()
  } catch {
    avatarError.value = 'Avatar yangilashda xatolik yuz berdi.'
  }
}

// ─── Profil ────────────────────────────────────────────────────────────────

const savingProfile  = ref(false)
const profileError   = ref('')
const profileSuccess = ref('')

const profileInitial = computed(() => ({
  full_name: user.value?.full_name ?? '',
  phone:     user.value?.phone     ?? '',
}))

const profileSchema = yup.object({
  full_name: yup.string().min(2, 'Kamida 2 belgi').nullable(),
  phone:     yup.string()
    .matches(/^\+998[0-9]{9}$/, 'Format: +998901234567')
    .nullable()
    .transform(v => v || null),
})

async function onProfileSubmit(values) {
  savingProfile.value = true
  profileError.value  = ''
  profileSuccess.value = ''
  try {
    await api.put('/auth/me', {
      full_name: values.full_name || undefined,
      phone:     values.phone     || undefined,
    })
    await authStore.fetchMe()
    profileSuccess.value = 'Ma\'lumotlar saqlandi!'
  } catch (err) {
    profileError.value = err.response?.data?.detail || 'Saqlashda xatolik.'
  } finally {
    savingProfile.value = false
  }
}

// ─── Parol ─────────────────────────────────────────────────────────────────

const savingPassword  = ref(false)
const passwordError   = ref('')
const passwordSuccess = ref('')

const passwordSchema = yup.object({
  old_password:     yup.string().required('Joriy parol kiritilmagan'),
  new_password:     yup.string().min(8, 'Kamida 8 ta belgi').required('Yangi parol kiritilmagan'),
  confirm_password: yup.string()
    .oneOf([yup.ref('new_password')], 'Parollar mos kelmadi')
    .required('Tasdiqlash majburiy'),
})

async function onPasswordSubmit(values, { resetForm }) {
  savingPassword.value  = true
  passwordError.value   = ''
  passwordSuccess.value = ''
  try {
    await api.post('/auth/change-password', {
      old_password: values.old_password,
      new_password: values.new_password,
    })
    passwordSuccess.value = 'Parol muvaffaqiyatli o\'zgartirildi!'
    resetForm()
  } catch (err) {
    passwordError.value = err.response?.data?.detail || 'Parolni o\'zgartirishda xatolik.'
  } finally {
    savingPassword.value = false
  }
}

// ─── Logout ────────────────────────────────────────────────────────────────

function handleLogout() {
  authStore.logout()
  router.push('/login')
}
</script>
