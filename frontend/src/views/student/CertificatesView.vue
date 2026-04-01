<template>
  <div class="space-y-6">

    <!-- Header -->
    <div class="flex items-center gap-3">
      <div class="w-12 h-12 rounded-2xl bg-secondary-100 dark:bg-secondary-900/20 flex items-center justify-center flex-shrink-0">
        <Award class="w-6 h-6 text-secondary-500" />
      </div>
      <div>
        <h1 class="text-2xl font-bold text-gray-900 dark:text-white">Sertifikatlarim</h1>
        <p class="text-sm text-gray-500 dark:text-gray-400 mt-0.5">Tugatilgan kurslar uchun sertifikatlar</p>
      </div>
    </div>

    <!-- Error -->
    <div v-if="error" class="rounded-xl border border-danger-200 dark:border-danger-800/30 bg-danger-50 dark:bg-danger-900/10 px-4 py-3">
      <p class="text-sm font-medium text-danger-600 dark:text-danger-400">{{ error }}</p>
    </div>

    <!-- Loading skeletons -->
    <div v-if="loading" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
      <div
        v-for="i in 3"
        :key="i"
        class="rounded-2xl border border-gray-100 dark:border-gray-800 bg-white dark:bg-surface p-6 animate-pulse"
      >
        <div class="flex items-start justify-between mb-5">
          <div class="w-12 h-12 rounded-2xl bg-gray-200 dark:bg-gray-700" />
          <div class="h-6 w-20 rounded-full bg-gray-200 dark:bg-gray-700" />
        </div>
        <div class="space-y-2 mb-4">
          <div class="h-4 bg-gray-200 dark:bg-gray-700 rounded-lg w-3/4" />
          <div class="h-3 bg-gray-100 dark:bg-gray-800 rounded-lg w-full" />
        </div>
        <div class="h-6 bg-gray-100 dark:bg-gray-800 rounded-lg w-2/3 mb-4" />
        <div class="h-10 bg-gray-200 dark:bg-gray-700 rounded-xl" />
      </div>
    </div>

    <!-- Empty state -->
    <div
      v-else-if="!certificates.length"
      class="rounded-2xl border-2 border-dashed border-gray-200 dark:border-gray-700 p-16 text-center"
    >
      <Award class="w-14 h-14 text-gray-200 dark:text-gray-700 mx-auto mb-4" />
      <h3 class="text-lg font-semibold text-gray-400 mb-1">Hali sertifikat yo'q</h3>
      <p class="text-sm text-gray-400 mb-6">Kurslarni tugatib sertifikat oling</p>
      <RouterLink
        to="/dashboard/courses"
        class="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-primary-500 hover:bg-primary-600 text-white text-sm font-semibold shadow-sm hover:shadow-md hover:-translate-y-0.5 active:translate-y-0 transition-all duration-200"
      >
        Kurslarga o'tish
      </RouterLink>
    </div>

    <!-- Certificates grid -->
    <div
      v-else
      class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5"
    >
      <CertificateCard
        v-for="cert in certificates"
        :key="cert.certificate_number"
        :certificate="cert"
      />
    </div>

  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { RouterLink } from 'vue-router'
import { Award } from 'lucide-vue-next'
import { getAllCertificates } from '@/api/certificate.js'
import CertificateCard from '@/components/student/CertificateCard.vue'
import AppAlert from '@/components/ui/AppAlert.vue'
import AppButton from '@/components/ui/AppButton.vue'

const certificates = ref([])
const loading = ref(false)
const error = ref(null)

onMounted(async () => {
  loading.value = true
  error.value = null
  try {
    const { data } = await getAllCertificates()
    certificates.value = data
  } catch (err) {
    error.value = err.response?.data?.detail ?? 'Sertifikatlar yuklanmadi'
  } finally {
    loading.value = false
  }
})
</script>
