<template>
  <div
    class="rounded-2xl border-2 border-secondary-200 dark:border-secondary-800/40 bg-white dark:bg-surface p-6
           hover:border-secondary-400 dark:hover:border-secondary-600
           hover:shadow-lg hover:shadow-secondary-500/10
           transition-all duration-300 group"
  >
    <!-- Top -->
    <div class="flex items-start justify-between mb-5">
      <div class="w-12 h-12 rounded-2xl bg-secondary-50 dark:bg-secondary-900/20 flex items-center justify-center flex-shrink-0">
        <Award class="size-6 text-secondary-500" />
      </div>
      <span class="inline-flex items-center rounded-full px-3 py-1 text-xs font-semibold bg-secondary-100 dark:bg-secondary-900/20 text-secondary-700 dark:text-secondary-400">
        Sertifikat
      </span>
    </div>

    <!-- Course title -->
    <h3 class="text-base font-semibold text-gray-900 dark:text-white mb-2 line-clamp-2 group-hover:text-secondary-600 dark:group-hover:text-secondary-400 transition-colors">
      {{ certificate.course_title }}
    </h3>

    <!-- Cert number -->
    <p class="font-mono text-xs bg-gray-100 dark:bg-gray-800 text-gray-500 dark:text-gray-400 px-3 py-1.5 rounded-lg inline-block mb-2">
      {{ certificate.certificate_number }}
    </p>

    <!-- Date -->
    <p class="text-xs text-gray-400 flex items-center gap-1.5 mb-5">
      <Calendar class="size-3.5" />
      {{ formatDate(certificate.issued_at) }}
    </p>

    <!-- Actions -->
    <div class="flex gap-2">
      <RouterLink
        :to="`/dashboard/certificates/${certificate.certificate_number}`"
        class="flex-1 inline-flex items-center justify-center gap-1.5 px-4 py-2.5 rounded-xl text-sm font-semibold text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
      >
        <Eye class="size-4" />
        Ko'rish
      </RouterLink>
      <button
        type="button"
        :disabled="downloading"
        class="flex-1 inline-flex items-center justify-center gap-1.5 px-4 py-2.5 rounded-xl text-sm font-semibold bg-secondary-50 dark:bg-secondary-900/20 text-secondary-700 dark:text-secondary-400 hover:bg-secondary-500 hover:text-white dark:hover:bg-secondary-500 dark:hover:text-white border border-secondary-200 dark:border-secondary-800 hover:border-transparent transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
        @click="handleDownload"
      >
        <Loader2 v-if="downloading" class="size-4 animate-spin" />
        <Download v-else class="size-4" />
        Yuklab olish
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { RouterLink } from 'vue-router'
import { Award, Calendar, Download, Eye, Loader2 } from 'lucide-vue-next'
import { downloadCertificate } from '@/api/certificate.js'

const props = defineProps({
  certificate: { type: Object, required: true },
})

const downloading = ref(false)

function formatDate(iso) {
  if (!iso) return ''
  return new Date(iso).toLocaleDateString('uz-UZ', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
  })
}

async function handleDownload() {
  downloading.value = true
  try {
    const response = await downloadCertificate(props.certificate.certificate_number)
    // Blob dan yuklab olish
    const blob = new Blob([response.data], { type: 'application/pdf' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `EduUz-Sertifikat-${props.certificate.certificate_number}.pdf`
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
