<template>
  <div>
    <!-- Label -->
    <p v-if="label" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
      {{ label }}
    </p>

    <!-- Fayl tanlangan holat -->
    <div
      v-if="selectedFile"
      class="rounded-xl border border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-900/50 p-3 flex items-center gap-3"
    >
      <!-- Fayl ikoni -->
      <component
        :is="isImageFile ? ImageIcon : File"
        class="w-8 h-8 text-primary-500 flex-shrink-0"
      />
      <!-- Fayl ma'lumotlari -->
      <div class="flex-1 min-w-0">
        <p class="text-sm font-medium text-gray-900 dark:text-gray-100 truncate">{{ selectedFile.name }}</p>
        <p class="text-xs text-gray-400">{{ formatFileSize(selectedFile.size) }}</p>
      </div>
      <!-- O'chirish tugmasi -->
      <button
        type="button"
        class="w-7 h-7 rounded-lg hover:bg-danger-50 dark:hover:bg-danger-900/20 hover:text-danger-500 text-gray-400 flex items-center justify-center transition-colors flex-shrink-0"
        aria-label="Faylni olib tashlash"
        @click="removeFile"
      >
        <X class="size-3.5" />
      </button>
    </div>

    <!-- Drag-drop zonasi (fayl tanlanmagan) -->
    <div
      v-else
      class="rounded-2xl border-2 border-dashed p-8 text-center cursor-pointer transition-all duration-200 group"
      :class="[
        isDragOver
          ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/20'
          : 'border-gray-200 dark:border-gray-700 hover:border-primary-400 dark:hover:border-primary-500 hover:bg-primary-50/50 dark:hover:bg-primary-900/10',
        uploading ? 'pointer-events-none opacity-60' : '',
      ]"
      @click="triggerPicker"
      @dragover.prevent="isDragOver = true"
      @dragleave.prevent="isDragOver = false"
      @drop.prevent="onDrop"
    >
      <!-- Upload ikoni -->
      <UploadCloud class="w-10 h-10 text-gray-300 dark:text-gray-600 group-hover:text-primary-400 mx-auto mb-3 transition-colors" />
      <!-- Matn -->
      <p class="text-sm text-gray-500 dark:text-gray-400">
        Faylni shu yerga tashlang yoki <span class="text-primary-500 font-medium">tanlang</span>
      </p>
      <!-- Accept hint -->
      <p v-if="accept" class="text-xs text-gray-400 mt-2">{{ accept }}</p>
    </div>

    <!-- Yuklash overlay -->
    <div
      v-if="uploading"
      class="mt-3 rounded-xl bg-gray-50 dark:bg-gray-900/50 p-3 flex items-center gap-3"
    >
      <Loader2 class="w-5 h-5 text-primary-500 animate-spin flex-shrink-0" />
      <div class="flex-1">
        <div class="h-1.5 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
          <div
            class="h-full bg-primary-500 rounded-full transition-all duration-300"
            :style="{ width: `${uploadProgress}%` }"
          />
        </div>
        <p class="text-xs text-gray-400 mt-1">{{ uploadProgress }}% yuklandi</p>
      </div>
    </div>

    <!-- Xato xabari -->
    <p v-if="error" class="mt-1.5 text-xs text-danger-500 flex items-center gap-1">
      <AlertCircle class="size-3.5 flex-shrink-0" />
      {{ error }}
    </p>

    <!-- Yashirin fayl input -->
    <input
      ref="fileInputRef"
      type="file"
      :accept="accept"
      class="hidden"
      @change="onFileChange"
    />
  </div>
</template>

<script setup>
import { ref, watch, computed } from 'vue'
import { UploadCloud, File, ImageIcon, Loader2, X, AlertCircle } from 'lucide-vue-next'
import api from '@/api/axios.js'
import { getMediaUrl } from '@/api/upload.js'

const props = defineProps({
  // Endpoint — "/upload/thumbnail" yoki "/upload/avatar"
  endpoint: { type: String, required: true },
  // Mavjud rasm URL (tahrirlashda ko'rsatish uchun)
  currentUrl: { type: String, default: null },
  // Maydon yorlig'i
  label: { type: String, default: '' },
  // Qabul qilinadigan fayl turlari
  accept: { type: String, default: '' },
})

const emit = defineEmits(['uploaded'])

// ─── State ───────────────────────────────────────────────────────────────────
const fileInputRef   = ref(null)
const isDragOver     = ref(false)
const uploading      = ref(false)
const uploadProgress = ref(0)
const error          = ref('')
const previewUrl     = ref(null)
const selectedFile   = ref(null)

// Fayl rasm ekanligini tekshirish
const isImageFile = computed(() => {
  if (!selectedFile.value) return false
  return selectedFile.value.type.startsWith('image/')
})

// currentUrl o'zgarganda preview ni yangilash
watch(
  () => props.currentUrl,
  (val) => { previewUrl.value = getMediaUrl(val) },
  { immediate: true },
)

// ─── Fayl hajmini formatlash ─────────────────────────────────────────────────
function formatFileSize(bytes) {
  if (!bytes) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return `${parseFloat((bytes / Math.pow(k, i)).toFixed(1))} ${sizes[i]}`
}

// ─── Faylni olib tashlash ─────────────────────────────────────────────────────
function removeFile() {
  selectedFile.value = null
  error.value = ''
}

// ─── Faylni ochish ────────────────────────────────────────────────────────────
function triggerPicker() {
  if (!uploading.value) fileInputRef.value?.click()
}

// ─── Drag-and-drop ────────────────────────────────────────────────────────────
function onDrop(event) {
  isDragOver.value = false
  const file = event.dataTransfer?.files?.[0]
  if (file) processFile(file)
}

// ─── File picker ─────────────────────────────────────────────────────────────
function onFileChange(event) {
  const file = event.target.files?.[0]
  if (file) processFile(file)
  // Inputni reset qilish (bir xil faylni qayta tanlash mumkin bo'lsin)
  event.target.value = ''
}

// ─── Fayl tekshirish (client-side) ────────────────────────────────────────────
const ALLOWED_TYPES = new Set(['image/jpeg', 'image/png', 'image/webp'])
const MAX_SIZE = 5 * 1024 * 1024

function validateClient(file) {
  if (!ALLOWED_TYPES.has(file.type)) {
    error.value = 'Faqat JPG, PNG, WEBP formatlar qabul qilinadi.'
    return false
  }
  if (file.size > MAX_SIZE) {
    error.value = 'Fayl hajmi 5MB dan oshmasligi kerak.'
    return false
  }
  return true
}

// ─── Faylni yuklash ───────────────────────────────────────────────────────────
async function processFile(file) {
  error.value = ''
  if (!validateClient(file)) return

  selectedFile.value = file

  // Local preview
  previewUrl.value = URL.createObjectURL(file)

  // Serverga yuborish
  uploading.value = true
  uploadProgress.value = 0

  const form = new FormData()
  form.append('file', file)

  try {
    const response = await api.post(props.endpoint, form, {
      onUploadProgress: (e) => {
        if (e.total) {
          uploadProgress.value = Math.round((e.loaded / e.total) * 100)
        }
      },
    })

    const url = response.data.url
    // Preview ni backend URL ga yangilash
    previewUrl.value = getMediaUrl(url)
    emit('uploaded', url)
  } catch (err) {
    const detail = err.response?.data?.detail
    if (Array.isArray(detail)) {
      error.value = detail.map(d => d.msg).join(', ')
    } else {
      error.value = detail || 'Yuklashda xatolik yuz berdi. Qaytadan urinib ko\'ring.'
    }
    // Preview ni eski holatga qaytarish
    previewUrl.value = getMediaUrl(props.currentUrl)
    selectedFile.value = null
  } finally {
    uploading.value = false
  }
}
</script>
