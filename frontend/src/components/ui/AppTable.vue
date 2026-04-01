<template>
  <div class="w-full rounded-2xl border border-gray-100 dark:border-gray-800 overflow-hidden">
    <table class="w-full text-left">
      <!-- Header -->
      <thead class="bg-gray-50 dark:bg-gray-900/50">
        <tr>
          <th
            v-for="col in columns"
            :key="col.key"
            :style="col.width ? `width: ${col.width}` : ''"
            class="px-6 py-3 text-xs font-semibold uppercase tracking-wider text-gray-500 dark:text-gray-400 whitespace-nowrap"
            :class="{ 'sticky top-0 z-10 bg-gray-50 dark:bg-gray-900/50': stickyHeader }"
          >
            {{ col.label }}
          </th>
        </tr>
      </thead>

      <!-- Body -->
      <tbody class="bg-white dark:bg-surface divide-y divide-gray-100 dark:divide-gray-800">

        <!-- Loading skeleton -->
        <template v-if="loading">
          <tr v-for="i in skeletonRows" :key="`sk-${i}`" class="animate-pulse">
            <td
              v-for="col in columns"
              :key="col.key"
              class="px-6 py-4"
            >
              <div class="h-4 bg-gray-200 dark:bg-gray-700 rounded-lg w-3/4" />
            </td>
          </tr>
        </template>

        <!-- Bo'sh holat -->
        <tr v-else-if="rows.length === 0">
          <td :colspan="columns.length" class="text-center py-12 text-sm text-gray-400">
            <div class="flex flex-col items-center gap-2 text-gray-400">
              <Inbox class="w-10 h-10 opacity-40" />
              <span>Ma'lumot topilmadi</span>
            </div>
          </td>
        </tr>

        <!-- Data rows -->
        <template v-else>
          <tr
            v-for="(row, rowIdx) in rows"
            :key="row.id ?? rowIdx"
            class="hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors duration-150"
          >
            <td
              v-for="col in columns"
              :key="col.key"
              class="px-6 py-4 text-sm text-gray-700 dark:text-gray-300 whitespace-nowrap"
            >
              <!-- Custom slot yoki default matn -->
              <slot :name="`cell-${col.key}`" :row="row" :value="row[col.key]">
                {{ row[col.key] ?? '—' }}
              </slot>
            </td>
          </tr>
        </template>

      </tbody>
    </table>
  </div>
</template>

<script setup>
import { Inbox } from 'lucide-vue-next'

defineProps({
  columns: {
    type: Array,
    default: () => [],
    // [{ key: 'name', label: 'Ism', width: '200px' }, ...]
  },
  rows: {
    type: Array,
    default: () => [],
  },
  loading: {
    type: Boolean,
    default: false,
  },
  skeletonRows: {
    type: Number,
    default: 5,
  },
  stickyHeader: {
    type: Boolean,
    default: false,
  },
})
</script>
