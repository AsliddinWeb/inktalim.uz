import { defineStore } from 'pinia'
import { ref, watch } from 'vue'

const SIZES = ['text-sm', 'text-base', 'text-lg']
const LABELS = ['A-', 'A', 'A+']
const STORAGE_KEY = 'inktalim-font-size'

export const useFontSizeStore = defineStore('fontSize', () => {
  const saved = localStorage.getItem(STORAGE_KEY)
  const sizeIndex = ref(SIZES.indexOf(saved) !== -1 ? SIZES.indexOf(saved) : 1)

  function apply() {
    const el = document.documentElement
    SIZES.forEach(s => el.classList.remove(s))
    el.classList.add(SIZES[sizeIndex.value])
    localStorage.setItem(STORAGE_KEY, SIZES[sizeIndex.value])
  }

  function increase() {
    if (sizeIndex.value < SIZES.length - 1) {
      sizeIndex.value++
      apply()
    }
  }

  function decrease() {
    if (sizeIndex.value > 0) {
      sizeIndex.value--
      apply()
    }
  }

  const currentLabel = () => LABELS[sizeIndex.value]
  const canIncrease = () => sizeIndex.value < SIZES.length - 1
  const canDecrease = () => sizeIndex.value > 0

  // Dastlabki qo'llash
  apply()

  return { sizeIndex, increase, decrease, currentLabel, canIncrease, canDecrease }
})
