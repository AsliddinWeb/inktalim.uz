<template>
  <div class="max-w-3xl mx-auto">

    <!-- Back link -->
    <RouterLink
      to="/dashboard/certificates"
      class="inline-flex items-center gap-1.5 text-sm text-gray-500 dark:text-gray-400 hover:text-primary-600 dark:hover:text-primary-400 transition-colors mb-6"
    >
      <ArrowLeft class="w-4 h-4" />
      Sertifikatlarimga qaytish
    </RouterLink>

    <!-- Skeleton -->
    <div v-if="loading" class="space-y-4">
      <div class="h-10 bg-gray-200 dark:bg-gray-800 animate-pulse rounded-xl w-1/2" />
      <div class="h-96 bg-gray-200 dark:bg-gray-800 animate-pulse rounded-2xl" />
    </div>

    <!-- Error -->
    <div v-else-if="error" class="rounded-xl border border-danger-200 dark:border-danger-800/30 bg-danger-50 dark:bg-danger-900/10 px-4 py-3">
      <p class="text-sm font-medium text-danger-600 dark:text-danger-400">{{ error }}</p>
    </div>

    <!-- Certificate preview -->
    <div v-else-if="cert">

      <div
        class="relative rounded-2xl overflow-hidden shadow-2xl mb-6"
        style="background: linear-gradient(135deg, #0F0E2A 0%, #1C1A3E 50%, #0F0E2A 100%)"
      >
        <!-- Decorative blobs -->
        <div class="absolute -top-16 -left-16 w-52 h-52 rounded-full opacity-20" style="background: radial-gradient(circle, #6C63FF, transparent)" />
        <div class="absolute -bottom-16 -right-16 w-52 h-52 rounded-full opacity-15" style="background: radial-gradient(circle, #F59E0B, transparent)" />

        <!-- Inner border -->
        <div
          class="relative m-4 rounded-xl p-8 sm:p-10"
          style="border: 1.5px solid rgba(108,99,255,0.5); background: rgba(28,26,62,0.8)"
        >
          <!-- Gold inner frame -->
          <div class="absolute inset-3 rounded-xl pointer-events-none" style="border: 0.5px solid rgba(245,158,11,0.3)" />

          <!-- Corner decorations -->
          <div class="absolute top-5 left-5 w-6 h-6 border-t-2 border-l-2 border-amber-400 rounded-tl-sm" />
          <div class="absolute top-5 right-5 w-6 h-6 border-t-2 border-r-2 border-amber-400 rounded-tr-sm" />
          <div class="absolute bottom-5 left-5 w-6 h-6 border-b-2 border-l-2 border-amber-400 rounded-bl-sm" />
          <div class="absolute bottom-5 right-5 w-6 h-6 border-b-2 border-r-2 border-amber-400 rounded-br-sm" />

          <!-- Content -->
          <div class="text-center relative z-10">

            <!-- Logo -->
            <div class="w-14 h-14 rounded-full bg-primary-500 flex items-center justify-center mx-auto mb-3 shadow-lg shadow-primary-500/30">
              <span class="text-white font-bold text-lg">EDU</span>
            </div>

            <p class="text-white font-bold text-xl mb-0.5">EduUz</p>
            <p class="text-gray-400 text-xs mb-6">Online Ta'lim Platformasi</p>

            <h1
              class="text-3xl sm:text-4xl font-black mb-1 tracking-wide"
              style="color: #F59E0B; text-shadow: 0 0 20px rgba(245,158,11,0.4)"
            >
              SERTIFIKAT
            </h1>
            <div class="w-24 h-0.5 bg-amber-400 mx-auto mb-6 opacity-60" />

            <p class="text-gray-400 text-sm mb-2">Ushbu sertifikat</p>
            <p class="text-2xl sm:text-3xl font-bold mb-2" style="color: #857EFA">
              {{ cert.course_title ? ownerName : '' }}
            </p>
            <p class="text-gray-400 text-sm mb-1">ga</p>
            <p class="text-lg sm:text-xl font-semibold italic mb-2" style="color: #FDE68A">
              "{{ cert.course_title }}"
            </p>
            <p class="text-gray-400 text-sm mb-8">kursini muvaffaqiyatli tugatganligi uchun berildi</p>

            <div class="border-t border-gray-700/60 mb-5" />

            <div class="flex flex-col sm:flex-row items-center justify-between gap-4 text-sm">
              <div class="text-center sm:text-left">
                <p class="text-gray-500 text-[10px] uppercase tracking-widest mb-0.5">Sertifikat raqami</p>
                <p class="font-mono font-bold text-amber-400">{{ cert.certificate_number }}</p>
              </div>
              <div class="text-center">
                <p class="text-gray-500 text-[10px] uppercase tracking-widest mb-0.5">Berilgan sana</p>
                <p class="font-semibold text-white">{{ formatDate(cert.issued_at) }}</p>
              </div>
              <div class="text-center sm:text-right">
                <p class="text-gray-500 text-[10px] uppercase tracking-widest mb-0.5">Imzo</p>
                <p class="text-primary-400 italic text-sm">EduUz Ta'lim Platformasi</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Download button -->
      <div class="flex justify-center">
        <button
          type="button"
          :disabled="downloading"
          class="inline-flex items-center gap-2 px-8 py-3.5 rounded-2xl font-semibold text-sm text-white transition-all duration-200 disabled:opacity-60 disabled:cursor-not-allowed"
          style="background: linear-gradient(135deg, #F59E0B, #D97706); box-shadow: 0 4px 16px rgba(245,158,11,0.3)"
          @click="handleDownload"
        >
          <svg v-if="downloading" class="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
          </svg>
          <Download v-else class="w-5 h-5" />
          {{ downloading ? 'Yuklanmoqda...' : 'PDF yuklab olish' }}
        </button>
      </div>

    </div>

  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import { ArrowLeft, Download, Loader2 } from 'lucide-vue-next'
import { getAllCertificates, downloadCertificate } from '@/api/certificate.js'
import { useAuthStore } from '@/stores/auth.js'
import AppAlert from '@/components/ui/AppAlert.vue'

const route = useRoute()
const authStore = useAuthStore()

const certNumber = route.params.number
const cert = ref(null)
const loading = ref(false)
const error = ref(null)
const downloading = ref(false)

const ownerName = ref(authStore.user?.full_name ?? '')

function formatDate(iso) {
  if (!iso) return ''
  return new Date(iso).toLocaleDateString('uz-UZ', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
  })
}

onMounted(async () => {
  loading.value = true
  error.value = null
  try {
    const { data } = await getAllCertificates()
    cert.value = data.find(c => c.certificate_number === certNumber) ?? null
    if (!cert.value) {
      error.value = 'Sertifikat topilmadi'
    }
  } catch (err) {
    error.value = err.response?.data?.detail ?? 'Sertifikat yuklanmadi'
  } finally {
    loading.value = false
  }
})

async function handleDownload() {
  downloading.value = true
  try {
    const response = await downloadCertificate(certNumber)
    const blob = new Blob([response.data], { type: 'application/pdf' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `EduUz-Sertifikat-${certNumber}.pdf`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  } catch (err) {
    console.error('Yuklab olishda xatolik:', err)
  } finally {
    downloading.value = false
  }
}
</script>
