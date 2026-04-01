<template>
  <div
    class="relative inline-flex flex-shrink-0"
    :class="[editable ? 'cursor-pointer group' : '', sizeClasses]"
    @click="editable && triggerUpload()"
  >
    <!-- Rasm yoki initials -->
    <div
      class="w-full h-full rounded-full overflow-hidden flex items-center justify-center select-none"
      :class="!imageUrl ? 'bg-primary-100 dark:bg-primary-900/30' : ''"
    >
      <img
        v-if="imageUrl"
        :src="imageUrl"
        :alt="name || 'Avatar'"
        class="rounded-full object-cover w-full h-full"
        @error="onImageError"
      />
      <span
        v-else
        class="font-semibold text-primary-600 dark:text-primary-400 uppercase"
        :class="textSizeClass"
      >
        {{ initials }}
      </span>
    </div>

    <!-- Online dot -->
    <span
      v-if="online"
      class="absolute bottom-0 right-0 w-2.5 h-2.5 rounded-full bg-success-500 ring-2 ring-white dark:ring-surface"
    />

    <!-- Tahrirlash overlay (editable=true, hover da ko'rinadi) -->
    <div
      v-if="editable"
      class="absolute inset-0 rounded-full bg-black/50 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center"
    >
      <span v-if="uploading">
        <Loader2 class="text-white animate-spin" :class="iconSizeClass" />
      </span>
      <Camera v-else class="text-white" :class="iconSizeClass" />
    </div>

    <!-- Yashirin fayl input -->
    <input
      v-if="editable"
      ref="fileInputRef"
      type="file"
      accept="image/jpeg,image/png,image/webp"
      class="hidden"
      @change="onFileChange"
    />
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { Camera, Loader2 } from 'lucide-vue-next'
import { uploadAvatar, getMediaUrl } from '@/api/upload.js'

const props = defineProps({
  // Rasm URL — null bo'lsa initials ko'rsatiladi
  url: { type: String, default: null },
  // Initials hisoblash uchun ism
  name: { type: String, default: '' },
  // O'lcham: sm | md | lg | xl
  size: {
    type: String,
    default: 'lg',
    validator: (v) => ['sm', 'md', 'lg', 'xl'].includes(v),
  },
  // Online holat ko'rsatkichi
  online: { type: Boolean, default: false },
  // Tahrirlash rejimi — true bo'lsa kamera ikoni ko'rinadi va click ishlaydi
  editable: { type: Boolean, default: false },
})

const emit = defineEmits(['updated'])

// ─── O'lcham sozlamalari ─────────────────────────────────────────────────────
const sizeClasses = computed(() => ({
  sm: 'w-8 h-8 text-xs',
  md: 'w-10 h-10 text-sm',
  lg: 'w-12 h-12 text-base',
  xl: 'w-16 h-16 text-lg',
}[props.size]))

const textSizeClass = computed(() => ({
  sm: 'text-xs',
  md: 'text-sm',
  lg: 'text-base',
  xl: 'text-lg',
}[props.size]))

const iconSizeClass = computed(() => ({
  sm: 'w-3 h-3',
  md: 'w-4 h-4',
  lg: 'w-5 h-5',
  xl: 'w-6 h-6',
}[props.size]))

// ─── Initials ─────────────────────────────────────────────────────────────────
const initials = computed(() => {
  if (!props.name) return '?'
  return props.name
    .split(' ')
    .filter(Boolean)
    .map(w => w[0].toUpperCase())
    .slice(0, 2)
    .join('')
})

// ─── Rasm URL ─────────────────────────────────────────────────────────────────
const imageUrl = ref(getMediaUrl(props.url))

watch(
  () => props.url,
  (val) => { imageUrl.value = getMediaUrl(val) },
)

// Rasm yuklanmasa initials ga qaytish
function onImageError() {
  imageUrl.value = null
}

// ─── Fayl yuklash ─────────────────────────────────────────────────────────────
const fileInputRef = ref(null)
const uploading    = ref(false)

function triggerUpload() {
  if (!uploading.value) fileInputRef.value?.click()
}

async function onFileChange(event) {
  const file = event.target.files?.[0]
  event.target.value = ''
  if (!file) return

  // Client-side tekshiruv
  const ALLOWED = new Set(['image/jpeg', 'image/png', 'image/webp'])
  if (!ALLOWED.has(file.type)) return
  if (file.size > 5 * 1024 * 1024) return

  uploading.value = true

  // Lokal preview — tezkor ko'rsatish uchun
  imageUrl.value = URL.createObjectURL(file)

  try {
    const data = await uploadAvatar(file)
    imageUrl.value = getMediaUrl(data.url)
    emit('updated', data.url)
  } catch {
    // Xato bo'lsa eski rasmga qaytish
    imageUrl.value = getMediaUrl(props.url)
  } finally {
    uploading.value = false
  }
}
</script>
