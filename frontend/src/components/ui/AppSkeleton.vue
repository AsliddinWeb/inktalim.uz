<template>
  <div :class="wrapperClass">

    <!-- text skeleton -->
    <template v-if="type === 'text'">
      <div :class="count > 1 ? 'space-y-3' : ''">
        <div
          v-for="i in count"
          :key="i"
          class="animate-pulse bg-gradient-to-r from-gray-200 via-gray-100 to-gray-200 dark:from-gray-800 dark:via-gray-700 dark:to-gray-800 rounded-xl h-4"
          :class="i === count && count > 1 ? 'w-3/4' : 'w-full'"
        />
      </div>
    </template>

    <!-- circle skeleton -->
    <template v-else-if="type === 'circle'">
      <div
        v-for="i in count"
        :key="i"
        class="animate-pulse bg-gradient-to-r from-gray-200 via-gray-100 to-gray-200 dark:from-gray-800 dark:via-gray-700 dark:to-gray-800 rounded-full w-10 h-10"
      />
    </template>

    <!-- avatar skeleton -->
    <template v-else-if="type === 'avatar'">
      <div :class="count > 1 ? 'flex gap-3' : ''">
        <div
          v-for="i in count"
          :key="i"
          class="animate-pulse bg-gradient-to-r from-gray-200 via-gray-100 to-gray-200 dark:from-gray-800 dark:via-gray-700 dark:to-gray-800 rounded-full flex-shrink-0"
          :class="{
            'w-8 h-8': size === 'sm',
            'w-10 h-10': size === 'md' || !size,
            'w-12 h-12': size === 'lg',
          }"
        />
      </div>
    </template>

    <!-- card skeleton -->
    <template v-else-if="type === 'card'">
      <div :class="count > 1 ? 'space-y-3' : ''">
        <div
          v-for="i in count"
          :key="i"
          class="animate-pulse rounded-2xl p-6 bg-gray-100 dark:bg-gray-800"
        >
          <div class="space-y-3">
            <div class="h-4 bg-gray-200 dark:bg-gray-700 rounded-xl w-2/3" />
            <div class="h-4 bg-gray-200 dark:bg-gray-700 rounded-xl w-full" />
            <div class="h-4 bg-gray-200 dark:bg-gray-700 rounded-xl w-4/5" />
          </div>
        </div>
      </div>
    </template>

    <!-- course-card skeleton -->
    <template v-else-if="type === 'course-card'">
      <div :class="count > 1 ? 'space-y-4' : ''">
        <div
          v-for="i in count"
          :key="i"
          class="animate-pulse rounded-2xl overflow-hidden border border-gray-100 dark:border-gray-800"
        >
          <!-- Thumbnail -->
          <div class="aspect-video bg-gray-200 dark:bg-gray-700" />
          <!-- Content -->
          <div class="p-5 space-y-3">
            <div class="h-4 bg-gray-200 dark:bg-gray-700 rounded-xl w-4/5" />
            <div class="h-3.5 bg-gray-200 dark:bg-gray-700 rounded-xl w-full" />
            <div class="h-3.5 bg-gray-200 dark:bg-gray-700 rounded-xl w-3/4" />
            <div class="h-10 bg-gray-200 dark:bg-gray-700 rounded-xl mt-2" />
          </div>
        </div>
      </div>
    </template>

    <!-- table-row skeleton -->
    <template v-else-if="type === 'table-row'">
      <div :class="count > 1 ? 'space-y-2' : ''">
        <div
          v-for="i in count"
          :key="i"
          class="animate-pulse flex gap-4 py-4 px-6 bg-white dark:bg-surface"
        >
          <div class="h-4 bg-gray-200 dark:bg-gray-700 rounded-xl w-1/4" />
          <div class="h-4 bg-gray-200 dark:bg-gray-700 rounded-xl w-1/3" />
          <div class="h-4 bg-gray-200 dark:bg-gray-700 rounded-xl w-1/5" />
          <div class="h-4 bg-gray-200 dark:bg-gray-700 rounded-xl w-1/6" />
        </div>
      </div>
    </template>

    <!-- button skeleton -->
    <template v-else-if="type === 'button'">
      <div :class="count > 1 ? 'flex gap-3' : ''">
        <div
          v-for="i in count"
          :key="i"
          class="animate-pulse bg-gradient-to-r from-gray-200 via-gray-100 to-gray-200 dark:from-gray-800 dark:via-gray-700 dark:to-gray-800 h-10 rounded-xl w-28"
        />
      </div>
    </template>

    <!-- Default skeleton -->
    <template v-else>
      <div :class="count > 1 ? 'space-y-3' : ''">
        <div
          v-for="i in count"
          :key="i"
          class="animate-pulse bg-gradient-to-r from-gray-200 via-gray-100 to-gray-200 dark:from-gray-800 dark:via-gray-700 dark:to-gray-800 rounded-xl h-4"
        />
      </div>
    </template>

  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  type: {
    type: String,
    default: 'text',
    validator: (v) => ['text', 'circle', 'avatar', 'card', 'course-card', 'table-row', 'button', 'lesson'].includes(v),
  },
  count: {
    type: Number,
    default: 1,
  },
  size: {
    type: String,
    default: 'md',
    validator: (v) => ['sm', 'md', 'lg'].includes(v),
  },
  // grid uchun wrapper klass
  wrapperClass: {
    type: String,
    default: '',
  },
})
</script>
