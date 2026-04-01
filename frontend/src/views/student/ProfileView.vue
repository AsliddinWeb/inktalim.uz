<template>
  <div class="max-w-2xl mx-auto space-y-6">

    <!-- Header -->
    <div>
      <h1 class="text-2xl font-bold text-gray-900 dark:text-white">Profilim</h1>
      <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">Shaxsiy ma'lumotlarni boshqarish</p>
    </div>

    <!-- Avatar card -->
    <div class="rounded-2xl border border-gray-100 dark:border-gray-800 bg-white dark:bg-surface p-6">
      <div class="flex items-center gap-5">
        <div class="flex flex-col items-center gap-1.5">
          <AppAvatar
            :url="authStore.user?.avatar_url"
            :name="authStore.user?.full_name || authStore.user?.email"
            size="xl"
            :editable="true"
            @updated="onAvatarUpdated"
          />
          <p class="text-xs text-gray-400">Rasmni o'zgartirish</p>
        </div>
        <div>
          <p class="text-lg font-bold text-gray-900 dark:text-white">{{ authStore.user?.full_name }}</p>
          <p class="text-sm text-gray-500 dark:text-gray-400">{{ authStore.user?.email }}</p>
          <span class="mt-2 inline-flex items-center rounded-full px-3 py-1 text-xs font-semibold bg-primary-100 dark:bg-primary-900/20 text-primary-700 dark:text-primary-400">
            {{ authStore.isAdmin ? 'Admin' : 'Student' }}
          </span>
        </div>
      </div>
      <div v-if="avatarError" class="mt-3 flex items-center gap-3 rounded-xl border border-danger-200 dark:border-danger-800/30 bg-danger-50 dark:bg-danger-900/10 px-4 py-3">
        <p class="text-sm font-medium text-danger-600 dark:text-danger-400">{{ avatarError }}</p>
      </div>
    </div>

    <!-- Profile form -->
    <div class="rounded-2xl border border-gray-100 dark:border-gray-800 bg-white dark:bg-surface p-6">
      <h2 class="text-base font-semibold text-gray-900 dark:text-white mb-5">Profil ma'lumotlari</h2>

      <div v-if="profileSuccess" class="flex items-center gap-3 rounded-xl border border-success-200 dark:border-success-800/30 bg-success-50 dark:bg-success-900/10 px-4 py-3 mb-4">
        <svg class="w-4 h-4 text-success-500 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
        </svg>
        <p class="text-sm font-medium text-success-700 dark:text-success-400">Profil muvaffaqiyatli yangilandi!</p>
      </div>
      <div v-if="profileError" class="flex items-center gap-3 rounded-xl border border-danger-200 dark:border-danger-800/30 bg-danger-50 dark:bg-danger-900/10 px-4 py-3 mb-4">
        <p class="text-sm font-medium text-danger-600 dark:text-danger-400">{{ profileError }}</p>
      </div>

      <form class="space-y-4" @submit.prevent="updateProfile">
        <AppInput
          v-model="profileForm.full_name"
          label="To'liq ism"
          placeholder="Sardor Raximov"
          :icon-left="User"
          :error="profileErrors.full_name"
          required
          @blur="validateProfileField('full_name')"
        />
        <AppInput
          v-model="profileForm.phone"
          label="Telefon raqami"
          placeholder="+998901234567"
          :icon-left="Phone"
          :error="profileErrors.phone"
          hint="Format: +998XXXXXXXXX"
          required
          @blur="validateProfileField('phone')"
        />
        <div class="pt-2">
          <button
            type="submit"
            :disabled="savingProfile"
            class="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-primary-500 hover:bg-primary-600 text-white text-sm font-semibold shadow-sm hover:shadow-md hover:-translate-y-0.5 active:translate-y-0 transition-all duration-200 disabled:opacity-60 disabled:cursor-not-allowed disabled:transform-none"
          >
            <svg v-if="savingProfile" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
            </svg>
            <Save v-else class="w-4 h-4" />
            Saqlash
          </button>
        </div>
      </form>
    </div>

    <!-- Password form -->
    <div class="rounded-2xl border border-gray-100 dark:border-gray-800 bg-white dark:bg-surface p-6">
      <h2 class="text-base font-semibold text-gray-900 dark:text-white mb-5">Parolni o'zgartirish</h2>

      <div v-if="passwordSuccess" class="flex items-center gap-3 rounded-xl border border-success-200 dark:border-success-800/30 bg-success-50 dark:bg-success-900/10 px-4 py-3 mb-4">
        <p class="text-sm font-medium text-success-700 dark:text-success-400">Parol muvaffaqiyatli o'zgartirildi!</p>
      </div>
      <div v-if="passwordError" class="flex items-center gap-3 rounded-xl border border-danger-200 dark:border-danger-800/30 bg-danger-50 dark:bg-danger-900/10 px-4 py-3 mb-4">
        <p class="text-sm font-medium text-danger-600 dark:text-danger-400">{{ passwordError }}</p>
      </div>

      <form class="space-y-4" @submit.prevent="changePassword">
        <AppInput
          v-model="passwordForm.old_password"
          label="Joriy parol"
          placeholder="Hozirgi parolingiz"
          type="password"
          :icon-left="Lock"
          :error="passwordErrors.old_password"
          required
          @blur="validatePasswordField('old_password')"
        />
        <AppInput
          v-model="passwordForm.new_password"
          label="Yangi parol"
          placeholder="Kamida 8 ta belgi"
          type="password"
          :icon-left="Lock"
          :error="passwordErrors.new_password"
          required
          @blur="validatePasswordField('new_password')"
        />
        <AppInput
          v-model="passwordForm.confirm_password"
          label="Yangi parolni tasdiqlang"
          placeholder="Yangi parolni qayta kiriting"
          type="password"
          :icon-left="ShieldCheck"
          :error="passwordErrors.confirm_password"
          required
          @blur="validatePasswordField('confirm_password')"
        />
        <div class="pt-2">
          <button
            type="submit"
            :disabled="changingPassword"
            class="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-surface text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-800 text-sm font-semibold transition-all duration-200 disabled:opacity-60 disabled:cursor-not-allowed"
          >
            <svg v-if="changingPassword" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
            </svg>
            <KeyRound v-else class="w-4 h-4" />
            Parolni o'zgartirish
          </button>
        </div>
      </form>
    </div>

    <!-- Logout card -->
    <div class="rounded-2xl border border-gray-100 dark:border-gray-800 bg-white dark:bg-surface p-6">
      <div class="flex items-center justify-between">
        <div>
          <p class="font-medium text-gray-900 dark:text-white">Hisobdan chiqish</p>
          <p class="text-sm text-gray-500 dark:text-gray-400 mt-0.5">Barcha qurilmalardan chiqish</p>
        </div>
        <button
          type="button"
          class="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-danger-50 dark:bg-danger-900/20 text-danger-600 dark:text-danger-400 hover:bg-danger-500 hover:text-white dark:hover:bg-danger-500 dark:hover:text-white border border-danger-200 dark:border-danger-800 hover:border-transparent text-sm font-semibold transition-all duration-200"
          @click="authStore.logout()"
        >
          <LogOut class="w-4 h-4" />
          Chiqish
        </button>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { User, Phone, Lock, ShieldCheck, Save, KeyRound, LogOut } from 'lucide-vue-next'
import * as yup from 'yup'

import api from '@/api/axios.js'
import { useAuthStore } from '@/stores/auth.js'
import AppCard     from '@/components/ui/AppCard.vue'
import AppInput    from '@/components/ui/AppInput.vue'
import AppButton   from '@/components/ui/AppButton.vue'
import AppBadge    from '@/components/ui/AppBadge.vue'
import AppAlert    from '@/components/ui/AppAlert.vue'
import AppAvatar   from '@/components/ui/AppAvatar.vue'

const authStore = useAuthStore()

// ─── Avatar ───────────────────────────────────────────────────────────────────
const avatarError = ref('')

async function onAvatarUpdated(url) {
  try {
    await authStore.fetchMe()
  } catch {
    avatarError.value = 'Avatar yangilashda xatolik yuz berdi.'
  }
}

// ─── Profil forma ─────────────────────────────────────────────────────────────
const profileForm = reactive({
  full_name: authStore.user?.full_name ?? '',
  phone:     authStore.user?.phone ?? '',
})
const profileErrors  = reactive({ full_name: '', phone: '' })
const savingProfile  = ref(false)
const profileSuccess = ref(false)
const profileError   = ref('')

const profileSchemas = {
  full_name: yup.string().required('Ism kiriting').min(2, 'Ism kamida 2 belgi'),
  phone:     yup.string().required('Telefon kiriting').matches(/^\+998[0-9]{9}$/, 'Format: +998XXXXXXXXX'),
}

async function validateProfileField(field) {
  try {
    await profileSchemas[field].validate(profileForm[field])
    profileErrors[field] = ''
  } catch (err) {
    profileErrors[field] = err.message
  }
}

async function updateProfile() {
  profileSuccess.value = false
  profileError.value = ''
  let valid = true
  for (const field of ['full_name', 'phone']) {
    try {
      await profileSchemas[field].validate(profileForm[field])
      profileErrors[field] = ''
    } catch (err) {
      profileErrors[field] = err.message
      valid = false
    }
  }
  if (!valid) return

  savingProfile.value = true
  try {
    await api.put('/auth/me', {
      full_name: profileForm.full_name,
      phone:     profileForm.phone,
    })
    await authStore.fetchMe()
    profileSuccess.value = true
    setTimeout(() => { profileSuccess.value = false }, 4000)
  } catch (err) {
    profileError.value = err.response?.data?.detail || 'Saqlashda xatolik yuz berdi.'
  } finally {
    savingProfile.value = false
  }
}

// ─── Parol o'zgartirish ────────────────────────────────────────────────────────
const passwordForm = reactive({
  old_password:     '',
  new_password:     '',
  confirm_password: '',
})
const passwordErrors   = reactive({ old_password: '', new_password: '', confirm_password: '' })
const changingPassword = ref(false)
const passwordSuccess  = ref(false)
const passwordError    = ref('')

const passwordSchemas = {
  old_password:     yup.string().required('Joriy parolni kiriting'),
  new_password:     yup.string().required('Yangi parolni kiriting').min(8, 'Kamida 8 belgi'),
  confirm_password: yup.string()
    .required('Parolni tasdiqlang')
    .test('match', 'Parollar mos kelmadi', () => passwordForm.new_password === passwordForm.confirm_password),
}

async function validatePasswordField(field) {
  try {
    await passwordSchemas[field].validate(passwordForm[field])
    passwordErrors[field] = ''
  } catch (err) {
    passwordErrors[field] = err.message
  }
}

async function changePassword() {
  passwordSuccess.value = false
  passwordError.value = ''
  let valid = true
  for (const field of ['old_password', 'new_password', 'confirm_password']) {
    try {
      await passwordSchemas[field].validate(passwordForm[field])
      passwordErrors[field] = ''
    } catch (err) {
      passwordErrors[field] = err.message
      valid = false
    }
  }
  if (!valid) return

  changingPassword.value = true
  try {
    await api.post('/auth/change-password', {
      old_password: passwordForm.old_password,
      new_password: passwordForm.new_password,
    })
    passwordSuccess.value = true
    passwordForm.old_password = ''
    passwordForm.new_password = ''
    passwordForm.confirm_password = ''
    setTimeout(() => { passwordSuccess.value = false }, 4000)
  } catch (err) {
    passwordError.value = err.response?.data?.detail || 'Parolni o\'zgartirishda xatolik yuz berdi.'
  } finally {
    changingPassword.value = false
  }
}

onMounted(() => {
  profileForm.full_name = authStore.user?.full_name ?? ''
  profileForm.phone     = authStore.user?.phone ?? ''
})
</script>
